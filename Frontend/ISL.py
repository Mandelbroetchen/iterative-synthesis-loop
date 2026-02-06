from md import *
from api import *
import sys
import logging
import json
from pathlib import Path
import argparse


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

    # Config paths: override with CLI if given, else default
    api_config_path = Path(args.api_config) if args.api_config else in_path / ".api.json"
    loop_config_path = Path(args.loop_config) if args.loop_config else in_path / ".loop.json"
    prompt_md_path = in_path / ".prompt.md"

    api_config = load_config(api_config_path)
    loop_config = load_config(loop_config_path)

    out_path = Path(loop_config.get("out_path", "."))  # fallback to current dir

    # Setup logging
    logging.basicConfig(
        filename='.log.md',
        filemode='w',
        format='---\n ```%(asctime)s``` \n %(message)s \n',
        level=logging.INFO
    )
    print(api_config)
    api = API(api_config)

    prompt = load_md(prompt_md_path)

    response = api.get_response(prompt)

    logging.info(response)

    # Write output to file
    out_file = out_path / "response.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        f.write(response)

    print(f"Response saved to: {out_file}")


if __name__ == "__main__":
    main()
