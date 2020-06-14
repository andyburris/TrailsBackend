from model.Region import Region, dict_to_region
from trailsbackend.local.db_repo import *
import trailsbackend.local.region_repo as region_repo
import urllib.request
import asyncio
import datetime
import xml.etree.ElementTree as ET 
from pymongo import ReplaceOne

import sys
import os

print(os.getcwd())

def load_all_regions():
    asyncio.run(load_all_regions_async())

async def load_all_regions_async():
    print("Loading all")
    child_jobs = []
    for i in range(1,5):
        child_jobs.append(asyncio.create_task(load_with_children(i)))
    all_regions = []
    for job in child_jobs:
        all_regions += await job # will concat the list returned by the job 
    save_update_regions(all_regions)


async def load_with_children(id):
    xml = load_region_xml(id)
    child_region_ids = xml.find("regions")

    region = parse_region_xml(xml)

    name = xml.find("name").text
    #print("Loaded Region: " + name.encode('utf-8', errors = 'replace'))
    child_jobs = []
    if(child_region_ids != None):
        for child_region in child_region_ids:
            child_id = child_region.get("id")
            child_jobs.append(asyncio.create_task(load_with_children(child_id)))
    child_regions = []
    for job in child_jobs:
        child_regions += await job # will concat the list returned by the job 
    return child_regions + [region]

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

def parse_id_tag(tag):
    return tag.get("id")

def save_update_regions(regions):
    saved_regions = list(map(lambda d: dict_to_region(d), region_repo.get_all_regions(0)))
    new_or_updated = [item for item in regions if item not in saved_regions] # need to create update objects for both new objects and updated ones

    print("new or updated = " + str(new_or_updated))

    if(len(new_or_updated) == 0):
        return

    for region in new_or_updated:
        region.last_update = datetime.datetime.now()

    db.regions.bulk_write(list(map(lambda r: ReplaceOne({'_id': r.id}, r.to_dict(), upsert=True), new_or_updated)))