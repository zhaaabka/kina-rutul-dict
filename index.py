from jinja2 import Environment, FileSystemLoader
import os
import sys

env = Environment(loader=FileSystemLoader("."))

index_template = env.get_template("templates/index_template.html")
base_template = env.get_template("templates/base.html")

content = index_template.render(
    title="Kina Rutul Dictionary",
    paragraphs=[
        "This is the dictionary of the Rutul language (&lt; Lezgic &lt; Nakh-Dagestanian; <a href='https://glottolog.org/resource/languoid/id/rutu1240'>rutu1240</a>), spoken in the settlement of Kina (Russia, Dagestan Republic).",
        "This dictionary was collected during the fieldwork in 2016–2023 of Linguistic convergence laboratory (HSE University). We are very grateful for all the consultants who helped us in our work. The dictionary contains 1200+ lexical entries of different parts of speech (nouns, verbs, etc.), list of meanings collected for these entries, exemplifying sentences and also some morphological information."
    ],
    bibtex_title="How to cite",
    citation_text=('Alekseeva, Anastasia, Nikita Beklemishev, Michael Daniel, Nina Dobrushina, Konstantin Filatov, Anastasia Ivanova, Timur Maisak (2025). <i>Dictionary of Kina Rutul</i>. Moscow: Linguistic Convergence Laboratory. HSE University. <a href="https://zhaaabka.github.io/kina-rutul-dict/">https://zhaaabka.github.io/kina-rutul-dict/</a>.'),
    citation_bibtex=(
        "@book{alekseevaetal2025,<br>"
        "  title = {Dictionary of Kina Rutul},<br>"
        "  author = {Anastasia Alekseeva and Nikita Beklemishev and Michael Daniel and Nina Dobrushina and Kinstantin Filatov and Anastasia Ivanova and Timur Maisak},<br>"
        "  year = {2025},<br>"
        "  publisher = {Linguistic Convergence Laboratory, HSE University},<br>"
        "  address = {Moscow},<br>"
        "  url = {https://zhaaabka.github.io/kina-rutul-dict/}<br>"
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
