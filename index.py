from jinja2 import Environment, FileSystemLoader
import os
import sys

env = Environment(loader=FileSystemLoader("."))

index_template = env.get_template("templates/index_template.html")
base_template = env.get_template("templates/base.html")

content = index_template.render(
    title="Kina Rutul Dictionary",
    paragraphs=[
        "This is the dictionary of the Rutul language (Lezgic &lt; East-Caucasian; <a href='https://glottolog.org/resource/languoid/id/rutu1240'>rutu1240</a>), spoken in the settlement of Kina (Russia, Dagestan Republic).",
        "This dictionary was collected during the fieldwork in 2016–2023 of Linguistic convergence laboratory (HSE University). We are grateful for all the consultants who helped us in our work.",
        "The dictionary contains 1200+ lexical entries of different parts of speech (nouns, verbs, etc.), list of meanings collected for these entries, exemplifying sentences and also some morphological information."
    ],
    bibtex_title="How to cite",
    citation_text=(
        "Dictionary of Kina Rutul.<br>"
        "Moscow.<br>"
        "<a href='https://lingconlab.github.io/kina-rutul-dict/'>https://lingconlab.github.io/kina-rutul-dict/</a>"
    ),
    citation_bibtex=(
        "@misc{alekseevaetal2025,<br>"
        "  title = {Dictionary of Kina Rutul},<br>"
        "  author = {A. Alekseeva and N. Beklemishev and M. Daniel and N. Dobrushina and K. Filatov and A. Ivanova and T. Maisak},<br>"
        "  year = 2025,<br>"
        "  publisher = {Linguistic Convergence Laboratory, HSE University},<br>"
        "  address = Moscow,<br>"
        "  url = https://lingconlab.github.io/kina-rutul-dict/<br>"
        "}"
    )
)

html = base_template.render(
    title="Dictionary of Kina Rutul",
    content=content,
    base_url="/kina-rutul-dict/"
)


with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Сгенерирован index.html")
