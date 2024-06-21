import pdfplumber
import json
import os

FileDescriptorOrPath: int | str

def extract_pdf_info(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            #print colored text in python
            text+=page.extract_text()
            text+=f"\n---{page.page_number}----------------------------\n"
        return text

def pdf_page_to_json(page, heightlim = 10000):
    content = page.extract_words()
    json = {}
    index = 0
    for word_token in content:
        if word_token['top'] >= heightlim :
            print(f"Scan stopped at {content[index]}")
            break
        font_size = word_token['height']
        direction = word_token['direction']
        x, y = word_token['x0'], word_token['top']
        text = word_token['text']
        json[str(index)] = {'text' : text, 'font_size' : font_size, 'direction' : direction, 'position':{'x' : x, 'y': y}}             
        index += 1
    return json

def pdf_to_json_file(json_fpath: str, pdf_file_path: str, heightlim=10000):
    pdf = pdfplumber.open(pdf_file_path)
    print("Json relative path: " + (json_fpath := os.path.relpath(json_fpath, os.getcwd())))

    remove_extension = lambda fname : fname[:fname.rfind('.')]
    for page in pdf.pages:
        jsonData = pdf_page_to_json(page, heightlim)
        json_fpath = json_fpath.join(".json") if (not json_fpath.endswith(".json")) else \
            (remove_extension(json_fpath)  + f"_{page.page_number}.json") if page.page_number > 1  else json_fpath
        json.dump(jsonData, open(json_fpath, 'w'), indent = 4)

def pdf_fpaths(dir = os.getcwd()) :
    pdf_dir = os.path.join(os.getcwd(), dir) if dir != os.getcwd() else dir  #C://..//pdf_folder
    pdf_fnames = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')] #*.pdf in files
    file_paths = [os.path.join(pdf_dir, f) for f in pdf_fnames] #C://current_folder/Files/*.pdf
    return file_paths
