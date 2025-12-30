from pprint import pprint
from pathlib import Path
from typing import Generator, List, Tuple
import csv
import re
import os
from tqdm import tqdm

from jinja2 import (Environment, FileSystemLoader, Template)

def merge_meanings(data: dict) -> None:
    """Merges meanings in a dict.

    {'meaning_1': 'let in',                 'meaning_2': 'bath (child)',
     'meaning_1_rus': 'впускать внутрь',    'meaning_2_rus': 'искупать (ребенка)',
     'example_1': 'χala aʁʷa zɨ!',          'example_2': 'χɨnɨχ xije aʁura',
     'example_1_cyr': 'хала агъва зы!',     'example_2_cyr': 'хыных хьийе агъура',
     'example_1_rus': 'В дом пусти меня!',  'example_2_rus': 'Ребенка искупали',
     'diathesis_1': 'abs',                    'diathesis_2': 'abs'}
    
    will become

    {'meanings': [
        {'meaning': 'let in', 'meaning_rus': 'впускать внутрь',
         'example': 'χala aʁʷa zɨ!', 'example_cyr': 'хала агъва зы!', 'example_rus': 'В дом пусти меня!',
         'diathesis': 'abs'},
        {'meaning': 'bath (child)', 'meaning_rus': 'искупать (ребенка)',
         'example': 'χɨnɨχ xije aʁura', 'example_cyr': 'хыных хьийе агъура', 'example_rus': 'Ребенка искупали',
         'diathesis': 'abs'}
    ]}

    Args:
        data (dict): dict that will be modified in-place
    """
    data['meanings'] = []
    for i in range(1, 5):
        data['meanings'].append({
            'meaning': data[f'meaning_{i}'],
            'meaning_rus': data[f'meaning_{i}_rus'],
            'example': data[f'example_{i}'],
            'example_cyr': data[f'example_{i}_cyr'],
            'example_rus': data[f'example_{i}_rus'],
            'diathesis': data[f'diathesis_{i}']
        })
        del data[f'meaning_{i}'], data[f'meaning_{i}_rus'], \
            data[f'example_{i}'], data[f'example_{i}_rus'], data[f'diathesis_{i}']

def split_examples(data: dict) -> None:
    """Splits examples in a dict

    {'meanings': [{
        ...
        'example': "mašinbɨr ara jiˁlχɨra; q'ʷaˁd čabɨlešdɨ süri ara jiˁlχɨraj',
        'example_rus': 'Машины столкнулись; Две отары баранов смешались'
        ...
    }]}

    will become 

    {'meanings': [{
        ...
        'examples': [
            'examples': [
                {'original': 'mašinbɨr ara jiˁlχɨra',
                 'rus': 'Машины столкнулись'},
                {'original': "q'ʷaˁd čabɨlešdɨ süri ara jiˁlχɨraj",
                 'rus': 'Две отары баранов смешались'}]
        ...
    }]}

    Args:
        data (dict): dict that will be modified in-place
    """
    for meaning in data['meanings']:
        examples = meaning['example'].split(' ; ')
        examples = [x.strip() for x in examples]
        examples_cyr = meaning['example_cyr'].split(' ; ')
        examples_cyr = [x.strip() for x in examples_cyr]
        examples_rus = meaning['example_rus'].split(' ; ')
        examples_rus = [x.strip() for x in examples_rus]
        del meaning['example'], meaning['example_cyr'], meaning['example_rus']
        meaning['examples'] = [{'original': f'{orig}', 'cyr': cyr, 'rus': rus}
                               for orig, cyr, rus in zip(examples, examples_cyr, examples_rus)
                               if orig or cyr or rus]

