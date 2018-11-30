import requests
import json
import collections
import time

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

def dfs_backtrack(token, visited, prev_action):
    curr_state = get_maze_state(token)
    curr_loc = curr_state['current_location']
    if curr_loc == None:
        return True

    print("Current Location ==> " + str(curr_loc))
    visited.add((curr_loc[0], curr_loc[1]))

    directions = ['RIGHT', 'DOWN', 'LEFT', 'UP']
    num_dirs = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    for dir in directions:
        new_loc = [curr_loc[0] + num_dirs[dir][0], curr_loc[1] + num_dirs[dir][1]]
        # print('TRYING TO MOVE ' + dir + ' TO ' + str(new_loc))
        if (new_loc[0], new_loc[1]) in visited:
            # print('HAS BEEN VISITED')
            continue
        resp = update_maze(token, dir)
        if resp == 'END':
            print('END FOUND')
            return True
        elif resp == 'SUCCESS':
            print('MOVING ' + dir)
            result = dfs_backtrack(token, visited, dir)
            if result:
                return True

    opposite_dir = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }

    update_maze(token, opposite_dir[prev_action])
    # bt_loc = get_maze_state(token)['current_location']
    print("BACKTRACKING")

    return False

def solve_maze(token):
    visited = set()
    dfs_backtrack(token, visited, None)

def main():
    token = get_token()
    print("Token ==> " + str(token))
    state = get_maze_state(token)

    start_time = time.time()
    total_time = 0
    maze_no = 1
    while state['status'] != 'FINISHED':
        solve_maze(token)
        elapsed = time.time() - start_time
        print("=== MAZE " + str(maze_no) + " SOLVED IN " + str(elapsed) + " ===")
        total_time += elapsed
        start_time = time.time()
        maze_no += 1
        state = get_maze_state(token)

    print(str(state['levels_completed']) + " mazes finished! Total time taken: " + str(total_time))

if __name__ == "__main__":
    main()
