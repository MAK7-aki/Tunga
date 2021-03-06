import cv2
from imutils.video import VideoStream

def show_webcam(mirror=False):
    scale=50

    cam = VideoStream(src="rtsp://admin:tunga@2020@10.223.45.100 ").start()
    while True:
        image = cam.read()
        if mirror: 
            image = cv2.flip(image, 1)


        #get the webcam size
        height=480
        width = 640

        #prepare the crop
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)

        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY

        cropped = image[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height)) 

        cv2.imshow('my webcam', resized_cropped)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

        #add + or - 5 % to zoom

        if cv2.waitKey(1) == ord('e'): 
            scale += 10  # +5

        if cv2.waitKey(1) == ord('q'): 
            scale -= 10  # +5

    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()