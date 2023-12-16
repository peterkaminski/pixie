# Pixie - Command-line Image Analysis Using GPT-4 with Vision API

## Overview

Pixie analyzes an image using OpenAI's [GPT-4 with Vision API](https://platform.openai.com/docs/guides/vision). The script allows users to provide an image file, optionally provide a prompt to guide the analysis, and specify the maximum number of output tokens. The script then scales the image so its largest dimension is 512 pixels or less, sends the image to GPT-4 for analysis, and outputs the GPT-4 analysis along with some basic information about the image and the approximate computational cost incurred.

## Features

- Image analysis using GPT-4 with Vision API.
- Customizable prompts for tailored image analysis.
- Control over the maximum number of output tokens.

## Prerequisites

- Python 3.x
- A virtual environment (recommended for Python package management)

## Setup

### Step 1: Clone the Repository

Clone the repository to your local machine using:

```shell
git clone https://github.com/peterkaminski/pixie
```

### Step 2: Create a Virtual Environment

Navigate to the cloned directory and create a virtual environment:

```shell
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment.

On Windows:

```powershell
.\venv\Scripts\activate
```

On Unix or MacOS:

```shell
source venv/bin/activate
```

### Step 4: Install Required Packages

Install the necessary Python packages:

```shell
pip install -r requirements.txt
```

### Step 5: Set up OpenAI API key

Sign up for an OpenAI developer account, and generate an API key in settings. See [Where do I find my API Key?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) in the OpenAI Help Center. OpenAI provides a document about [Best Practices for API Key Safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety), which you should review.

Then on Unix or MacOS, copy the `env.sh-template` file to `env.sh`, then edit `env.sh` to insert your OpenAI API key. Add your API key to the shell environment:

```shell
source env.sh
```

On Windows, the process will be similar, but we do not have documentation for the process yet.

In any case, make sure you do not push any file with your API key back to your upstream Git host, such as GitHub.

## Usage

### Running the Script

Run the script like this:

```shell
./pixie.py [-p <optional-prompt>] [-t <max-tokens>] -i <image-file-name> 
```

### Arguments

- `-i`, `--input`: (Required) The path and name of the image file to analyze.
- `-p`, `--prompt`: (Optional) A prompt to guide the GPT-4 analysis. Default is "Describe this image."
- `-t`, `--tokens`: (Optional) The maximum number of output tokens. Default is 300.

### Example

```shell
./pixie.py -i example.jpg -p "Consider this image. Print applicable keywords and a short description." -t 500
```

This command analyzes the image `example.jpg` with the prompt "Consider this image. Print applicable keywords and a short description." and a maximum of 500 tokens for the output.

## Output

The script will output:

- The original dimensions of the image.
- The aspect ratio of the image.
- The number of tokens used in the analysis and the approximate cost.
- A warning note if the maximum output tokens limit was met.
- The analysis response from GPT-4.

## Processing Multiple Files

Pixie can be used to process multiple files using standard shell techniques. Here are two examples for Unix or MacOS.

```shell
for i in *.png ; do /path/to/pixie.py -i "$i" > "$i.txt"; done
```

```shell
find /path/to/images -iname '*.png' \
-exec sh -c '/path/to/pixie.py -i "$1" > "$1.txt"' _ {} \;
```

Pixie currently outputs to STDOUT, but in the future, there will be a `--output` / `-o` flag to specify output destination, which will be preferred over the output redirection techniques above.

## Notes

- The software is provided "as is", without warranty of any kind. See the LICENSE file for more details.
- This is a "1.0" version of the script, so some features may be missing, more error checking may be needed, etc. Please provide feedback!
- You are responsible for providing your OpenAI API key to operate the software. Your API key is not part of this software. You are responsible for keeping your API key secure.
- The image analysis is generated by GPT-4; if you get a surprising written response, or a refusal to analyze a script, it's due to OpenAI and GPT-4. Try providing a different prompt with `--prompt`.
- The approximate cost is calculated using hardcoded prices retrieved on 2023-12-15 from [OpenAI Pricing](https://openai.com/pricing). Before you can rely on the approximate price calcuation, you must confirm the prices are up-to-date and the same as given on the OpenAI website.
- This version is hard-coded to use the `low` detail setting, to maintain lower API costs for the user. A future version may enable the use of `high` detail as well. The `low` detail setting requires 
- If the GPT-4 output is truncated due to reaching the maximum token limit, consider increasing the `--tokens` value.
- see the [[Roadmap.md]] file for plans and ideas for future development.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions to this script are welcome. Feel free to fork, modify, and send a pull request.

## Support

For any issues or questions, please open an issue in the repository or contact [Peter Kaminski](mailto:kaminski@istori.com).

