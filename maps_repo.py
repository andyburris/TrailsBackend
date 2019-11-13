import urllib.request
import datetime
import asyncio
from Map import *
from Update import *
from Thumbnail import *
from Area import *
from db_repo import *

import xml.etree.ElementTree as ET 

def get_all_maps():
    return sorted(db.table('maps').all(), key=lambda a: a['id'])

def get_maps_count():
    return len(db.table('maps'))

def get_map(map_id):
    return db.table('maps').search(where('id')==map_id)

def get_all_map_updates(last_update):
    updates = db.table('updates').search((where('type')==UPDATE_TYPE_MAP) & (where('time')>=last_update))
    return list(map(lambda u: get_map(u['object_key']), updates))

def clear_maps():
    db.table('maps').purge()

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
    image_height_to_width_ratio = (int(image_tag.get("width")))/(int(image_tag.get("height")))
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

def load_all_maps():
    asyncio.run(load_from_areas())

async def load_from_areas():
    areas = db.table('areas').all()
    child_jobs = []
    for area in areas:
        for map_id in area.get("maps"):
            child_jobs.append(asyncio.create_task(load_save_map(map_id)))
    for job in child_jobs:
        await job
    #await load_save_map(14834)

async def load_save_map(map_id):
    loaded_map = parse_map_xml(load_map_xml(map_id))
    save_update_map(loaded_map)

def save_update_map(map_to_save):
    #print("save_update_map: " + str(map))
    id = map_to_save.id
    returned_query = db.table('maps').search(where('id')==id)
    if (len(returned_query)>0):
        other = returned_query[0]
        db.table('maps').upsert(map_to_save.to_dict(), where('id')==id)
        if not map_to_save.to_dict() == other:
            print("Replacing updated")
            update = Update(time = datetime.now(), type = UPDATE_TYPE_MAP, object_key = map_to_save.id)
            db.table('updates').insert(update.to_dict())
        else:
            print("Not replacing")
    else:
        print("Adding map " + str(map_to_save.id))
        db.table('maps').insert(map_to_save.to_dict())
        update = Update(time = datetime.now(), type = UPDATE_TYPE_MAP, object_key = map_to_save.id)
        db.table('updates').insert(update.to_dict())
