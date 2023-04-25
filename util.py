import cv2
import numpy as np
#1280 x 720
heightImg = 640
widthImg  = 480


## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver









def adaptiveThreshold(image):
    try:
        imgWarpGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)
        return imgWarpGray, imgAdaptiveThre
    except:
        print("Unable to produce Adaptive Thresold")
        return None,None


def findContours(image , highThresold , lowThresold):

    ## FIND ALL COUNTOURS

    imgContours = image.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = image.copy()
    contours, hierarchy = cv2.findContours(highThresold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS

    # FIND THE BIGGEST COUNTOUR
    biggest, maxArea = biggestContour(contours)  # FIND THE BIGGEST CONTOUR

    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
        imgBigContour = drawRectangle(imgBigContour, biggest, 2)
        pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(image, matrix, (widthImg, heightImg))
        return imgContours,imgBigContour, imgWarpColored
    else:
        print("Unable to get Paper from the given image")
        return None,None,None




def edge_detector(image,kernel):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(gray_img, (5, 5), 1)
    edges = cv2.Canny(imgBlur, 20, 30)
    edges_high_thresh = cv2.Canny(imgBlur, 60, 120)


    edgesDial = cv2.dilate(edges, kernel, iterations=2)  # APPLY DILATION
    edgesimgThreshold = cv2.erode(edgesDial, kernel, iterations=1)  # APPLY EROSION

    edges_highDial = cv2.dilate(edges_high_thresh, kernel, iterations=2)  # APPLY DILATION
    edges_highThreshold = cv2.erode(edges_highDial, kernel, iterations=1)  # APPLY EROSION

    return edges_highThreshold , edgesimgThreshold





def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def drawRectangle(img, biggest, thickness):
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)

    return img


if __name__ == '__main__':

    kernel = np.ones((5, 5))
    image = cv2.imread("img/test.jpg")
    image = cv2.resize(image, (widthImg, heightImg))
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    highThresold , lowThresold = edge_detector(image,kernel)
    imgContours,imgBigContour, imgWarpColored = findContours(image ,highThresold, lowThresold)
    imgWarpGray, imgAdaptiveThre = adaptiveThreshold(imgWarpColored)

    # Image Array for Display
    if imgAdaptiveThre is not None:
        #imageArray = ([image, gray_img, highThresold, imgContours],
                      #imgBigContour, imgWarpColored, imgWarpGray, imgAdaptiveThre])
        imageArray = ([image, gray_img, highThresold, imgContours])

    else:
        #imageArray = ([image, gray_img, highThresold, imgContours],
                     # [imgBlank, imgBlank, imgBlank, imgBlank])

        imageArray = ([image, gray_img, highThresold, imgContours])

    # LABELS FOR DISPLAY
    #lables = [["Original", "Gray", "Threshold", "Contours"],
             # ["Biggest Contour", "Warp Prespective", "Warp Gray", "Adaptive Threshold"]]

    lables = [["Original", "Gray", "Threshold", "Contours"]]

    stackedImage = stackImages(imageArray, 0.75, lables)
    cv2.imshow("Result", stackedImage)
    cv2.waitKey(1)

    # It is for removing/deleting created GUI window from screen
    # and memory
    cv2.destroyAllWindows()



