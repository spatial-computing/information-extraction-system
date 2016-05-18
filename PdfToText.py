# encoding=utf8
__author__ = 'shilpagulati'

from nltk import sent_tokenize
from cStringIO import StringIO
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
import json
import sys


def pdf_to_text(pdf_name):
    #takes pdf file as input and extract text data from it

    resource__mgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    la_params = LAParams()
    device = TextConverter(resource__mgr, sio, codec=codec, laparams=la_params)
    interpreter = PDFPageInterpreter(resource__mgr, device)
    fp = file(pdf_name, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)

    fp.close()
    text = sio.getvalue()
    device.close()
    sio.close()
    return text


def sentence_tokens(text):
    # input data in text and get sentence segments

    global sentence_tokenize_list
    sentence_tokenize_list = []

    sentence_tokenize_list = sent_tokenize(text.decode('utf-8'))

    with open("RawCorpus2.txt",'w') as outfile:
        for each in sentence_tokenize_list:
            outfile.write(each.encode('utf-8'))
            outfile.write('\n')

    outfile.close()


def main(arg):

    document_text = pdf_to_text("RegulationDocuments/"+arg)

    new_document_text = document_text.replace('\n', '').replace(";", ". ")
    sentence_tokens(new_document_text)


if __name__ == "__main__":
    main(sys.argv[1])





