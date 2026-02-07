import subprocess
from md import *
from api import *
import sys
import logging
import json
from pathlib import Path
import argparse
import re


def load_config(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run LLM prompt with config")
    parser.add_argument("in_path", type=str, help="Input folder path")
    parser.add_argument("-a", "--api_config", type=str, help="Override API config path")
    parser.add_argument("-l", "--loop_config", type=str, help="Override loop config path")
    args = parser.parse_args()

    in_path = Path(args.in_path)

    api_config_path = Path(args.api_config) if args.api_config else in_path / ".api.json"


    api_config = load_config(api_config_path)
    #oop_config = load_config(loop_config_path)

    #out_path = Path(loop_config.get("out_path", "."))  # fallback to current dir

    # Setup logging
    logging.basicConfig(
        filename='.log.md',
        filemode='w',
        format='---\n ```%(asctime)s``` \n %(message)s \n',
        level=logging.INFO
    )

    api = API(api_config)

    prompt = load_md(in_path, ".template-prompt.md")
    prompt_file = in_path / ".embeded-prompt.md"
    with prompt_file.open("w", encoding="utf-8") as f:
        f.write(prompt)

    response = api.get_response(prompt)

    logging.info(response)

    # Write output to file
    out_file = in_path / ".overwrite.py"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        response = re.sub(r'^```.*?\n|\n```$', '', response, flags=re.S)
        f.write(response)

    subprocess.run(["python", in_path / ".overwrite.py"])


if __name__ == "__main__":
    main()
