import re
import sys,os
from pathlib import Path

INSERT_RE = re.compile(
    r'<insert\s+src="([^"]+)">\s*</insert>',
    re.IGNORECASE
)

def load_md(path, name):
    with open(path / name, "r", encoding="utf-8") as f:
        content = f.read()

    def replace(match):
        src = match.group(1)

        def wrap_file(filepath, base_path=None):
            """Wrap a single file in the Markdown-style block."""
            if base_path is None:
                base_path = os.path.dirname(filepath)
            rel_path = os.path.relpath(filepath, base_path)
            extension = os.path.splitext(filepath)[1][1:]  # extension without dot
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"<file src = \"{rel_path}\">\n\n{content}\n</file>"
            except Exception:
                return ""

        def read_files_recursively(base_path):
            combined_content = []
            for root, dirs, files in os.walk(base_path):
                # Skip hidden folders
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.startswith('.'):
                        continue
                    filepath = os.path.join(root, file)
                    combined_content.append(wrap_file(filepath, base_path))
            return "\n\n".join(combined_content)

        if os.path.isdir(src):
            return read_files_recursively(src)
        elif os.path.isfile(src):
            return wrap_file(src)
        else:
            return ""

    return INSERT_RE.sub(replace, content)


if __name__ == "__main__":
    in_path = sys.argv[1]
    name = sys.argv[2]
    out_path = sys.argv[3]
    prompt = load_md(Path(in_path), name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(prompt)