# This server is used to evaluate the feature coverage of a test suite in an application.
import re
import json
import redis
from flask import Flask, request, session
from flask_cors import CORS
from flask_session import Session


app = Flask(__name__)
CORS(app)

# Redis Configuration
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')  # Adjust Redis connection details
app.config['SESSION_PERMANENT'] = False  # Sessions expire when the browser closes
app.config['SESSION_USE_SIGNER'] = False   # Use a secret key to sign session data (for security)

# Initialize Flask-Session
Session(app)


BASE_FUNC_DIR = './funcs'


def match(steps, functionalities):
    '''
    Match the steps to a functionality in the application.
    '''
    steps = ''.join(list(map(lambda x: x.split('-')[0], steps)))
    
    for func, pattern in functionalities.items():
        if re.match(pattern, steps) is not None:
            return func
    return None


@app.route('/set-mode/<mode>')
def set_mode(mode):
    '''
    Set the mode of the application.
    Create: Gather functionality click data for regex creation.
    Test: Gather functionality click data for coverage calculation.
    '''
    if mode not in ['create', 'test']:
        return "Invalid request"
    session['mode'] = mode
    return f"Mode set to {mode}"


@app.route('/start-evaluate/<app_name>')
def start_evaluate(app_name):
    '''
    Start tracking the functionality coverage of a test suite in an application.
    '''
    if 'mode' not in session or session['mode'] != 'test':
        return "Invalid request"
    
    with open(f'{BASE_FUNC_DIR}/{app_name}.json', 'r', encoding='utf-8') as f:
        funcs = json.load(f)
        session['funcs'] = funcs
    
    session['coverage_tracking'] = True
    session['tracked_funcs'] = []
    
    return f"Started tracking functionality coverage for {app_name}"


@app.route('/start-track-func')
def start_track_func():
    '''
    Start tracking the executed steps to match to a functionality in the application.
    '''
    if 'mode' not in session or session['mode'] != 'test' or session['coverage_tracking'] is not True:
        return "Invalid request"
    
    session['steps'] = []
    
    return "Started tracking functionality coverage"


@app.route('/func-step', methods=['POST'])
def func_step():
    '''
    Add another step to the tracked steps.
    '''
    if 'mode' not in session or session['mode'] != 'test' or session['coverage_tracking'] is not True:
        return "Invalid request"
    
    data = json.loads(request.data)
    action = data['message']
    
    steps = session['steps']
    steps.append(action)
    session['steps'] = steps

    return 'Logged action'


@app.route('/end-track-func')
def end_track_func():
    '''
    End tracking the executed steps and match to a functionality in the application.
    '''
    if 'mode' not in session or session['mode'] != 'test' or session['coverage_tracking'] is not True:
        return "Invalid request"
    
    tracked_funcs = session['tracked_funcs']
    steps = session['steps']
    matched_func = match(steps, session['funcs'])
    
    print(matched_func)
    
    if matched_func is not None:
        tracked_funcs.append(matched_func)
        session['tracked_funcs'] = tracked_funcs
    
    session.pop('steps', None)
    
    return 'Matched functionality'


@app.route('/end-evaluate')
def end_evaluate():
    '''
    Stop tracking the functionality coverage of a test suite in an application.
    '''
    if 'mode' not in session or session['mode'] != 'test' or session['coverage_tracking'] is not True:
        return "Invalid request"
    
    tracked_funcs = session['tracked_funcs']
    
    coverage = len(set(tracked_funcs)) / len(session['funcs'])
    
    session['coverage_tracking'] = False
    session.pop('funcs', None)
    
    return str(coverage)


@app.route('/test-session')
def session_test():
    print(session['funcs'])
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)
