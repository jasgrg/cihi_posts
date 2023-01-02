import json
import boto3
import requests


def get_and_validate_token():
    secret = get_secret()
    if "accessToken" in secret:
        if validate_token(secret["accessToken"]):
            return secret["accessToken"]
        else: 
            print("accessToken is no longer valid")
    else:
        print("No accessToken")
    return None
    

def validate_token(accessToken):
	response = requests.get(f"https://graph.facebook.com/debug_token?input_token={accessToken}&access_token={accessToken}")
	if response.status_code == 200:
		data = response.json()
		print(f"response from validate token {data}")
		response_data = data["data"]
		print(data)
		if 'is_valid' in response_data and response_data['is_valid']:
			return True
	return False
		
		
def get_secret():
    print(f"getting secret")
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId="CIHI-app")
    print(f"secret is: {secret}")
    return json.loads(secret["SecretString"])
	

def get_posts_from_api(token):
    fields = "from,attachments,full_picture,child_attachments,description,created_time,icon,id,message,name,object_id,comments,permalink_url,link"
    response = requests.get(f"https://graph.facebook.com/906270957045326/feed?access_token={token}&fields={fields}")
    if response.status_code == 200:
        # TODO: adding paging/caching to make sure we get all of the posts without going over request limit
        return response.json()["data"]
    else:
        print(f"error getting posts: {response.status_code}")
    return None
        
def send_posts_to_subscribers(posts):
    #TODO: get subscribers list
    #TODO: format posts in email/attachment
    #TODO: send posts to subscriber list
    for post in posts:
        print(f"Sending post {post['id']}")

def handler(event, context) :
    token = get_and_validate_token()
    posts = get_posts_from_api(token)
    
    send_posts_to_subscribers(posts)
