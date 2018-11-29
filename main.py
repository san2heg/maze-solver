import requests
import json

BASE_URL = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com'

def get_token():
    payload = {'uid': '604788993'}
    r = requests.post(BASE_URL + '/session', data=payload)
    return r.json()['token']

def get_maze_state(token):
    params = {'token': token}
    r = requests.get(BASE_URL + '/game', params=params)
    return r.json()

def update_maze(token, action):
    params = {'token': token}
    payload = {'action': action}
    r = requests.post(BASE_URL + '/game', params=params, data=payload)
    return r.json()['result']

def main():
    token = get_token()
    print(get_maze_state(token))

if __name__ == "__main__":
    main()
