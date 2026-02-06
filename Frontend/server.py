import os
import sys
import subprocess
import shutil
# REMOVED: import tkinter as tk (We will import it only if needed)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_WORKSPACE = os.getcwd()

# Data Models
class FileRequest(BaseModel):
    path: str
    content: Optional[str] = None

class ProjectRequest(BaseModel):
    parent_path: str
    project_name: str

# --- Routes ---

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/system_pick_folder")
def system_pick_folder():
    """Opens the native OS folder picker (Cross-platform)."""
    try:
        # 1. macOS Method (AppleScript) - No imports needed
        if sys.platform == "darwin":
            script = """
            set theFolder to choose folder with prompt "Select the project folder:"
            POSIX path of theFolder
            """
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            path = result.stdout.strip()
            return {"path": path if path else ""}

        # 2. Windows / Linux Method (Tkinter)
        else:
            # MOVED IMPORTS HERE: Only load if we are NOT on Mac
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            path = filedialog.askdirectory()
            root.destroy()
            return {"path": path}

    except Exception as e:
        return {"path": "", "error": str(e)}

def get_file_tree(path):
    tree = []
    try:
        with os.scandir(path) as entries:
            sorted_entries = sorted(entries, key=lambda e: (not e.is_dir(), e.name.lower()))
            for entry in sorted_entries:
                if entry.name.startswith('.'): continue
                node = {
                    "name": entry.name,
                    "path": entry.path,
                    "type": "folder" if entry.is_dir() else "file",
                    "children": []
                }
                if entry.is_dir():
                    try:
                        node["children"] = get_file_tree(entry.path)
                    except PermissionError:
                        node["children"] = []
                tree.append(node)
    except PermissionError:
        pass
    return tree

@app.get("/files")
def list_files():
    return get_file_tree(CURRENT_WORKSPACE)

@app.post("/open_folder")
def open_folder(req: FileRequest):
    global CURRENT_WORKSPACE
    if os.path.exists(req.path) and os.path.isdir(req.path):
        CURRENT_WORKSPACE = req.path
        return {"status": "success", "new_path": CURRENT_WORKSPACE}
    raise HTTPException(status_code=400, detail="Directory does not exist")

@app.post("/read_file")
def read_file(req: FileRequest):
    try:
        with open(req.path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save_file")
def save_file(req: FileRequest):
    try:
        with open(req.path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_project")
def create_project(req: ProjectRequest):
    base = os.path.join(req.parent_path, req.project_name)
    if os.path.exists(base):
        raise HTTPException(status_code=400, detail="Project folder already exists")

    try:
        os.makedirs(base)
        folders = ["prompt-raw", "prompt-final", "code-raw", "code-final"]

        with open(os.path.join(base, ".api.json"), "w") as f: f.write('{"openai_api_key": ""}')
        with open(os.path.join(base, ".isl.json"), "w") as f: f.write("{}")

        for folder in folders:
            path = os.path.join(base, folder)
            os.makedirs(path)

            with open(os.path.join(path, ".api.json"), "w") as f: f.write("{}")
            with open(os.path.join(path, ".loop.json"), "w") as f: f.write("{}")
            with open(os.path.join(path, ".overwrite.json"), "w") as f: f.write("{}")
            with open(os.path.join(path, ".prompt.md"), "w") as f: f.write("")

            if folder == "prompt-raw":
                with open(os.path.join(path, "raw-prompt.md"), "w") as f: f.write("# Raw Prompt\nDescribe your physics simulation here.")
            elif folder == "prompt-final":
                open(os.path.join(path, "readme.md"), "w").close()

        global CURRENT_WORKSPACE
        CURRENT_WORKSPACE = base
        return {"status": "created", "path": base}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compile")
def compile_project():
    """
    Runs the central 'isl.py' located in the server folder,
    but passes the 'CURRENT_WORKSPACE' as the target argument.
    """
    server_dir = os.path.dirname(os.path.abspath(__file__))
    compiler_script = os.path.join(server_dir, "isl.py")

    if not os.path.exists(compiler_script):
        return {
            "stdout": "",
            "stderr": f"CRITICAL ERROR: 'isl.py' not found!\nExpected location: {compiler_script}\n\nPlease make sure your server.py and isl.py are in the same folder."
        }

    try:
        python_cmd = "python3" if sys.platform != "win32" else "python"
        cmd = [python_cmd, "isl.py", CURRENT_WORKSPACE]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=server_dir
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"stderr": str(e), "stdout": ""}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)