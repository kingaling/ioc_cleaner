works = '''
This code is not namespace friendly so I opted for the DOM code below.

import xml.etree.ElementTree as ET
import re

tree = ET.parse("/Users/shaneking/cirt/iocs/1882ac07-a326-4cf6-b602-9b287604feff.ioc")
root = tree.getroot()
ns = re.split('}', root.tag)[0] + '}'

for indicator in root.iter(ns + "Indicator"):
    for indicatoritem in indicator:
        for content in indicatoritem:
            if content.tag == ns + "Content":
                if content.text == "20bad126b881d3fb54004dfb7880981a":
                    ET.Element.remove(indicator, indicatoritem)


tree.write("/Users/shaneking/Desktop/lmao.txt")
#for indicator in fuckinroot.iter(ns + "definition"):
#    for indicatoritem in indicator.iter(ns + "Indicator"):
#        a = 0

xzy = 0
'''

import xml.dom.minidom as dom
import os
import re

targets = open("/Users/shaneking/Desktop/targeted.txt", 'r').readlines()


def main():
    ioc_path = "/Users/shaneking/cirt/iocs"
    write_path = "/Users/shaneking/Desktop/new-iocs"

    for root, dirs, files in os.walk(ioc_path):
        for name in files:
            breakout = 0
            ioc_file = os.path.join(root, name)

            #if ioc_file.endswith('.ioc'):
            if ioc_file == "/Users/shaneking/cirt/iocs/1882ac07-a326-4cf6-b602-9b287604feff.ioc":
            #if ioc_file == "/Users/shaneking/cirt/iocs/00bf1366-e709-4a92-b9cc-7fe8967480df.ioc":
                found = 0
                removed = 0
                tree = dom.parse(ioc_file)
                for indicator in tree.getElementsByTagName("Indicator"):
                    if breakout == 1:
                        continue
                    parent = indicator
                    if indicator.attributes._attrs["operator"].value == "OR":
                        for indicatoritem in indicator.getElementsByTagName("IndicatorItem"):
                            if indicatoritem.parentNode != parent:
                                continue
                            if indicatoritem.getElementsByTagName("Context")[0]._attrs["search"].value == "PortItem/remoteIP" \
                                    or indicatoritem.getElementsByTagName("Context")[0]._attrs["search"].value == "Network/DNS":
                                for content in indicatoritem.getElementsByTagName("Content"):
                                    found = 0
                                    for target in targets:
                                        if found == 1:
                                            break
                                        target = re.sub('\n', '', target)
                                        if content.firstChild.data == target:
                                            found = 1
                                    if found == 0:
                                        print "Removing " + content.attributes._attrs["type"].value + ": " + content.firstChild.data
                                        indicator.removeChild(indicatoritem)
                                        found = 1
                                        removed = 1
                    else:
                        breakout = 1
                if removed == 1:
                    f = open(os.path.join(write_path, name), 'w')
                    tree.writexml(f)
                    f.close()

if __name__ == "__main__":
    main()

stop = 0