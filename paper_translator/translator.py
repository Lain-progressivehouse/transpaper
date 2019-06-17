from googletrans import Translator
from paper_translator import pdf_reader
import re
import os
import sys
import time
from tqdm import tqdm


def get_translate(file):
    doc = pdf_reader.get_pdf_strings(file)
    doc = re.sub(r"\s[\s]+", " ", re.sub("[\n\t]", " ", doc))

    translator = Translator()

    write_list = []
    sentences = ""

    print("translate-start")

    # 一回に翻訳できる文字数は5000まで
    for d in tqdm(doc.split(". ")):
        if len(sentences) + len(d) > 5000:
            sentences = sentences[:-1]
            translate_sentences = translator.translate(sentences, dest="ja").text + "\n"
            for s, t in zip(sentences.split("\n"), translate_sentences.split("\n")):
                write_list.append(s)
                write_list.append(t + "\n")

            sentences = ""
            time.sleep(1)

        sentences += d + ". " + "\n"

    sentences = sentences[:-1]
    translate_sentences = translator.translate(sentences, dest="ja").text + "\n"
    for s, t in zip(sentences.split("\n"), translate_sentences.split("\n")):
        write_list.append(s)
        write_list.append(t + "\n")

    print("translate-end")

    with open(os.path.splitext(file)[0] + ".txt", mode="w") as f:
        f.write("\n".join(write_list))


if __name__ == '__main__':
    args = sys.argv
    get_translate(args[1])
