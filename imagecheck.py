# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
import os
import tkinter
from tkinter.font import BOLD, Font
from PIL import Image, ImageTk
import shutil
import sys

# Function loads an image for the GUI, scaling it, such that it will fit in the window
def LoadImage(img):
    im = Image.open(img)
    width, height = im.size
    # 700 is the maximum height 
    # 700 is the maximum width
    if width > height:
        scale = (700, int(700 * height / width))
    else:
        scale = (int(700 * width / height), 700)
    return ImageTk.PhotoImage(im.resize(scale)), scale[0]

# Function that gets the file size for the GUI
def GetFileSize(file):
    fileSize = 1.0 * os.path.getsize(file)
    suffix = ['b', 'kb', 'mb']
    suffixV = 0
    while fileSize > 1000:
        suffixV += 1
        fileSize /= 1000
    return format(fileSize, ".1f") + suffix[suffixV]

# This function is called by the GUI, when the user clicks on either of the Move buttons or the Cancel button
def MovePic(file):
    print(file)
    if file != "":                                                              # file variable is blank if the user clicked the move button, which is why we have this if statement
        toFile = os.path.join(pathDup, file[file.rfind('/'):])
        print(f"Move file from {file} to {toFile}")
        shutil.move(file, toFile)
    else:
        print("Both files left in original directory")
    window.destroy()

# This function creates the Move Choice Window, given the two image files and the mse and ssie values of the two
def MoveChoiceWindow(file1, file2, mse, ssie):
    global window

    # Create the Window,
    window = tkinter.Tk()
    window.title("Same Image?")                             # Set the window title
    window.geometry("1500x900")                             # Set the window size (which I haave just fixed, but fits on all 1080 monitors)
    window.configure(background = '#fff0b3')                # Set the background

    # Add a label at the top, middle which gives the mse and ssie values
    topLabel = tkinter.Label(window, text=f"mse = {mse}, ssie = {ssie}", font=Font(window, size=25, weight=BOLD))           
    topLabel.place(relx=0.5, rely=0, anchor = 'n')

    # Add in the left hand image and centre it on the left
    lImage, width = LoadImage(file1)
    lPic = tkinter.Label(window, image=lImage)
    lPic.image = lImage
    lPic.place(x=360 - int(width/2), y=450, anchor = 'w')

    # Add a label centred under the image giving the file size
    lSizeLabel = tkinter.Label(window, text=file1[file1.rfind('/')+1:] + "\n" + GetFileSize(file1), font=Font(window, size=16, weight=BOLD))
    lSizeLabel.place(x=360, y=100, anchor = 's')

    # Add the 'Move' button as well underneath the image for this image.
    lButton = tkinter.Button(window, text="Move", command=lambda: MovePic(file1), height=2, width=10, font=Font(window, size=16))
    lButton.place(x=360, y=850, anchor = 'center')

    # Add the right hand image and centre it on the right
    rImage, width = LoadImage(file2)
    xPos = int(1490 - (700 - width)/2)
    rPic = tkinter.Label(window, image=rImage)
    rPic.image = rImage
    rPic.place(x=xPos, y=450, anchor = 'e')

    # Add a label centred under the image giving the file size
    rSizeLabel = tkinter.Label(window, text=file2[file2.rfind('/')+1:] + "\n" + GetFileSize(file2), font=Font(window, size=16, weight=BOLD))
    rSizeLabel.place(x=xPos - int(width/2), y=100, anchor = 's')

    # Add the 'Move' button as well underneath the image for this image.
    rButton = tkinter.Button(window, text="Move", command=lambda: MovePic(file2), height=2, width=10, font=Font(window, size=16))
    rButton.place(x=xPos - int(width/2), y=850, anchor = 'center')

    # Add a central 'Cancel' button in case the user does not want to move either file.
    cButton = tkinter.Button(window, text="Cancel", command=lambda: MovePic(""), height=2, width=10, font=Font(window, size=16))
    cButton.place(x=750, y=850, anchor = 'center')

    # Enter the main loop of the window, which is all dealt with in the background
    # Python waits until the Window is destroyed before returning from this function
    window.mainloop()

