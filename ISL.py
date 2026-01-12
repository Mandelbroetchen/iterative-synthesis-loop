from md import *
from api import *
import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(
        filename='.log.md',
        filemode='w',
        format='---\n ```%(asctime)s``` \n %(message)s \n',
        level=logging.INFO
    )

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    config = load_config(f"{in_path}/.api.json")
    api = MistralAPI(config)
    prompt = load_md(f"{in_path}", ".prompt.md")
    
    logging.info("\n" + prompt)
    
    response = api.test(prompt)
    
    logging.info("\n" + response)
