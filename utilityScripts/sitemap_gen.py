import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime

from xml.etree import ElementTree
from xml.dom import minidom

from io import BytesIO

#from ElementTree_pretty import prettify
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding='utf8', method='xml')
    
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ")



root = Element('urlset')
root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

url = SubElement(root, 'url')

loc = SubElement(url, 'loc')
loc.text="loc1"

lastmod = SubElement(url, 'lastmod')
lastmod.text="latmod1"

changefreq = SubElement(url, 'changefreq')
changefreq.text="changfred1"

priority = SubElement(url, 'priority')
priority.text="priority1"


url = SubElement(root, 'url')

loc = SubElement(url, 'loc')
loc.text="loc2"

lastmod = SubElement(url, 'lastmod')
lastmod.text="latmod2"

changefreq = SubElement(url, 'changefreq')
changefreq.text="changfred2"

priority = SubElement(url, 'priority')
priority.text="priority2"



print prettify(root)

# create a new XML file with the results

sitemap = open("sitemap.xml", "w")
sitemap.write(prettify(root) )


