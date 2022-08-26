# Scanned_Invoice_PDF_OCR
Using Tesseract-OCR, off the shelve solution to extract serial number from scanned pdf of hardcopy

Used openCV for Image pre-processing before applying tesseract OCR, e.g rotate, crop, grey-scale, remove noise, thresholding

Used PyPDF2, pdf2image, img2pdf for handling, reading, writing, converting pdf files

Limitations: Scanned copy of handwritten invoice could be inllegible for Tesseract OCR to detect
