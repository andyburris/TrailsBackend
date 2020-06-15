import sys
#sys.path.insert(0,"/mnt/s/VSCodeProjects/trails-backend-3")

from flask import Flask, jsonify, request
import local.region_repo as region_repo
import local.area_repo as area_repo
import local.maps_repo as maps_repo


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


############## Regions ##############
@app.route('/regions/')
def regions_all():
    last_time = request.args.get('last') or 0
    return jsonify(region_repo.get_all_regions(int(last_time)))

@app.route('/regions/count')
def regions_count():
    return jsonify(region_repo.get_regions_count())

# @app.route('/regions/clear')
# def regions_delete():
#     region_repo.clear_regions()
#     return "Deleted"


############## Areas ##############

@app.route('/areas/')
def areas_all():
    last_time = request.args.get('last') or 0
    return jsonify(area_repo.get_all_areas(int(last_time)))

@app.route('/areas/count')
def areas_count():
    return jsonify(area_repo.get_areas_count())

# @app.route('/areas/clear')
# def areas_delete():
#     area_repo.clear_areas()
#     return "Deleted"


############## Maps ##############

@app.route('/maps/')
def maps_all():
    last_time = request.args.get('last') or 0
    return jsonify(maps_repo.get_all_maps(int(last_time)))

@app.route('/maps/count')
def maps_count():
    return jsonify(maps_repo.get_maps_count())

# @app.route('/maps/clear')
# def maps_delete():
#     maps_repo.clear_maps()
#     return "Deleted"


############## Test ##############

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
