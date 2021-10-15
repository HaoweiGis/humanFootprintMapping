import os.path as osp
import numpy as np

import argparse
from osgeo import gdal,ogr,osr
# from gdalconst import GA_ReadOnly
from scipy.signal.filter_design import band_stop_obj


def GeoImgR(filename):
    dataset = gdal.Open(filename)
    im_porj = dataset.GetProjection()
    im_geotrans = dataset.GetGeoTransform()
    im_data = np.array(dataset.ReadAsArray())
    if len(im_data.shape) == 2:
        im_data = im_data[np.newaxis,:, :]
    del dataset
    return im_data, im_porj, im_geotrans

def GeoImgW(filename,im_data, im_geotrans, im_porj,driver='GTiff'):
    im_shape = im_data.shape
    driver = gdal.GetDriverByName(driver)
    if "int8" in im_data.dtype.name:
        datetype = gdal.GDT_Byte
    elif "int16" in im_data.dtype.name:
        datetype = gdal.GDT_UInt16
    elif "int32" in im_data.dtype.name:
        datetype = gdal.GDT_UInt32
    else :
        datetype = gdal.GDT_Float32
    # driver.Create weight hight
    dataset = driver.Create(filename, im_shape[2], im_shape[1], im_shape[0], datetype)
    dataset.SetGeoTransform(im_geotrans)
    dataset.SetProjection(im_porj)
    for band_num in range(im_shape[0]):
        img = im_data[band_num,:,:]
        band_num = band_num + 1
        dataset.GetRasterBand(band_num).WriteArray(img)
    del dataset

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert shp to semantic segmentation datasets')
    parser.add_argument('--image', default=r'datasets' ,help='raster data path' )
    parser.add_argument('--output', default=r'analysisForhfp', help='output path')
    parser.add_argument('--clipsize', default=512, help='support to byte')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    
    im_data, im_porj, im_geotrans = GeoImgR(r'D:\2_HaoweiPapers\7_MappingHumanFootprint\1_Mappinghumanfootprint\2_output\HFP2013_diff_oneearth.tif')
    im_data = im_data.astype('float')
    im_data[np.where(im_data <-100)] = np.nan
    im_data[np.where(im_data >100)] = np.nan
    wildernessIndex = np.where(im_data <-1)
    intactIndex = np.where((im_data >1)&(im_data <-1))
    modifiedIndex = np.where(im_data >1)

    wildernessArea = wildernessIndex[1].shape[0]
    intactArea = intactIndex[1].shape[0]
    modifiedArea = modifiedIndex[1].shape[0]
    

    line_list = [wildernessArea, intactArea, modifiedArea]

    line = ','.join([str(i) for i in line_list])
    print(line)