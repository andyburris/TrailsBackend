from model.Area import Area, dict_to_area
import local.area_repo as area_repo
from local.db_repo import *
import urllib.request
import asyncio
import xml.etree.ElementTree as ET 
import datetime
from pymongo import ReplaceOne

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
        child_jobs.append(asyncio.create_task(get_area(child_area_id)))
    all_areas = []
    for job in child_jobs:
        all_areas.append(await job)
    save_update_areas(all_areas)
    
async def get_area(id):
    return parse_area_xml(load_area_xml(id))

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

def save_update_areas(areas):
    saved_areas = list(map(lambda d: dict_to_area(d), area_repo.get_all_areas(0)))
    new_or_updated = [item for item in areas if item not in saved_areas] # need to create update objects for both new objects and updated ones

    print("new or updated = " + str(new_or_updated))

    if(len(new_or_updated) == 0):
        return

    for area in new_or_updated:
        area.last_update = datetime.datetime.now()

    db.areas.bulk_write(list(map(lambda r: ReplaceOne({'_id': r.id}, r.to_dict(), upsert=True), new_or_updated)))