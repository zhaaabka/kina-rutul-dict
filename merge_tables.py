import pandas as pd
import os
import sys


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)


n = pd.read_csv("data/NOUN_full.tsv", sep = "\t")
v = pd.read_csv("data/VERB_full.tsv", sep = "\t")
a = pd.read_csv("data/ADJ_full.tsv", sep = "\t")
cv = pd.read_csv("data/Complex_VERB.tsv", sep = "\t")

merged_dict = pd.concat([n, v, a, cv])

merged_dict_sorted = merged_dict.sort_values(by='Orthography')

merged_dict_sorted.to_csv("data/rutul_dict.tsv", sep='\t')
