from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate("./service_account.json")
firebase_admin.initialize_app(cred)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    token = data.get('token')
    title = data.get('title', 'Default Title')
    body = data.get('body', 'Default Body')

    # Create Notification
    notification = messaging.Notification(
        title=title,
        body=body
    )

    # Create Message
    message = messaging.Message(
        notification=notification,
        token=token
    )

    # Send Message
    try:
        response = messaging.send(message)
        return jsonify({'message': 'Notification sent successfully', 'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
