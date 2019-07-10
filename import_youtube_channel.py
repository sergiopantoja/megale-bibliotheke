import boto3
import json
import os
import googleapiclient.discovery
from urllib.parse import urlparse

SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    channel_id = channel_id_from_url(event['channel_url'])
    channel_content = channel_content_details(YOUTUBE_API_KEY, channel_id)
    playlist_id = playlist_id_from_channel_content(channel_content)
    video_ids = videos_for_playlist(YOUTUBE_API_KEY, playlist_id)

    sqs_message_ids = []
    for id in video_ids:
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=f"https://www.youtube.com/watch?v={id}"
        )
        sqs_message_ids.append(response.get('MessageId'))

    return {
        'statusCode': 200,
        'video_count': len(sqs_message_ids),
        'sqs_message_ids': sqs_message_ids
    }

def youtube(api_key):
    return googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def channel_id_from_url(url):
    return urlparse(url).path.split('/')[-1]

def channel_content_details(api_key, channel_id):
    return youtube(api_key).channels().list(part='contentDetails', id=channel_id).execute()

def playlist_id_from_channel_content(channel_content):
    return channel_content['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def videos_for_playlist(api_key, playlist_id):
    videos, response = videos_for_playlist_subfunction(api_key, playlist_id)

    while 'nextPageToken' in response:
        additional_videos, response = videos_for_playlist_subfunction(api_key, playlist_id, response['nextPageToken'])
        videos += additional_videos

    return videos

def videos_for_playlist_subfunction(api_key, playlist_id, page_token=None):
    response = youtube(api_key).playlistItems().list(
        part='contentDetails',
        maxResults=50,
        playlistId=playlist_id,
        pageToken=page_token
    ).execute()

    videos = list(map(extract_video_id, response['items']))

    return (videos, response)

def extract_video_id(response_item):
    return response_item['contentDetails']['videoId']
