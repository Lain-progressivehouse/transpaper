from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import sys
import re
import os


def get_pdf_strings(file, is_file=True):
    rsrcmgr = PDFResourceManager()
    rettxt = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, rettxt, codec="utf-8", laparams=laparams)
    # ページを集めるPageAggregatorオブジェクトを作成。
    pager = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 処理するPDFを開く
    if is_file:
        fp = open(file, 'rb')
    else:
        fp = file.stream
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # maxpages：ページ指定（0は全ページ）
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)

    document = rettxt.getvalue()

    fp.close()
    device.close()
    rettxt.close()

    return document


def save_pdf_to_txt(file):
    doc = get_pdf_strings(file)
    doc = re.sub(r"\s[\s]+", " ", re.sub("[\n\t]", " ", doc))

    with open(os.path.splitext(file)[0] + ".txt", mode="w") as f:
        f.write(". \n".join(doc.split(". ")))


if __name__ == '__main__':
    args = sys.argv
    save_pdf_to_txt(args[1])