def load_inflection(*files) -> dict:
    """Loads inflection data

    Returns:
        dict: Inflection data dict. Keys - lexeme ids; values - data dict
    """
    inflection_data = {}
    for f_name in files:
        with open(f_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            col_names = next(reader)
            for row in reader:
                data = dict(zip(col_names, row))
                lex_id = data['lexeme_id']
                del data['lexeme_id']
                inflection_data[lex_id] = data
    return inflection_data

def load_glossing_labels(file: str) -> dict:
    """Loads key-value glossing labels dict

    Args:
        file (str): dict file

    Returns:
        dict: key - lexeme_id; value - glossing label
    """
    labels = {}
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        col_names = next(reader)
        for row in tqdm(reader, desc='Loading labels'):
            data = dict(zip(col_names, row))
            labels[data['lexeme_id']] = data['Glossing label']
    return labels

def insert_inflection(data: dict, inflection_data: dict) -> None:
    """Inserts corresponding inflection data and filters out 
    blacklisted keys.

    Args:
        data (dict): current word data. Will be modified in-place
        inflection_data (dict): all words inflection data
    """
    blacklist = ['Orthography',
                 'Glossing label',
                 'Lexical entry']
    if data['lexeme_id'] in inflection_data:
        data['inflection_data'] = inflection_data[data['lexeme_id']]
        for k in blacklist:
            del data['inflection_data'][k]
    else:
        data['inflection_data'] = None

page_names = set()
def check_page_name(label: str) -> None:
    """Checkpage name if it
    
    1) has the right format

    2) is unique

    Args:
        label (str): page name

    Raises:
        ValueError: format is incorrect
        ValueError: label is not unique (this func met it before)
    """
    chars = "[a-zA-Z0-9_\-'.]"
    if not re.match(f'^{chars}+(?:, )?{chars}*$', label):
        raise ValueError(f"Invalid format of page name: '{label}'")
    if label in page_names:
        raise ValueError(
            f"Not unique page name: '{label}'. There is already an entry with such name"
        )
    page_names.add(label)

def generate_pages(data_file: str, infl_files: List[str]):
    template_file = "word_template.html"
    out_dir = 'words'
    complex_poses = {}

    root = Path(__file__).parent.absolute()
    out_dir = root.joinpath(out_dir)
    if not out_dir.is_dir():
        out_dir.mkdir()
    
    env = Environment(loader=FileSystemLoader("."))
    word_template = env.get_template("templates/word_template.html")
    base_template = env.get_template("templates/base.html")


    inflection_data = load_inflection(*infl_files)
    glossing_labels = load_glossing_labels(data_file)

    os.system(f'rm {out_dir}/*')

    with open(data_file, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        col_names = next(reader)
        for row in tqdm(reader, desc='Generating pages'):
            data = dict(zip(col_names, row))
            merge_meanings(data)
            split_examples(data)
            insert_inflection(data, inflection_data)

            check_page_name(data['lexeme_id'])

            if data["Part of Speech"].startswith("complex"):
                complex_poses[data["lexeme_id"]] = f"This is a {data['Part of Speech']} consisting of the words: "
                complws = ["main_word", "2nd_word", "3rd_word"]
                complexx = []
                for compl in complws:
                    if data[compl]:
                        if data[f'{compl}_id']:
                            idd = data[f'{compl}_id']
                            complexx.append('<a href="{{ base_url }}words/' + f'{idd}">{data[compl]}</a>')
                        else:
                            complexx.append(data[compl])
                complexx = ", ".join(complexx)
                complex_poses[data["lexeme_id"]] += complexx

            out_file = out_dir.joinpath(
                f"{data['lexeme_id'].replace(', ', '-')}.html"
            )
            
            word_content = word_template.render(
                data=data,
                complex_poses=complex_poses,
                glossing_labels=glossing_labels
            )

            
            full_html = base_template.render(
                title=f"Kina Rutul — {data['Lexical entry']}",
                content=word_content,
                base_url="/kina-rutul-dict/"
            )


            
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_html)


if __name__ == '__main__':
    data_file = 'data/rutul_dict.tsv'
    infl_files = ['data/infl_adj.tsv',
                  'data/infl_noun.tsv',
                  'data/infl_verb.tsv']
    generate_pages(data_file, infl_files)