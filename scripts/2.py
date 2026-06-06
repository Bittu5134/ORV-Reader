import os
import re
import subprocess
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# --- CONFIGURATION ---
INPUT_ROOT = "./original_images"
DESTINATION_ROOT = "./images"
MAX_NAME_LENGTH = 30
WEBP_QUALITY = "95"
LOSSLESS_DEFAULT = False


# "Beautiful" Log Formatting
class BeautifulFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s | %(levelname)-8s | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(BeautifulFormatter())
logger = logging.getLogger("ORV_Processor")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def sanitize_filename(original_name):
    name_stem = Path(original_name).stem
    sanitized = name_stem.replace(" ", "_")
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", sanitized)
    return sanitized[:MAX_NAME_LENGTH].lower()


def process_single_image(args):
    img_path, output_dir = args
    img_path = Path(img_path)
    is_webp = img_path.suffix.lower() == ".webp"

    new_name = sanitize_filename(img_path.name)
    output_path = Path(output_dir) / f"{new_name}.webp"

    # Collision Check
    if output_path.exists():
        return {
            "status": "SKIPPED",
            "src": str(img_path),
            "dest": str(output_path),
            "reason": "Collision/Exists",
        }

    cmd = ["magick", str(img_path), "-strip"]
    if is_webp:
        cmd.extend(["-define", "webp:lossless=true"])
    else:
        cmd.extend(["-quality", WEBP_QUALITY])
        if LOSSLESS_DEFAULT:
            cmd.extend(["-define", "webp:lossless=true"])

    cmd.append(str(output_path))

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return {"status": "SUCCESS", "src": str(img_path), "dest": str(output_path)}
    except subprocess.CalledProcessError as e:
        return {
            "status": "ERROR",
            "src": str(img_path),
            "reason": e.stderr.decode().strip(),
        }


def main():
    logger.info("🚀 INITIALIZING: ORV Image Processor")

    input_root = Path(INPUT_ROOT)
    dest_root = Path(DESTINATION_ROOT)

    if not input_root.exists():
        logger.error(f"❌ Source folder '{INPUT_ROOT}' not found.")
        return

    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
    all_tasks = []

    for img_path in input_root.rglob("*"):
        if img_path.suffix.lower() in valid_extensions:
            rel_path = img_path.parent.relative_to(input_root)
            target_dir = dest_root / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)
            all_tasks.append((img_path, target_dir))

    total_input = len(all_tasks)
    logger.info(f"📂 SCAN COMPLETE: Found {total_input} images to process.")

    results = []
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(process_single_image, task): task for task in all_tasks
        }

        for future in as_completed(futures):
            res = future.result()
            results.append(res)

            # Real-time Logging
            if res["status"] == "SUCCESS":
                logger.info(f"✅ {Path(res['src']).name} -> {Path(res['dest']).name}")
            elif res["status"] == "SKIPPED":
                logger.warning(f"⚠️  SKIPPED: {Path(res['src']).name} ({res['reason']})")
            else:
                logger.error(f"❌ ERROR: {Path(res['src']).name} - {res['reason']}")

    # --- FINAL REPORT ---
    success_list = [r for r in results if r["status"] == "SUCCESS"]
    skipped_list = [r for r in results if r["status"] == "SKIPPED"]
    error_list = [r for r in results if r["status"] == "ERROR"]

    print("\n" + "━" * 50)
    print("📊 FINAL CONVERSION SUMMARY")
    print("━" * 50)
    print(f"  📥 Total Input Images:  {total_input}")
    print(f"  📤 Successfully Saved: {len(success_list)}")
    print(f"  ⚠️  Files Skipped:      {len(skipped_list)}")
    print(f"  ❌ Errors Encountered:  {len(error_list)}")
    print("━" * 50)

    if skipped_list:
        print("\n🔍 DETAILED SKIP LIST:")
        for item in skipped_list:
            print(
                f"  - {item['src']} \n    -> Destination {item['dest']} already exists."
            )

    if error_list:
        print("\n🔍 DETAILED ERROR LIST:")
        for item in error_list:
            print(f"  - {item['src']}: {item['reason']}")

    logger.info("✨ Process complete.")


if __name__ == "__main__":
    main()
