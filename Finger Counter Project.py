from ast import And
import cv2 as cv
import time 
import os 
import HandTrackingModule as htm


get = cv.VideoCapture(0)
wCam , hCam = 640, 480
pTime = 0
get.set(3, wCam)
get.set(4, hCam)


FolderPath = 'Fingers'
imgs = os.listdir(FolderPath) # We can print a list of names of all the files present in the specified path.
print(imgs)
overlaylist = []
for path in imgs:
    image = cv.imread(f'{FolderPath}/{path}')
    
    overlaylist.append(image)# The direction path was created
    
    print(path)
    
  
   
# print(overlaylist)
# print(len(overlaylist))
# print(overlaylist[0])

hDetector = htm.handDetector(detectionCon= 0.75) # Detection confidence was increased to prevent fails. 


finger = [4,8,12,16,20]
result = cv.VideoWriter('Finger Counter.mp4',cv.VideoWriter_fourcc(*'mp4V'),10,(wCam,hCam)) # The format is defined 

while True:
    
    
    
    success, img = get.read()
    
    
    
    
    # print(got.shape) # The shape of the picture was appeared.
    
    img=hDetector.findHands(img)
    lmList = hDetector.findPositon(img,draw = False)
    # print(lmList)
    
    if len(lmList) != 0:
        indexs = []
        # For thumbs
        if lmList[finger[0]][1]>lmList[finger[0]-1][1]:
            indexs.append(1)
            # print('index is open')
        else:
            indexs.append(0)
            # print('index is close')
            
        # Another fingers
        for id in range(1,5):
            
            if lmList[finger[id]][2]<lmList[finger[id]-2][2]:
                # print('index is open')
                indexs.append(1)
            else:
                # print('index is close')
                indexs.append(0)
        # print(indexs)
        
        total = indexs.count(1)
        
        print(total)
    
        
        got = cv.resize(overlaylist[total-1],(200,200),3)  # The picture was resized, because it was used smaller than normal.  
        h,w,c = got.shape
        img[0:h,0:w] = got # The picture was resized and put on the IMG corner.
        
        cv.rectangle(img,(20,220),(170,425),(255,0,0),cv.FILLED)
        cv.putText(img,str(total),(45,375),cv.FONT_HERSHEY_PLAIN,10,(0,255,0),25)
        
        # cv.imshow('image',got)    # This display is incorrect. 
                
            
    
    
    # h,w,c=overlaylist[0].shape
    # print(h,w,c)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv.putText(img,f'Fps:{int(fps)}',(480,60),4,cv.FONT_HERSHEY_PLAIN,(255,0,0),2)    
    
    if success == True: 
        
    
        result.write(img) # The video is saved
        
        cv.imshow('image',img)
        if cv.waitKey(20) & 0xFF == ord('a'):
            break
    
 
cv.destroyAllWindows()