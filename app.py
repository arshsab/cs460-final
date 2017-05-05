from blockchain import *
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
    print(message)

    resp = requests.post(server + '/vote', params={'vote': message})
    print(resp)
    resp = resp.json()

    if resp['success']:
        print('Successfully voted.')
    else:
        print('Voting failed. :(')

def results(server):
    resp = requests.get(server + '/results').json()

    for cand, votes in resp.items():
        print(cand, 'got', votes, 'votes')

def checkvote(server):
    pass

def main():
    server = input('Server: ')

    if not requests.get(server + '/status').ok:
        print('Server not active')
        return

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


if __name__ == '__main__':
    main()
