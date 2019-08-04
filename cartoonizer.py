"""
This is intermediate file ,it is used in Gui_cartoonizer.py file.
In this file we create a lot of functions to performing required operations
"""

# Import given below lib. into this program.
import cv2

# import numpy as allias name np
import numpy as np


# define a function for reading image 
def readImage(path) :
    
    # Read an image from specified path
    img_bgr = cv2.imread(path)

    # Assigning number of rows, coulmns and
    # Planes to the respective variables 
    row,col,plane = img_bgr.shape

    # return multiple values using list 
    return [img_bgr, row, col]


# Define a function for performing downsampling on the image
# downsampling means to decrease the size of an image
def downsampling(img, x, y, row, col, plane) :

    # Assign Blue plane of the BGR image
    # to the blue_plane variable
    blue_plane = img[:,:,0]

    # Assign Green plane of the BGR image
    # to the green_plane variable
    green_plane = img[:,:,1]

    # Assign Red plane of the BGR image
    # to the red_plane variable
    red_plane = img[:,:,2]

    # we take one-x and one-y pixel of rows and columns from
    # each plane respectively so that, it is one-x time of image matrix.

    # Here we take row,column pixel at an interval of x,y of blue plane.
    resize_blue_plane = blue_plane[1::x, 1::y]

    # Here we take row,column pixel at an interval of x,y of green plane.
    resize_green_plane = green_plane[1::x, 1::y]

    # Here we take row,column pixel at an interval of x,y of red plane.
    resize_red_plane = red_plane[1::x, 1::y]

    # Here image is of class 'uint8', the range of values  
    # that each colour component can have is [0 - 255]

    # Create a zero matrix of specified order of 3-dimension
    resize_img = np.zeros((row//x, col//y, plane),np.uint8)

    # Assigning resized blue, green and red plane of image matrix to the
    # corresponding blue, green, red plane of resize_img matrix variable.
    resize_img[:,:,0] = resize_blue_plane
    resize_img[:,:,1] = resize_green_plane
    resize_img[:,:,2] = resize_red_plane

    # return the resized image
    return resize_img


# Define a function for performing
# Upsampling on the image
# upsamping means increase the size of the image
def upsampling(img, x, y, row, col, plane) :

    # create a zero matrix of same order as original image
    temp_upscale_img = np.zeros((row, col,plane),np.uint8)
    
    i, m = 0, 0

    # run a loop untill if one the condition is become false
    while i < row and m < img.shape[0]:

        j, n = 0, 0
        
        # run a loop untill if one the condition is become false
        while j < col and n < img.shape[1]:
            temp_upscale_img[i, j, 0] = img[m, n, 0]
            temp_upscale_img[i, j, 1] = img[m, n, 1]
            temp_upscale_img[i, j, 2] = img[m, n, 2]

            # increment the j by y
            # for take a pixel at an interval of y
            j += y

            # increment the n by 1
            # for take a pixel continuously
            n += 1

        # increment the m by 1
        # for take a pixel continuously
        m += 1

        # increment the i by x
        # take a pixel at an interval of x
        i += x

    # return upscale image 
    return temp_upscale_img

# Define a function for performing
# Median Blur on images
def MedianBlur(img,size) :
    Ic = img

    # run a loop from half of the size + 1 to  upto
    # number of rows present in the image
    for i in range(size//2 + 1, Ic.shape[0]) :
        
        # run a loop  from half of the size + 1 upto
        # number of columns present in the image
        for j in range(size//2 +1, Ic.shape[1]) :

            # Take a sub-matrix of specifed order form Ic image matrix 
            N = Ic[i-size//2 : i+ size//2 + 1, j - size//2: j+ size//2 + 1]

            # find out median of submatrix
            med = np.median(N)

            # assing that medium value to the specified pixel coordinates 
            img[i, j] = med

    # return blur image
    return img


# define a function for performing cartoon
# effect on the original image
def cartoonEffect(img_bgr) :

    # Assigning number of rows, coulmns and
    # Planes to the respective variables 
    row, col, plane = img_bgr.shape
    
    # number of bilateral filtering steps
    num_bilateral = 50
    

    # give value by which you want to resize an image
    # here we want to resize an image as one half of the original image
    x1, y1 = 2,2 

    # performing downsampling on the image 
    img_color = downsampling(img_bgr,x1,y1, row, col, plane)

    # repeatedly apply small bilateral filter instead of
    # applying one large filter
    for i in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9,
                                        sigmaColor=9,
                                        sigmaSpace=7)


    x2,y2 = 2, 2

    # performing upsampling on the image 
    upscale_img = upsampling(img_color, x2,y2,row, col, plane)

    img_color = upscale_img

    # create a zero matrix of same order as original image
    img_edge = np.zeros((img_bgr.shape),np.uint8)

    # Assign Blue plane of the BGR image
    # to the blue_plane variable
    blue_plane = img_bgr[:, :, 0]

    # Assign Green plane of the BGR image
    # to the green_plane variable
    green_plane = img_bgr[:, :, 1]
    
    # Assign red plane of the BGR image
    # to the red_plane variable
    red_plane = img_bgr[:, :, 2]

    # Take a size of neighbourhood filter
    size = 5

    # applying median blur on nlue plane
    blue_plane_blur = MedianBlur(blue_plane,size)

    # applying median blur on nlue plane
    green_plane_blur = MedianBlur(green_plane,size)

    # applying median blur on nlue plane
    red_plane_blur = MedianBlur(red_plane, size)


    # detect and enhance edges of blue plane
    # using adaptiveThreshold technique
    blue_plane_img_edge = cv2.adaptiveThreshold(blue_plane_blur , 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)

    # detect and enhance edges of green plane
    # using adaptiveThreshold technique
    green_plane_img_edge = cv2.adaptiveThreshold(green_plane_blur , 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)
    # detect and enhance edges of blue plane
    # using adaptiveThreshold technique
    red_plane_img_edge = cv2.adaptiveThreshold(red_plane_blur , 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)


    # Assigning enhance edges of blue, green and red plane of image matrix to the
    # corresponding blue, green, red plane of img_edge matrix variable.
    img_edge[:, :, 0] = blue_plane_img_edge
    img_edge[:, :, 1] = green_plane_img_edge
    img_edge[:, :, 2] = red_plane_img_edge

    # for handling size of an image
    if img_color.shape[0] != img_edge.shape[0] or img_color.shape[1] != img_edge.shape[1] :
        img_color = cv2.resize(img_color,(img_edge.shape[1],img_edge.shape[0]))

    # performing bitwise and operation on the both image matrix
    img_cartoon = cv2.bitwise_and(img_color, img_edge, mask = None)

    # return cartoonified image 
    return img_cartoon

