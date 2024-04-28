import os
import shutil
import sys

def copy_files(source_path, target_path, file_extension=None):
    count = 0

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file_extension is None or file.endswith(file_extension):
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_file_path, source_path)
                target_file_path = os.path.join(target_path, relative_path)
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                shutil.copy2(source_file_path, target_file_path)
                count += 1

    return count

def main():
    if len(sys.argv) < 3:
        print("Usage: python copy_files.py <source_path> <target_path> [<file_extension>]")
        return

    source_path = sys.argv[1]
    target_path = sys.argv[2]
    file_extension = None

    if len(sys.argv) > 3:
        file_extension = sys.argv[3]

    count = copy_files(source_path, target_path, file_extension)
    print(f"Successfully copied {count} file(s) from {source_path} to {target_path}.")

if __name__ == "__main__":
    main()
