import os
import subprocess
import glob
from concurrent.futures import ThreadPoolExecutor

src_dir = r"E:\Coding\ORV-Reader\temp_mtl"
dest_dir = r"E:\Coding\ORV-Reader\temp_mtl"

def convert_file(docx_path):
    base = os.path.basename(docx_path)
    name, _ = os.path.splitext(base)
    md_path = os.path.join(dest_dir, name + ".md")
    
    try:
        # Convert to markdown
        subprocess.run(["pandoc", docx_path, "-o", md_path], check=True)
    except Exception as e:
        print(f"Error converting {base}: {e}")

def main():
    docx_files = glob.glob(os.path.join(src_dir, "*.docx"))
    print(f"Found {len(docx_files)} docx files to convert.")
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(convert_file, docx_files)
        
    print("Conversion complete!")

if __name__ == "__main__":
    main()
