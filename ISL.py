from md import *
from api import *
import sys
import logging


if __name__ == "__main__":
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    config = load_config(f"{in_path}/.api.json")
    api = MistralAPI(config)
    prompt = load_md(f"{in_path}/.prompt.md")
    
    logging.info(prompt)
    
    response = api.test(prompt)
    
    logging.info(response)
