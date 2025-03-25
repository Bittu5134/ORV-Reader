import re
import os
import urllib
import random
import urllib.parse
import csv

with open('.\scripts\main_epub_processor\data\data.csv', 'r') as file:
    data = csv.DictReader(file)
    systemLines = []
    for i in data:
        if i["type"] == "true":
            systemLines.append(i["line"])


images = []
counter = 0

for file_index,file in enumerate(os.listdir("formatted")):
    if not file.endswith(".txt"):
        continue
    with open(f"./formatted/{file}", "r", encoding="utf-8") as f:
        textStr = f.read()
        text = textStr.split("\n")
    
    for index,line in enumerate(text):
        if line.startswith("<!>"):
            match = line.replace("<!>", "")
            match: str = match.lower()
            match = re.findall(r"[a-z0-9'<> ]?", match)
            match = "".join(match)
            match = re.sub(r"(\w)'(\w)", r"\1\2", match)
            match = re.sub(r"'.*?'", "BLANK", match)
            match = re.sub(r"[0-9]+", "0", match)
            match = re.sub(r"<.*?>", "NEBULA", match)
            match = match.replace("'", "")
            if not match in systemLines:
                counter += 1
                text[index] = line.replace("<!>", f"<@>")
                

    with open(f"./formatted/{file}", "w", encoding="utf-8") as f:
        f.write("\n".join(text))


print(counter)

