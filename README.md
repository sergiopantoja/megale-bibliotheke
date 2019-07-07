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

6. Upload the function code by uploading the zip via the Lambda UI in the AWS Console, or using this command below (you'll need the AWS CLI setup with an AWS account that has the `UpdateFunctionCode` permission for Lambda):
```bash
aws lambda update-function-code --function-name your-function-name --zip-file fileb://function.zip
```

## Usage
```bash
aws lambda invoke --function-name your-function-name --payload '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' outfile
```
