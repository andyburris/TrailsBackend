import urllib.request
import datetime
import asyncio
from entities import *

from google.cloud import firestore
import xml.etree.ElementTree as ET 

def get_all_areas():
    docs = list(get_all_areas_query().stream())
    return list(map(lambda doc: doc.to_dict(), docs))

def get_all_areas_query():
    query = client.collection(u'Area')
    return query

def clear_areas():
    for area in get_all_areas().stream():
        area.key.delete()

def load_area_xml(id):
    url = "https://skimap.org/SkiAreas/view/" + str(id) + ".xml"
    print("Loading area: " + str(id))
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)
    return root

def parse_area_id_tag(tag):
    return tag.get("id")

def parse_area_xml(root):
    id = int(root.get("id"))
    name = root.find("name").text
    map_elements = root.find("skiMaps").findall("skiMap")
    print("map_elements: " + str(map_elements))
    maps = list(map(parse_area_id_tag, map_elements))
    info = dict()
    info_tags = ['liftCount', 'runCount', 'openingYear', 'officialWebsite', 'operatingStatus']
    for tag in info_tags:
        element = root.find(tag)
        if(element!=None):
            info[tag] = element.text
    print("info: "+ str(info))
    parent_elements = root.find("regions").findall("region")
    print("parent_elements: " + str(parent_elements))
    parent_ids = list(map(parse_area_id_tag, parent_elements))
    return Area(id=id, name=name, maps=maps, info=info, parent_ids=parent_ids)

def load_all_areas():
    load_from_index()

def load_from_index():
    url = "https://skimap.org/SkiAreas/index.xml"
    print("Loading areas index")
    resp = urllib.request.urlopen(url)
    content = resp.read()
    root = ET.fromstring(content)

    child_area_ids = list(map(parse_area_id_tag, root.findall("skiArea")))
    print("Loaded area index: " + str(child_area_ids))
    for child_area_id in child_area_ids:
        area = parse_area_xml(load_area_xml(child_area_id))
        area.to_entity()

def save_update_area(area):
    query = client.query(kind = 'Area')
    query.add_filter('id', '=', str(area.id))
    returned_query = list(query.fetch())
    if (len(returned_query)>0):
        other = returned_query[0]
        client.put(area.to_entity())
        if not area == other:
            print("Replacing updated")
            update = Update(time = datetime.now(), type = UPDATE_TYPE_AREA, object_key = area.id)
            client.put(update.to_entity())
        else:
            print("Not replacing")
    else:
        print("Adding area")
        client.put(area.to_entity())