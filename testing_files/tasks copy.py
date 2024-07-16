# celery_basic_app/tasks.py
from celery import shared_task
import time
import requests
from django.conf import settings
import os
import subprocess
import shutil
import time
from datetime import datetime


LIVE_STREAM_URL = 'https://www.youtube.com/@geonews/live'

base_path = settings.BASE_DIR

OUTPUT_DIRECTORY = os.path.join(base_path, 'static','stream')

print(OUTPUT_DIRECTORY)

TS_OUTPUT_DIRECTORY = os.path.join(base_path, 'static','Ts_output')
COPY_DESTINATION = os.path.join(base_path, 'static','ts_copied')

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

if not os.path.exists(TS_OUTPUT_DIRECTORY):
    os.makedirs(TS_OUTPUT_DIRECTORY)

if not os.path.exists(COPY_DESTINATION):
    os.makedirs(COPY_DESTINATION)


# @shared_task
def fetch_stream_url():
    try:
        streamlink_cmd = [
            'streamlink',
            LIVE_STREAM_URL,
            'best',
            '-f',
            '--stream-url',
        ]
        result = subprocess.run(streamlink_cmd, capture_output=True, text=True, check=True)
        stream_url = result.stdout.strip()
        return stream_url
    except subprocess.CalledProcessError as e:
        print(f"Error fetching stream URL: {e}")
        return None


# @shared_task
# def copy_ts_files():
#     try:
#         while True:
#             ts_files = [f for f in os.listdir(OUTPUT_DIRECTORY) if f.endswith('.ts')]
#             if ts_files:
#                 for ts_file in ts_files:
#                     source_path = os.path.join(OUTPUT_DIRECTORY, ts_file)
#                     destination_path = os.path.join(COPY_DESTINATION, ts_file)
#                     if not os.path.exists(destination_path):  # Copy only if not already copied
#                         shutil.copy(source_path, COPY_DESTINATION)
#                         print(f'Copied .ts file: {ts_file}')
#             else:
#                 print("No .ts files found in OUTPUT_DIRECTORY.")
#             time.sleep(2)
#     except Exception as e:
#         print(f'Error copying .ts files: {str(e)}')




@shared_task
def process_stream(stream_url, playlist_path):
    try:
        ffmpeg_cmd = [
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            '-i', stream_url,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-tune', 'zerolatency',
            '-g', '48',
            '-preset', 'veryfast',
            '-max_muxing_queue_size', '1024',
            '-hls_time', '10',
            '-hls_list_size', '0',
            '-f', 'hls',
            playlist_path,
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'Saved live stream as HLS playlist: {playlist_path}')
    except Exception as e:
        print(f'Error saving live stream as HLS playlist: {str(e)}')


@shared_task
def save_live_stream_hls():
    try:
        stream_url = fetch_stream_url()
        if not stream_url:
            print("Error: Unable to fetch stream URL.")
            return

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        playlist_filename = f'output_{timestamp}.m3u8'
        playlist_path = os.path.join(OUTPUT_DIRECTORY, playlist_filename)

        # Enqueue the task to process the stream in the background
        process_stream.delay(stream_url, playlist_path)

        print(f'Started saving live stream as HLS playlist: {playlist_filename}')
        return playlist_path
    except Exception as e:
        print(f'Error saving live stream as HLS playlist: {str(e)}')




@shared_task
def add(x, y):
    try:
        time.sleep(10)  
        result = x + y
        print(f'Task completed with result: {result}')
        return result
    except Exception as e:
        print(f'Task failed with error: {e}')
        raise


@shared_task
def fetch_quote():
    time.sleep(5)
    category = 'happiness'
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    response = requests.get(api_url, headers={'X-Api-Key': 'tNb1k+cFV07v7yrmxXnehg==2d2Sg0N09WRlY7hI'})

    if response.status_code == requests.codes.ok:
        quotes = response.json()
        return quotes[0]['quote'] if quotes else 'No quotes found'
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")




@shared_task
def Gold_Price():
    try:
        time.sleep(5)  # Simulating a delay or processing time
        api_url = 'https://api.api-ninjas.com/v1/goldprice'
        response = requests.get(api_url, headers={'X-Api-Key': 'tNb1k+cFV07v7yrmxXnehg==2d2Sg0N09WRlY7hI'})

        if response.status_code == requests.codes.ok:
            goldprice = response.json()
            if 'price' in goldprice and 'updated' in goldprice:
                return {
                    'price': goldprice['price'],
                    'updated': goldprice['updated']
                }
            else:
                return 'Incomplete data received'  # Handle case where expected keys are missing
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return 'Failed to fetch data'  # Handle HTTP error
    except Exception as e:
        print(f"Error in Gold_Price task: {e}")
        raise  # Re-raise the exception for visibility and debugging




@shared_task
def Crypto_Price():
    try:
        time.sleep(5)  # Simulating a delay or processing time
        symbol = 'LTCBTC'
        api_url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
        
        response = requests.get(api_url, headers={'X-Api-Key': 'tNb1k+cFV07v7yrmxXnehg==2d2Sg0N09WRlY7hI'})
        if response.status_code == requests.codes.ok:
            crypt = response.json()
            if 'symbol' in crypt and 'price' in crypt:
                return {
                    'symbol': crypt['symbol'],
                    'price': crypt['price']
                }
            else:
                return 'Incomplete data received'  # Handle case where expected keys are missing
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return 'Failed to fetch data'  # Handle HTTP error
    except Exception as e:
        print(f"Error in Gold_Price task: {e}")
        raise  # Re-raise the exception for visibility and debugging

