from constants import DATA_PATH


def remove_duplicates():
    duplicates = list(DATA_PATH.glob("*(1).md"))
    if duplicates:
        for dupe in duplicates:
            print(f"Removing duplicate file: {dupe}")
            dupe.unlink()

def md_to_text(md_file):
        txt_file_name = f"{md_file.stem.casefold()}.txt"
        txt_file_path = DATA_PATH / txt_file_name
        with open(md_file, "r", encoding="utf-8") as md:
            content = md.read()

        with open(txt_file_path, "w", encoding="utf-8") as txt:
            txt.write(content)  

        print(f"converted {md_file} to {txt_file_name}")
    
if __name__ == "__main__":    
    remove_duplicates()

    for file in DATA_PATH.glob("*.md"):
        md_to_text(file)
