import json
import pandas as pd

df = pd.read_csv("data/rutul_dict.tsv", sep='\t')

dict = {}

for _, r in df.iterrows():
    word = f"{r['No stress']} | {r['Orthography']}"
    pos = r['Part of Speech']
    if pos == "complex verb":
        pos = 'cv'
    elif pos == "complex noun":
        pos = 'cn'
    elif pos == "noun, adjective":
        pos = 'n/adj'
    elif pos == "adjective":
        pos = "adj"
    else:
        pos = pos[0]
    
    dict[word] = {}
    dict[word]['id'] = r['lexeme_id']
    dict[word]['pos'] = pos
    dict[word]['inflection'] = []

    infls = ["Gender", "Attributive", "Co-verbal form", "Adverbial form", "IPFV.3", "INF.3", "IMP.3", "PROH.3"]
    for infl in infls:
        if str(r[infl]) != "nan":
            dict[word]['inflection'].append(r[infl])
    
    dict[word]['translations'] = []
    for i in range(1, 5):
        if str(r[f'meaning_{i}']) != "nan":
            transl = {}
            transl['text_rus'] = r[f'meaning_{i}_rus']
            transl['text_en'] = r[f'meaning_{i}']
            dict[word]['translations'].append(transl)
    
    dict[word]['examples'] = []
    for i in range(1, 5):
        example = r[f'example_{i}']
        if str(example) != "nan":
            examples = example.split(" ; ")
            examples_cyr = r[f'example_{i}_cyr'].split(" ; ")
            examples_transl = r[f'example_{i}_rus'].split(" ; ")
            length = min(len(examples), min(len(examples_cyr), len(examples_transl)))
            for l in range(length):
                ex = {}
                ex['original'] = examples[l] + " | " + examples_cyr[l]
                ex['translation'] = examples_transl[l]
                dict[word]['examples'].append(ex)
            
with open("full_dict.js", "w", encoding="utf-8") as f:
    f.write("window.data = ")
    json.dump(
        dict,
        f,
        ensure_ascii=False,
        indent=2
    )
    f.write(";\n")