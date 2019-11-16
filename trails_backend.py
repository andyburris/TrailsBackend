from flask import Flask, jsonify, request
from flask_executor import Executor
from region_repo import *
from area_repo import *
from maps_repo import *
from threading import Thread



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
executor = Executor(app)

############## Regions ##############
@app.route('/regions/')
def regions_all():
    return jsonify(get_all_regions())

@app.route('/regions/count')
def regions_count():
    return jsonify(get_regions_count())

@app.route('/regions/load')
def regions_load():
    #load_all_regions()
    executor.submit(load_all_regions)
    return "Loading regions..."

@app.route('/regions/new')
def regions_updates():
    last_time = request.args.get('last') or 0
    return jsonify(get_all_region_updates(int(last_time)))

@app.route('/regions/clear')
def regions_clear():
    clear_regions()
    return "Clearing regions..."

############## Areas ##############

@app.route('/areas/')
def areas_all():
    return jsonify(get_all_areas())

@app.route('/areas/count')
def areas_count():
    return jsonify(get_areas_count())

@app.route('/areas/new')
def areas_new():
    last_time = request.args.get('last') or 0
    return jsonify(get_all_area_updates(int(last_time)))

@app.route('/areas/load')
def areas_load():
    #load_all_areas()
    executor.submit(load_all_areas)
    return "Loading areas..."

@app.route('/areas/clear')
def areas_clear():
    clear_areas()
    return "Clearing areas..."

############## Maps ##############

@app.route('/maps/')
def maps_all():
    return jsonify(get_all_maps())

@app.route('/maps/count')
def maps_count():
    return jsonify(get_maps_count())

@app.route('/maps/load')
def maps_load():
    #load_all_maps()
    executor.submit(load_all_maps)
    return "Loading maps..."

@app.route('/maps/new')
def maps_updates():
    last_time = request.args.get('last') or 0
    return jsonify(get_all_map_updates(int(last_time)))

@app.route('/maps/clear')
def maps_clear():
    clear_maps()
    return "Clearing maps..."

############## Test ##############

@app.route('/test')
def test():
    return bucket.name

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
