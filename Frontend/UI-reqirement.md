
## Essentials
- Menu - File - Open Project
Select a folder and open it in the file explorer
- Menu - File - New Project
Create a folder, select and load a template. 
```
https://github.com/Mandelbroetchen/iterative-synthesis-loop/tree/master/example
project-root-folder/
    .api.json
    .isl.ison
    prompt-raw/
        .api.json
        .loop.ison
        .overwrite.json
        .prompt.md
        raw-prompt.md
    prompt-final/
        .api.json
        .loop.ison
        .overwrite.json
        .prompt.md
        class-diagram.uml
        package-diagram.uml
        usecase-diagram.uml
        readme.md
    code-raw/
        .api.json
        .loop.ison
        .overwrite.json
        .prompt.md
    code-final/
```
- Menu - File - Save File
- Menu - Compile - Compile
Run the background program `isl.py`
- Menu - Windows - Terminal
Opens / Closes the terminal window

## Version Control 
- Menu - Windows - Git
Open a panel to view all versions for all folders
- Menu - File - New Project
Also initialize git version control in all folders 
```
prompt-raw/
prompt-final/
code-raw/
code-final/
```
- Menu - Git - Versions
List all versions of all repos, select a version to checkout
- Menu - Git - Commit
Select a repo to commit
