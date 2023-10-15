'''
This basic program allows users to open image, convert it to black and white image, show edges of the image (by using Canny method), detect lines(by HoughlinesP method), circles(by Houghcircles method) and human faces(by Haar Cascade method) in the image using OpenCV. The purpose of this program is to allow the users to test the limits of OpenCV and to find its breaking point easily using the tracebar that can change various parameters.This helps beginner learners of OpenCV to get the idea about the effect of each parameter.

'''

import tkinter as tk
from tkinter import filedialog as fd
import cv2 as cv
import numpy as np

window=tk.Tk()
window.title("Play with OpenCV")
window.geometry('900x700')
window.config(bg='black')

frame_heading=tk.Frame(window,background='#2CE0F9')
label_heading=tk.Label(frame_heading,text='Play with OpenCV',font='roman 25 bold italic',padx=5,pady=5,bg='#1951F0' ,fg='white',borderwidth=5,relief='solid')
label_heading.pack(padx=1,pady=1)
frame_heading.pack(padx=10,pady=10)

frame_info=tk.Frame(window,background='white')
label_info=tk.Label(frame_info,text='This basic program allows you to open image, convert it to black and white image, show edges of the image, detect lines, circles and human faces in the image using OpenCV.\n \n The purpose of this program is to allow the users to test the limits of OpenCV and to find its breaking point easily using the tracebar that can change various parameters.\n This helps beginner learners of OpenCV to get the idea about the effect of each parameter.',font='calibri 12  ',padx=5,pady=5,bg='black' ,fg='white',wraplength=600)
label_info.pack(padx=1,pady=1)
frame_info.pack(padx=10,pady=10)

