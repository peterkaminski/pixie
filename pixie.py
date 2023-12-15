#!/usr/bin/env python3

# Pixie v1.0.0 - https://github.com/peterkaminski/pixie

# Copyright 2023 Peter Kaminski. Licensed under MIT license, see accompanying LICENSE file.

import argparse
import base64
import json
import logging
import os

import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_gpt4(image_path, prompt):
    # Retrieving the API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Please set the 'OPENAI_API_KEY' environment variable")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Set up the prompt
    if prompt is None:
        prompt = "Describe this image."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    response_json = response.json()
    return response_json['choices'][0]['message']['content']


def main():
    parser = argparse.ArgumentParser(description="Analyze an image file with GPT-4 with Vision API.")
    parser.add_argument('-i', '--input', required=True, help="Image file name")
    parser.add_argument('-p', '--prompt', help="Prompt to give to GPT-4")
    args = parser.parse_args()

    response = analyze_image_with_gpt4(args.input, args.prompt)
    print(response)

if __name__ == "__main__":
    main()
