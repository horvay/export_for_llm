import os
import datetime
import argparse


def generate_folder_structure_md(folder_path, output_file, exclude_folders):
    """
    Generate a markdown file showing folder structure and contents of Python files.

    Args:
        folder_path (str): Path to the folder to analyze
        output_file (str): Path to the output markdown file
        exclude_folders (list): List of folder names to exclude
    """
    # Validate folder path
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        return

    # Convert exclude_folders to absolute paths and just folder names for comparison
    exclude_paths = set()
    exclude_names = set()
    for folder in exclude_folders:
        abs_path = os.path.abspath(folder)
        exclude_paths.add(abs_path)
        exclude_names.add(os.path.basename(abs_path.rstrip("/\\")))

    # Open the output file
    with open(output_file, "w", encoding="utf-8") as md_file:
        # Write header
        md_file.write("# Project Structure and Code\n\n")
        md_file.write(
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )
        md_file.write(f"Root folder: `{folder_path}`\n\n")
        if exclude_folders:
            md_file.write(f"Excluded folders: {', '.join(exclude_names)}\n\n")

        # Write folder structure header
        md_file.write("## Folder Structure\n\n")
        md_file.write("```\n")

        # Generate folder structure
        for root, dirs, files in os.walk(folder_path):
            # Skip if this directory is in exclude list
            if os.path.abspath(root) in exclude_paths:
                dirs[:] = []  # Prevent descending into subdirectories
                continue

            # Skip hidden directories and excluded directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and not d.startswith("__")
                and not d == "dist"
                and not d == "build"
                and os.path.abspath(os.path.join(root, d)) not in exclude_paths
                and d not in exclude_names
            ]

            # Calculate indentation level
            level = root.replace(folder_path, "").count(os.sep)
            indent = "  " * level

            # Write directory name
            dir_name = os.path.basename(root) or os.path.basename(folder_path)
            md_file.write(f"{indent}{dir_name}/\n")

            # Write files (excluding hidden files)
            for file in sorted(files):
                if not file.startswith("."):
                    md_file.write(f"{indent}  {file}\n")

        md_file.write("```\n\n")

        # Write Python files content header
        md_file.write("## Python Files Content\n\n")

        # Process Python files
        for root, dirs, files in os.walk(folder_path):
            # Skip if this directory is in exclude list
            if os.path.abspath(root) in exclude_paths:
                dirs[:] = []
                continue

            # Skip hidden directories and excluded directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and os.path.abspath(os.path.join(root, d)) not in exclude_paths
                and d not in exclude_names
            ]

            for file in files:
                if (
                    file.endswith(".py")
                    or file.endswith(".cs")
                    or file.endswith(".sql")
                ):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)

                    md_file.write(f"### {relative_path}\n\n")
                    md_code_type = (
                        "python"
                        if file.endswith(".py")
                        else "csharp"
                        if file.endswith(".cs")
                        else "sql"
                    )
                    md_file.write(f"```{md_code_type}\n")

                    try:
                        with open(file_path, "r", encoding="utf-8") as py_file:
                            md_file.write(py_file.read())
                    except Exception as e:
                        md_file.write(f"# Error reading file: {str(e)}\n")

                    md_file.write("\n```\n\n")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate a markdown file with project structure and Python code"
    )
    parser.add_argument("folder_path", help="Path to the project folder")
    parser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="Folder to exclude (can be used multiple times)",
    )

    # Parse arguments
    args = parser.parse_args()

    folder_path = args.folder_path
    exclude_folders = args.exclude
    output_file = "project_structure.md"

    generate_folder_structure_md(folder_path, output_file, exclude_folders)
    print(f"Markdown file generated: {output_file}")


if __name__ == "__main__":
    main()
