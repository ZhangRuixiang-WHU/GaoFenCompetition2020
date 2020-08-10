import os
import numpy as np
import xml.etree.ElementTree as ET
from tqdm import trange

src_label_dir = '/data/zrx/DDRomote/split/trainval/labels/'
label_list = os.listdir(src_label_dir)

dst_label_dir = '/data/zrx/DDRomote/split/trainval/newlabels/'

try:
    os.mkdir(dst_label_dir)
except:
    pass

category_change={
    'harbor': 'harbor',
    'ship': 'ship',
    'small-vehicle': 'small-vehicle',
    'large-vehicle': 'large-vehicle',
    'storage-tank': 'storage-tank',
    'plane': 'plane',
    'soccer-ball-field': 'soccer-ball-field',
    'bridge': 'bridge',
    'baseball-diamond': 'baseball-diamond',
    'tennis-court': 'tennis-court',
    'helicopter': 'helicopter',
    'roundabout': 'roundabout',
    'swimming-pool': 'swimming-pool',
    'ground-track-field': 'ground-track-field',
    'basketball-court': 'basketball-court',
    'airplane': 'plane',
    'airport': 'airport',
    'baseballfield': 'baseball-diamond',
    'basketballcourt': 'basketball-court',
    'chimney': 'chimney',
    'dam': 'dam',
    'Expressway-Service-area': 'Expressway-Service-area',
    'Expressway-toll-station': 'Expressway-toll-station',
    'golffield': 'golffield',
    'groundtrackfield':'ground-track-field',
    'overpass': 'overpass',
    'stadium': 'stadium',
    'storagetank': 'storage-tank',
    'tenniscourt': 'tennis-court',
    'trainstation': 'trainstation',
    'vehicle': 'small-vehicle',
    'windmill': 'windmill'}

for idx in trange(len(label_list)):
    name_xml = label_list[idx]
    filename = name_xml.split('.xml')[0]

    xmlFilePath = os.path.join(src_label_dir,name_xml)
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()

    width = root.find('size').find('width').text
    height = root.find('size').find('height').text

    save_xml_path = os.path.join(dst_label_dir, name_xml)
    xml_file = open(save_xml_path, 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(filename) + '.png' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of image on xml file
    for subobject in root.findall('object'):
        classname = subobject.find('name').text
        newclassname = category_change[classname]

        xmin = subobject.find('bndbox').find('xmin').text
        ymin = subobject.find('bndbox').find('ymin').text
        xmax = subobject.find('bndbox').find('xmax').text
        ymax = subobject.find('bndbox').find('ymax').text

        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + newclassname + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + xmin + '</xmin>\n')
        xml_file.write('            <ymin>' + ymin + '</ymin>\n')
        xml_file.write('            <xmax>' + xmax + '</xmax>\n')
        xml_file.write('            <ymax>' + ymax + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>')
