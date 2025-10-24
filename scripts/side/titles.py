import re
import os
import json

titles = []

for file_index, file in enumerate(os.listdir("chapters/cont")):
    if not file.endswith(".txt"):
        continue
    with open(f"./chapters/cont/{file}", "r", encoding="utf-8") as f:
        textStr = f.read()
        text = textStr.split("\n")

    titles.append(
        {"index": int(file.replace(".txt",""))-1, "title": text[0].replace("<title>", "")}
    )

titles = sorted(titles, key=lambda d: d['index'])

# Ensure non-ASCII characters are written properly
json.dump(
    titles,
    open("./website/meta/cont.json", "w", encoding="utf-8"),
    ensure_ascii=False,
)

with open("./website/meta/cont_meta.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(
            {
                "title": "Omniscient Reader's Viewpoint Sequel (Ch 553+)",
                "author": "Sing Shong",
                "chapters": len(titles),
                "status": "Ongoing",
            }
        )
    )

for index, item in enumerate(titles):
    print(
        f"""<div class="chapter_item"><p><a href="#chapter{index}">{item["title"]}</a></p></div>"""
    )
