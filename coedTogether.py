import os

# change this to your extracted folder path
base_dir = r"D:\FiFa 19\anything-llm-master\anything-llm-master"

# extensions you want to include
code_extensions = {
    ".py", ".js", ".ts", ".jsx", ".json", ".yaml", ".yml",
    ".css", ".html",".cjs", ".mjs", ".prisma"
}

output_file = "all_code_combined.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(base_dir):
        for file in sorted(files):
            ext = os.path.splitext(file)[1].lower()
            if ext in code_extensions:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception as e:
                    content = f"<< Could not read file: {e} >>"
                
                out.write("-----\n")
                out.write(file + "\n")
                out.write("-----\n")
                out.write(content + "\n\n")

print(f"All code files scraped and saved into {output_file}")
