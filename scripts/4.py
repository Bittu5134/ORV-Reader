import os
import re
import asyncio
import json
import shutil
import imagesize
from pathlib import Path
import frontmatter

# --- CONFIGURATION ---

# Where your .webp images are physically located (for imagesize)
IMG_STORAGE_DIR = Path("images")

# The URL prefix 11ty will use for images in the final site
IMG_PUBLIC_PREFIX = "/assets/chapters"

# 11ty settings
LAYOUT_NAME = "layouts/chapter.njk"
OUTPUT_ROOT = Path("website/src/story/")
META_OUTPUT_PATH = Path("website/src/data/meta.json")

MAX_CONCURRENT_TASKS = 75
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
completed_count = 0
PATHS = ["./chapters/orv/original/"]

# --- CORE LOGIC ---


def process_html_images(html_content):
    """
    Finds img tags, ensures paths point to /assets/images/orv/...,
    reads dimensions from local storage, and injects width/height.
    """

    def replacer(match):
        full_tag = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', full_tag)
        if not src_match:
            return full_tag

        old_path = src_match.group(1)
        normalized_path = old_path.replace("\\", "/")

        if "/images/" in normalized_path:
            relative_part = normalized_path.split("/images/")[-1]
        elif "images/" in normalized_path:
            relative_part = normalized_path.split("images/")[-1]
        else:
            relative_part = Path(old_path).name

        rel_path_obj = Path(relative_part)
        new_src = f"{IMG_PUBLIC_PREFIX}/{rel_path_obj.as_posix()}"
        local_file_path = IMG_STORAGE_DIR / rel_path_obj

        width_attr = ""
        height_attr = ""

        if local_file_path.exists():
            try:
                w, h = imagesize.get(local_file_path)
                width_attr = f' width="{w}"'
                height_attr = f' height="{h}"'
            except:
                pass
        else:
            print(f"::warning::Image not found for sizing: {local_file_path}")

        new_tag = re.sub(r'src=["\'].*?["\']', f'src="{new_src}"', full_tag)

        # Inject dimensions and lazy loading for static HTML
        dims = f'{width_attr}{height_attr} loading="lazy"'
        if "/>" in new_tag:
            new_tag = new_tag.replace("/>", f"{dims} />")
        else:
            new_tag = new_tag.replace(">", f"{dims}>")

        return new_tag

    return re.sub(r"<img\s+[^>]*?>", replacer, html_content, flags=re.DOTALL)


async def convert_chapter(post_content, post_meta, output_file, total_tasks):
    global completed_count

    async with semaphore:
        # We use Pandoc to convert MD to HTML while keeping your ORV-specific divs
        process = await asyncio.create_subprocess_exec(
            "pandoc",
            "-f",
            "markdown",
            "-t",
            "html",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate(input=post_content.encode("utf-8"))

        if stderr:
            print(f"Pandoc Error for {post_meta.get('title')}: {stderr.decode()}")

        html_body = process_html_images(stdout.decode("utf-8"))

        # Add 11ty-specific frontmatter
        # We merge your original metadata with the 11ty layout requirement
        eleventy_meta = post_meta.copy()
        eleventy_meta["layout"] = LAYOUT_NAME
        eleventy_meta["story"] = "ORV"
        eleventy_meta["tl"] = "ORIGINAL"

        # Construct the final file: Frontmatter + Pandoc HTML
        final_output = frontmatter.dumps(frontmatter.Post(html_body, **eleventy_meta))

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_output)

        completed_count += 1
        if completed_count % 10 == 0 or completed_count == total_tasks:
            print(f"Progress: [{completed_count}/{total_tasks}]")


async def main():
    paths = PATHS

    if OUTPUT_ROOT.exists():
        # Only clean the specific book subfolder to be safe
        book_dir = OUTPUT_ROOT / "orv"
        if book_dir.exists():
            shutil.rmtree(book_dir)
            print(f"Cleaned {book_dir}")

    tasks_data = []
    meta_map = {}

    for path in paths:
        if not os.path.exists(path):
            continue

        # Load master metadata for the book
        master_path = Path(path) / "0000.md"
        if not master_path.exists():
            continue

        masterMD = frontmatter.load(master_path)
        bookID = masterMD.get("metaBook", "orv")
        bookTL = masterMD.get("metaTl", "original").lower()

        if bookID not in meta_map:
            meta_map[bookID] = {}
        meta_map[bookID][bookTL] = []

        files = sorted(
            [f for f in os.listdir(path) if f.endswith(".md") and f != "0000.md"]
        )
        print(f"Indexing {len(files)} chapters for {bookID}...")

        for file in files:
            post = frontmatter.load(os.path.join(path, file))
            slug = str(post.metadata.get("slug"))

            # Remove H1 (redundant with layout title)
            post.content = re.sub(r"^#\s+.*", "", post.content, flags=re.MULTILINE)
            post.content = re.sub(r"^##\s+.*", "", post.content, flags=re.MULTILINE, count=1)

            if not slug:
                continue

            meta_map[bookID][bookTL].append(post.metadata)

            # Create folder-per-chapter for clean URLs (e.g., /read/orv/original/1/)
            dest_dir = OUTPUT_ROOT / bookID / bookTL / slug
            dest_dir.mkdir(parents=True, exist_ok=True)

            tasks_data.append(
                {
                    "content": post.content,
                    "meta": post.metadata,
                    "dest": dest_dir
                    / "index.html",  # Using index.html inside a slug folder
                }
            )

    # Save meta data for 11ty collections or sidebars
    META_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(META_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_map, f, indent=2)

    tasks_data = tasks_data[:50]

    total = len(tasks_data)
    print(f"Building {total} static pages...")

    tasks = [
        convert_chapter(td["content"], td["meta"], td["dest"], total)
        for td in tasks_data
    ]

    await asyncio.gather(*tasks)
    print("Build Complete. Ready for 11ty processing.")


if __name__ == "__main__":
    asyncio.run(main())
