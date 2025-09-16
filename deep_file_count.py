import os
import sys

# Default: current directory, or use first CLI arg as root
ROOT_DIR = sys.argv[1] if len(sys.argv) > 1 else "."

total_files = 0
max_depth = 0
filetype_stats = {}
total_dirs = 0

def crawl_dir(path, depth=1):
    global total_files, max_depth, filetype_stats, total_dirs
    if depth > max_depth:
        max_depth = depth
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total_files += 1
                ext = os.path.splitext(entry.name)[-1].lower()
                filetype_stats[ext] = filetype_stats.get(ext, 0) + 1
            elif entry.is_dir():
                total_dirs += 1
                crawl_dir(entry.path, depth+1)
    except Exception as e:
        print(f"Error reading {path}: {e}")

# <-- This line actually runs the count!
crawl_dir(ROOT_DIR)

print(f"Total directories: {total_dirs}")
print(f"Total files: {total_files}")
print(f"Max depth reached: {max_depth}")
print("Filetype breakdown:")
for ext, count in sorted(filetype_stats.items(), key=lambda x: -x[1]):
    if ext:  # Only show files with real extensions
        print(f"  {ext}: {count}")
