import json
import os
import cv2
import datetime


def create_image_info(image_id, image_size, file_name, license_id=1,
                    coco_url="", flickr_url="",
                    date_captured=datetime.datetime.utcnow().isoformat(' ')):

    image_info = {
        "id": image_id,
        "width": image_size[0],
        "height": image_size[1],
        "file_name": file_name,
        "license": license_id,
        "coco_url": coco_url,
        "flickr_url": flickr_url,
        "date_captured": date_captured
    }

    return image_info


def create_image_annotation(annotation_id, image_id, category_id, polygon,
                          iscrowd, bbox=[], area=0.0):
    
    annotation = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "segmentation": [polygon],
        "area": area,
        "bbox": bbox,
        "iscrowd": iscrowd
    }
    return annotation


pwd = os.getcwd()
print(pwd)
file = open('./balloon/train/via_region_data.json')
#file = open('./balloon/val/via_region_data.json')
data = json.load(file)
datas = json.loads(json.dumps(data))

INFO = {
    "description": "Example Dataset",
    "url": "https://github.com/matterport/Mask_RCNN/releases",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "matterport",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'ballon',
        'supercategory': 'ballons',
    },
 ]

coco_output = {
    "info": INFO,
    "licenses": LICENSES,
    "categories": CATEGORIES,
    "images": [],
    "annotations": []
    }

img_id = 1
annotation_id = 1

for key in datas:
    img_meta_data = datas[key]
    filename = img_meta_data['filename']
    selfize = img_meta_data['size']
    path = os.path.join(pwd, "balloon/train", filename)
    #path = os.path.join(pwd, "balloon/val", filename)
    img = cv2.imread(path, 0)
    height = img.shape[0]
    width = img.shape[1]
    img_size = [height, width]
    image_info = create_image_info(img_id, img_size, filename)
    coco_output["images"].append(image_info)
    for region in img_meta_data['regions']:
        shapeform = img_meta_data['regions'][region]['shape_attributes']['name']
        if shapeform == "polygon":
            polygon = []
            allxs = img_meta_data['regions'][region]['shape_attributes']['all_points_x']
            allys = img_meta_data['regions'][region]['shape_attributes']['all_points_y']
            for i in range(0,len(allxs)):
                polygon.append(allxs[i])
                polygon.append(allys[i])
        max_x = max(allxs)
        max_y = max(allys)
        min_x = min(allxs)
        min_y = min(allys)
        bbox = [min_x, min_y,max_x - min_x, max_y - min_y]
        area = (max_x - min_x) * (max_y - min_y)
        annotation = create_image_annotation(annotation_id, img_id, 1, polygon, 0, bbox, area)
        coco_output["annotations"].append(annotation)
        annotation_id = annotation_id + 1
        
    img_id = img_id + 1

with open('ballons_coco.json', 'w') as fp:
    json.dump(coco_output, fp)