# Print iterations progress
# Found @ https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters - Thank you much appreciated
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# This function calculates the mse value between the two images.
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def main():
    global path
    global pathDup

    # Check that the correct paramaters have been given, otherwise error out
    if len(sys.argv) != 3:
        print('Set folder as a parameters. For example:\n>>> python imagecheck.py <input folder path> <folder where duplicates are saved>')
        exit()
    else:
        path = sys.argv[1]
        pathDup = sys.argv[2]

    # Check the paramaters are actaully folders, otherwise error out
    if not os.path.isdir(path) or not os.path.isdir(pathDup):
        print('At least one of the parameter given is not a folder.')
        print('Set folder as a parameters. For example:\n>>> python imagecheck.py <input folder path> <folder where duplicates are saved>')
        exit()

    # Define the bounds for mse and ssie for which we believe the two pictures are the same.
    mseMax = 100                                            # The lower this value the more likely the two pictures are the same - zero => the pictures are identical
    ssieMin = 0.8                                           # This value is between -1 and 1, 0 => pictures are NOT identical, -1 or 1 => pictures are identical
                                                            #           We just deal with the absolute value, when comparing the images.

    # Get a list of all the pictures (png and jpg) contained within the folder
    print("Getting list of image files in specified directory")
    listFiles = os.listdir(path)
    files = []
    for f in listFiles:
        fPath = os.path.join(path, f)
        fRoot, fExt = os.path.splitext(f)
        if os.path.isfile(fPath) and fExt in {".png", ".jpg"}:
            files.append(fPath)
    print("Found all image files in specificed directory")
    print("Checking for duplicates now")

    # Initialise the array which will hold the pairs of picture files that we think are identical
    samePics = []

    # Calculate total iterations
    totalIter = len(files)*(len(files)-1) / 2
    curItem = 0
    printProgressBar(curItem, totalIter, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # Now loop through the images, checking whether any of them are a good match
    for i in range(0, len(files)):
        # Load image 1, convert to gray scale and get its shape
        image1 = cv2.imread(files[i])
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image1Shape = image1.shape
        for j in range(i+1, len(files)):                                            # Only loop through the files, that come after file[i], as the files before that have already been compared.
            # Load Image 2, convert to gray scale and get its shape
            image2 = cv2.imread(files[j])
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            image2Shape = image2.shape

            # Check if the ratio of the heights = ratio of width, otherwise we assume the images are not the same
            # Note, if one image has been slightly cropped, is unlikely to be considered the same
            if image1Shape[0] / image2Shape[0] == image1Shape[1] / image2Shape[1]:
                # If the images are not the same size, then we resize image 2 to match image 1
                #       Note the images must be the same size for us to compare them, otherwise the mse and ssie comparisons fail
                if image1Shape[0] != image2Shape[0]:                                                            
                    image2 = cv2.resize(image2, (image1Shape[1], image1Shape[0]), interpolation = cv2.INTER_CUBIC)

                # Get the mse and ssie values of the two pictures
                mseValue = mse(image1, image2)
                ssieValue = ssim(image1, image2)
                # If either value falls within the threshold where we consider the images to the same, append the information to samePics list
                if mseValue < mseMax or abs(ssieValue) > ssieMin:
                    print(f"Images '{files[i]}' and '{files[j]}' are similar, mse = {mseValue}, ssie = {ssieValue}")                # A debug print out information is given
                    samePics.append([files[i], files[j], mseValue, ssieValue])
            #Print the updated progress bar
            curItem += 1
            printProgressBar(curItem, totalIter, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # Now that we have found all the identical pictures, we loop through the pairings, displaying a window, where the user can choose
    # which, if either of the images, they want to be moved to the duplicate folder.
    # Note, if two images are identical then we automatically move the second file found to the duplicate folder.
    #       this from testing appears to only happen if the two files are of the same size anyway.
    for file1, file2, mseValue, ssieValue in samePics:
        if os.path.exists(file1) and os.path.exists(file2):                             # We check that both files still exist, i.e. one has not already been moved, which can occur when more than 2 images are identical
            if mseValue == 0:                                                           # If the pictures are identical, move file 2 to duplicates
                toFile = os.path.join(pathDup, file2[file2.rfind('/'):])
                print(f"Move file from {file2} to {toFile}")
                shutil.move(file2, toFile)
            else:
                print(f"Comparing {file1} and {file2}...")
                MoveChoiceWindow(file1, file2, mseValue, ssieValue)                     # Otherwise ask the user which one they want moving.

if __name__ == "__main__":
    main()

