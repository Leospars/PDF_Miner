import os
import json
from colorama import Fore
from pdf_json import pdf_to_json_file
from pdf_json import pdf_fpaths

cls = lambda: os.system("cls") if os.name == 'nt' \
    else os.system("clear")
cls()

keywords = ['Name', 'Address', 'Phone', 'Email', 'Date', 'Education', 'Experience', 'Skill']

# noinspection PyShadowingNames
def is_key_word(word: str, keywords=keywords):
    appends = [':', 's', 's:', '-', '']
    for append in appends:
        if word in [keyword + append for keyword in keywords]:
            return True


# if __name__ == "__main__":
fpaths = pdf_fpaths("Files")
json_fpath = os.path.join('Data', 'raw_data.json')
pdf_to_json_file(json_fpath, pdf_file_path=fpaths[0], heightlim=1000)

with open(json_fpath, 'r') as file:
    pdf_json = json.load(file)

extracted = {"Name": pdf_json['0']['text'] + " " + pdf_json['1']['text']}
print(extracted)

collect_key_data = False

for key in pdf_json:
    if key == "page":
        continue

    value = pdf_json[key]
    word = value['text']

    if is_key_word(word[0:-1]):  # Recall the last character is ':', e.g. 'Education:' so we exclude it
        keyword = word[0:-1]
        collect_key_data = True
        extracted[keyword] = ""
        continue

    if collect_key_data:
        extracted[keyword] += ' ' + word

#Store the extracted data in a json file
extract_fpath = os.path.join('Data', 'extract.json')
with open(extract_fpath, 'w') as f:
    json.dump(extracted, f, indent=4) #store the extracted data in a json file

client_name = extracted["Name"]
newdir = os.path.join("Client", client_name)
newpdf = os.path.join(newdir, client_name + " Resume.pdf")
newtxt = os.path.join(newdir, client_name + " Info.txt")

with open(newpdf, "wb") as dest, open(fpaths[0], "rb") as src:
    dest.write(src.read())

with open(newtxt, "w", encoding="UTF-16") as f:
    for key in extracted:
        f.write(f"{key} : {extracted[key]}\n")
