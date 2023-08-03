import xml.etree.ElementTree as ET
import os

path_dir = "/Users/feus/new_imi_image/gongju/smb_xml_1/normal/truck"
file_list = os.listdir(path_dir)
count = 0
for file in file_list:
    xml_file = f"{path_dir}/{file}"
    doc = ET.parse(xml_file)
    root = doc.getroot()

    for _ in root.iter("object"):
        count = count + 1

print(count)
