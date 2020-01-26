import sys
sys.path.insert(0,"</path/to/project/directory>")

from flask import Flask, jsonify, request
import trailsbackend.local.region_repo as region_repo
import trailsbackend.local.area_repo as area_repo
import trailsbackend.local.maps_repo as maps_repo


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

############## Regions ##############
@app.route('/regions/')
def regions_all():
    return jsonify(region_repo.get_all_regions())

@app.route('/regions/count')
def regions_count():
    return jsonify(region_repo.get_regions_count())

@app.route('/regions/new')
def regions_updates():
    last_time = request.args.get('last') or 0
    return jsonify(region_repo.get_all_region_updates(int(last_time)))

############## Areas ##############

@app.route('/areas/')
def areas_all():
    return jsonify(area_repo.get_all_areas())

@app.route('/areas/count')
def areas_count():
    return jsonify(area_repo.get_areas_count())

@app.route('/areas/new')
def areas_new():
    last_time = request.args.get('last') or 0
    return jsonify(area_repo.get_all_area_updates(int(last_time)))
############## Maps ##############

@app.route('/maps/')
def maps_all():
    return jsonify(maps_repo.get_all_maps())

@app.route('/maps/count')
def maps_count():
    return jsonify(maps_repo.get_maps_count())

@app.route('/maps/new')
def maps_updates():
    last_time = request.args.get('last') or 0
    return jsonify(maps_repo.get_all_map_updates(int(last_time)))


############## Test ##############

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
