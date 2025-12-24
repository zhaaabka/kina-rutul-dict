
import pandas as pd
import html
import os
import sys
from jinja2 import Environment, FileSystemLoader

INPUT_TSV = os.path.join("data", "rutul_dict.tsv")
OUTPUT_HTML = "dictionary.html"

if not os.path.exists(INPUT_TSV):
    print(f"Ошибка: не найден {INPUT_TSV}", file=sys.stderr)
    sys.exit(1)


df = pd.read_csv(INPUT_TSV, sep="\t", dtype=str)
orig_cols = list(df.columns)

col_lexeme = "lexeme_id"
col_glossing = "Glossing label"
col_nostress = "No stress"
col_orth = "Orthography"
col_pos = "Part of Speech"
        
if col_glossing is None or col_lexeme is None:
    print("Не найдены обязательные колонки Glossing.label или lexeme_id.", file=sys.stderr)
    sys.exit(1)

rows_html = []
for _, r in df.iterrows():
    lex = r[col_lexeme] if not pd.isna(r[col_lexeme]) else ""
    lex_s = str(lex).replace(", ", "-")
    href = f'words/{html.escape(lex_s)}.html'

    gloss_label = r[col_glossing] if not pd.isna(r[col_glossing]) else ""
    gloss_label = html.escape(str(gloss_label))
    href_html = f'<a href="{href}">{gloss_label}</a>'

    lex_entry = r[col_nostress] if col_nostress and not pd.isna(r[col_nostress]) else ""
    orth = r[col_orth] if col_orth and not pd.isna(r[col_orth]) else ""
    pos = r[col_pos] if col_pos and not pd.isna(r[col_pos]) else ""

    meanings_rus = []
    meanings_eng = []
    for i in range(1, 5):
        if str(r[f"meaning_{i}_rus"]) != "nan":
            meanings_rus.append(r[f"meaning_{i}_rus"])
        if str(r[f"meaning_{i}"]) != "nan":
            meanings_eng.append(r[f"meaning_{i}"])

    if len(meanings_rus) > 1:
        rus_html = ""
        for j in range(len(meanings_rus)):
            sep = "<br>" if j < len(meanings_rus) - 1 else ""
            rus_html += f"{j + 1}. {html.escape(meanings_rus[j])}{sep}"
    else:
        rus_html = html.escape(meanings_rus[0])

    
    if len(meanings_eng) > 1:
        eng_html = ""
        for j in range(len(meanings_eng)):
            sep = "<br>" if j < len(meanings_eng) - 1 else ""
            eng_html += f"{j + 1}. {html.escape(meanings_eng[j])}{sep}"
    else:
        eng_html = html.escape(meanings_eng[0])


    rows_html.append({
        "Glossing Label": href_html,
        "Lexical entry": html.escape(str(lex_entry)) if lex_entry is not None else "",
        "Orthography": html.escape(str(orth)) if orth is not None else "",
        "Russian": rus_html,
        "English": eng_html,
        "Part of Speech": html.escape(str(pos)) if pos is not None else ""
    })

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=True
)

dict_template = env.get_template("templates/dictionary_template.html")
base_template = env.get_template("templates/base.html")


columns = [
    "Glossing Label",
    "Lexical entry",
    "Orthography",
    "Russian",
    "English",
    "Part of Speech"
]

content = dict_template.render(
    columns=columns,
    rows=rows_html
)

html_out = base_template.render(
    title="Dictionary of Kina Rutul",
    content=content,
    base_url="/kina-rutul-dict/"
)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"Сгенерирован {OUTPUT_HTML}")
