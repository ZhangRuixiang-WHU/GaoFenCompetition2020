from mmdet.apis import init_detector, inference_detector, show_result_pyplot, save_result_pyplot
import cv2
import os 
import gdal
import numpy as np

def read_gaofen(img_file, convert=None):
    # r,g,b
    '''
    if imgFormat == "png" or imgFormat=="jpg":
        img_bgr = cv2.imread(img_file)
        [img_b, img_g, img_r] = cv2.split(img_bgr)
        img_rgb = cv2.merge([img_r, img_g, img_b])
        img_bgr = cv2.merge([img_b, img_g, img_r])
    elif imgFormat == "tif" or imgFormat=="tiff":
    '''
    if img_file is not None:
        data = gdal.Open(img_file)
        #print("finished gdal.Open")
        width = data.RasterXSize
        height = data.RasterYSize

        if data.RasterCount==4:
            #4bands b,g,r,Nr]
            band1 = data.GetRasterBand(3)
            img_r = band1.ReadAsArray(0,0,width,height)
            img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
            img_r = np.round(img_r*255)
            img_r = np.uint8(img_r)

            band2 = data.GetRasterBand(2)
            img_g = band2.ReadAsArray(0,0,width,height)
            img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
            img_g = np.round(img_g*255)
            img_g = np.uint8(img_g)

            band3 = data.GetRasterBand(1)
            img_b = band3.ReadAsArray(0,0,width,height)
            img_b = (img_b-img_b.min())/(img_b.max()-img_b.min())
            img_b = np.round(img_b*255)
            img_b = np.uint8(img_b)
            img_rgb = cv2.merge([img_r, img_g, img_b])
            img_bgr = cv2.merge([img_b, img_g, img_r])

        elif data.RasterCount==3:
            #
            band1 = data.GetRasterBand(1)
            img_r = band1.ReadAsArray(0,0,width,height)
            img_r = (img_r-img_r.min())/(img_r.max()-img_r.min())
            img_r = np.round(img_r*255)
            img_r = np.uint8(img_r)

            band2 = data.GetRasterBand(2)
            img_g = band2.ReadAsArray(0,0,width,height)
            img_g = (img_g-img_g.min())/(img_g.max()-img_g.min())
            img_g = np.round(img_g*255)
            img_g = np.uint8(img_g)

            band3 = data.GetRasterBand(3)
            img_b = band3.ReadAsArray(0,0,width,height)
            img_b = (img_b-img_b.min())/(img_b.max()-img_b.min())
            img_b = np.round(img_b*255)
            img_b = np.uint8(img_b)
            img_rgb = cv2.merge([img_r, img_g, img_b])
            img_bgr = cv2.merge([img_b, img_g, img_r])

        elif data.RasterCount == 1:
            band1 = data.GetRasterBand(1)
            img_arr = band1.ReadAsArray(0,0,width,height)
            if convert:
                img_mean = img_arr.mean()
                img_sigm = np.sqrt(img_arr.var())
                img_arr[img_arr[:]>img_mean+3*img_sigm]=img_mean+3*img_sigm

            img_arr = (img_arr-img_arr.min())/(img_arr.max()-img_arr.min())
            
            img_arr = np.uint8(np.round(img_arr*255))

            img_rgb = cv2.merge([img_arr,img_arr,img_arr])
            img_bgr = cv2.merge([img_arr,img_arr,img_arr])
    else:
        #raise TypeError("Please input correct image format: png, jpg, tif/tiff!")
        img_rgb = None
        img_bgr = None
    return img_rgb, img_bgr


