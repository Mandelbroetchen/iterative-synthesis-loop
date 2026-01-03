import os
from openai import OpenAI

def get_api_key():
    with open("API_KEY.txt") as f: return f.read()

class API:
    def __init__(self):
        self.api_key = get_api_key()
        self.client = OpenAI(api_key = self.api_key,
      base_url = "https://litellm.s.studiumdigitale.uni-frankfurt.de/v1"
    )


    def get_response(self, text):
        response = self.client.chat.completions.create(
          model = "qwen2.5-coder-32b-instruct",
          messages = [
            {"role": "user", "content": text}
          ]
        )
        return response


if __name__ == "__main__":
    api = API()

    print(api.get_response("How do i use the OpenAI python library to simulate a conversation?").choices[0].message.content)
