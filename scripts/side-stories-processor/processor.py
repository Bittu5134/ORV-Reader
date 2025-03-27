import os
import re



for file_index,file in enumerate(os.listdir("downloads")):

    file_index = re.match(r"[0-9]+", file)
    file_index = int(file_index.group(0))
    # if file_index != -1:
    #     continue

    if not file.endswith(".txt"):
        continue
    with open(f"./downloads/{file}", "r", encoding="utf-8") as f:
        text = f.read().split("\n")

    chap = ""
    title = file.replace(".txt", "")
    chap += f"<title>{title.replace("Chapter","Ch")}\n"

    text.pop(0)

    for index,line in enumerate(text):

        if line == "":
            chap += "\n"
        elif line.startswith("["):
                cleaned_text = re.sub(r"[\[\]]", "", line)
                chap += f"<!>[{cleaned_text}]\n"
        elif line.startswith("【"):
                cleaned_text = re.sub(r"[【】]", "", line)
                chap += f"<#>【{cleaned_text}】\n"
        elif line.startswith("「"):
                cleaned_text = re.sub(r"[「」]", "", line)
                chap += f"<&>「{cleaned_text}」\n"
        elif line.startswith("(TL"):
                cleaned_text = re.sub(r"[()]", "", line)
                chap += f"<?>{cleaned_text.replace("TL: ", "")}"
        elif line == "*":
            chap += f"***\n"
        else:
            chap += line+"\n"
        
    with open(f"./chapters/cont/{file_index}.txt", "w", encoding="utf-8") as f:
        f.write(chap)
