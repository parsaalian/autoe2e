# This server is used for manual feature extraction in an application, prior to coverage evaluation.
import os
import json
from flask_cors import CORS
from flask import Flask, request


app = Flask(__name__)
CORS(app)


def is_process_active():
    '''
    Check to see if a functionality is being tracked.
    '''
    with open('./status.log', 'r', encoding='utf-8') as f:
        return f.read() == 'running'


def get_current_process_file():
    dir_len = len(os.listdir('./logs'))
    return f'./logs/process_{dir_len}.log'


def get_new_process_number():
    dir_len = len(os.listdir('./logs'))
    return dir_len + 1


@app.route('/start')
def start():
    '''
    Start tracking a functionality in a log file.
    '''
    running = is_process_active()
    
    if not running:
        with open('./status.log', 'w', encoding='utf-8') as f:
            f.write('running')
        
        new_process_log = f'./logs/process_{get_new_process_number()}.log'
        open(new_process_log, 'a', encoding='utf-8').close()
    
    return 'started tracking functionality'


@app.route('/restart')
def restart():
    running = is_process_active()
    
    if running:
        current_file = get_current_process_file()
        with open(current_file, 'w', encoding='utf-8') as f:
            f.write('')
    
    return 'restarted tracking functionality'


@app.route('/stop')
def stop():
    '''
    Stop tracking a functionality in a log file.
    '''
    with open('./status.log', 'w', encoding='utf-8') as f:
        f.write('stopped')
    return 'stopped tracking functionality'


@app.route('/log', methods=['POST'])
def log():
    '''
    Log a new action in a log file.
    '''
    running = is_process_active()
    
    if running:
        data = json.loads(request.data)

        log_name = get_current_process_file()
        with open(log_name, 'a', encoding='utf-8') as f:
            action = data['message']
            f.write(action + '\n')
    
    return 'Logged action'


@app.route('/status')
def status():
    '''
    Get the current status of the tracking functionality.
    '''
    return 'tracking' if is_process_active() else 'stopped'
