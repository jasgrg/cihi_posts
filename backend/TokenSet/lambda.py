import json
import boto3
import requests

def validate_token(event):
	if('accessToken' in event):
        
        # TODO: whitelist user ids, or validate that the user is an admin of CIHI

		response = requests.get(f"https://graph.facebook.com/debug_token?input_token={event['accessToken']}&access_token={event['accessToken']}")
		if response.status_code == 200:
			data = response.json()
			response_data = data["data"]
			print(data)
			if 'is_valid' in response_data and response_data['is_valid']:
				return True
	else:
		print("No accessToken")
	return False
		
def save_secret(event):
	data_string = json.dumps(event)
	client = boto3.client('secretsmanager')
	client.put_secret_value(
		SecretId="CIHI-app",
		SecretString=data_string)

def handler(event, context) :
	if validate_token(event):
		save_secret(event)
		return {
			"valid": True
		}
	return {
		"valid": False
	}