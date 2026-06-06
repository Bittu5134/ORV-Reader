import os
import re
import subprocess
import frontmatter
import datetime
from collections import defaultdict

# --- CONFIGURATION ---
PATH = "./chapters/orv/original/"
OUTPUT_FOLDER = "./epub"
CSS_PATH = "./scripts/epub.css"
COVER_IMAGE = "./images/orv/cover.webp"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
today = datetime.date.today().strftime("%B %d, %Y")


def build_orv():
    print(f"{'='*100}\n🚀 Starting Robust ORV Build")

    # 1. Index Chapters
    files = [f for f in os.listdir(PATH) if f.endswith(".md") and f != "0000.md"]
    chapters_by_vol = defaultdict(list)

    for file in files:
        post = frontmatter.load(os.path.join(PATH, file))
        vol_key = post.metadata.get("section")
        chapters_by_vol[vol_key].append(
            {
                "index": post.metadata["index"],
                "discussion": post.metadata.get("discussion", 1),
                "content": post.content,
            }
        )

    print(f"📂 Indexed {len(files)} chapters. Processing template...")

    # 2. Extract Metadata and Template from 0000.md
    with open(os.path.join(PATH, "0000.md"), "r", encoding="utf-8") as f:
        raw_0000 = f.read().lstrip()  # CRITICAL: Remove any leading whitespace

    # We find the end of the YAML block to keep the exact original text
    # This prevents the "expected -" YAML error from earlier
    meta_end_index = raw_0000.find("---", 3)
    if meta_end_index == -1:
        print("❌ Error: Could not find end of YAML metadata in 0000.md")
        return

    # Extract the block INCLUDING the separators
    yaml_header = raw_0000[: meta_end_index + 3].strip()
    template_body = raw_0000[meta_end_index + 3 :]

    # Apply global replacements to the body
    template_body = template_body.replace("{{DATE}}", today)
    template_body = template_body.replace("{{TYPE}}", "Digital Edition")

    # 3. Split the template by your new placeholder format
    template_parts = re.split(r"(--\[vol\d+\] --)", template_body)

    temp_md_path = os.path.join(OUTPUT_FOLDER, "temp_orv_build.md")

    # 4. Stream to Disk
    with open(temp_md_path, "w", encoding="utf-8") as build_file:
        # Write YAML Header - This MUST be the first thing written
        build_file.write(yaml_header + "\n\n")

        for part in template_parts:
            # Check if current part is a placeholder
            match = re.match(r"--\[(vol\d+)\] --", part)

            if match:
                vol_name = match.group(1)
                if vol_name in chapters_by_vol:
                    print(
                        f"📦 Injecting {vol_name} ({len(chapters_by_vol[vol_name])} chapters)"
                    )

                    # Sort chapters
                    chapters_by_vol[vol_name].sort(key=lambda x: int(x["index"]))

                    for chap in chapters_by_vol[vol_name]:
                        content = chap["content"].strip()
                        # Path fix for Pandoc
                        content = content.replace("(/images/", "(images/")

                        build_file.write(content + "\n\n")

                        # Footer
                        footer = f"___\n- [Read Comments](https://github.com/Bittu5134/ORV-Reader/discussions/{chap['discussion']})\n\n"
                        build_file.write(footer)
            else:
                # Normal template text (Foreword, Afterword, Volume Titles)
                build_file.write(part)

    # 5. Run Pandoc
    # Extract title for filename
    title_match = re.search(r"text:\s*'(.*?)'", yaml_header)
    book_title = title_match.group(1) if title_match else "ORV"
    epub_filename = f"{book_title} - Original.epub"
    epub_path = os.path.join(OUTPUT_FOLDER, epub_filename)

    print(f"🛠️  Invoking Pandoc...")

    cmd = [
        "pandoc",
        temp_md_path,
        "-o",
        epub_path,
        "--to=epub3",
        "--css",
        CSS_PATH,
        "--toc",
        "--toc-depth=3",
        "--split-level=2",
        f"--epub-cover-image={COVER_IMAGE}",
        "--epub-title-page=false",
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✨ SUCCESS! EPUB structure preserved: {epub_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc Error: {e}")


if __name__ == "__main__":
    build_orv()
