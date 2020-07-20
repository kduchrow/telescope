import flask
from focuser import Focuser
from threading import Thread


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def do_work(value):
        # do something that takes a long time
        Focuser.go(value)

@app.route('/run', methods=['GET'])
def run():
    Thread(target=do_work, kwargs={'value': 1}).start()
    Focuser.go(1)
    return "run"

@app.route('/stop', methods=['GET'])
def stop():
    return Focuser.stop(1)

@app.route('/set/<int:value>', methods=['POST'])
def set(value):
    return str(value)

@app.route('/', methods=['GET'])
def home():
    return Focuser.getstatus(1)

@app.route('/init', methods=['GET'])
def init():
    Focuser.init()
    return "inited"




app.run(host= '0.0.0.0')    # startet app und nutzt Host ip


