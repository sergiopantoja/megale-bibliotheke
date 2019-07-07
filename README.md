# Megale Bibliotheke
Your personal internet archive.

## Installation
1. In AWS, create Lambda function with the latest Python runtime and the following settings:
   - Execution role: any role that allows it to `PutObject` on your S3 bucket
   - Max timeout: 15 minutes, 0 seconds
   - Memory: 1024 MB (probably more than needed, feel free to tune it)
   - Handler: `lambda_function.lambda_handler`

2. Set the environment variables for your Lambda function:
   - `MEGALE_S3_BUCKET`: where you want the YouTube videos to be saved
   - `MEGALE_FILENAME_TEMPLATE`: this formats the S3 key that will be saved for each video, for example: `files/{uploader}/{upload_date}-{id} - {title}.{ext}` These variables are currently supported:
      - `uploader`
      - `upload_date`
      - `id`
      - `title`
      - `ext`

3. Clone this repo:
```bash
git clone https://github.com/sergiopantoja/megale-bibliotheke
cd megale-bibliotheke
```

4. Download the latest `youtube-dl` and place it in the same folder as this repo:
```bash
curl -L https://yt-dl.org/downloads/latest/youtube-dl -o ./youtube-dl
chmod a+rx ./youtube-dl
```

5. Zip the files up:
```bash
zip function.zip lambda_function.py youtube-dl
```

6. Upload the function code via the Lambda UI in the AWS Console, or by using this command below (make sure your CLI user has the `UpdateFunctionCode` permission for Lambda):
```bash
aws lambda update-function-code --function-name your-function-name --zip-file fileb://function.zip
```

## Usage
Instructions for using this with AWS API Gateway coming soon. In the meantime, you can invoke the function using this AWS CLI command (make sure your CLI user has the `InvokeFunction` permission for Lambda):
```bash
aws lambda invoke --function-name your-function-name --payload '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' outfile
```
