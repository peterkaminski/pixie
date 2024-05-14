#!/usr/bin/env python3

# Pixie v1.0.0 - https://github.com/peterkaminski/pixie

# Copyright 2023 Peter Kaminski. Licensed under MIT license, see accompanying LICENSE file.

import argparse
import base64
from fractions import Fraction
import io
import logging
import math
import os

import requests
from PIL import Image

# Set up vision model to request. Also check `pricing_model` in compute_cost().
VISION_MODEL = 'gpt-4-vision-preview'

# Set up logging
logging.basicConfig(level=logging.INFO)

# Resize and encode the image
def encode_image(image_path):
    # Read the image
    with Image.open(image_path) as img:
        # Original dimensions
        original_width, original_height = img.size

        # Calculate and reduce the aspect ratio
        aspect_ratio = Fraction(original_width, original_height).limit_denominator()

        # Calculate new dimensions preserving aspect ratio
        max_size = 512
        if original_width > original_height:
            new_width = min(original_width, max_size)
            new_height = round(new_width / aspect_ratio)
        else:
            new_height = min(original_height, max_size)
            new_width = round(new_height * aspect_ratio)

        # Resize image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to PNG
        with io.BytesIO() as buffer:
            img.save(buffer, format="PNG")
            buffer.seek(0)
            image_png = buffer.read()

    # Encode to base64
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Return base64 string, original dimensions, and aspect ratio
    return image_base64, (original_width, original_height), (aspect_ratio.numerator, aspect_ratio.denominator)


def analyze_image_with_gpt4(image_path, prompt, max_tokens):
    # Retrieving the API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Please set the 'OPENAI_API_KEY' environment variable")

    # Getting the base64 string
    base64_image, original_dimensions, aspect_ratio = encode_image(image_path)

    # Set up the prompt
    if prompt is None:
        prompt = "Describe this image."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": VISION_MODEL,
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
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    response_json = response.json()
    return \
        response_json['model'], \
        original_dimensions, \
        aspect_ratio, \
        (response_json['usage']['prompt_tokens'], response_json['usage']['completion_tokens']), \
        response_json['choices'][0]['message']['content']

def compute_cost(tokens, actual_model):
    """
    Compute the cost of using input and output tokens.

    Args:
    tokens (tuple): A tuple containing two integers, the first for input tokens and the second for output tokens.

    Returns:
    float: The total cost calculated based on the given rates, rounded to four decimal places.
    """
    # Unpacking the tuple
    input_tokens, output_tokens = tokens

    # Cost calculation
    # https://openai.com/pricing - change all of pricing_model, input_cost, output_cost at the same time
    pricing_model = 'gpt-4-1106-vision-preview'
    input_cost = input_tokens / 1000 * 0.01
    output_cost = output_tokens / 1000 * 0.03
    if actual_model != pricing_model:
        logging.info(f'Note: using pricing for "{pricing_model}", but actual model is "{actual_model}".')

    # Total cost
    total_cost = input_cost + output_cost

    # Rounding up to four decimal places
    rounded_cost = math.ceil(total_cost * 10000) / 10000

    return total_cost

def main():
    parser = argparse.ArgumentParser(description="Analyze an image file with GPT-4 with Vision API.")
    parser.add_argument('-i', '--input', required=True, help="Image file name")
    parser.add_argument('-p', '--prompt', help="Prompt to give to GPT-4")
    parser.add_argument('-t', '--tokens', default=300, help="Maximum output tokens")
    parser.add_argument('-c', '--cost', action="store_true", help="Include tokens used and estimated cost in output")
    args = parser.parse_args()

    model, original_dimensions, aspect_ratio, tokens, response = analyze_image_with_gpt4(args.input, args.prompt, args.tokens)
    print(f"Original dimensions: {original_dimensions[0]} x {original_dimensions[1]}")
    print(f"Aspect ratio: {aspect_ratio[0]}:{aspect_ratio[1]}")
    if (args.cost):
        cost = compute_cost(tokens, model)
        print(f"Tokens: {tokens[0]}+{tokens[1]} (${cost:.4f})")
    if tokens[1] >= int(args.tokens):
        print(f"Note: Maximum output tokens ({args.tokens}) reached - output may be truncated. Consider increasing --tokens.")
    print(f"\n{response}")

if __name__ == "__main__":
    main()
