from ast import And
import cv2 as cv
import time 
import os 
import HandTrackingModule as htm


get = cv.VideoCapture(0)

pTime = 0
get.set(3,640)
get.set(4,480)

hDetector = htm.handDetector(detectionCon= 0.75) # Detection confidence was increased to prevent fails. 

FolderPath = 'Fingers'
imgs = os.listdir(FolderPath) # We can print a list of names of all the files present in the specified path.
print(imgs)
overlaylist = []
for path in imgs:
    overlaylist.append(f'{FolderPath}/{path}')# The direction path was created
    print(path)
    
    
   
# print(overlaylist)
# print(len(overlaylist))
print(overlaylist[0])


finger = [8,12,16,20]

while True:
    
    
    
    success, img = get.read()
    
    
    
    
    # print(got.shape) # The shape of the picture was appeared.
    
    img=hDetector.findHands(img)
    lmList = hDetector.findPositon(img,draw = True)
    # print(lmList)
    
    if len(lmList) != 0:
        indexs = []
        if lmList[4][1]>lmList[3][1]:
            indexs.append(1)
            # print('index is open')
        else:
            indexs.append(0)
            # print('index is close')
        for id in finger:
            
            if lmList[id][2]<lmList[id-2][2]:
                # print('index is open')
                indexs.append(1)
            else:
                # print('index is close')
                indexs.append(0)
        # print(indexs)
        howMany = 0
        for Sum in indexs:
            howMany+=Sum
        print(howMany)
        got = cv.imread(str(overlaylist[howMany-1]))
        got = cv.resize(got,(200,200),3)  # The picture was resized, because it was used smaller than normal.  
        img[0:200,0:200] = got # The picture was resized and put on the IMG corner.
        cv.imshow('image',got) 
            
            
    
    
    # h,w,c=overlaylist[0].shape
    # print(h,w,c)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv.putText(img,f'Fps:{int(fps)}',(480,60),4,cv.FONT_HERSHEY_PLAIN,(255,0,0),2)    
    
    
    
    
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == ord('a'):
        break
    
get.release()    
cv.destroyAllWindows()