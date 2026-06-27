import re
import os
import json

# Load existing discussion mapping if it exists to preserve discussion IDs
existing_discussions = {}
try:
    if os.path.exists("./website/meta/orv.json"):
        with open("./website/meta/orv.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            for item in existing_data:
                if "index" in item and "discussion" in item:
                    existing_discussions[item["index"]] = item["discussion"]
except Exception as e:
    print(f"Warning: Could not parse existing orv.json to load discussion IDs: {e}")

titles = []

for file_index, file in enumerate(os.listdir("chapters/orv")):
    if not file.endswith(".txt"):
        continue
    with open(f"./chapters/orv/{file}", "r", encoding="utf-8") as f:
        textStr = f.read()
        text = textStr.split("\n")

    index = int(file.replace("chap_","").replace(".txt",""))-1
    title_entry = {
        "index": index,
        "title": text[0].replace("<title>", "")
    }
    if index in existing_discussions:
        title_entry["discussion"] = existing_discussions[index]

    titles.append(title_entry)

titles = sorted(titles, key=lambda d: d['index'])

# Ensure non-ASCII characters are written properly
with open("./website/meta/orv.json", "w", encoding="utf-8") as f:
    json.dump(
        titles,
        f,
        ensure_ascii=False,
        indent=2,
    )

with open("./website/meta/orv_meta.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(
            {
                "title": "Omniscient Reader's Viewpoint",
                "author": "Sing Shong",
                "chapters": len(titles),
                "status": "Completed",
            },
            indent=2,
        )
    )

for index, item in enumerate(titles):
    print(
        f"""<div class="chapter_item"><p><a href="#chapter{index}">{item["title"]}</a></p></div>"""
    )
