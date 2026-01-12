# api.py

import os
import json
import time
from openai import OpenAI
import requests
from dotenv import load_dotenv

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class MistralAPI:
    def __init__(self, config):
        load_dotenv()

        self.api_key = os.getenv("API_KEY_MISTRAL")
        if not self.api_key:
            raise RuntimeError("API_KEY missing in .env")

        self.url = config["request"]["url"]
        self.timeout = config["request"]["timeout_ms"] / 1000
        self.retries = config["metadata"]["retry"]["max_attempts"]

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self.model = config["model"]["model"]

    def send_request(self, text: str):
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        for attempt in range(1, self.retries + 1):
            try:
                r = requests.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                r.raise_for_status()
                return r.json()

            except requests.RequestException as e:
                if r is not None:
                    print("Status:", r.status_code)
                    print("Body:", r.text)

                if attempt == self.retries:
                    raise RuntimeError("Request failed after retries") from e

                time.sleep(2 ** attempt)
    def test(self, prompt):
        result = self.send_request(prompt)
        return result["choices"][0]["message"]["content"]

class OpenAIAPI:
    def __init__(self):
        self.api_key = os.getenv("API_KEY_OPENAI")
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
    config = load_config("idea/.api.json")
    api = MistralAPI(config)
    response = api.test("Hello, world!")
    print("Response:", response)
