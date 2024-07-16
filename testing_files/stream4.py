# # main.py

# import time
# from datetime import datetime
# import os

# import subprocess
# import shutil

# LIVE_STREAM_URL = 'https://www.youtube.com/ArynewsTvofficial/live'

# OUTPUT_DIRECTORY = r"D:\mca\static"
# TS_OUTPUT_DIRECTORY = r"D:\mca\ts_files"  # new folder for .ts files
# COPY_DESTINATION = r"D:\mca\ts_copied"  # Destination folder for copied .ts files

# os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
# os.makedirs(TS_OUTPUT_DIRECTORY, exist_ok=True)
# os.makedirs(COPY_DESTINATION, exist_ok=True)

# def fetch_stream_url():
#     try:
#         streamlink_cmd = [
#             'streamlink',
#             LIVE_STREAM_URL,
#             'best',
#             '-f',
#             '--stream-url',
#         ]
#         result = subprocess.run(streamlink_cmd, capture_output=True, text=True, check=True)
#         stream_url = result.stdout.strip()
#         return stream_url
#     except subprocess.CalledProcessError as e:
#         print(f"Error fetching stream URL: {e}")
#         return None

# def copy_ts_files():
#     try:
#         ts_files = [f for f in os.listdir(OUTPUT_DIRECTORY) if f.endswith('.ts')]
#         if ts_files:
#             for ts_file in ts_files:
#                 shutil.copy(os.path.join(OUTPUT_DIRECTORY, ts_file), COPY_DESTINATION)
#                 print(f'Copied .ts file: {ts_file}')
#         else:
#             print("No .ts files found in OUTPUT_DIRECTORY.")
#     except Exception as e:
#         print(f'Error copying .ts files: {str(e)}')





# def save_live_stream_hls():
#     try:
#         stream_url = fetch_stream_url()
#         if not stream_url:
#             print("Error: Unable to fetch stream URL.")
#             return

#         timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#         playlist_filename = f'output_{timestamp}.m3u8'
#         playlist_path = os.path.join(OUTPUT_DIRECTORY, playlist_filename)

#         # Enqueue the task to process the stream in the background
#         process_stream(stream_url, playlist_path)

#         print(f'Started saving live stream as HLS playlist: {playlist_filename}')
#         return playlist_path
#     except Exception as e:
#         print(f'Error saving live stream as HLS playlist: {str(e)}')

# while True:
#     playlist_path = save_live_stream_hls()
#     if playlist_path:
#         copy_ts_files()
#     # Sleep for some time before saving the next chunk
#     time.sleep(10)  # Adjust the sleep time as needed
