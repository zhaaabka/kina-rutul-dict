from pathlib import Path
import subprocess

root_dir = Path(__file__).parent

scripts = [
    root_dir / "misc_code" / "merge_tables.py",
    root_dir / "misc_code" / "full_dict_generate.py",
    root_dir / "dictionary.py",
    root_dir / "index.py",
    root_dir / "instructions.py",
    root_dir / "search.py",
    root_dir / "word_generate.py"
]


for s in scripts:
    print(f"Запускаем {s}...")
    subprocess.run(["python", str(s)], check=True, cwd=root_dir)
