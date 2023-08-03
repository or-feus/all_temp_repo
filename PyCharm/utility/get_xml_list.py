import xml.etree.ElementTree as ET
import os

path_dir = "/Users/feus/new_imi_image/taean/nsw_xml/normal"
dir_list = os.listdir(path_dir)

count = 0
for dir in dir_list:
    # print(f"{path_dir}/{dir}")
    data_dir = f"{path_dir}/{dir}"
    list = os.listdir(data_dir)
    for file in list:

        xml_file = f"{data_dir}/{file}"
        # print(xml_file)

        try:
            doc = ET.parse(xml_file)
            root = doc.getroot()

            for _ in root.iter("object"):
                count = count + 1

        except:
            print(xml_file)
print(count)