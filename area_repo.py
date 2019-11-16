import urllib.request
import datetime
import asyncio
from db_repo import *
from Area import *
from Update import *

import xml.etree.ElementTree as ET 

def get_all_areas():
    return sorted(db.table('areas').all(), key=lambda a: a['id'])

def get_areas_count():
    return len(db.table('areas'))

def get_area(area_id):
    return db.table('areas').search(where('id')==area_id)

def get_all_area_updates(last_update):
    updates = db.table('updates').search((where('type')==UPDATE_TYPE_AREA) & (where('time')>=last_update))
    return list(map(lambda u: get_area(u['object_key']), updates))

def clear_areas():
    db.table('areas').purge()

def load_area_xml(id):
    url = "https://skimap.org/SkiAreas/view/" + str(id) + ".xml"
    print("Loading area: " + str(id))
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)
    return root

def parse_id_tag(tag):
    return tag.get("id")

def parse_area_xml(root):
    id = int(root.get("id"))
    name = root.find("name").text
    map_elements = root.find("skiMaps").findall("skiMap")
    #print("map_elements: " + str(map_elements))
    maps = list(map(parse_id_tag, map_elements))
    info = dict()
    info_tags = ['liftCount', 'runCount', 'openingYear', 'officialWebsite', 'operatingStatus']
    for tag in info_tags:
        element = root.find(tag)
        if(element!=None):
            info[tag] = element.text
    #print("info: "+ str(info))
    parent_elements = root.find("regions").findall("region")
    #print("parent_elements: " + str(parent_elements))
    parent_ids = list(map(parse_id_tag, parent_elements))
    return Area(id=id, name=name, maps=maps, info=info, parent_ids=parent_ids)

def load_all_areas():
    asyncio.run(load_from_index())

async def load_from_index():
    url = "https://skimap.org/SkiAreas/index.xml"
    print("Loading areas index")
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)

    child_area_ids = list(map(parse_id_tag, root.findall("skiArea")))
    print("Loaded area index: " + str(child_area_ids))
    child_jobs = []
    for child_area_id in child_area_ids:
        child_jobs.append(asyncio.create_task(load_save_area(child_area_id)))
    for job in child_jobs:
        await job

async def load_save_area(area_id):
    area = parse_area_xml(load_area_xml(area_id))
    if(area.name!="" and area.name!=None):
        save_update_area(area)

def save_update_area(area):
    #print("save_update_area: " + str(area))
    id = area.id
    returned_query = db.table('areas').search(where('id')==id)
    if (len(returned_query)>0):
        other = returned_query[0]
        db.table('areas').upsert(area.to_dict(), where('id')==id)
        if not area.to_dict() == other:
            print("Replacing updated")
            update = Update(time = datetime.now(), type = UPDATE_TYPE_AREA, object_key = area.id)
            db.table('updates').insert(update.to_dict())
        else:
            print("Not replacing")
    else:
        print("Adding area " + str(area.id))
        db.table('areas').insert(area.to_dict())
        update = Update(time = datetime.now(), type = UPDATE_TYPE_MAP, object_key = area.id)
        db.table('updates').insert(update.to_dict())