def select_file():
    filename = fd.askopenfilename(title='Choose image',filetypes=(('image files', '.png'),('image files', '.jpg')))

    img=cv.imread(filename)
    gsimg=cv.imread(filename,cv.IMREAD_GRAYSCALE)
    edgesimg=cv.Canny(gsimg,200,300)

    def func_showimage():
        cv.imshow("Image",img)
        cv.waitKey()
        cv.destroyAllWindows()

    def func_showbwimage():
        cv.imshow("Grayscale image", gsimg) 
        cv.waitKey()
        cv.destroyAllWindows()

    def func_edge_detection():
        def edgedetection(x,y):
            gsimg=cv.imread(filename,cv.IMREAD_GRAYSCALE)
            edgesimg=cv.Canny(gsimg,y,x)
            cv.imshow("Edge detection-Press 'Esc' to exit", edgesimg)

        cv.namedWindow("Edge detection-Press 'Esc' to exit")
        cv.createTrackbar("Upper Threshold", "Edge detection-Press 'Esc' to exit", 50, 150, edgedetection)
        cv.createTrackbar("Lower Threshold", "Edge detection-Press 'Esc' to exit",40, 140, edgedetection)

        while True:
            k = cv.waitKey(1) & 0xFF
            if k == 27:  
                break
            x = cv.getTrackbarPos("Upper Threshold", "Edge detection-Press 'Esc' to exit")
            y = cv.getTrackbarPos("Lower Threshold", "Edge detection-Press 'Esc' to exit")
            edgedetection(x,y)
        cv.destroyAllWindows()
    
    def func_line_detection():
        def linedetection(x,y,z):
            lineimg_cp=img.copy()
            lines=cv.HoughLinesP(edgesimg,1,np.pi/180,x,minLineLength=y,maxLineGap=z) 
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv.line(lineimg_cp, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.imshow("Line detection-Press 'Esc' to exit", lineimg_cp)
            
        cv.namedWindow("Line detection-Press 'Esc' to exit")
        cv.createTrackbar("Threshold", "Line detection-Press 'Esc' to exit", 20, 100, linedetection)
        cv.createTrackbar("Minimum line length", "Line detection-Press 'Esc' to exit", 20, 100, linedetection)
        cv.createTrackbar("Max line gap", "Line detection-Press 'Esc' to exit", 5, 100, linedetection)

        while True:
            k = cv.waitKey(1) & 0xFF
            if k == 27: 
                break
            x = cv.getTrackbarPos("Threshold", "Line detection-Press 'Esc' to exit")
            y = cv.getTrackbarPos("Minimum line length", "Line detection-Press 'Esc' to exit")
            z = cv.getTrackbarPos("Max line gap", "Line detection-Press 'Esc' to exit")
            linedetection(x,y,z)
        cv.destroyAllWindows()

    def func_circle_detection():
        def circledetection(x,y,z):
            circleimg_cp=img.copy()
            blurgsimg=cv.medianBlur(gsimg, 5)
            circles = cv.HoughCircles(blurgsimg,cv.HOUGH_GRADIENT,1,120,param1=x,param2=y,minRadius=z,maxRadius=0)
            circles = np.uint16(np.around(circles))
            for i in circles[0]:
                cv.circle(circleimg_cp,(i[0],i[1]),i[2],(0,0,255),2)
                cv.circle(circleimg_cp,(i[0],i[1]),2,(0,0,255),3)
            cv.imshow("Circle detection-Press 'Esc' to exit", circleimg_cp)
                    

        cv.namedWindow("Circle detection-Press 'Esc' to exit")
        cv.createTrackbar("Parameter 1", "Circle detection-Press 'Esc' to exit", 100, 200, circledetection)
        cv.createTrackbar("Parameter 2", "Circle detection-Press 'Esc' to exit", 80, 200, circledetection)
        cv.createTrackbar("Min radius", "Circle detection-Press 'Esc' to exit", 40, 100, circledetection)

        while True:
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
            x = cv.getTrackbarPos("Parameter 1", "Circle detection-Press 'Esc' to exit")
            y = cv.getTrackbarPos("Parameter 2", "Circle detection-Press 'Esc' to exit")
            z = cv.getTrackbarPos("Min radius", "Circle detection-Press 'Esc' to exit")
            circledetection(x,y,z)
        cv.destroyAllWindows()

    def func_face_detection():
        
        def facedetection(x):
            faceimg_cp=img.copy()
            face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gsimg, 1.08, x)
            for (x, y, w, h) in faces:
                faceimg_cp = cv.rectangle(faceimg_cp, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.imshow("Face detection-Press 'Esc' to exit", faceimg_cp)

        cv.namedWindow("Face detection-Press 'Esc' to exit")
        cv.createTrackbar("Parameter", "Face detection-Press 'Esc' to exit", 50, 150, facedetection)

        while True:
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
            x = cv.getTrackbarPos("Parameter", "Face detection-Press 'Esc' to exit")
            facedetection(x)
        cv.destroyAllWindows()

    frame_main_border=tk.Frame(window,bg='#3DE514')  
    frame_main_border.pack(pady=25)     


    frame_main=tk.Frame(frame_main_border,bg='black')
    frame_main.pack(padx=1,pady=1)


    frame_showimage=tk.Frame(frame_main,background='white')
    button_show_image = tk.Button(frame_showimage,text='Image',command=func_showimage)
    label_showimage=tk.Label(frame_showimage,text='Load the selected image',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_show_image.pack(side=tk.LEFT)
    label_showimage.pack(padx=1,pady=1,side=tk.LEFT)
    frame_showimage.pack(padx=10,pady=10)

    frame_showbwimage=tk.Frame(frame_main,background='white')
    button_show_bwimage = tk.Button(frame_showbwimage,text='Black and White image',command=func_showbwimage)
    label_showbwimage=tk.Label(frame_showbwimage,text='Load the black and white image',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_show_bwimage.pack(side=tk.LEFT)
    label_showbwimage.pack(padx=1,pady=1,side=tk.LEFT)
    frame_showbwimage.pack(padx=10,pady=10)

    frame_edge_detection=tk.Frame(frame_main,background='white')
    button_edge_detection = tk.Button(frame_edge_detection,text='Edge Detection',command=func_edge_detection)
    label_edge_detection=tk.Label(frame_edge_detection,text='Detects edges by Canny method',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_edge_detection.pack(side=tk.LEFT)
    label_edge_detection.pack(padx=1,pady=1,side=tk.LEFT)
    frame_edge_detection.pack(padx=10,pady=10)

    frame_line_detection=tk.Frame(frame_main,background='white')
    button_line_detection = tk.Button(frame_line_detection,text='Lines Detection',command=func_line_detection)
    label_line_detection=tk.Label(frame_line_detection,text='Detects lines by HoughLinesP method',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_line_detection.pack(side=tk.LEFT)
    label_line_detection.pack(padx=1,pady=1,side=tk.LEFT)
    frame_line_detection.pack(padx=10,pady=10)

    frame_circle_detection=tk.Frame(frame_main,background='white')
    button_circle_detection = tk.Button(frame_circle_detection,text='Circles Detection',command=func_circle_detection)
    label_circle_detection=tk.Label(frame_circle_detection,text='Detects Circles by HoughCircles method',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_circle_detection.pack(side=tk.LEFT)
    label_circle_detection.pack(padx=1,pady=1,side=tk.LEFT)
    frame_circle_detection.pack(padx=10,pady=10)

    frame_face_detection=tk.Frame(frame_main,background='white')
    button_face_detection = tk.Button(frame_face_detection,text='Human Face Detection',command=func_face_detection)
    label_face_detection=tk.Label(frame_face_detection,text='Detects faces of humans by Haar Cascade Algorithm',font='calibri 12  ',padx=0,pady=0,bg='black' ,fg='white',borderwidth=5,relief='solid')
    button_face_detection.pack(side=tk.LEFT)
    label_face_detection.pack(padx=1,pady=1,side=tk.LEFT)
    frame_face_detection.pack(padx=10,pady=10)

button_open_image = tk.Button(window,text='Select the image',command=select_file)
button_open_image.pack(pady=10)

window.mainloop()
