# Pexels Downloader
by 3XCeptional

## Description

Pexels Downloader is a Python script that allows you to download images and videos from Pexels using the Pexels API. It provides a simple command-line interface to search and download media based on various criteria such as search queries, media type, quality, and orientation.
<!-- This is a test comment -->

## Features

- Downloads images and videos from Pexels.
- Supports specifying media type (images or videos).
- Allows setting quality and orientation for media.
- Downloads multiple media items based on a search query.
- Reads search queries from command line, input file, or stdin.
- Dockerfile for easy containerization.

## Dependencies

- certifi==2024.12.14
- charset-normalizer==3.4.1
- fake-useragent==2.0.3
- idna==3.10
- python-dotenv==1.0.1
- requests==2.32.3
- urllib3==2.3.0

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/3XCeptional/pexel_downloader
   cd pexel_downloader
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Pexels API key:
   - You need to obtain an API key from the [Pexels website](https://www.pexels.com/api/).
   - Set the API key as an environment variable named `PEXELS_API_KEY`. You can do this by:
     - Exporting it in your terminal:
       ```bash
       export PEXELS_API_KEY=YOUR_API_KEY
       ```
     - Or by creating a `.env` file in the project root with the following content:
       ```
       PEXELS_API_KEY=YOUR_API_KEY
       ```

## Usage

Run the `app.py` script with a search query as the input. You can provide the query directly in the command line, from a text file, or via stdin.

**Command Line:**

```bash
python app.py <search_query> [options]
```

**Example:** Download 3 HD landscape videos of "Augmented Reality" to the `downloads` directory:

```bash
python app.py "Augmented Reality" -t videos -n 3 -q hd -o landscape -d downloads
```

**Options:**

- `-t`, `--media-type` {images, videos}: Type of media to download (default: videos).
- `-q`, `--quality` TEXT: Quality (hd/uhd for videos, any valid size for images) (default: hd).
- `-o`, `--orientation` {landscape, portrait, square}: Media orientation (default: landscape).
- `-n`, `--number` INTEGER: Number of items to download (default: 2).
- `-d`, `--output` TEXT: Output directory (default: downloads).

**Input from File:**

Create a text file (e.g., `queries.txt`) with search queries, one per line:

```
Augemented Reality
Artifical Intelligence
AR VR
Virtual reality
```

Then run the script with the input file:

```bash
python app.py queries.txt -n 2
```

**Input from Stdin:**

```bash
echo "Artificial Intelligence" | python app.py - -n 1
```

## Docker

1. **Build the Docker image:**

   ```bash
   docker build -t pexels-downloader .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -it --rm -e PEXELS_API_KEY=YOUR_API_KEY -v $(pwd)/downloads:/app/downloads pexels-downloader "Virtual Reality"
   ```

   - `-e PEXELS_API_KEY=YOUR_API_KEY`:  Passes your Pexels API key as an environment variable to the container.
   - `-v $(pwd)/downloads:/app/downloads`: Mounts the local `downloads` directory to the `/app/downloads` directory in the container, so downloaded files are accessible on your host machine.

## Notes

- **Rate Limiting:** The script includes a delay between requests to comply with the Pexels API rate limit of 200 requests per hour.
- **Output Directory:** Downloaded media files are saved in the `downloads` directory by default. You can change this using the `-d` or `--output` option.
This is a test commit by 3XCeptional