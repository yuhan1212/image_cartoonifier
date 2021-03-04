'''
Image Cartoonifier
Using Tkinter and OpenCV to build a Cartoonifier
that can transform image into cartoon style.
'''

''' import requred modules'''
import cv2           #for image processing
import numpy as np   #to store image and deal with numbers (image taken as arrays)
import imageio       #to read image stored at particular path
import sys
import matplotlib.pyplot as plt  # visualization and plotting
import os                        # read the path and save images to that path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image


''' main window '''
window = tk.Tk()
window.geometry('400x300')
window.title('Image Cartoonifier')
window.configure(background='#FFF5D6')
label=Label(window, background='#DB93A0', font=('Ayuthaya',25,'bold'))
is_save_button = False
resize_cartoon = None
image_path = None

''' fileopenbox opens the box to choose file and help us store file path as string '''
def upload():
    global image_path
    image_path = filedialog.askopenfilename()
    window.update()
    cartoonify(image_path)
    

def cartoonify(image_path):
    global is_save_button, resize_cartoon
    # read the image
    original_image = cv2.imread(image_path)
    # confirm that image is chosen
    if original_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    ''' resize_original '''
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # print(original_image)          # image is stored in form of numbers
    (width, height, channel) = original_image.shape
    # print(WIDTH, HEIGHT, CHANNEL)  # image size can be obtained as a tuple
    WIDTH: int = 960
    HEIGHT: int = int(960 / width * height)
    resize_original = cv2.resize(original_image, (HEIGHT, WIDTH))
    # plt.imshow(resize_original, cmap='gray')
    ''' resize_gray '''
    # converting an image to grayscale
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    resize_gray = cv2.resize(gray_scale_image, (HEIGHT, WIDTH))
    # plt.imshow(resize_gray, cmap='gray')
    ''' resize_smooth_gray '''
    # applying median blur to smoothen an image
    smooth_gray_scale = cv2.GaussianBlur(gray_scale_image,(5,5),0)
    resize_smooth_gray = cv2.resize(smooth_gray_scale, (HEIGHT, WIDTH))
    # plt.imshow(resize_smooth_gray, cmap='gray')
    ''' resize_edge '''
    # retrieving the edges for cartoon effect by using thresholding technique
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
                                     cv2.THRESH_BINARY, 11, 11)
    resize_edge = cv2.resize(get_edge, (HEIGHT, WIDTH))
    # plt.imshow(resize_edge, cmap='gray')
    ''' resize_color '''
    #applying bilateral filter to remove noise and keep edge sharp as required
    color_image = cv2.bilateralFilter(original_image, d=9, sigmaColor=9, sigmaSpace=7)
    resize_color = cv2.resize(color_image, (HEIGHT, WIDTH))
    # plt.imshow(resize_color, cmap='gray')
    ''' resize_cartoon '''
    # masking edged image with our "BEAUTIFY" image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    resize_cartoon = cv2.resize(cartoon_image, (HEIGHT, WIDTH))
    # plt.imshow(resize_cartoon, cmap='gray')
    ''' put 6 images together '''
    # Plotting the whole transition
    print('create im')
    images=[resize_original, resize_gray, resize_smooth_gray,\
            resize_edge, resize_color, resize_cartoon]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]},\
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    print('front')
    if not is_save_button:
        save_button()
        is_save_button = True
    print(save_button)
    print('end')
    plt.show()