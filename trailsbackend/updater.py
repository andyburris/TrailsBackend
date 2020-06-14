import sys
#sys.path.insert(0,"/mnt/s/VSCodeProjects/trails-backend-3")

import trailsbackend.remote.region_updater as region_updater
import trailsbackend.remote.area_updater as area_updater
import trailsbackend.remote.map_updater as map_updater

region_updater.load_all_regions()
area_updater.load_all_areas()
map_updater.load_all_maps()