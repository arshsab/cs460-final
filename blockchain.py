from ecdsa import SigningKey, VerifyingKey
import json
import time
import os

def generate_key_pair():
    sk = SigningKey.generate()
    vk = sk.get_verifying_key()

    return (sk.to_string().hex(), vk.to_string().hex())

def sign_message(message, sk_string):
    sk = SigningKey.from_string(bytes.fromhex(sk_string))
    return sk.sign(message.encode('UTF-8'))

def verify_message(message, signature, vk_string):
    payload = message['payload']
    vk_string = message['vk']
    signature = message['sig']

    vk = VerifyingKey.from_string(bytes.fromhex(vk_string))
    return vk.verify(bytes.fromhex(signature), payload)

def generate_message(payload, sk_string, vk_string):
    return json.dumps(
            {"payload": payload,
             "vk": vk_string,
             "sig": sign_message(payload, sk_string).hex()})

def generate_vote_message(sk_string, vk_string, choice):
    payload = json.dumps(
            {"choice": choice,
             "action": 'vote',
             "timestamp": round(time.time()),
             "nonce": os.urandom(32).hex()})

    return generate_message(payload, sk_string, vk_string)

def generate_registration_message(sk_string, vk_string, name, new_vk):
    message = json.dumps(
            {"name": name,
             "action": "register",
             "vk": new_vk,
             "timestamp": round(time.time()),
             "nonce": os.urandom(32).hex()})

    return generate_message(message, sk_string, vk_string)
