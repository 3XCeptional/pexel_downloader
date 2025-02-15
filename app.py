#!./venv/script/python

import argparse
import multiprocessing
import requests
import os
import sys
import time
from dotenv import load_dotenv
import logging
from fake_useragent import UserAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
REQUEST_DELAY = 18  # 200 requests/hour compliance
DEFAULTS = {
    'media_type': 'videos',
    'orientation': 'landscape',
    'quality': 'hd',
    'number': 2
}

class MediaDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
        
    def _make_request(self, url, params=None):
        headers = {
            "Authorization": self.api_key,
            "User-Agent": UserAgent().random
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None

    def search_media(self, query, media_type, orientation, quality, per_page):
        endpoint = "/videos/search" if media_type == 'videos' else "/search"
        params = {
            "query": query,
            "orientation": orientation,
            "per_page": per_page
        }
        
        data = self._make_request(f"{self.base_url}{endpoint}", params)
        return self._process_results(data, media_type, quality) if data else []

    def _process_results(self, data, media_type, quality):
        if media_type == 'videos':
            return [v['video_files'] for v in data.get('videos', [])]
        return [p['src'].get(quality, p['src']['original']) for p in data.get('photos', [])]

class PexelsDownloader:
    def __init__(self):
        self.api_key = os.getenv('PEXELS_API_KEY')
        self.downloader = MediaDownloader(self.api_key or os.getenv('PEXELS_API_KEY'))
        
    def run(self, args):
        queries = self._get_queries(args.input)
        for query in queries:
            self._process_query(query, args)

    def _get_queries(self, input_source):
        if input_source == '-':
            return [line.strip() for line in sys.stdin if line.strip()]
        return [input_source] if not os.path.exists(input_source) else open(input_source).read().splitlines()

    def _process_query(self, query, args):
        logging.info(f"Searching: {query}")
        results = self.downloader.search_media(
            query, args.media_type, args.orientation,
            args.quality, args.number
        )
        if results:
            self._download_items(results, query, args)

    def _download_items(self, items, query, args):
        os.makedirs(args.output, exist_ok=True)
        for idx, item in enumerate(items[:args.number]):
            try:
                url = self._get_media_url(item, args) if args.media_type == 'videos' else item
                if url: self._download_file(url, args.output, query, idx)
            except Exception as e:
                logging.error(f"Download failed: {e}")

    def _get_media_url(self, video_files, args):
        return next((f['link'] for f in video_files if f['quality'] == args.quality), None)

    def _download_file(self, url, output_dir, query, index):
        ext = 'mp4' if 'video' in url else url.split('.')[-1]
        filename = os.path.join(output_dir, f"{query}_{index+1}.{ext}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logging.info(f"Downloaded: {filename}")
        time.sleep(REQUEST_DELAY)

def main():
    parser = argparse.ArgumentParser(
        description="Pexels Downloader: Simplified with Smart Defaults (Video/Landscape/1080p)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input', help="Search query, text file path, or '-' for stdin")
    parser.add_argument('-t', '--media-type', choices=['images', 'videos'], default=DEFAULTS['media_type'],
                      help="Type of media to download")
    parser.add_argument('-q', '--quality', default=DEFAULTS['quality'],
                      help="Quality (hd/uhd for videos, any valid size for images)")
    parser.add_argument('-o', '--orientation', default=DEFAULTS['orientation'],
                      choices=['landscape', 'portrait', 'square'], help="Media orientation")
    parser.add_argument('-n', '--number', type=int, default=DEFAULTS['number'],
                      help="Number of items to download")
    parser.add_argument('-d', '--output', default='downloads', help="Output directory")

    args = parser.parse_args()
    
    try:
        PexelsDownloader().run(args)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
