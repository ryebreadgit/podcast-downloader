# Podcast Downloader

This Python program is designed to download podcasts from RSS feeds. It reads the RSS feed URLs from the "rss.txt" file, retrieves the podcast episodes' information, and downloads the new episodes to a specified directory. The program utilizes the `requests` library for making HTTP requests and the `xml.etree.ElementTree` module for parsing XML.

## Prerequisites

- Python 3.x
- `requests` library
- `sanitize_filename` library (install via `pip install sanitize-filename`)

## Usage

1. Place the RSS feed URLs in the "rss.txt" file, with each URL on a new line.
2. Make sure the target download directory is correctly set in the `dl_path` variable.
3. Run the program by executing the Python script.
4. The program will check for updates in each RSS feed and download any new podcast episodes to the specified directory.
5. The program creates a log file named after the script with the extension ".log" to log its progress and any errors encountered.

## Configuration

- `dl_path`: Set the target download directory for the podcast episodes.
- `rss.txt`: Add the RSS feed URLs, with each URL on a new line.

## Dependencies

This program relies on the following Python libraries:

- `requests`: A library for making HTTP requests.
- `xml.etree.ElementTree`: A module for parsing XML data.
- `sanitize_filename`: A library for sanitizing filenames to ensure compatibility.

## Contributing

Contributions to this program are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This program is licensed under the MIT License. Feel free to modify and distribute it as needed.

## Acknowledgments

This program was created to simplify the process of downloading podcasts from RSS feeds. Thanks to the developers of the `requests` library and the `sanitize_filename` library for providing the necessary functionality.
