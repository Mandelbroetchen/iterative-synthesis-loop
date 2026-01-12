import re

INSERT_RE = re.compile(
    r'<insert\s+src="([^"]+)">\s*</insert>',
    re.IGNORECASE
)

def load_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
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
    prompt = load_md("idea/.prompt.md")
    print(prompt)