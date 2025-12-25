import pandas as pd

path = "D:/github/kina-rutul-dict/kina-rutul-dict/data/"

n = pd.read_csv(path + "NOUN_full.tsv", sep = "\t")
v = pd.read_csv(path + "VERB_full.tsv", sep = "\t")
a = pd.read_csv(path + "ADJ_full.tsv", sep = "\t")
cv = pd.read_csv(path + "Complex_VERB.tsv", sep = "\t")

merged_dict = pd.concat([n, v, a, cv])

merged_dict_sorted = merged_dict.sort_values(by='Orthography')

merged_dict_sorted.to_csv(path + "rutul_dict.tsv", sep='\t')

print('Общая таблица сгенерирована!')