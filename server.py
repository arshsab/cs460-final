from flask import Flask, request
import config
import time
from blockchain import *
import json
from collections import Counter

app = Flask(__name__)
keys = {}
names = set()
results = Counter()

server_sk, server_vk = generate_key_pair()

def publish_vote(msg):
    pass

def publish_registration(msg):
    pass

@app.route('/key')
def verify():
    return server_vk

@app.route('/register')
def register():
    name = request.args.get('name')

    if name in names:
        return json.loads({"success": False})

    sk, vk = generate_key_pair()
    message = generate_registration_message(server_sk, server_vk, name, vk)
    publish_registration(message)

    names.add(name)
    keys[vk] = 0

    return json.dumps({"success": True,
                       "vk": vk,
                       "sk": sk})

@app.route('/vote', methods=['POST'])
def vote():
    print(request.args)
    vote = json.loads(request.args.get('vote'))
    vk = vote['vk']

    if vk not in keys:
        return json.dumps({"success": False})
    if not verify_message(vote):
        return json.dumps({"success": False})

    payload = json.loads(vote['payload'])
    choice = payload['choice']
    action = payload['action']
    sub_time = payload['timestamp']

    if choice not in config.choices:
        return json.dumps({"success": False})
    if action != 'vote':
        return json.dumps({"success": False})

    time, choice = keys[ck]
    if time >= sub_time:
        return json.dumps({"success": False})

    publish_vote(vote)
    keys[vk] = sub_time, choice
    results[choice] += 1

    return json.dumps({"success": True})

@app.route('/results')
def get_results():
    return json.dumps(results)

if __name__ == '__main__':
    app.run(port=8080)
