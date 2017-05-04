from ecdsa import SingingKey, VerifyingKey

def generate_key_pair():
    sk = SigningKey.generate()
    vk = sk.get_verifying_key()

    return (sk.to_string().hex(), vk.to_string().hex())

def sign_message(message, sk_string):
    sk = SigningKey.from_string(bytes.fromhex(sk_string))
    return sk.sign(message.encode('UTF-8'))

def verify_message(message, signature, vk_string):
    vk = VerifyingKey.from_string(bytes.fromhex(vk_string))
    return vk.verify(bytes.fromhex(signature), message)
