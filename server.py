from flask import Flask, request
from config import *
import time
from blockchain import *
import json
from collections import Counter

app = Flask(__name__)
keys = {}
names = set()
results = Counter()
ledger = []

server_sk, server_vk = generate_key_pair()

def publish_vote(msg):
    pass

def publish_registration(msg):
    pass

@app.route('/status')
def status():
    return ''

@app.route('/key')
def verify():
    return server_vk

@app.route('/choices')
def choices():
    return json.dumps(options)

@app.route('/register', methods=['POST'])
def register():
    name = request.args.get('name')
    vk = request.args.get('vk')

    if name in names:
        return json.loads({"success": False})

    message = generate_registration_message(server_sk, server_vk, vk)
    publish_registration(message)
    ledger.append(message)

    names.add(name)
    keys[vk] = 0, None

    return json.dumps({"success": True,
                       "vk": vk})

@app.route('/vote', methods=['POST'])
def vote():
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

    if choice not in options:
        return json.dumps({"success": False})
    if action != 'vote':
        return json.dumps({"success": False})

    ledger.append(request.args.get('vote'))

    time, old_choice = keys[vk]
    if time >= sub_time:
        return json.dumps({"success": False})

    publish_vote(vote)
    keys[vk] = sub_time, choice

    results[choice] += 1
    if old_choice:
        results[old_choice] -= 1

    return json.dumps({"success": True})

@app.route('/results')
def get_results():
    return json.dumps(results)

@app.route('/ledger')
def get_ledger():
    return json.dumps({'vks': [server_vk], 'ledger': ledger})

if __name__ == '__main__':
    app.run(port=8080)
