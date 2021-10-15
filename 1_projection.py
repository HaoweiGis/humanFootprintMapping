
import os.path as osp
import os
import subprocess
import numpy as np
from numpy.core.fromnumeric import shape

from osgeo import gdal,ogr,osr
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert shp to semantic segmentation datasets')
    parser.add_argument('--targetimg', default=r'D:\2_HaoweiPapers\7_MappingHumanFootprint\1_Mappinghumanfootprint\2_output\HFP2009_origin.tif' ,help='raster data path' )
    parser.add_argument('--imagedir', default=r'D:\2_HaoweiPapers\7_MappingHumanFootprint\1_Mappinghumanfootprint\2_output\HumanfootprintDatasets\2_ArcGIS_merge\hfp2014' ,help='raster data path' )
    parser.add_argument('--outdir', default=r'D:\2_HaoweiPapers\7_MappingHumanFootprint\1_Mappinghumanfootprint\4_product' ,help='raster data path' )
    args = parser.parse_args()
    return args

def reSamplebyimg(intimg,targetimg,outimg,pixsize=1000):
    '''
    employ gdal_translate is not resample,therefore crs is consistent
    '''
    data = gdal.Open(targetimg)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    cmd1 = ['gdalwarp', "-tr", str(pixsize), str(pixsize), "-te" ,str(minx),str(miny), str(maxx), str(maxy), intimg, outimg]
    print(' '.join(cmd1))
    subprocess.call(cmd1)
    print(outimg + " reSamplebyimg is finally!"+'\n')
# reSamplebyimg(intimg,targetimg,outimg)


if __name__ == "__main__":
    args = parse_args()
    intdir = args.imagedir
    outdir = args.outdir
    targetimg = args.targetimg
    for i in range(2017,2018):

        intimg = osp.join(intdir.replace('2014',str(i)),'hfp'+ str(i) + '_merge.tif')
        outfile = osp.join(outdir,'hfp'+ str(i) + '.tif')
        reSamplebyimg(intimg,targetimg,outfile)
