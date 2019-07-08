import boto3
import json
import os
import shlex
import subprocess

S3_BUCKET = os.environ['S3_BUCKET']
FILENAME_TEMPLATE = os.environ['FILENAME_TEMPLATE']

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        url = record['body']
        download_youtube_video_to_s3(url)

def download_youtube_video_to_s3(url):
    filename = youtube_video_filename(url)
    stream = youtube_video_stream(url)
    s3.upload_fileobj(stream, S3_BUCKET, filename)

    return {
        'statusCode': 200,
        'filename': filename
    }

def youtube_video_stream(url):
    command = f"./youtube-dl --cache-dir '/tmp' '{url}' -o -"
    ytdl_process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    return ytdl_process.stdout

def youtube_video_filename(url):
    info = youtube_video_info(url)

    id = info['id']
    uploader = info['uploader']
    title = info['title']
    upload_date = info['upload_date']
    ext = info['ext']

    return FILENAME_TEMPLATE.format(id=id, uploader=uploader, title=title, upload_date=upload_date, ext=ext)

def youtube_video_info(url):
    command = f"./youtube-dl --dump-json '{url}'"
    result = subprocess.check_output(shlex.split(command), universal_newlines=True)
    return json.loads(result)