def write_xml(results, save_path, filename, score = 0.3):

    row, col = results.shape

    xml_file = open((save_path + '/' + filename + '.xml'), 'w')
    # xml_file.write('<?xml version=' + '\"1.0\"' + ' encoding='+ 'utf-8' + '?>\n')
    xml_file.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n')
    xml_file.write('<annotation>\n')
    xml_file.write('	<source>\n')
    xml_file.write('		<filename>' + str(filename) + '.tiff' + '</filename>\n')
    xml_file.write('		<origin>'+ 'GF2/GF3' + '</origin>\n')
    xml_file.write('	</source>\n')
    xml_file.write('	<research>\n')
    xml_file.write('		<version>'+ '4.0' + '</version>\n')
    xml_file.write('		<provider>'+ 'WHU' + '</provider>\n')
    xml_file.write('		<author>'+ 'Captain_VIPG_Ship' + '</author>\n')
    xml_file.write('		<pluginname>'+ 'Ship Detection in SAR Images' + '</pluginname>\n')
    xml_file.write('		<pluginclass>'+ 'Detection' + '</pluginclass>\n')
    xml_file.write('		<time>'+ '2020-07-2020-11' + '</time>\n')
    xml_file.write('	</research>\n')
    xml_file.write('	<objects>\n')

    TT = 0
    # write the region of image on xml file
    for idx in range(row):
        label = results[idx,:].tolist()
        if label[4] >= score:
            TT += 1
            xmin = label[0]
            xmax = label[2]
            ymin = label[1]
            ymax = label[3]
            xml_file.write('    	<object>\n')
            xml_file.write('        	<coordinate>pixel</coordinate>\n')
            xml_file.write('			<type>rectangle</type>\n')
            xml_file.write('			<description>None</description>\n')
            xml_file.write('			<possibleresult>\n')
            xml_file.write('				<name>ship</name>\n')
            xml_file.write('				<probability>' + str(label[4]) + '</probability>\n')
            xml_file.write('			</possibleresult>\n')
            xml_file.write('			<points>\n')
            xml_file.write('				<point>' + str(xmin) + ', ' + str(ymin) + '</point>\n')
            xml_file.write('				<point>' + str(xmin) + ', ' + str(ymax) + '</point>\n')
            xml_file.write('				<point>' + str(xmax) + ', ' + str(ymax) + '</point>\n')
            xml_file.write('				<point>' + str(xmax) + ', ' + str(ymin) + '</point>\n')
            xml_file.write('				<point>' + str(xmin) + ', ' + str(ymin) + '</point>\n')
            xml_file.write('			</points>\n')
            xml_file.write('    	</object>\n')
        else:
            pass
    xml_file.write('	</objects>\n')
    xml_file.write('</annotation>')

    return TT




config_file = '/home/zhangrx/objectdetection/mmlab_RS/mmdetection/mySARcascadeX/cascade_rcnn_x101_32x4d_fpn_1x_coco.py'
checkpoint_file = '/home/zhangrx/objectdetection/mmlab_RS/mmdetection/work_dirs/cascade_rcnn_x101_32x4d_fpn_1x_SARship/epoch_9.pth'
# checkpoint_file = '/home/zhangrx/objectdetection/mmlab_RS/mmdetection/work_dirs/cascade_rcnn_x101_32x4d_fpn_1x_SARship/epoch_9.pth'
# '/home/zhangrx/objectdetection/mmlab_RS/mmdetection/work_dirs/cascade_rcnn_x101_32x4d_optpre_allsar/epoch_21.pth'
# /home/zhangrx/objectdetection/mmlab_RS/mmdetection/work_dirs/cascade_rcnn_x101_32x4d_fpn_1x_SARship/epoch_9.pth
 

model = init_detector(config_file, checkpoint_file)
 
'''
val_path = "/data/zrx/SAR_ship/data/val-jpg/"
res_path = "/data/zrx/SAR_ship/data/val-res-faster/"
resxml_path = "/data/zrx/SAR_ship/data/val-resxml-cascadeX-epoch9-nms0.3/"
'''

val_path = "/data/zrx/SAR_ship/data/newimage/"
res_path = "/data/zrx/SAR_ship/data/val-res-faster/"
resxml_path = "/data/zrx/SAR_ship/data/train-resxml-cascadeX-epoch9-nms0.3/"

try:
    os.mkdir(res_path)
except:
    pass
try:
    os.mkdir(resxml_path)
except:
    pass

imgs = os.listdir(val_path)

ST = 0
for i, img_name in enumerate(imgs):
    filename = img_name.split('.png')[0]# .jpg for val
    img_path = os.path.join(val_path, img_name)
    det_result = inference_detector(model, img_path)
    results_ship = det_result[0]
    TT = write_xml(results_ship, resxml_path,filename)
    print(i)
    ST=ST+TT
print(ST)

    # save the detection results with images
'''
img_rgb, img_bgr = read_gaofen(img_path, True)
img_res = save_result_pyplot(model,img_path,result)
save_path = os.path.join(res_path, img_name)
cv2.imwrite(save_path,img_res)
print(i)
'''



# imgpath = '/data/zrx/SAR_ship/alldata/coco/val2017/12.jpg'
# img_rgb, img_bgr = read_gaofen(imgpath,True)
# result = inference_detector(model, img_rgb)
# print(result[0])
# show_result_pyplot(model,img,result)

# img_bgr = save_result_pyplot(model,img,result)
# cv2.imwrite('./res12.jpg',img_bgr)

 

# imgs = ['test1.jpg', 'test2.jpg']
# for i, result in enumerate(inference_detector(model, imgs, device='cuda:0')):
#     show_result(imgs[i], result, model.CLASSES, out_file='result_{}.jpg'.format(i))
