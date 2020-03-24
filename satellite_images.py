import sys
import requests
from IPython.core.display import HTML 
from IPython.core.display import Image, display
import os
import webbrowser
import tarfile
import re
import rasterio
from rasterio.mask import mask
import geopandas as gp
import numpy as np
import shapely
from shapely import geometry
from shapely.geometry import shape, Point, LineString, Polygon , mapping
import matplotlib.pyplot as plt
from rasterio.plot import show
import pyproj
from pyproj import CRS
import fiona
import os 
import re
from rasterio.plot import adjust_band
from rasterio.plot import reshape_as_raster, reshape_as_image
import matplotlib.pyplot as plt
from pyproj import transform
from pyproj import Proj
import ast
import pandas as pd
from IPython.display import Audio, display
from timeit import default_timer as timer

def find_images_sentinel(coords,sensing_date_FROM,sensing_date_TO,filename, sentinel=2) :
    global USERNAME
    global PASSWORD
    command = "dhusget.sh -u "+USERNAME+" -p "+PASSWORD +" -S "+sensing_date_FROM+" -E "+sensing_date_TO +" -c "+coords
    if sentinel !=0 :
        command = command + " -m Sentinel-"+ str(sentinel)
    command = command + " -q " + filename +  ".xml -C " + filename + ".csv"
    os.system(command)

def show_img_from_url(url) :
	display(Image(url, width=700, unconfined=True))

def download_landsat_img(index,img_data):
	metadataUrl = img_data["metadataUrl"]
	splitted = metadataUrl.split('/')
	idimg = splitted[len(splitted)-3]
	fullid = splitted[len(splitted)-2]
	download_tifs_url = 'https://earthexplorer.usgs.gov/download/' + idimg + '/' + fullid + '/STANDARD/INVSVC'
	

	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
	webbrowser.get(chrome_path).open(download_tifs_url)
def unzipping_landsatfiles(path):
	indexs = os.listdir(path) 
	print ( indexs)  # indexes of fires of images founded
	for index in indexs :
	    path_with_index = path+ index
	    images_ids = os.listdir(path_with_index) # images founded for index choosen
	    for file in images_ids : 
	        path_with_img_id = path_with_index + "/" + file
	        file_id = file[:-7]
	        if ( tarfile.is_tarfile(path_with_img_id) and os.stat(path_with_img_id).st_size >0  ) :
	            with tarfile.open(path_with_img_id,"r") as tar_ref:
	                names = tar_ref.getmembers()
	                regexp = re.compile(r'^\w+_B[1234].TIF')
	                img_data = []
	                for f in names :
	                    if  regexp.search(f.name) :
	                        img_data.append(f)
	                print(len(img_data))
	                outputpath= path_with_index + "/" + file_id
	                tar_ref.extractall(  members =  img_data ,path = outputpath )
	        os.remove(path_with_img_id)


def color_stretch(image, index):
    colors = image[:, :, index].astype(np.float64)
    for b in range(colors.shape[2]):
        colors[:, :, b] = rasterio.plot.adjust_band(colors[:, :, b])
    return colors

def image_true_color_landsat(index, img_data_id, images_path ,x1=0,y1=0,radius=1000) :
    # path to jp2 files
    path = images_path + index + '/' + img_data_id
    regexp = re.compile(r'_B[1234]')
    sentinal_band_paths = [os.path.join(path, f) for f in os.listdir(path) if regexp.search(f) ]
    sentinal_band_paths.sort()
    for i in sentinal_band_paths : 
        print(i)
        src = rasterio.open(i)
        meta = src.meta


    img_fp = path + '/bands_img_data_' + index + '_' + img_data_id +  '.tif'

    if ( not os.path.isfile(img_fp) ):
        # Read metadata of first file and assume all other bands are the same
        with rasterio.open(sentinal_band_paths[0]) as src0:
            meta = src0.meta

        # Update metadata to reflect the number of layers
        meta.update(count = len(sentinal_band_paths))

        # Read each layer and write it to stack
        with rasterio.open(img_fp, 'w', **meta) as dst:
            for id, layer in enumerate(sentinal_band_paths, start=1):
                with rasterio.open(layer) as src1:
                    dst.write_band(id, src1.read(1))
                    
    full_dataset = rasterio.open(img_fp)
    img_rows, img_cols = full_dataset.shape
    img_bands = full_dataset.count
    with rasterio.open(img_fp) as src:
        img = src.read()[:,  :  ,   :  ]
        meta = src.meta
        print("META: " + str(meta))
        
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init= full_dataset.crs  )
    x2,y2 = transform(inProj,outProj,x1,y1)
    a = full_dataset.transform

    # x, y to col, row
    col, row = ~a * ( x2 , y2 )
    
    xlimit = meta["width"]
    ylimit = meta["height"]

    xmin = int( col - radius ) 
    xmax = int( col + radius ) 
    ymin = int( row - radius ) 
    ymax = int( row + radius ) 

    if (x1==0 and y1==0):
        xmin = 0
        xmax = xlimit
        ymin = 0
        ymax = ylimit
    
    if (xmin < 0) :
        xmin = 0
    if (ymin < 0) :
        ymin = 0
    if (xmax > xlimit) :
        xmax = xlimit
    if (ymax > ylimit) :
        ymax = ylimit

    if (xmax < 0) :
        xmax = radius
    if (ymax < 0) :
        ymax = radius
    if (xmin > xlimit) :
        xmin = xlimit
    if (ymin > ylimit) :
        ymin = ylimit

    print ( xmin , xmax ,  ymin , ymax )
    img_train = img[:, xmin : xmax ,  ymin : ymax ]

    #show(img_train[[2,1,0], :, :])
    reshaped_img_train = reshape_as_image(img_train)
    fig, axs = plt.subplots(1,figsize=(18,18))
    img_stretched_train = color_stretch(reshaped_img_train, [2,1,0])
    axs.imshow(img_stretched_train)
    plt.show()