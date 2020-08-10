import os
import numpy as np
import xml.etree.ElementTree as ET
from tqdm import trange

label_dir = '/data/zrx/DDRomote/split/trainval/labels/'
label_list = os.listdir(label_dir)

all_categories = {}

for idx in trange(len(label_list)):
    name_xml = label_list[idx]
    xmlFilePath = os.path.abspath(label_dir + name_xml)
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()

    for subobject in root.findall('object'):

        category = subobject.find('name').text

        if category in all_categories:
            all_categories[category] += 1
        else:
            all_categories[category] = 1

print(all_categories)



'''

original_dota_class = { 'harbor': 1, 
                        'ship': 2, 
                        'small-vehicle': 3, 
                        'large-vehicle': 4, 
                        'storage-tank': 5, 
                        'plane': 6, 
                        'soccer-ball-field': 7, 
                        'bridge': 8, 
                        'baseball-diamond': 9, 
                        'tennis-court': 10, 
                        'helicopter': 11, 
                        'roundabout': 12, 
                        'swimming-pool': 13, 
                        'ground-track-field': 14, 
                        'basketball-court': 15}


new_class = {
    'harbor',
    'ship',
    'small-vehicle',
    'large-vehicle'
    'storage-tank'
    'plane'
    'soccer-ball-field'
    'bridge'
    'baseball-diamond'
    'tennis-court'
    'helicopter'
    'roundabout'
    'swimming-pool'
    'ground-track-field'
    'basketball-court'
}


original_dior_class = { 'airplane':                     1, ---
                        'airport':                      2, 
                        'baseballfield':                3, ---
                        'basketballcourt':              4, ----
                        'bridge':                       5, ----
                        'chimney':                      6, 
                        'dam':                          7, 
                        'Expressway-Service-area':      8, 
                        'Expressway-toll-station':      9, 
                        'golffield':                    10, 
                        'groundtrackfield':             11, ----
                        'harbor':                       12, ----
                        'overpass':                     13, 
                        'ship':                         14, ----
                        'stadium':                      15, 
                        'storagetank':                  16, ---
                        'tenniscourt':                  17, ---
                        'trainstation':                 18, 
                        'vehicle':                      19, ---
                        'windmill':                     20}


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







'harbor','ship','small-vehicle','storage-tank','basketball-court','tennis-court','baseball-diamond','bridge','plane','overpass','swimming-pool','ground-track-field','dam','large-vehicle','airport','windmill','chimney','roundabout','Expressway-toll-station','Expressway-Service-area','soccer-ball-field','trainstation','golffield','stadium','helicopter'


'''