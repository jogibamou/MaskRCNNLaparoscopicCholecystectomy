# coding: utf-8
import cv2
import os
import json
file = open('test.json')
data = json.load(file)
new_data = {}
new_data = {"info":{}, "images":[], "annotations":[], "licenses":[]
}
new_data['info']['version'] = "1.0"
new_data['info']['description'] = "yes"
new_data['info']['contributor'] = "Me"
new_data['info']['url'] = "somesite.com"
import time
import datetime
new_data['info']['date_created'] = datetime.date(2019,1,11)
keys = list(data.keys())
    
    
    
id_count = 0
    
    
current_image_id = 0
current_annotation_id = 0    
new_data['images'] = []
new_data['annotations'] = []
for key in keys:
    img = cv2.imread('test/' + key.split('.jpg')[0] + '.jpg')
    height = img.shape[0]
    width = img.shape[1]
    current_id = current_image_id
    file_name = 'test/' + key.split('.jpg')[0]+ '.jpg'
    license = 0
    flickr_url = "yes"
    coco_url = "no"
    date_captured = '2019/01/01'
    new_data['images'].append({"id": current_id, "width": width, "height": height, 
    "file_name": file_name, "license": license, "flickr_url":flickr_url, 
    "coco_url":coco_url, "date_captured":date_captured})
    regions = data[key]['regions']
    region_keys = list(regions.keys())
    for region in region_keys:
        reg = regions[region]
        ant_id = current_annotation_id
        ant_img_id = current_id
        #segmentation = [x,y for x,y in region['shape_attributes']['all_points_x'] and region['shape_attributes']['all_points_y']]
        segmentation = [[]]
        for x,y in zip(reg['shape_attributes']['all_points_x'], reg['shape_attributes']['all_points_y']):
            segmentation[0].append(x)
            segmentation[0].append(y)
        max_x = max(reg['shape_attributes']['all_points_x'])
        max_y = max(reg['shape_attributes']['all_points_y'])
        min_x = min(reg['shape_attributes']['all_points_x'])
        min_y = min(reg['shape_attributes']['all_points_y'])
        area = abs(max_x - min_x * max_y - min_y)
        bbox = [min_x, min_y, max_x - min_x, max_y - min_y]
        iscrowd = 0
        new_data['annotations'].append({"id":ant_id, "image_id":current_image_id,"category_id":0,"segmentation":segmentation, "area":area, "bbox":bbox, "iscrowd":iscrowd})
        current_annotation_id += 1
    current_image_id += 1


    
    

    
    
new_data['categories'] = [{"id":0, "name":"balloon","supercategory":"balloon"}]
    
    
    
new_data['info']
new_data['info']['date_created'] = '2019/01/01'
new_data['licenses'].append({"id":0,"name":"y","url":"u"})

with open('data_test_.json', 'w') as out:
    json.dump(new_data, out)
    
out.close()
