import re
import os
import json

titles = []

for file_index, file in enumerate(os.listdir("chapters/orv")):
    if not file.endswith(".txt"):
        continue
    with open(f"./chapters/orv/{file}", "r", encoding="utf-8") as f:
        textStr = f.read()
        text = textStr.split("\n")

    titles.append(
        {"index": int(file.replace("chap_","").replace(".txt",""))-1, "title": text[0].replace("<title>", "")}
    )

# Ensure non-ASCII characters are written properly
json.dump(
    titles,
    open("./website/meta/orv.json", "w", encoding="utf-8"),
    ensure_ascii=False,
)

with open("./website/meta/orv_meta.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(
            {
                "title": "Omniscent Reader's Viewpoint",
                "author": "Sing Shong",
                "chapters": len(titles),
                "status": "Completed",
            }
        )
    )

for index, item in enumerate(titles):
    print(
        f"""<div class="chapter_item"><p><a href="#chapter{index}">{item["title"]}</a></p></div>"""
    )
