#coding:utf-8
#!D:/ProgramFiles/python
from PIL import Image
from numpy import *
from scipy import *
from scipy.ndimage import filters
import matplotlib.pyplot as pyplot


#各个图层数据去除道路
#输入：需要处理的图层（除了背景层和道路层），道路层
#输出：去除了道路的地物图层
def my_deleteRoad(layerWithRoad,layerRoad):
    lwr = layerWithRoad.convert("RGBA");
    lr = layerRoad.convert("RGBA");
    
    bands_lwr=lwr.split();
    lwr_r = bands_lwr[0];
    lwr_g = bands_lwr[1];
    lwr_b = bands_lwr[2];
    lwr_a = bands_lwr[3];
    
    bands_lr=lr.split();
    lr_r = bands_lr[0];
    lr_g = bands_lr[1];
    lr_b = bands_lr[2];
    lr_a = bands_lr[3];
    
    lwr_r = asarray(lwr_r)
    lwr_g = asarray(lwr_g)
    lwr_b = asarray(lwr_b)
    lwr_a = asarray(lwr_a)
    
    lr_r = asarray(lr_r)
    lr_g = asarray(lr_g)
    lr_b = asarray(lr_b)
    lr_a = asarray(lr_a)
    
    lwr_r.flags.writeable = True
    lwr_g.flags.writeable = True
    lwr_b.flags.writeable = True
    lwr_a.flags.writeable = True
    
    for i in range(0,len(lr_r)):
        for j in range(0,len(lr_r[i])):
            if(lr_r[i][j]==255):
                lwr_r[i][j]=0
                lwr_g[i][j]=0
                lwr_b[i][j]=0
                
    new_r = Image.fromarray(lwr_r)
    new_g = Image.fromarray(lwr_g)
    new_b = Image.fromarray(lwr_b)
    new_a = Image.fromarray(lwr_a)
    layerWithoutRoad = Image.merge("RGBA", (new_r,new_g,new_b,new_a))
    
    return layerWithoutRoad
    
    
#第一步：高斯模糊
#输入：RGB模式的图片，如果不是RGB的话转化成RGB模式,convert("RGB")
#输出：RGB模式的png格式图片，输出的图片用于二值化
def my_gauss(img_origin,sigma):
    image_origin = array(img_origin.convert("RGB"))

    image_zeros = zeros([4096,4096,3])
    for i in range(3):
        image_zeros[:,:,i] = filters.gaussian_filter(image_origin[:,:,i],sigma)
    
    image_gauss = uint8(image_zeros)
    image_gauss = Image.fromarray(image_gauss)

    #返回的是三通道的PIL对象
    return image_gauss



#第二步：二值化
#输入：灰度图，如果不是灰度图则转化成灰度图，此处用到的高斯模糊的结果为RGB模式，convert("L")
#输出：单通道，二值化图，用于生成图层的白色部分、白色部分的灰色边缘
def my_binary(img_gauss,threshold):
    image_gauss=img_gauss.convert("L")
    
    #threshold以下的，即偏黑色的均归类为黑色，如果白色区域要偏小，threshold则要偏大
    table = []
    
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
        
    image_binary = image_gauss.point(table,"1")
    
    #返回的是单通道的二值化图
    return image_binary



#第三步（1）：背景层地物白底
#输入：二值化图，单通道需要转化成RGBA模式，convert("RGBA")
#输出：黑色地物变白色，白色区域透明图，RGBA模式，用于图像融合
def my_whiteBorder(img_binary):
    image_binary=img_binary.convert("RGBA")
    
    bands=image_binary.split()
    image_r=bands[0]
    image_g=bands[1]
    image_b=bands[2]
    image_a=bands[3]

    image_r = asarray(image_r)
    image_g = asarray(image_g)
    image_b = asarray(image_b)
    image_a = asarray(image_a)
    
    image_r.flags.writeable = True
    image_g.flags.writeable = True
    image_b.flags.writeable = True
    image_a.flags.writeable = True
    
    for i in range(0,len(image_r)):
        for j in range(0,len(image_r[i])):
            if(image_r[i][j]==255 and image_g[i][j]==255 and image_b[i][j]==255):
                image_a[i][j]=0
            else:
                image_r[i][j]=255
                image_g[i][j]=255
                image_b[i][j]=255
                
    r = Image.fromarray(image_r)
    g = Image.fromarray(image_g)
    b = Image.fromarray(image_b)
    a = Image.fromarray(image_a)
    image_whiteBorder = Image.merge("RGBA", (r,g,b,a))
    
    return image_whiteBorder



