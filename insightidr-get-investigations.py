import requests

url = 'https://us2.api.insight.rapid7.com/idr/v1/investigations'
headers = {
"X-Api-Key": "8ea43599-e617-4c6a-a106-5d9984df1332"
}

params = {
"statuses": "OPEN"
}

print(requests.get(url, headers=headers, params=params).content)