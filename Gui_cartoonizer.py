"""
This is the main file ,in this we create gui 
which can take image and applying cartoon efect on it
by using cartoonizer.py file
"""

# import os module for working performing os related work
# like change the directory and know current working directory
import os

# import everything from tkinter modules 
# it is used for creating gui
from tkinter import *

# import everything from tkinter.filedialog modules
# it is used for opening dialog boxes
from tkinter.filedialog import *

# import messagebox class from tkinter module
# is it used for creating messagebox
from tkinter import messagebox

# import ImageTk,Image class from the PIL module
# it is used for opening the .jpg and .png format image
from PIL import ImageTk,Image

# import readImage,cartoonEffect function from the cartoonizer.py file
from cartoonizer import readImage,cartoonEffect

# import everything from tkinter.ttk module
# it is used for dealing with .bmp and .png
# format image.
# it is use in set image on the buttons
from tkinter.ttk import *

# import cv2
# this is used here for conversion from bgr to rgb
import cv2

# global declaration

# multiple assignment
# i,j and k is used as counter
i, j, k = 0, 0, 0

# global declaration

# This is declare here we can you these in different function calls
panelA = None
panelB = None
img_bgr = None
cartoon_img_bgr = None
welcome_image = None


# define a function for selecting an image
# from the computer and show it in the tkinter gui
def select_image() :

    # grab a reference to the image panels
    global panelA, panelB, img_bgr, welcome_image,j

        
    # open a file chooser dialog and allow the user
    # to select an input image
    path = askopenfilename( title = "Select file",
                            initialdir = "/",
                            filetypes=[("Jpg image","*.jpg")])
    
    # ensure a file path was selected
    if len(path) > 0:

        img_bgr,row,col = readImage(path)
        
	# OpenCV represents images in BGR order; however PIL represents
	# images in RGB order, so we need to swap the channels
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)        
        
        # convert the images to PIL format image
        image = Image.fromarray(img_rgb)
        
        # now convert PIL format image into ImageTk format
        # so that we can able to use in Label's image attribute 
        image = ImageTk.PhotoImage(image)

        # if the panelA is None, initialize them
        if panelA is None :

            # the first panel will store our original image
            panelA = Label(image = image)
            panelA.image = image
            panelA.grid(row = 3, column = 2,ipadx = "5",ipady = "5")

        # otherwise, update the image panels
        else :

            # update the pannels
            panelA.configure(image = image)
            panelA.image = image
            
            panelB.configure(image = welcome_image)
            panelB.image = welcome_image

    # if path is None   
    else :
        
        # show error message
        messagebox.showerror("error","please choose any image..")

    # increment 
    j += 1


# define function for performing cartooning effect
# on the selected image
def CreateCartoonImage() :

    # grab a reference to the image panels
    global panelB,img_bgr,cartoon_img_bgr, k

    # increment
    k += 1

    # if img_bgr is none then show error msg and return back
    if img_bgr is None  :
        messagebox.showerror("error","please choose any image..")
        return

    # calling cartoonEffect function
    # this function return image with cartoon effect
    cartoon_img_bgr = cartoonEffect(img_bgr)

    # changes bgr to rgb channels because PIL module support rgb channels
    cartoon_img_rgb = cv2.cvtColor(cartoon_img_bgr, cv2.COLOR_BGR2RGB)

    # convert the images to PIL format image
    cartoon_image = Image.fromarray(cartoon_img_rgb)
    cartoon_image = ImageTk.PhotoImage(cartoon_image)
    
    # if the panelB is None, initialize them
    if panelB is None:

        # while the second panel will store the cartoon image
        panelB = Label(image = cartoon_image)
        panelB.image = cartoon_image
        
        # grid method is used for placing 
        # the widgets at respective positions 
        # in table like structure .       
        panelB.grid(row = 3, column = 4,ipadx = "5",ipady = "5")

     # otherwise, update the image panels
    else :

        # update the pannels
        panelB.configure(image = cartoon_image)
        panelB.image = cartoon_image

    
