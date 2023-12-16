# Pixie Roadmap

Plans and ideas for future development.

See [[Readme.md]] for general information about Pixie.

## --output, -o

Specify output format and destination. If this flag is present with no argument, or just the file extension, the path and filename (with original extension removed) of the image file is used, with the file extension provided appended. Or, specify the whole filename, and optionally path, to save to a different filename.

- txt (default)
- md or markdown
- html - creates a simple HTML page with embedded scaled-down image and returned text
- json

If --output is not given, output goes to STDOUT.

With "txt" and "md", a first run will create the output text file; subsequent runs will append a separator ("\n---\n") and the new output to the existing file.

## --aspect, -a

OpenAI's documentation notes the need to scale the longest dimension down to the appropriate size for the detail setting, but it does not specify whether it's best to preserve the original image's aspect ratio, or to scale to square to maximize the number of pixels sent, at the cost of changing the visiospatial relationships in the image. Initial tests were inconclusive as to which was better, and the current code without this flag uses "preserve". The planned default for this flag is "preserve", but may be changed upon further testing.

- preserve (default)
- square

## --detail, -d

Passed to OpenAI. Input image is scaled to the size appropriate for the detail setting.

- low (default)
- high

## More error checking, better error handling

Things like detecting a file that's not an image, catching known exceptions in `main()`, etc.