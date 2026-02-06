import re
import sys

INSERT_RE = re.compile(
    r'<insert\s+src="([^"]+)">\s*</insert>',
    re.IGNORECASE
)

def load_md(path: str, name: str) -> str:
    with open(path + "/" + name, "r", encoding="utf-8") as f:
        content = f.read()

    def replace(match):
        src = match.group(1)
        try:
            with open(src, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    return INSERT_RE.sub(replace, content)


if __name__ == "__main__":
    in_path = sys.argv[1]
    name = sys.argv[2]
    out_path = sys.argv[3]
    prompt = load_md(in_path, name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(prompt)