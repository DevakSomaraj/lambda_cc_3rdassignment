import boto3
import json

# Initialize Rekognition and S3 clients
rekognition_client = boto3.client('rekognition', region_name='us-west-2')  # Replace with your region
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        if 'Records' in event and len(event['Records']) > 0:
            bucket_name = event['Records'][0]['s3']['bucket']['name']
            object_key = event['Records'][0]['s3']['object']['key']
            print(f"Bucket: {bucket_name}, Object Key: {object_key}")
        else:
            raise ValueError("Invalid event structure")
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid event structure'})
        }
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    
    # Call Rekognition to detect labels in the image
    try:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            MaxLabels=10  # Set number of labels to detect
        )
        
        # Extract and log the labels detected by Rekognition
        labels = [label['Name'] for label in response['Labels']]
        print(f"Detected labels: {labels}")
        
        # Return a simple response with labels
        return {
            'statusCode': 200,
            'body': json.dumps({
                'bucket': bucket_name,
                'objectKey': object_key,
                'labels': labels
            })
        }

    except rekognition_client.exceptions.InvalidS3ObjectException as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid S3 object or permissions issue.'})
        }
