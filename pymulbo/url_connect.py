from flask import Flask
from pathlib import Path
from datetime import datetime
import pandas as pd
app = Flask(__name__)


def add_url(input_token, input_url):
    urcon_index = "library/urcon_index_df.pkl"
    if not Path(urcon_index).exists():
        print(f"urcon_index: {urcon_index} does not exist, creating")
        df = pd.DataFrame(columns=["url", "token", "timestamp"])
        df.to_pickle(urcon_index)

    # make new entry
    df = pd.read_pickle(urcon_index)
    data_dict = {"url": input_url,
                 "token": input_token,
                 "timestamp": datetime.now()}
    df = df.append(data_dict, ignore_index=True)
    df.to_pickle(urcon_index)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/urcon/<int:input_token>/<string:input_url>')
def urcon(input_token, input_url):
    print(f"save_url: token:{input_token}, url:{input_url}")
    add_url(input_token, input_url)
    return 'success'
