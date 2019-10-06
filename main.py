# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, jsonify
from flask_executor import Executor
from google.cloud import firestore
from entities import *
from region_repo import *
from area_repo import *
import asyncio
from threading import Thread



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
executor = Executor(app)

@app.route('/load')
def load():
    #executor.submit(load_all_regions)
    #executor.submit(load_all_areas)
    return "Loading..."

@app.route('/regions')
def regions():
    #Return all 
    return jsonify(get_all_regions())

@app.route('/areas')
def areas():
    #Return all 
    return jsonify(get_all_areas())

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