#第三步（2）：地物层纹理
#输入：二值化图，转化成RGBA，convert("RGBA")，以图层融合的形式或者赋值的形式修改像素
#输出：地物带纹理，非地物部分透明，等待大融合
def my_objectTexture(img_binary,ob_texture):
    image_binary=img_binary.convert("RGBA")
    object_texture=ob_texture.convert("RGBA")
    
    bands=image_binary.split()
    image_r=bands[0]
    image_g=bands[1]
    image_b=bands[2]
    image_a=bands[3]

    image_r = asarray(image_r)
    image_g = asarray(image_g)
    image_b = asarray(image_b)
    image_a = asarray(image_a)
    
    image_r.flags.writeable = True
    image_g.flags.writeable = True
    image_b.flags.writeable = True
    image_a.flags.writeable = True
    
    for i in range(0,len(image_r)):
        for j in range(0,len(image_r[i])):
            if(image_r[i][j]==255):
                image_a[i][j]=0
    
    r = Image.fromarray(image_r)
    g = Image.fromarray(image_g)
    b = Image.fromarray(image_b)
    a = Image.fromarray(image_a)
    image_object = Image.merge("RGBA", (r,g,b,a))
    
    
    object_composite= Image.alpha_composite(object_texture,image_object);
    
    bands=object_composite.split()
    image_r=bands[0]
    image_g=bands[1]
    image_b=bands[2]
    image_a=bands[3]

    image_r = asarray(image_r)
    image_g = asarray(image_g)
    image_b = asarray(image_b)
    image_a = asarray(image_a)
    
    image_r.flags.writeable = True
    image_g.flags.writeable = True
    image_b.flags.writeable = True
    image_a.flags.writeable = True
    
    for i in range(0,len(image_r)):
        for j in range(0,len(image_r[i])):
            if(image_r[i][j]==0):
                image_a[i][j]=0
    
    r = Image.fromarray(image_r)
    g = Image.fromarray(image_g)
    b = Image.fromarray(image_b)
    a = Image.fromarray(image_a)
    image_object = Image.merge("RGBA", (r,g,b,a))
    
    return image_object



#第四步：背景层白底的灰色边缘
#输入：二值化图，转成RGB模式，高斯模糊和alpha通道赋值
#输出：白色区域透明，黑色区域依旧是黑色，但是黑色边缘像素透明度加大(alpha值变小了)的图
def my_grayBorder(img_binary):
    image_binary=array(img_binary.convert("RGB"))
    
    image_zeros = zeros([4096,4096,3])
    for i in range(3):
        image_zeros[:,:,i] = filters.gaussian_filter(image_binary[:,:,i],5)
    
    image_binary_gauss = uint8(image_zeros)
    image_binary_gauss = Image.fromarray(image_binary_gauss)

    image_binary_gauss=image_binary_gauss.convert("RGBA")
    bands=image_binary_gauss.split()
    
    image_r=bands[0]
    image_g=bands[1]
    image_b=bands[2]
    image_a=bands[3]

    image_r = asarray(image_r)
    image_g = asarray(image_g)
    image_b = asarray(image_b)
    image_a = asarray(image_a)
    
    image_r.flags.writeable = True
    image_g.flags.writeable = True
    image_b.flags.writeable = True
    image_a.flags.writeable = True

#    for i in range(0,len(image_r)):
#        for j in range(0,len(image_r[i])):
#            if(image_r[i][j]>220):
#                image_a[i][j]=0
#            elif(image_r[i][j]<220 and image_r[i][j]>50):
#                image_a[i][j]=image_r[i][j]/2
    
    for i in range(0,len(image_r)):
        for j in range(0,len(image_r[i])):
            if(image_r[i][j]>50):
                image_a[i][j]=255-image_r[i][j]
                image_r[i][j] = image_r[i][j]*0.6+100
                image_g[i][j] = image_g[i][j]*0.6+100
                image_g[i][j] = image_b[i][j]*0.6+100


    r = Image.fromarray(image_r)
    g = Image.fromarray(image_g)
    b = Image.fromarray(image_b)
    a = Image.fromarray(image_a)
    image_grayBorder = Image.merge("RGBA", (r,g,b,a))

    return image_grayBorder



