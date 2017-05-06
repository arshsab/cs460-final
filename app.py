from blockchain import *
from collections import Counter
import requests

def create(server):
    name = input('Name? ')
    sk, vk = generate_key_pair()

    resp = requests.post(server + '/register',
                         params={'vk': vk, 'name': name}).json()

    if resp['success']:
        print('Successfully registered.')
    else:
        print('Registration Failed. Are you already registered?')

    with open('key', 'w+') as f:
        f.write(sk)
        f.write('\n')
        f.write(vk)

def vote(server):
    with open('key') as f:
        lines = f.readlines()

    [sk, vk] = [x.strip() for x in lines]

    choices = requests.get(server + '/choices').json()
    print('Available candidates are:', choices)

    choice = input('Who do you vote for? ')
    message = generate_vote_message(sk, vk, choice)

    resp = requests.post(server + '/vote', params={'vote': message})
    resp = resp.json()

    if resp['success']:
        print('Successfully voted.')
    else:
        print('Voting failed. :(')

def fetch_ledger(server):
    resp = requests.get(server + '/ledger').json()

    return resp['vks'], resp['ledger']

def results(server):
    servks, ledger = fetch_ledger(server)

    keys = {}
    results = Counter()

    for message in ledger:
        message = json.loads(message)

        if not verify_message(message):
            continue

        vk = message['vk']
        payload = json.loads(message['payload'])

        if payload['action'] == 'vote' and vk in keys:
            new_choice = payload['choice']
            new_time = payload['timestamp']

            old_time, old_choice = keys[vk]
            if old_time < new_time:
                keys[vk] = new_time, new_choice

                results[new_choice] += 1
                if old_choice:
                    results[old_choice] -= 1
        elif payload['action'] == 'register' and vk in servks:
            new_vk = payload['vk']
            keys[new_vk] = 0, None

    for cand, votes in results.items():
        print(cand, 'got', votes, 'votes')

def checkvote(server):
    servks, ledger = fetch_ledger(server)

    with open('key') as f:
        lines = f.readlines()

    [_, vk] = [x.strip() for x in lines]

    curr_time, curr_choice = 0, None
    for message in ledger:
        message = json.loads(message)

        if not verify_message(message):
            continue

        if message['vk'] != vk:
            continue


        payload = json.loads(message['payload'])
        if payload['action'] == 'vote':
            new_choice = payload['choice']
            new_time = payload['timestamp']

            if curr_time < new_time:
                curr_time = new_time
                curr_choice = new_choice

    print('You chose: ', curr_choice)

def main():
    server = input('Server: ')

    if not requests.get(server + '/status').ok:
        print('Server not active')
        return

    while True:
        action = input('Action (register, vote, results, checkvote): ')
        action = action.lower()

        if action == 'register':
            create(server)
        elif action == 'results':
            results(server)
        elif action == 'vote':
            vote(server)
        elif action == 'checkvote':
            checkvote(server)
        else:
            print('Option not recognized')

        cont = input('Perform another action (y/n)?')

        if cont != 'y':
            break

if __name__ == '__main__':
    main()
