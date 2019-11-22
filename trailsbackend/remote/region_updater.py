from model.Region import Region
from model.Update import Update
from local.db_repo import *
import urllib.request
import asyncio
import xml.etree.ElementTree as ET 

import sys
import os

print(os.getcwd())
def load_region_xml(id):
    url = "https://skimap.org/Regions/view/" + str(id) + ".xml"
    print("Loading Region: " + str(id))
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)
    return root

def parse_id_tag(tag):
    return tag.get("id")

def parse_region_xml(root):
    id = int(root.get("id"))
    name = root.find("name").text
    map_count = int(root.find("maps").get("count"))
    child_regions = []
    child_areas = []
    child_list = root.find("regions")
    if(child_list!=None):
        child_regions = list(map(parse_id_tag, child_list.findall("region")))
    child_list = root.find("skiAreas")
    if(child_list!=None):
        child_areas = list(map(parse_id_tag, child_list.findall("skiArea")))
    parent_id = 0
    parents = root.find("parents")
    parents_length = len(parents.getchildren())
    if(parents_length > 0):
        parent = parents.getchildren()[parents_length-1]
        parent_id = int(parent.attrib.get("id"))
    return Region(id=id, name=name, child_regions=child_regions, child_areas=child_areas, map_count=map_count, parent_id=parent_id)

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
    save_update_region(region)

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
    returned_query = db.table('regions').search(where('id')==region.id)
    if (len(returned_query)>0):
        other = returned_query[0]
        db.table('regions').upsert(region.to_dict(), where('id')==region.id)
        if not region.to_dict() == other:
            print("Replacing updated")
            update = Update(type = Update.TYPE_REGION, object_key = region.id)
            db.table('updates').insert(update.to_dict())
        else:
            print("Not replacing")
    else:
        print("Adding region")
        db.table('regions').insert(region.to_dict())
        update = Update(type = Update.TYPE_REGION, object_key = region.id)
        db.table('updates').insert(update.to_dict())