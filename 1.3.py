import numpy as np
import cv2
import cv2.aruco as aruco
import scipy.io
import imutils


#path_to_image=cv2.imread('S:\circles.jpg')
image1=cv2.imread('G:pics\Image2.jpg')
def aruco_detect():
    
    
    #rgb = image1[...,::-1]
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

    #lower_green1 = np.array([56,0,0])
    #lower_green2 = np.array([86,255,255])
    #upper_green1 = np.array([87,0,0])
    #upper_green2 = np.array([90,255,255])

    
    
    #mask1 = cv2.inRange(hsv, lower_green1, lower_green1)
    #mask2 = cv2.inRange(hsv, upper_green1, upper_green2)
    mask1 = cv2.inRange(hsv, (40, 100, 100), (72, 255,255))
   
    
    res1 = cv2.bitwise_and(image1,image1, mask= mask1)
    #res2 = cv2.bitwise_and(image1,image1, mask= mask2)


    
    #dest1=cv2.add(res1,res2)
    #cv2.imshow("res",dest3)

    #d1=cv2.add(mask1,mask2)
    cv2.imshow("mask",mask1)
    
    

    
    
    edges = cv2.Canny(mask1,150,250,apertureSize=3)
    image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    
    cnt1=contours[0]
    MC=cv2.moments(cnt1)
    cx1=int(MC['m10']/MC['m00'])
    cy1=int(MC['m01']/MC['m00'])
    shape_detect(cnt1,cx1,cy1)
    c1=repr(cx1)
    c2=repr(cy1)
    c9=" , "
    
            
    im2 = cv2.drawContours(image1, contours, -1, (0,0,255), 25)
    cv2.circle(image1, (cx1, cy1), 4, (0, 0, 0), -1)
    cv2.putText(image1,c1+c9+c2, (cx1-40,cy1+30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    #im2 = cv2.drawContours(image1, contours, 2, (0,255,0), 25)
    #cv2.circle(image1, (cx2, cy2), 4, (0, 0, 0), -1)
    #cv2.putText(image1,c3+c9+c4, (cx2-50,cy2+40),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    aruco_detect1()
    #cv2.imshow("canny",im2)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()







    
   
        

   

    
def aruco_detect1():
    
    aruco_list = {}
    rgb = image1[...,::-1]
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    
    
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)#aruco.Dictionary_get(aruco.DICT_4X4_50)   #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
    print(aruco_dict)
    parameters = aruco.DetectorParameters_create()  #refer opencv page for clarification
        #lists of ids and the corners beloning to each id
    print(parameters)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
        #corners is the list of corners(numpy array) of the detected markers. For each marker, its four corners are returned in their original order (which is clockwise starting with top left). So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
    #print len(corners), corners, ids
    print(corners)
    print(len(corners))
    gray = aruco.drawDetectedMarkers(gray, corners,ids)
    cv2.imshow('frame',gray)
    print (type(corners[0]))
    if len(corners):    #returns no of arucos
        print (len(corners))
        print (len(ids))
        for k in range(len(corners)):
            temp_1 = corners[k]
            temp_1 = temp_1[0]
            temp_2 = ids[k]
            temp_2 = temp_2[0]
            aruco_list[temp_2] = temp_1
        return aruco_list
  
        
   


    
   
    
    img = cv2.imread(path_to_image)     #give the name of the image with the complete path
    id_aruco_trace = 0
    det_aruco_list = {}
    img2 = img[0:x,0:y,:]   #separate out the Aruco image from the whole image
    det_aruco_list = detect_Aruco(img2)
    if det_aruco_list:
        img3 = mark_Aruco(img2,det_aruco_list)
        id_aruco_trace = calculate_Robot_State(img3,det_aruco_list)
        print(id_aruco_trace)        
        cv2.imshow('image',img2)
        cv2.waitKey(0)
        
     
        
        
        
    cv2.destroyAllWindows()


def mark_Aruco(img, aruco_list):    #function to mark the centre and display the id
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry is a numpy array with shape (4,2)
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#so being numpy array, addition is not list addition
        centre[:] = [int(x / 4) for x in centre]    #finding the centre
        print (centre)
        orient_centre = centre + [0.0,5.0]
        print (orient_centre)
        centre = tuple(centre)  
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        print (centre)
        print (orient_centre)
        cv2.circle(img,centre,1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
        cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
        cv2.circle(img,orient_centre,1,(0,0,255),8)
        cv2.line(img,centre,orient_centre,(255,0,0),4) #marking the centre of aruco
        cv2.putText(img, str(key), (int(centre[0] + 20), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA) # displaying the idno
    return img
    






def shape_detect(c ,xc,yc):
    shape="unidentified"
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.04*peri,True)
    if len(approx) == 3:
        shape="triangle"
        cv2.putText(image1,shape, (xc-40,yc-20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    elif len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        ar=w/float(h)
        if ar >= 0.95 and ar <=1.05:
            shape="square"
            cv2.putText(image1,shape, (xc-40,yc-20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        else:
            shape="rectangle"
            cv2.putText(image1,shape, (xc-40,yc-20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    elif len(approx) == 5:
        shape="pentagon"
    else:
        shape="circle"
        cv2.putText(image1,shape, (xc-30,yc-20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    return shape
 

    
    

def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
    angle_list_1 = list(range(359,0,-1))
    angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]
    angle=int(math.degrees(math.atan2(y,x))) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    return int(angle)  
   
   

  
   
   
  
if __name__=='__main__':   
    aruco_detect()
    aruco_detect1()
   




    
    
        
    

