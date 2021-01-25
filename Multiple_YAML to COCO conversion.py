import os
import sys
from os import system, name
from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2
import json
from collections.abc import Mapping, Sequence
from collections import OrderedDict
import ruamel.yaml
import glob






if __name__ == '__main__':

    #clear_console()
    print('Starting conversion to COCO')


    # Create instance of class ArgumentParser and set help to false (help is added later).
    parser = argparse.ArgumentParser(description='Go over a directory and interactively select images to convert to COCO format.')


    # Create 1 group for required arguments and 1 group for optional arguments
    ##optional_arguments = parser._action_groups.pop() # Edited this line

    required_arguments = parser.add_argument_group('required arguments')
    optional_arguments = parser.add_argument_group('optional arguments')

    required_arguments.add_argument('-s', '--source_path',
                                    metavar='',
                                    help='Path to the root directory where the images are stored.',
                                    dest='source_path',
                                    required=True)
    # required_arguments.add_argument('-i', '--images_path',
    #                                 metavar='',
    #                                 help='Path to the directory where the images are stored.',
    #                                 dest='images_path',
    #                                 required=True)
    args = parser.parse_args()

    args.source_path = os.path.abspath(args.source_path)

    optional_arguments.add_argument('-d', '--coco_save_path',
                                    metavar='',
                                    help='Path to the directory where annotations are stored.',
                                    #default='./coco_annotation',
                                    default = os.path.join(args.source_path,'coco_annotation'),
                                    dest='coco_save_path')
    # Add back help
    ##parser._action_groups.append(optional_arguments) # added this line



    args = parser.parse_args()

    #args.source_path = os.path.abspath(args.source_path)
    #args.images_path = os.path.abspath(args.images_path)
    args.coco_save_path = os.path.abspath(args.coco_save_path)


    if os.path.exists(args.source_path):
        pass
    else:
        print('Source path is not valid, please enter valid source path.')
        raise
    if os.path.exists(os.path.dirname(args.coco_save_path)):
        if os.path.exists(args.coco_save_path):
            print("hey.. i am not here")
            #os.mkdir(args.coco_save_path)
            pass
        else:
            os.mkdir(args.coco_save_path)
            print("hey.. i am here")
    else:
        print('Destination path is not valid, please enter valid destination path.')
        raise

    yaml = ruamel.yaml.YAML(typ='safe')
    ind = dict()
    data = dict(info=ind)


    yaml_file_path = 'annotations/objects/*.yaml'
    #files = glob.glob("C:/path to multiple yaml files for an image/*.yaml")
    files = glob.glob(os.path.join(args.source_path,yaml_file_path))
    #print(files)
    file1 = os.path.join(args.source_path,'data.yaml')
    #print(file1)
    dataa = []
    def read_yaml_file(filename):
        with open(filename, 'r') as stream:
            try:
                print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    s1=[]
    json_dict = {"info":[],"licenses":[],"images":[],"categories":[],"annotations":[]}
    categories = {"id": 1, "name": "item", "supercategory": ""}
    #da1 = yaml.load(open(file1))
#with open("C:/path to common data file/data.yaml", 'r') as stream:
    with open(file1, 'r') as stream:
        datamap = yaml.load(stream)
    image_data=datamap['webotate']
    create_date= image_data['creation_date']
    image_id= datamap['counter']

    # for k in datamap['webotate']:
    #     print(k)
    format=[]
    height=[]
    name=[]
    resources=[]
    time=[]
    width=[]

    for q in datamap['resources']:
        #print(q.values())
        format=q['format']
        height=q['height']
        name=q['name']
        resource=q['resource']
        time=q['time']
        width=q['width']
        img={
                "format": format,
                "image_id":image_id,
                "file_name": name,
                "coco_url": resource,
                "height": height,
                "width": width,
                "date_captured": "2013-11-14 17:02:52",
                "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
                #"id": id,
        }
        print(format)
        print(height)
        break;
    count = 0




    for file in files:
        da = yaml.load_all(open(file))
        for a in da:
            ##print("fuss")
            _id =a['_id']
            for c in a['elements']:
                abc = c['data']
                type = c['type']
                #print(type)
                count = count+1
                sad= [d['x'] for d in abc]
                sad_y= [d['y'] for d in abc]
                sad_min = min(sad)
                sad_max = max(sad)
                sd_y_min = min(sad_y)
                sd_y_max = max(sad_y)
                #print(sad_min)

                s1=[]

                for ce in abc:


                    s1.extend((ce.values()))

                    anna = {

                                "id":count,
                                "image_id": image_id,
                                "category_id": 1,
                                "i_id": _id,
                                "area":"",
                                "bbox":[sad_min,sad_max, sd_y_min, sd_y_max],
                                "segmentation":[s1],
                                "type":type,
                                "iscrowd":0,


                                }



                break;

            json_dict["annotations"].append(anna)



    inf = {

                    "description": "COCO Dataset",
                    "date_created":create_date,



                }

    img={
            "id": image_id,
            "file_name": name,
            "coco_url": resource,
            "height": height,
            "width": width,
            #"height": height,
            #"width": width,
            "date_captured": "2013-11-14 17:02:52",
            "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
            #"id": id,
    }
    json_dict["info"].append(inf)
    json_dict["images"].append(img)
    json_dict["categories"].append(categories)





    json_fp = open(os.path.join(args.coco_save_path,"coco_format.json"), "w")
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
