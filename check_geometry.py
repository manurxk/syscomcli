# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
ns_uri = 'http://www.staruml.com'
ns = {'XPD': ns_uri}
path = "C:/Users/MANUEL RAMIREZ/Documents/SYSCOMCLI/SYSCOMCLI - version final.uml"
tree = ET.parse(path)
root = tree.getroot()

def attr_text(el, name):
    a = el.find('XPD:ATTR[@name="%s"]' % name, ns)
    return a.text if a is not None else None

def find_by_guid(guid):
    for el in root.iter('{%s}OBJ' % ns_uri):
        if el.get('guid') == guid:
            return el
    return None

dc = find_by_guid('me5z5T4DEuyNkifssVF+8AAA')  # DC_Especialidad
print("DC Name:", attr_text(dc,'Name'))

for cv in dc.iter('{%s}OBJ' % ns_uri):
    if cv.get('type') in ('UMLClassView','UMLActorView'):
        left = attr_text(cv,'Left'); top = attr_text(cv,'Top'); w = attr_text(cv,'Width'); h = attr_text(cv,'Height')
        # find model ref + name label
        model_guid = None
        for c in cv:
            if c.tag.endswith('REF') and c.get('name')=='Model':
                model_guid = c.text
        model_el = find_by_guid(model_guid) if model_guid else None
        mname = attr_text(model_el,'Name') if model_el is not None else '?'
        print(cv.get('type'), 'model=', mname, 'Left=',left,'Top=',top,'W=',w,'H=',h)

print()
print("Top-level OwnedViews of DiagramView (direct children only):")
for dv in dc.iter('{%s}OBJ' % ns_uri):
    if dv.get('name')=='DiagramView':
        for c in dv:
            if c.tag.endswith('OBJ') and c.get('name','').startswith('OwnedViews['):
                print(' ', c.get('name'), c.get('type'))
        break
