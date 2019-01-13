#----------------------------------------------------------------------------
# modified from:  http://www.lucaamore.com/?p=638
# license : BSD http://opensource.org/licenses/bsd-license.php
#----------------------------------------------------------------------------

import sys
import cv
import random

min_size = (20,20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING 
pt1 = pt2 = (0,0) 

frame = 15
game_time = 60
health = 10
time = 0
count = 0

img_saw = cv.LoadImage("files/saw.png", cv.CV_LOAD_IMAGE_COLOR) 
rx = img_saw.width/2 
ry = img_saw.height/2 


def game_over(state):
    
    if state == True:
        image_file_name = "files/smiley.jpg"
    else:
        image_file_name = "files/saw.jpg"
        
    image = cv.LoadImage(image_file_name, cv.CV_LOAD_IMAGE_COLOR) 
    cv.ShowImage("Make Your Choice", image)

    while True:
        if cv.WaitKey(0) == 27: # ESC
            break
        
    sys.exit()
    
     
def calculateCircleCenter(point1, point2, x, y):
    
    if x < (point1[0] + point2[0]) / 2:
        x += 3
    elif x > (point1[0] + point2[0]) / 2:
        x -= 3
       
    if y < (point1[1] + point2[1]) / 2:
        y += 3
    elif y > (point1[1] + point2[1]) / 2:
        y -= 3
        
    return x, y
 
 
def DetectFace(image, faceCascade):
    
    global min_size, image_scale, haar_scale, min_neighbors, haar_flags
    global pt1, pt2, rx, ry, count, time, img_saw

    time += 1
    
    if time/frame == game_time:
        game_over(True)

    # Allocate the temporary images
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale),
                                cv.Round(image.height / image_scale)), 8 ,1)
 
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    cv.Resize(grayscale, smallImage, cv.CV_INTER_LINEAR)
    cv.EqualizeHist(smallImage, smallImage)
 
    # Detect the faces
    faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
                                 haar_scale, min_neighbors, haar_flags, min_size )
 
    # If faces are found
    if faces:
        for ((x, y, w, h), n) in faces:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            
            cv.Rectangle(image, pt1, pt2, cv.RGB(0, 0, 255), 5, 8, 0)
            
    # If we caught
    if pt2[0]+img_saw.width/2 > rx > pt1[0]-img_saw.width/2 and pt2[1]+img_saw.height/2 > ry > pt1[1]-img_saw.height/2:
        
        rx = random.randint(img_saw.width, image.width - img_saw.width)
        ry = random.randint(img_saw.height, image.height- img_saw.height)
        
        count += 1 
        if count == health:
            game_over(False)
            
    
    rx, ry = calculateCircleCenter(pt1, pt2, rx, ry)
    #cv.Circle(image, (rx,ry), 10, cv.CV_RGB(255, 0, 0), 3)

    stacked = cv.CreateImage( ( image.width, image.height), image.depth, image.nChannels )
   
    cv.SetImageROI( stacked, ( 0, 0, image.width, image.height ) )
    cv.Copy(image, stacked)
    cv.SetImageROI( stacked, (rx-img_saw.width/2, ry-img_saw.height/2, img_saw.width, img_saw.height) )
    cv.Copy(img_saw, stacked)
    cv.ResetImageROI(stacked)
    
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
    cv.PutText(stacked, "Health: "+str(10 - count), (0, stacked.height - 20), font, cv.CV_RGB(0, 255, 0))
    cv.PutText(stacked, "Time: "+ str(game_time - time/frame), (stacked.width- 150, stacked.height - 20), font, cv.CV_RGB(0, 255, 0))
    
    return stacked


capture = cv.CaptureFromCAM(0)
faceCascade = cv.Load("files/haarcascade_frontalface_alt.xml")
 
while (cv.WaitKey(frame) != 27): # ESC
    
    img = cv.QueryFrame(capture)
    cv.Flip(img, None, 1)
    
    image = DetectFace(img, faceCascade)
    cv.ShowImage("Catch Me If You Can", image)
  
del(capture)