#第五步：背景层的融合
#输入：地物白底（地物区域外透明）、白底的灰色边缘（灰色区域外透明）、切片纹理（整张图，仅用于背景图层）
#输出：背景图层等待后续融合
def my_compositeBg(img_grayBorder,img_whiteBorder):
    image_grayBorder=img_grayBorder.convert("RGBA")
    image_whiteBorder=img_whiteBorder.convert("RGBA")
    image_compositeBg= Image.alpha_composite(image_grayBorder,image_whiteBorder);
    
    return image_compositeBg
    
    
    
#第六步：大融合
#输入：所有图层
#输出：完整切片
def my_compositeLast(img_bottom,img_top):
    image_bottom=img_bottom.convert("RGBA")
    image_top=img_top.convert("RGBA")
    
    result_composite= Image.alpha_composite(image_bottom,image_top);
    return result_composite
 
    
##主函数，处理入口  
#if __name__=="__main__": 
#    #底图图层 threshold 180
#    map_origin=Image.open('./origin/map.png')
#    map_gauss=my_gauss(map_origin,5)
#    map_binary=my_binary(map_gauss,180)
#    map_whiteBorder=my_whiteBorder(map_binary)
#    map_grayBorder=my_grayBorder(map_binary)
#    map_compositeBg=my_compositeBg(map_grayBorder,map_whiteBorder)
#    map_texture=Image.open('./texture/map_texture.png')
#    map_last=my_compositeBg(map_texture,map_compositeBg)
#    map_last.save("./result/map.png",'png') 
#    print("Map background layer was processed!")
#    
#    #道路图层 threshold 100
#    road_origin=Image.open('./origin/road.png')
#    road_texture=Image.open('./texture/road_texture.png')
#    road_gauss=my_gauss(road_origin,5)
#    road_binary=my_binary(road_gauss,100)
#    road_object=my_objectTexture(road_binary,road_texture)
#    road_object.save("./result/road.png",'png')
#    print("Road layer was processed!")
#    
#    #河流图层 threshold 150
#    river_origin=Image.open('./origin/river.png')
#    river_origin=my_deleteRoad(river_origin,road_origin);
#    river_texture=Image.open('./texture/river_texture.png')
#    river_gauss=my_gauss(river_origin,5)
#    river_binary=my_binary(river_gauss,150)
#    river_object=my_objectTexture(river_binary,river_texture)
#    river_object.save("./result/river.png",'png')
#    print("River layer was processed!")
#
#    #植被图层 threshold 150
#    vegetation_origin=Image.open('./origin/vegetation.png')
#    vegetation_origin=my_deleteRoad(vegetation_origin,road_origin);
#    vegetation_texture=Image.open('./texture/vegetation_texture.png')
#    vegetation_gauss=my_gauss(vegetation_origin,5)
#    vegetation_binary=my_binary(vegetation_gauss,150)
#    vegetation_object=my_objectTexture(vegetation_binary,vegetation_texture)
#    vegetation_object.save("./result/vegetation.png",'png') 
#    print("Vegetation layer was processed!")
#
#    #居民地图层 threshold 180
#    resident_origin=Image.open('./origin/resident.png')
#    resident_origin=my_deleteRoad(resident_origin,road_origin);
#    resident_texture=Image.open('./texture/resident_texture.png')
#    resident_gauss=my_gauss(resident_origin,5)
#    resident_binary=my_binary(resident_gauss,180)
#    resident_object=my_objectTexture(resident_binary,resident_texture)
#    resident_object.save("./result/resident.png",'png') 
#    print("Resident layer was processed!")
#    
#    result=my_compositeLast(map_last,river_object)
#    result=my_compositeLast(result,vegetation_object)
#    result=my_compositeLast(result,resident_object)
#    result=my_compositeLast(result,road_object)
#    result.save("./result/result.png",'png')
#    print("Check results!")
    
    
    