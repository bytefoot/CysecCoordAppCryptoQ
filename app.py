# Hi there,
# You didn't run to ur momma looking at the README?
# Hmm... Ballsy.
# Okie... I shall help hereforth

# Setup
# ====================================================================================================
# Okay so the below code is kinda useless for you
# Skip reading till the next line made of '='

from flask import Flask, request, jsonify
import hmac
import hashlib
from Crypto.Cipher import AES
import os
from dotenv import load_dotenv
import json
import binascii

app = Flask(__name__)

def get_env_var(name, default=None, required=True):
    """Safely get environment variable with validation"""
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"Environment variable {name} is required")
    return binascii.unhexlify(value.encode("utf-8"))

if os.path.exists('.env'):
    load_dotenv()

try:
    config = {
        'TASK1_KEY': get_env_var('TASK1_KEY'),
        'TASK1_HMAC': get_env_var('TASK1_HMAC'),
        'TASK2_KEY1': get_env_var('TASK2_KEY1'),
        'TASK2_IV1': get_env_var('TASK2_IV1'),
        'TASK2_KEY2': get_env_var('TASK2_KEY2'),
        'TASK2_IV2': get_env_var('TASK2_IV2'),
    }
except ValueError as e:
    app.logger.error(f"Configuration error: {str(e)}")
    raise

# ================== HELPER FUNCTIONS ==================
def verify_hmac(ciphertext, received_hmac):
    h = hmac.new(config['TASK1_HMAC'], ciphertext, hashlib.sha256)
    return hmac.compare_digest(h.digest(), received_hmac)

# ====================================================================================================
# Task 1
@app.route('/task1', methods=['POST'])
def task1():
    try:
        # Just retrieving data
        data = bytes.fromhex(request.json['frame'])
        if len(data) < 16 + 32:
            return jsonify({"error": "Frame too short"}), 400

        # SPlitting into characteristic chunks
        iv, ciphertext, received_hmac = data[:16], data[16:-32], data[-32:]
        
        # HMAC is used for message authentication
        # Basically its used to protect against a middle man tampering with the message.
        if not verify_hmac(ciphertext, received_hmac):
            return jsonify({"result": "Invalid HMAC"}), 200

        # Decryption
        cipher = AES.new(config['TASK1_KEY'], AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext).decode("utf-8")

        # Some validations on the data
        id = plaintext[:16]
        flag = plaintext[16:].lstrip("=")
        
        return jsonify(
            {"result": "Valid ID", "flag": flag} if id == '!!Valid_Header!!'
            else {"result": f"Invalid ID {id!r}", "flag": "Skill Issue Loser"}
        ), 200
        
    except Exception as e:
        # Bruh.. why u reading here? This not for you da.
        return jsonify({"error": str(e)}), 400

# ====================================================================================================
# Task 2
@app.route('/task2', methods=['POST'])
def task2():
    try:
        # Just taking the data
        ciphertext = bytes.fromhex(request.json['frame'])

        if len(ciphertext) > 80:
            return jsonify({"error": "Frame too long"}), 400

        # Decrypting outer layer
        cipher2 = AES.new(config['TASK2_KEY2'], AES.MODE_CBC, iv=config['TASK2_IV2'])
        intermediate = cipher2.decrypt(ciphertext)

        id = intermediate[:16]
        intermediate = intermediate[16:]

        # Verification of outer id
        if id != b'!ThisIsCorrect!!':
            return jsonify({"result": "Invalid ID", "flag": "Stoooopid kid"}), 200
        
        # Decrypting inner layer
        cipher1 = AES.new(config['TASK2_KEY1'], AES.MODE_CBC, iv=config['TASK2_IV1'])
        plaintext = cipher1.decrypt(intermediate)

        stamp = plaintext[:16]
        flag = plaintext[16:]

        # Verifying stamp (to make sure first block isnt changed)
        if stamp != b'!ArivoliIsBlack!':
            return jsonify({"result": "Invalid STAMP; must be \'!ArivoliIsBlack!\'", "flag": "Fundamental truth violated."}), 200
        
        return jsonify({"result": "Success", "flag": str(flag)[2:-1]}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ====================================================================================================
# Code not meant for you kid.

def lambda_handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {}
        
        headers = {k.lower(): v for k, v in event.get('headers', {}).items()}

        path = event.get('path', '')
        if not path:
            path = event.get('rawPath', '')
        path = path.split('/')[-1]  # Extract 'task1', 'task2', etc

        with app.test_request_context(
            path=event.get('path', '/task1' if path == 'task1' else '/task2'),
            method=event.get('httpMethod', 'POST'),
            headers=headers,
            json=body
        ):

            app.preprocess_request()

            if path == 'task1':
                response = task1()
            elif path == 'task2':
                response = task2()
            else:
                response = jsonify({"error": "Invalid endpoint"}), 404

            if isinstance(response, tuple):
                response_body, status_code = response
            else:
                response_body = response
                status_code = 200
            
            return {
                'statusCode': status_code,
                'body': json.dumps(response_body.get_json()),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)