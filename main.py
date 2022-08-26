from PIL import Image
import pytesseract
import os, shutil
import pdf2image
import img2pdf
import re
import cv2
import numpy as np
import PyPDF2
# MSR 1 white sheet + 1 Store issue
# Remove blue and yellow sheet, else program will fail,
# Since blue, yellow will also need to be detach as stapler bullet will jam printer

# Specify Scanned_Path for original inverted pdf
Scanned_Path ="C:/Users/ohjun/Desktop/Scanned_pdf"
os.chdir(Scanned_Path)

for file in os.listdir('.'):
    pdfIn = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfIn)
    pdfWriter = PyPDF2.PdfFileWriter()
    for pageNum in range(pdfReader.numPages):
        page = pdfReader.getPage(pageNum)
        page.rotateClockwise(180)
        pdfWriter.addPage(page)

    pdfOut = open("rotated.pdf", 'wb')
    pdfWriter.write(pdfOut)
    pdfOut.close()
    pdfIn.close()

PDF_File = pdf2image.convert_from_path(os.path.join(Scanned_Path, "rotated.pdf"))
# Split PDF into multiple images(.jpg), store at IMG_PATH folder
IMG_PATH = "C:/Users/ohjun/Desktop/test1"
os.chdir(IMG_PATH)
i = 1
for page in PDF_File:
    fname = str(i) + '.jpg'
    page.save(fname, 'JPEG')
    i += 1

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

# Using pytesseract OCR each image, extract MSR s/no, store in msr_list
IMG_File = sorted_alphanumeric(os.listdir(IMG_PATH))
msr_list = []
img_list = []
img_count = 1

r = 1
for w, jpg in enumerate(IMG_File):
    img_full_path = os.path.join(IMG_PATH, jpg)
    img_list.append(img_full_path)
    img = Image.open(jpg)

    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    def remove_noise(image):
        return cv2.medianBlur(image, 5)
    def erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    cc = cv2.imread(jpg)
    # cc[y:y, x:x]
    #cc = thresholding(erode(get_grayscale(cc[230:340, 1380:1600])))
    cc = thresholding(erode(get_grayscale(cc[230:360, 1380:1650])))
    # if 1 < w < len(IMG_File) :
    #     cv2.imshow("s.jpg", cc)
    #     cv2.waitKey(2500)
    
    # Detect only digits to improve accuracy
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    #text = pytesseract.image_to_string(cc)
    text = pytesseract.image_to_string(cc, config=custom_config))

    stripp = text.replace(" ", "")
    #print(stripp)

    for j, c in enumerate(stripp):
        if c.isdigit():
            stripp = stripp[j:j+6]
            if stripp.isdigit():

                msr_list.append(stripp)
            break

    if len(msr_list) != img_count:
       msr_list.append("invalid")

    img_count += 1
    img.close()

print(msr_list)
print(img_list)
# Sort msr_List, group same pdf page/image into respective pdf
x = 0
y = 0
unique_msr_list = []
sorted_img_list = [list() for f in range(len(img_list))]

while y < len(img_list):
    if msr_list[y] == "invalid":
        sorted_img_list[x - 1].append(img_list[y])
    else:
        sorted_img_list[x].append(img_list[y])
        unique_msr_list.append(msr_list[y])
        x += 1
    y += 1


for x in sorted_img_list:
    print(x)
    print("\n")

print(unique_msr_list)

for c, i in enumerate(sorted_img_list) :
    if c >= len(unique_msr_list):
        break
    with open(unique_msr_list[c] + "_MSR_No." + ".pdf", "wb") as f:
        f.write(img2pdf.convert([x for x in i]))

os.mkdir("Insert mechanic name")

for f in os.listdir("."):
    if f.endswith('.pdf'):
        s = os.path.join(IMG_PATH, f)
        d = os.path.join(IMG_PATH,"Insert mechanic name")
        shutil.move(s, d)

for ff in os.listdir(IMG_PATH):
    if ff.endswith('.jpg'):
        os.remove(ff)







