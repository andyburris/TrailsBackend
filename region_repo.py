import urllib.request
import datetime
import asyncio
from entities import *

from google.cloud import firestore
import xml.etree.ElementTree as ET 

def get_all_regions():
    docs = list(get_all_regions_query().stream())
    return list(map(lambda doc: doc.to_dict(), docs))

def get_all_regions_query():
    query = client.collection(u'Region')
    return query

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
    for i in range(1,4):
        load_with_children(i)

def load_with_children(id):
        xml = load_region_xml(id)
        child_regions = xml.find("regions")

        region = parse_region_xml(xml)
        region.to_entity()

        name = xml.find("name").text
        #print("Loaded Region: " + name.encode('utf-8', errors = 'replace'))
        if(child_regions != None):
             for child_region in child_regions:
                 child_id = child_region.get("id")
                 load_with_children(child_id)

def save_update_region(region):
    id = region.id
    query = client.query(kind = 'Region')
    query.add_filter('id', '=', str(id))
    returned_query = list(query.fetch())
    if (len(returned_query)>0):
        other = returned_query[0]
        client.put(region.to_entity())
        if not region == other:
            print("Replacing updated")
            update = Update(time = datetime.now(), type = UPDATE_TYPE_REGION, object_key = region.id)
            client.put(update.to_entity())
        else:
            print("Not replacing")
    else:
        print("Adding region")
        client.put(region.to_entity())