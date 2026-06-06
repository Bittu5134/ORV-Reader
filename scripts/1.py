import re
import os
from pathlib import Path

# Configuration for image naming
MAX_NAME_LENGTH = 30
INPUT_DIR = "tmpch/orv"
OUTPUT_DIR = "chapters/orv/original"


def get_section(index):
    """Formerly get_volume. Vol mapping for section key."""
    if index <= 188:
        return "vol1"
    if index <= 284:
        return "vol2"
    if index <= 372:
        return "vol3"
    if index <= 445:
        return "vol4"
    return "vol5"


def normalize_punctuation(text):
    """Converts fancy punctuation to standard Pandoc-safe versions."""
    replacements = {
        "—": "--",
        "–": "--",
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
        "［": "[",
        "］": "]",
    }
    for fancy, plain in replacements.items():
        text = text.replace(fancy, plain)
    return text


def sanitize_filename(original_name):
    """Sanitizes image filenames to match the output of the image processor."""
    name_stem = Path(original_name).stem
    sanitized = name_stem.replace(" ", "_")
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", sanitized)
    return sanitized[:MAX_NAME_LENGTH]


def clean_speech_enclosures(text):
    """Removes outer decorative brackets for speech tags."""
    return re.sub(r"[\[\]【】「」『』]", "", text).strip()


def escape_angles(text):
    """Escapes < and > for Pandoc safety."""
    # return text.replace("<", r"\<").replace(">", r"\>")
    return text.replace("<br>", "\n").replace("<", r"\<")


def semantic_wrap(text, is_speech=False):
    """Normalizes, cleans, escapes, and splits sentences."""
    if is_speech:
        text = clean_speech_enclosures(text)
    text = normalize_punctuation(text)
    text = escape_angles(text)
    sentences = re.split(r"(?<=[.!?]) +", text)
    return "\n".join(sentences)


def parse_title_info(line):
    """Parses Ch: Ep/Epilogue - Title. Returns (Title, CategoryString)."""
    clean_line = line.replace("<title>", "").strip()

    # Pattern for Epilogue: "Ch 517: Epilogue 1 - The World of Zero, I"
    epi_match = re.search(
        r"Ch\s*\d+[:\s]*Epilogue\s*(\d+)\s*[–—\-]\s*(.*)", clean_line, re.IGNORECASE
    )
    if epi_match:
        epi_num = epi_match.group(1).strip()
        return normalize_punctuation(epi_match.group(2)), f"Epilogue {epi_num}"

    # Pattern for Episode: "Ch 185: Ep. 35 - The 73rd Demon King, IV"
    match = re.search(
        r"Ch\s*\d+[:\s]*Ep\.\s*([\d.]+)\s*[–—\-]\s*(.*)", clean_line, re.IGNORECASE
    )
    if match:
        ep_num = match.group(1).strip()
        return normalize_punctuation(match.group(2)), f"Episode. {ep_num}"

    # Fallback for simple titles (like Prologue)
    match_simple = re.search(r"Ch\s*\d+[:\s]*(.*)", clean_line, re.IGNORECASE)
    title = (
        normalize_punctuation(match_simple.group(1))
        if match_simple
        else normalize_punctuation(clean_line)
    )
    return title, "Prologue"


def convert():
    input_dir = INPUT_DIR
    output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])

    for i, filename in enumerate(files, start=1):
        with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines()]

        title_line = next((l for l in lines if l.startswith("<title>")), "")
        title_text, category_text = parse_title_info(title_line)

        final_title = f'"{title_text}"' if title_text else "null"
        final_category = category_text

        md_content = [
            "---",
            f"title: {final_title}",
            f"category: {final_category}",
            f"index: {i}",
            f'slug: "{i}"',
            "discussion: 1",
            f"section: {get_section(i)}",
            "---",
            "",
        ]

        print(f"Converting: {i:03d} | {title_text}")

        cover_line = next((l for l in lines if l.startswith("<cover>")), None)
        if cover_line:
            img_match = re.findall(r"\[(.*?)\]", cover_line)
            if img_match:
                clean_img_name = sanitize_filename(img_match[0])
                md_content.append(
                    f'![Cover Image](/images/orv/{clean_img_name.lower()}.webp){{.hidden-caption fetchpriority="high"}}\n'
                )

        md_content.append(f"||[TITLE]||")

        skip_until_plus = False
        skip_next_line = False

        for idx, line in enumerate(lines):
            if skip_next_line:
                skip_next_line = False
                continue

            if line.startswith("<title>") or line.startswith("<cover>"):
                continue

            if line.startswith("<img>"):
                img_match = re.findall(r"\[(.*?)\]", line)
                if img_match:
                    clean_img_name = sanitize_filename(img_match[0])
                    alt_text = (
                        normalize_punctuation(img_match[1])
                        if len(img_match) > 1
                        else ""
                    )
                    if idx + 1 < len(lines) and lines[idx + 1].startswith("<?>"):
                        raw_note = lines[idx + 1].replace("<?>", "").strip()
                        alt_text = normalize_punctuation(
                            re.sub(r"^\[\d+\]\s*", "", raw_note)
                        )
                        skip_next_line = True
                    md_content.append(
                        f"![{alt_text}](/images/orv/{clean_img_name.lower()}.webp)\n"
                    )

            elif line == "+" or line == "++":
                cls = "orv-window" if line == "+" else "orv-box"
                if not skip_until_plus:
                    md_content.append(f"::: .{cls}")
                    skip_until_plus = True
                else:
                    md_content.append(":::\n")
                    skip_until_plus = False

            elif line.startswith(("<@>", "<!>", "<#>", "<&>")):
                tag = line[:3]
                class_map = {
                    "<@>": "constellation",
                    "<!>": "system",
                    "<#>": "outergod",
                    "<&>": "quote",
                }
                content = semantic_wrap(line[3:], is_speech=True)
                md_content.append(f"::: .{class_map[tag]}\n{content}\n:::\n")

            elif line.startswith(("—", "--")):
                content = semantic_wrap(line, is_speech=False)
                md_content.append(f"::: .generic-box\n{content}\n:::\n")

            elif line.startswith("<?>"):
                note_content = re.sub(
                    r"^\[\d+\]\s*", "", line.replace("<?>", "").strip()
                )
                note_content = escape_angles(normalize_punctuation(note_content))
                md_content.append(f"NOTE^[{note_content}]\n")

            elif line == "***":
                md_content.append("___\n")
            elif line == "":
                md_content.append("")
            else:
                if skip_until_plus:
                    content = semantic_wrap(line, is_speech=line.startswith("["))
                    md_content.append(content + "\n")
                else:
                    md_content.append(semantic_wrap(line, is_speech=False) + "\n")

        while md_content and (
            not md_content[-1].strip() or md_content[-1].strip() == "___"
        ):
            md_content.pop()

        # Generate Display Header String
        if final_category.startswith("Episode"):
            # Extract number from "Episode. 35"
            try:
                num = final_category.split(".")[1].strip()
                title_index_category = f"EP{num}"
            except:
                title_index_category = final_category
        elif final_category.startswith("Epilogue"):
            # Format as "EPILOGUE 5" -> "EPILOGUE 5" (or keep as is)
            title_index_category = final_category.upper()
        else:
            title_index_category = final_category.upper()

        for title_index in range(len(md_content)):
            if md_content[title_index] == "||[TITLE]||":
                md_content[title_index] = (
                    f"## {title_index_category}:CH{i} - {title_text}\n"
                )

        with open(os.path.join(output_dir, f"{i:04d}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))


if __name__ == "__main__":
    convert()
