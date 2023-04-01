import requests
import socket

# Server website: https://us-central1-hardwaregoblins.cloudfunctions.net/serveArray

def goblin_init():

    headers = {
    }

    params = {
    }

    response = requests.get('https://us-central1-hardwaregoblins.cloudfunctions.net/serveArray',
                            params=params, headers=headers)

    if response.status_code == 200: # Status: OK
        print(response.text)
        return response.text
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return None

if __name__ == '__main__':
    goblin_init()