from tkinter import *
from tkinter import filedialog
import cv2
from cv2 import imread
import os
from PIL import Image, ImageTk
from functools import partial

# global variable for the image selected by the user
queryImagePath = ''

def browseImage():

    global queryImagePath

    # query image path
    queryImagePath = filedialog.askopenfilename(initialdir=os.getcwd(), title="",
                                                filetypes=(("JPG File", "*.jpg"), ("JPEG File", "*.jpeg"), ("PNG File", "*.png"), ("All Files", "*.*")))
    img = Image.open(queryImagePath)
    # resize the image to fit the frame
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    queryImagelbl.configure(image=img)
    queryImagelbl.image = img


def findMatch(desList, imagesNames, thres = 10):

    # read the selected image
    queryImage = cv2.imread(queryImagePath,0)

    # clear old labels values
    matchImage1.configure(image='')
    matchImage2.configure(image='')
    matchImage3.configure(image='')

    print("finding match")
    # exracting features of the query image using ORB desscriptor
    keyPoints, queryImageDes = orb.detectAndCompute(queryImage,None)
    bf = cv2.BFMatcher()
    matchList = []
    finalMatchList = []
    try:
        # compare query image features with the collection of the images
        for des in desList:
            matches = bf.knnMatch(des, queryImageDes, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass

    print(matchList)

    if len(matchList) != 0:
        if max(matchList) > thres:
            resultLabel.config(text="Poosible Match(es)")
            # Find the top match
            finalMatchList.append(matchList.index(max(matchList)))
            img1 = Image.open(f'{images_path}/{imagesNames[finalMatchList[0]]}')
            img1.thumbnail((200, 200))
            result1 = ImageTk.PhotoImage(img1)
            matchImage1.configure(image=result1)
            matchImage1.image = result1

            # finding the second best match
            newList = set(matchList)
            newList.remove(max(newList))
            secondMathch = max(newList)
            if secondMathch > thres:
                finalMatchList.append(matchList.index(secondMathch))
                img2 = Image.open(f'{images_path}/{imagesNames[finalMatchList[1]]}')
                img2.thumbnail((200, 200))
                result2 = ImageTk.PhotoImage(img2)
                matchImage2.configure(image=result2)
                matchImage2.image = result2

                # finding the third best match
                newList1 = set(newList)
                newList1.remove(max(newList1))
                thirdMathch = max(newList1)
                if thirdMathch > thres:
                    finalMatchList.append(matchList.index(thirdMathch))
                    img3 = Image.open(f'{images_path}/{imagesNames[finalMatchList[2]]}')
                    img3.thumbnail((200, 200))
                    result3 = ImageTk.PhotoImage(img3)
                    matchImage3.configure(image=result3)
                    matchImage3.image = result3
        # if there is no match or the match is smaller than the threshold value
        # show => There is No Match
        else:
            resultLabel.config(text="No Match")
    else:
        resultLabel.config(text="No Match")

# Function to find the descriptor of the image collectin and store them in a list
def findDes(images, imagesNames):
    desList=[]
    i = 0
    for img in images:
        print('Extracting features from image %s' % imagesNames[i])
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
        i+=1
    return desList


# Driver code
if __name__ == '__main__':

    orb = cv2.ORB_create()
    # path to the images
    images_path = 'Image_Collection'

    images = []
    imagesNames = []
    myList = os.listdir(images_path)
    print("images list")
    print(myList)

    for cl in myList:
        currentImage = cv2.imread(f'{images_path}/{cl}', 0)
        images.append(currentImage)
        imagesNames.append(cl)

    desList = findDes(images, imagesNames)

    root = Tk()

    browseImageFrame = Frame()
    browseImageFrame.pack(side=TOP, padx=15, pady=15)

    browseBtn = Button(browseImageFrame, text="Browse", command=browseImage)
    browseBtn.pack()

    queryImagelbl = Label(browseImageFrame)
    queryImagelbl.pack()

    findMatchBtn = Button(browseImageFrame, text="find match", command=partial(findMatch, desList, imagesNames))
    findMatchBtn.pack()

    resultFrame = Frame()
    resultFrame.pack(side=TOP, padx=15, pady=15)

    resultLabel = Label(resultFrame, text=" ")
    resultLabel.pack(side=TOP)

    matchImage1 = Label(resultFrame)
    matchImage1.pack(side=LEFT)

    matchImage2 = Label(resultFrame)
    matchImage2.pack(side=LEFT)

    matchImage3 = Label(resultFrame)
    matchImage3.pack(side=LEFT)

    exitBtn = Button(root, text="Exit", command=lambda: exit())
    exitBtn.pack(side=BOTTOM)

    root.title("CBIR")
    root.geometry("800x800")
    root.mainloop()
