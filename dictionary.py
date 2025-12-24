
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_dictionary.py
Считывает ./data/rutul_dict.tsv и создаёт dictionary.html,
Адаптация исправляет пустые колонки Russian/English.
"""

import pandas as pd
import html
import os
import sys
from jinja2 import Environment, FileSystemLoader

INPUT_TSV = os.path.join("data", "rutul_dict.tsv")
OUTPUT_HTML = "dictionary.html"
STYLESHEET = "styles.css"

if not os.path.exists(INPUT_TSV):
    print(f"Ошибка: не найден {INPUT_TSV}", file=sys.stderr)
    sys.exit(1)

"""
def find_col(df_cols, keywords):
    lc = [c for c in df_cols]
    for kw in keywords:
        kwl = kw.lower()
        for orig, n in zip(df_cols, lc):
            if kwl in n:
                return orig
    return None

def make_meaning_html_from_row(row, cols):
    # cols: список реальных имён колонок, которые нужно проверить в порядке 1..4
    items = []
    for col in cols:
        if col in row.index:
            v = row[col]
            if pd.isna(v):
                continue
            s = str(v).strip()
            if s == "" or s.upper() == "NA":
                continue
            items.append(html.escape(s))
    if len(items) == 0:
        return ""
    elif len(items) == 1:
        return items[0]
    else:
        lis = "\n".join(f"<li>{it}</li>" for it in items)
        return f"<ol>\n{lis}\n</ol>"
"""

# Читаем tsv
df = pd.read_csv(INPUT_TSV, sep="\t", dtype=str)
orig_cols = list(df.columns)

col_lexeme = "lexeme_id"
col_glossing = "Glossing label"
col_nostress = "No stress"
col_orth = "Orthography"
col_pos = "Part of Speech"

"""
# Определяем реальные имена колонок для значений (если есть)
meanings_rus = []
meanings_eng = []
for i in range(1,5):
    # пытаемся найти разные варианты имени
    c_rus = f"meaning_{i}_rus"
    c_eng = f"meaning_{i}"
    meanings_rus.append(c_rus)
    meanings_eng.append(c_eng)
"""
    
"""
# Для простоты создадим стандартные колонки в df (они могут содержать None)
for i in range(1,5):
    df.setdefault(f"meaning_{i}_rus", None)
    df.setdefault(f"meaning_{i}", None)
    # Если исходные колонки найдены — скопируем их в стандартизованные имена
    if meaning_rus_cols[i-1] is not None:
        df[f"meaning_{i}_rus"] = df[meaning_rus_cols[i-1]]
    if meaning_eng_cols[i-1] is not None:
        df[f"meaning_{i}"] = df[meaning_eng_cols[i-1]]
"""
        
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

    """
    rus_html = make_meaning_html_from_row(r, [f"meaning_{i}_rus" for i in range(1,5)])
    eng_html = make_meaning_html_from_row(r, [f"meaning_{i}" for i in range(1,5)])
    """

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

# 1. рендерим КОНТЕНТ таблицы
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

print(f"Готово: сгенерирован {OUTPUT_HTML}")
