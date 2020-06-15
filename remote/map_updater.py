from model.Map import Map, dict_to_map
from model.Thumbnail import Thumbnail
from local.db_repo import *
from local.area_repo import *
import local.maps_repo as maps_repo
import urllib.request
import asyncio
import xml.etree.ElementTree as ET
import datetime
from pymongo import ReplaceOne

def load_all_maps():
    asyncio.run(load_from_areas())

async def load_from_areas():
    areas = get_all_areas(0)
    child_jobs = []
    for area in areas:
        for map_id in area.get("maps"):
            child_jobs.append(asyncio.create_task(get_map(map_id)))
    all_maps = []
    for job in child_jobs:
        all_maps.append(await job)
    save_update_maps(all_maps)

async def get_map(map_id):
    return parse_map_xml(load_map_xml(map_id))

def load_map_xml(id):
    url = "https://skimap.org/SkiMaps/view/" + str(id) + ".xml"
    print("Loading map: " + str(id))
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)
    return root

def parse_id_tag(tag):
    return tag.get("id")

def parse_map_xml(root):
    map_id = int(root.get("id"))
    year = root.find("yearPublished").text
    image_tag = root.find("unprocessed")
    image_url = image_tag.get("url")
    if(image_tag.attrib.__contains__("width") and image_tag.attrib.__contains__("height")): #width and height tags not availible on pdfs
        image_height_to_width_ratio = (int(image_tag.get("width")))/(int(image_tag.get("height")))
    else:
        image_height_to_width_ratio = 1
    thumbnail_tags = root.findall("thumbnail")
    thumbnails = []
    for tag in thumbnail_tags:
        if(tag.attrib.__contains__("width")):
            width = int(tag.get("width"))
            height = int(float(width) * image_height_to_width_ratio)
            thumbnails.append(Thumbnail(width, height, tag.get("url")))
        else:
            height = int(tag.get("height"))
            width = int(float(height) / image_height_to_width_ratio)
            thumbnails.append(Thumbnail(width, height, tag.get("url")))

    parent_id = root.find("skiArea").get("id")
    return Map(map_id, year, thumbnails, image_url, parent_id)

def save_update_maps(maps):
    saved_maps = list(map(lambda d: dict_to_map(d), maps_repo.get_all_maps(0)))
    new_or_updated = [item for item in maps if item not in saved_maps] # need to create update objects for both new objects and updated ones

    print("new or updated = " + str(new_or_updated))

    if(len(new_or_updated) == 0):
        return

    for map_item in new_or_updated:
        map_item.last_update = datetime.datetime.now()

    db.maps.bulk_write(list(map(lambda r: ReplaceOne({'_id': r.id}, r.to_dict(), upsert=True), new_or_updated)))

def purge_deleted_maps(area):
    old = db.maps.find(where('parent_id')==area.id)
    for map_id in old:
        if not area.maps.__contains__(map_id):
            db.maps.remove('id'==map_id)
