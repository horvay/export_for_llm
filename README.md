## export_for_llm
Takes a python project folder and exports all the code into an md file, to attach to an llm request

Assuming you have a folder named work with your project, and a folder inside of it called output and input you want to ignore, the syntax is something like:
```sh
uv run ai_export.py work -e output -e input
```
or if you are lame and still using pip/python directly:
```sh
python ai_export.py work -e output -e input
```
This will create a project_structure.md file that can be copy/pasted or attached to your request to your LLM overlords that do all your work for you (at least that's the hope.)
