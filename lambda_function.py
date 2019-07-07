import boto3
import json
import os
import shlex
import subprocess

s3 = boto3.client('s3')
bucket = os.environ['MEGALE_S3_BUCKET']

def lambda_handler(event, context):
    url = event['url']

    filename = youtube_video_filename(url)
    stream = youtube_video_stream(url)
    s3.upload_fileobj(stream, bucket, f"files/{filename}")

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

    return f"{uploader}/{upload_date}-{id} - {title}.{ext}"

def youtube_video_info(url):
    command = f"./youtube-dl --dump-json '{url}'"
    result = subprocess.check_output(shlex.split(command), universal_newlines=True)
    return json.loads(result)
