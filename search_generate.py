from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))

search_template = env.get_template("templates/search_template.html")
base_template = env.get_template("templates/base.html")

content = search_template.render(base_url="/kina-rutul-dict/")

html = base_template.render(
    title="Search — Kina Rutul",
    content=content,
    base_url="/kina-rutul-dict/"
)

with open("search.html", "w", encoding="utf-8") as f:
    f.write(html)
