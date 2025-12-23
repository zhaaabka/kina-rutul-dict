from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))

template = env.get_template("templates/index_template.html")

html = template.render(
    title="Dictionary of Kina Rutul",
    paragraphs=[
        "This is the dictionary of the Rutul language (Lezgic < East-Caucasian; <a href='https://glottolog.org/resource/languoid/id/rutu1240'>rutu1240</a>), spoken in the settlement of Kina (Russia, Dagestan Republic).",
        "This dictionary was collected during the fieldwork in 2016-2023 of Linguistic convergence laboratory (HSE University). We are grateful for all the consultants who helped us in our work.",
        "The dictionary contains 1200+ lexical entries of different parts of speech (nouns, verbs, etc.), list of meanings collected for these entries, exemplifying sentences and also some morphological information."
    ],
    bibtex_title="How to cite",
    citation_text=(
        "Dictionary of Kina Rutul.\n"
        "Moscow.\n"
        "<a href='https://lingconlab.github.io/kina-rutul-dict/'>https://lingconlab.github.io/kina-rutul-dict/</a>"
    ),
    citation_bibtex=(
        "@misc{alekseevaetal2025,\n"
        "  title = {Dictionary of Kina Rutul},\n"
        "  author = {A. Alekseeva and N. Beklemishev and M. Daniel and N. Dobrushina and K. Filatov and A. Ivanova and T. Maisak},\n"
        "  year = 2025,\n"
        "  publisher = {Linguistic Convergence Laboratory, HSE University},\n"
        "  address = Moscow,\n"
        "  url = <a href='https://lingconlab.github.io/kina-rutul-dict/'>https://lingconlab.github.io/kina-rutul-dict/</a>\n"
        "}"
    )
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html создан")