# define a function for incrementing i variable
# and hadling same image save problem
def increment() :
    global i
    i += 1

    # if value of i is greater then j or k then
    # show the error msg and return back
    if i > j or i > k  :
        messagebox.showerror("error","This image is already saved..")
        i -= 1
        return 

    # otherwise calling saveImage function
    # for saving the cartoon effet image
    saveImage(i)

# define a function for saving the image   
def saveImage(i) :

    global cartoon_img_bgr

    # if cartoon_img_bgr variable is None
    if cartoon_img_bgr is None :
        # then show error msg and return back
        messagebox.showerror("error","Don't have any image to save..")
        return

    # mention the specified path where we want to save the image
    path = "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python36\\all_prgm\\cartoon\\Final\\cartoon_images"

    # if mention path is not same as current working directory then change
    # current working directory to given path
    if path != os.getcwd() :
        os.chdir("cartoon_images\\")

    # if mention path is same as current working directory
    # then save the image in that path

    # imwrite function save the image at specified path
    cv2.imwrite("picture" +  str(i)+ ".jpg",cartoon_img_bgr)

    # show the information meassage 
    messagebox.showinfo("Done","image is saved..")


# define a function for exiting the gui application
def exitgui() :

    # destroy the root window of gui
    # and exit the program
    root.destroy()

    

# Driver code
if __name__ == "__main__" :
    
    # Create a GUI window  
    root = Tk()
    
    # set the name of tkinter GUI window  
    root.title("Cartoonizer GUI")

    # Set the background colour of GUI window  
    root.configure(background = 'light green')  

    # read an image
    welcome_image_bgr = cv2.imread("pic16.jpg")

    # changes bgr to rgb channels because PIL module support rgb channels
    welcome_image_rgb  = cv2.cvtColor(welcome_image_bgr , cv2.COLOR_BGR2RGB)

    # convert the images to PIL format image
    welcome_image = Image.fromarray(welcome_image_rgb)

    # now convert PIL format image into ImageTk format
    # so that we can able to use in Label's image attribute 
    welcome_image = ImageTk.PhotoImage(welcome_image)

    # this panel will store our welcome image
    panelC = Label(image = welcome_image)
    panelC.image = welcome_image

    # grid method is used for placing 
    # the widgets at respective positions 
    # in table like structure .
    panelC.grid(row = 3, column = 2)


    # Creating a photoimage object to use image.
    # photimage only supports .bmp and .png format image 
    icon1 = PhotoImage(file = "pic11.png")
    icon2 = PhotoImage(file = "pic12.png")
    icon3 = PhotoImage(file = "pic13.png")
    icon4 = PhotoImage(file = "pic14.png")

    # Resizing image to fit on buttons
    icon_1 = icon1.subsample(2, 2)
    icon_2 = icon2.subsample(3, 3)
    icon_3 = icon3.subsample(6, 6)
    icon_4 = icon4.subsample(7, 7)
    
    # create a button with text and images on it, then when pressed, it call the select_image function
    button1 = Button(root,text = "Select Image", image = icon_1 ,compound = LEFT, command = select_image)

    # create a button with text and images on it, then when pressed, it call the CreateCartoonImage function
    button2 = Button(root, text = "CartoonEffect", image = icon_2 ,compound = LEFT, command = CreateCartoonImage)

    # create a button with text and images on it, then when pressed,it call the exitgui function
    button3 = Button(root, text = "Exit",image = icon_3,compound = LEFT, command = exitgui)

    # create a button with text and images on it, then when pressed,it call the increment function
    button4 = Button(root, text = "Save Image",image = icon_4, compound = LEFT, command = increment)

    # grid method is used for placing 
    # the widgets at respective positions 
    # in table like structure then add the button the GUI
    button1.grid(row = 2, column = 2)
    button2.grid(row = 4, column = 2)
    button3.grid(row = 5, column = 2)
    button4.grid(row = 5, column = 4)
    
    # Start the GUI 
    root.mainloop() 
