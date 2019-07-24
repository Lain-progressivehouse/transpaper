from googletrans import Translator
from paper_translator import pdf_reader
import re
import os
import sys
import time
from tqdm import tqdm


def get_translate(file, is_file=True):
    doc = pdf_reader.get_pdf_strings(file, is_file)

    translator = Translator()

    write_list = []
    sentences = ""

    print("translate-start")

    for d in tqdm(doc.split("\n\n")):
        d = re.sub("-\n", "", d)
        d = re.sub(r"\s[\s]+", " ", re.sub("[\n\t]", " ", d))
        d = re.sub("\0", " ", d)

        if len(sentences) + len(d) > 4800:
            sentences = sentences[:-1]
            try:
                translate_sentences = translator.translate(sentences, dest="ja").text + "\n"
            except:
                print("Error")

            for s, t in zip(sentences.split("\n"), translate_sentences.split("\n")):
                write_list.append(s)
                write_list.append(t + "\n")

            sentences = ""
            time.sleep(1)

        sentences += d + "\n"

    sentences = sentences[:-1]
    translate_sentences = translator.translate(sentences, dest="ja").text + "\n"
    for s, t in zip(sentences.split("\n"), translate_sentences.split("\n")):
        write_list.append(s)
        write_list.append(t + "\n")

    print("translate-end")

    return "\n".join(write_list)


def get_translate_for_app(file, is_file=True):
    doc = pdf_reader.get_pdf_strings(file, is_file)
    doc = re.sub("-\n", "", doc)
    doc = re.sub(r"\s[\s]+", " ", re.sub("[\n\t]", " ", doc))
    doc = re.sub("\0", " ", doc)

    translator = Translator()

    write_list = []
    sentences = ""

    print("translate-start")

    # 一回に翻訳できる文字数は5000まで
    for d in tqdm(doc.split(". ")):
        if len(sentences) + len(d) > 4800:
            sentences = sentences[:-1]
            try:
                translate_sentences = translator.translate(sentences, dest="ja").text + "\n"
            except:
                print("Error")
                # with open(os.path.splitext(file)[0] + "_err.txt", mode="w") as f:
                #     f.write(sentences)

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

    return "\n".join(write_list)


def save_txt(file):
    with open(os.path.splitext(file)[0] + ".txt", mode="w") as f:
        f.write(get_translate(file))


if __name__ == '__main__':
    args = sys.argv
    save_txt(args[1])
