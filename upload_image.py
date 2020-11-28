import requests
import numpy as np
import base64

#Define your keys from the developer portal
consumer_key = 'xzeZVKNQeXaROhrvY5l7rI4sJ'
consumer_secret_key = 'vhXAthXQFWdF4qlEC8ESDFvGbQKADq0aWaRv7euKvmgYIF8G7P'
#Reformat the keys and encode them
key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
#Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')


base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
print(auth_resp.json())
access_token = auth_resp.json()['access_token']

file = open('C:\\Users\\hadya\\Downloads\\battery_20_black_192x192.png', 'rb')
data = file.read()
resource_url='https://upload.twitter.com/1.1/media/upload.json'
upload_image={
    'media':data,
    'media_category':'tweet_image'}
image_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

media_id=requests.post(resource_url,headers=image_headers,params=upload_image)
print(media_id.text)