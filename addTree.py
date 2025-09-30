import os

# change this to your extracted folder path
base_dir = r"D:\FiFa 19\anything-llm-master\anything-llm-master"

# extensions you want to keep
code_extensions = {
    ".py", ".js", ".ts", ".jsx", ".json", ".yaml", ".yml", ".sh", ".sql",
    ".css", ".html", ".md", ".cjs", ".mjs", ".toml", ".tf", ".prisma"
}

output_file = "code_files_tree.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(os.path.basename(base_dir) + "\n")  # root folder name

    for root, dirs, files in os.walk(base_dir):
        # build indentation based on depth
        level = root.replace(base_dir, "").count(os.sep)
        indent = "│   " * level

        # write folder name (skip root since already written)
        if root != base_dir:
            f.write(f"{indent}└── {os.path.basename(root)}\n")

        sub_indent = "│   " * (level + 1)
        for file in sorted(files):
            ext = os.path.splitext(file)[1].lower()
            if ext in code_extensions:
                f.write(f"{sub_indent}{file}\n")

print(f"Tree structure of code files saved to {output_file}")
