import json
import pandas as pd

df = pd.read_csv("data/rutul_dict.tsv", sep='\t')

pages = []

for _, r in df.iterrows():
    id = r['lexeme_id']
    content = ""
    cols = ["Lexical entry", "No stress", "Orthography", "Glossing label", "Attributive", "Co-verbal form", "Adverbial form", "PFV.3", "IPFV.3", "INF.3", "IMP.3", "PROH.3"]
    for i in range(1, 5):
        more_cols = [f"meaning_{i}", f"meaning_{i}_rus", f"example_{i}", f"example_{i}_cyr", f"example_{i}_rus"]
        for c in more_cols:
            cols.append(c)
    
    for col in cols:
        if str(r[col]) != "nan":
            content += str(r[col]) + " "
    
    
    pages.append({
        "id": id,
        "title": r["Lexical entry"],
        "content": content,
        "url": f"/kina-rutul-dict/words/{id}"
    })

with open("search.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)
