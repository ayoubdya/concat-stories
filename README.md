# Concat Stories

Concat Stories is a Python package that allows you to download Snapchat stories and merge them into a single video file.

## Features

- Download Snapchat stories
- Merge multiple stories into one video
- Easy to use

## Installation

You can install Concat Stories using pip:

```bash
pip install concat-stories
```

## Usage

Here is an example of how to use Concat Stories:

```bash
usage: concat-stories [-h] -u USERNAME [-o OUTPUT_NAME] [-d] [--sleep-interval INTERVAL] [-l LIMIT] [-v] [--image-duration DURATION]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Snapchat username ex. djkhaled305
  -o OUTPUT_NAME, --output OUTPUT_NAME
                        Output video name ex. dj_khaled_stories
  -d, --delete          Delete stories after download.
  --sleep-interval INTERVAL
                        Sleep between downloads in seconds. (Default: 1s)
  -l LIMIT, --limit-story LIMIT
                        Set maximum number of stories to download.
  -v, --verbose         FFmpeg output verbosity.
  --image-duration DURATION
                        Set duration for image in seconds. (Default: 1s)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
