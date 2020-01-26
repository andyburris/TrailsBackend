import sys
sys.path.insert(0,"</path/to/project/directory>")

import remote.region_updater as region_updater
import remote.area_updater as area_updater
import remote.map_updater as map_updater

region_updater.load_all_regions()
area_updater.load_all_areas()
map_updater.load_all_maps()