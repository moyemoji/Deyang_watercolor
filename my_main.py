#coding:utf-8
#!D:/ProgramFiles/python
from PIL import Image
from my_process import *
import json

global map_gaussDegree
global map_binaryThreshold
global map_borderGrayDegree
global river_gaussDegree
global river_binaryThreshold
global vegetation_gaussDegree
global vegetation_binaryThreshold
global resident_gaussDegree
global resident_binaryThreshold
global road_gaussDegree
global road_binaryThreshold

def setParameter():
    global map_gaussDegree
    global map_binaryThreshold
    global map_borderGrayDegree
    global river_gaussDegree
    global river_binaryThreshold
    global vegetation_gaussDegree
    global vegetation_binaryThreshold
    global resident_gaussDegree
    global resident_binaryThreshold
    global road_gaussDegree
    global road_binaryThreshold
    
    my_parameter = open("my_parameter.json")  
    my_setParameter = json.load(my_parameter)
    
    map_gaussDegree = my_setParameter['map']['map_gaussDegree']
    map_binaryThreshold = my_setParameter['map']['map_binaryThreshold']
    map_borderGrayDegree = my_setParameter['map']['map_borderGrayDegree']
    
    river_gaussDegree = my_setParameter['river']['river_gaussDegree']
    river_binaryThreshold = my_setParameter['river']['river_binaryThreshold']  
    
    vegetation_gaussDegree = my_setParameter['vegetation']['vegetation_gaussDegree']
    vegetation_binaryThreshold = my_setParameter['vegetation']['vegetation_binaryThreshold']
    
    resident_gaussDegree = my_setParameter['resident']['resident_gaussDegree']
    resident_binaryThreshold = my_setParameter['resident']['resident_binaryThreshold']
    
    road_gaussDegree = my_setParameter['road']['road_gaussDegree']
    road_binaryThreshold = my_setParameter['road']['road_binaryThreshold']
    

#主函数，处理入口  
if __name__=="__main__": 
    
    global map_gaussDegree
    global map_binaryThreshold
    global map_borderGrayDegree
    global river_gaussDegree
    global river_binaryThreshold
    global vegetation_gaussDegree
    global vegetation_binaryThreshold
    global resident_gaussDegree
    global resident_binaryThreshold
    global road_gaussDegree
    global road_binaryThreshold
    
    setParameter()
    
    #底图图层
    map_origin=Image.open('./origin/map.png')
    map_gauss=my_gauss(map_origin,map_gaussDegree)
    map_binary=my_binary(map_gauss,map_binaryThreshold)
    map_whiteBorder=my_whiteBorder(map_binary)
    map_grayBorder=my_grayBorder(map_binary,map_borderGrayDegree)
    map_compositeBg=my_compositeBg(map_grayBorder,map_whiteBorder)
    map_texture=Image.open('./texture/map_texture.png')
    map_last=my_compositeBg(map_texture,map_compositeBg)
#    map_last.save("./result/map.png",'png') 
    print("Map background layer was processed!")
    
    #道路图层
    road_origin=Image.open('./origin/road.png')
    road_texture=Image.open('./texture/road_texture.png')
    road_gauss=my_gauss(road_origin,road_gaussDegree)
    road_binary=my_binary(road_gauss,road_binaryThreshold)
    road_object=my_objectTexture(road_binary,road_texture)
#    road_object.save("./result/road.png",'png')
    print("Road layer was processed!")
    
    #河流图层
    river_origin=Image.open('./origin/river.png')
    river_origin=my_deleteRoad(river_origin,road_origin)
    river_texture=Image.open('./texture/river_texture.png')
    
    river_gauss=my_gauss(river_origin,river_gaussDegree)
    river_binary=my_binary(river_gauss,river_binaryThreshold)
    river_grayBorder=my_objectGrayBorder(river_binary)
#    river_grayBorder.save("./result/river_border.png",'png') 
    river_object=my_objectTexture(river_binary,river_texture)
    river_object=my_compositeLast(river_object,river_grayBorder)
#    river_object=my_colorBurn(river_object,river_grayBorder);
#    river_object.save("./result/river.png",'png') 
    print("River layer was processed!")
    

    #植被图层
    vegetation_origin=Image.open('./origin/vegetation.png')
    vegetation_origin=my_deleteRoad(vegetation_origin,road_origin)
    vegetation_texture=Image.open('./texture/vegetation_texture.png')
    vegetation_gauss=my_gauss(vegetation_origin,vegetation_gaussDegree)
    vegetation_binary=my_binary(vegetation_gauss,vegetation_binaryThreshold)
    vegetation_object=my_objectTexture(vegetation_binary,vegetation_texture)
#    vegetation_object.save("./result/vegetation.png",'png')
    print("Vegetation layer was processed!")

    #居民地图层
    resident_origin=Image.open('./origin/resident.png')
    resident_origin=my_deleteRoad(resident_origin,road_origin)
    resident_texture=Image.open('./texture/resident_texture.png')
    resident_gauss=my_gauss(resident_origin,resident_gaussDegree)
    resident_binary=my_binary(resident_gauss,resident_binaryThreshold)
    resident_object=my_objectTexture(resident_binary,resident_texture)
#    resident_object.save("./result/resident.png",'png') 
    print("Resident layer was processed!")
    
    
    
    result=my_compositeLast(map_last,river_object)
    result=my_compositeLast(result,vegetation_object)
    result=my_compositeLast(result,resident_object)
    result=my_compositeLast(result,road_object)
    result.save("./result/result.png",'png')
    print("Check results!")