import urllib.request
import datetime
import asyncio
from entities import *

import xml.etree.ElementTree as ET 

def get_all_regions():
    return db.table('regions').all()

def clear_regions():
    for region in get_all_regions().stream():
        region.key.delete()

def load_region_xml(id):
    url = "https://skimap.org/Regions/view/" + str(id) + ".xml"
    print("Loading Region: " + str(id))
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)
    return root

def parse_region_xml(root):
    id = int(root.get("id"))
    name = root.find("name").text
    map_count = int(root.find("maps").get("count"))
    parent_id = 0
    parents = root.find("parents")
    parents_length = len(parents.getchildren())
    if(parents_length > 0):
        parent = parents.getchildren()[parents_length-1]
        parent_id = int(parent.attrib.get("id"))
    return Region(id=id, name=name, map_count=map_count, parent_id=parent_id)

def load_all_regions():
    asyncio.run(load_all_regions_async())

async def load_all_regions_async():
    print("Loading all")
    child_jobs = []
    for i in range(1,5):
        child_jobs.append(asyncio.create_task(load_with_children(i)))
    for job in child_jobs:
        await job

async def load_with_children(id):
    print("Loading: " + str(id))
    xml = load_region_xml(id)
    child_regions = xml.find("regions")

    region = parse_region_xml(xml)
    region.to_entity()

    name = xml.find("name").text
    #print("Loaded Region: " + name.encode('utf-8', errors = 'replace'))
    child_jobs = []
    if(child_regions != None):
            for child_region in child_regions:
                child_id = child_region.get("id")
                child_jobs.append(asyncio.create_task(load_with_children(child_id)))

    for job in child_jobs:
        await job


def save_update_region(region):
    id = region.id
    returned_query = db.table('regions').search(where('id')==id)
    if (len(returned_query)>0):
        other = returned_query[0]
        db.table('regions').upsert(region.to_dict(), where('id')==id)
        if not region == other:
            print("Replacing updated")
            update = Update(time = datetime.now(), type = UPDATE_TYPE_REGION, object_key = region.id)
            db.table('updates').insert(update.to_dict())
        else:
            print("Not replacing")
    else:
        print("Adding region")
        db.table('regions').insert(region.to_dict())