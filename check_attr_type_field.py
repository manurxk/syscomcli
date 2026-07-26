# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
ns_uri = 'http://www.staruml.com'
ns = {'XPD': ns_uri}
path = "C:/Users/MANUEL RAMIREZ/Documents/SYSCOMCLI - copia (2).uml"
tree = ET.parse(path)
root = tree.getroot()

def attr_text(el, name):
    a = el.find('XPD:ATTR[@name="%s"]' % name, ns)
    return a.text if a is not None else None

# find any UMLAttribute and dump its full children to see how Type is stored
count = 0
for el in root.iter('{%s}OBJ' % ns_uri):
    if el.get('type') == 'UMLAttribute':
        print("=== UMLAttribute guid=", el.get('guid'))
        for c in el:
            print("  ", c.tag.split('}')[-1], c.get('name'), c.get('type'), repr(c.text)[:60])
        count += 1
        if count >= 3:
            break
