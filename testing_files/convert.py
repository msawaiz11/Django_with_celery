from pdf2docx import Converter
pdf_file = r'D:\celery_basic\Muhammad Sawaiz.pdf'
docx_file = r"D:\celery_basic\sample.docx"

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file)      # all pages by default
cv.close()