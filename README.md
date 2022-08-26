# Scanned_Invoice_PDF_OCR

Pre-processing for Tesseract
To avoid all the ways your tesseract output accuracy can drop, you need to make sure the image is appropriately pre-processed.
This includes rescaling, binarization, noise removal, deskewing, etc.
Used cv2(OpenCV computer vision) for Image pre-processing before applying tesseract OCR, e.g rotate, crop, grey-scale, remove noise, thresholding
cv2 (old interface in old OpenCV versions was named as cv ) is the name that OpenCV developers chose when they created the binding generators

Using Tesseract-OCR open source OCR engine, off the shelve solution to extract serial number from scanned pdf of hardcopy

Used PyPDF2, pdf2image, img2pdf for handling, reading, writing, converting pdf files

Limitations: Scanned copy of handwritten invoice could be inllegible for Tesseract OCR to detect
