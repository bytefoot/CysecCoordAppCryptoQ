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

# ================== ROUTES ==================
@app.route('/task1', methods=['POST'])
def task1():
    try:
        data = bytes.fromhex(request.json['frame'])
        if len(data) < 16 + 32:
            return jsonify({"error": "Frame too short"}), 400

        iv, ciphertext, received_hmac = data[:16], data[16:-32], data[-32:]
        
        if not verify_hmac(ciphertext, received_hmac):
            return jsonify({"result": "Invalid HMAC"}), 200

        cipher = AES.new(config['TASK1_KEY'], AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext).decode("utf-8")

        id = plaintext[:16]
        flag = plaintext[16:].lstrip("=")
        
        return jsonify(
            {"result": "Valid ID", "flag": flag} if id == '!!Valid_Header!!'
            else {"result": f"Invalid ID {id!r}", "flag": "Skill Issue Loser"}
        ), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/task2', methods=['POST'])
def task2():
    try:
        ciphertext = bytes.fromhex(request.json['frame'])

        cipher2 = AES.new(config['TASK2_KEY2'], AES.MODE_CBC, iv=config['TASK2_IV2'])
        intermediate = cipher2.decrypt(ciphertext)

        id = intermediate[:16]
        intermediate = intermediate[16:]

        if id != b'!ThisIsCorrect!!':
            return jsonify({"result": "Invalid ID", "flag": "Stoooopid kid"}), 200
        
        cipher1 = AES.new(config['TASK2_KEY1'], AES.MODE_CBC, iv=config['TASK2_IV1'])
        plaintext = cipher1.decrypt(intermediate)

        stamp = plaintext[:16]
        flag = plaintext[16:]\

        if stamp != b'!ArivoliIsBlack!':
            return jsonify({"result": "Invalid STAMP; must be \'!ArivoliIsBlack!\'", "flag": "Fundamental truth violated."}), 200
        
        return jsonify({"result": "Success", "flag": str(flag)[2:-1]}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# New Lambda handler with proper context management
def lambda_handler(event, context):
    try:
        # Parse API Gateway event
        body = json.loads(event.get('body', '{}'))
        headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
        path = event['path'].split('/')[-1]  # Extract 'task1', 'task2', etc
        
        # Route to the appropriate function
        with app.test_request_context(
            path=event['path'],
            method=event['httpMethod'],
            headers=headers,
            json=body
        ):
            # Explicitly push the context
            app.preprocess_request()
            
            # Dispatch based on path
            if path == 'task1':
                response = task1()
            elif path == 'task2':
                response = task2()
            else:
                response = jsonify({"error": "Invalid endpoint"}), 404
            
            return {
                'statusCode': response[1],
                'body': json.dumps(response[0].get_json()),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)