import requests

url = 'https://us2.api.insight.rapid7.com/validate'

x = requests.post(url, headers = {"X-Api-Key": "8ea43599-e617-4c6a-a106-5d9984df1332"})

print(x.text)