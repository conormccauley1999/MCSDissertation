from csv import reader as csv_reader, writer as csv_writer
from spacy_langdetect import LanguageDetector
import spacy

DIR = '../data/prepared/'
PATH_REVIEWS_IN = DIR + 'reviews/%d.csv'
PATH_REVIEWS_OUT = DIR + 'reviews/languages/%d.csv'
REVIEW_PAGES = 32

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(LanguageDetector(), name='lang-detect', last=True)

def prepare_review_languages():
    for page_num in range(1, REVIEW_PAGES + 1):
        print(f'page {page_num}/{REVIEW_PAGES}')
        data = []
        # create output file
        with open(PATH_REVIEWS_OUT % page_num, 'w+') as f:
            pass
        with open(PATH_REVIEWS_IN % page_num, 'r', encoding='utf-8', newline='') as f1:
            row_num = 0
            reader = csv_reader(f1, delimiter=',')
            for review in reader:
                raw_text = review[-1]
                text = nlp(raw_text)
                raw_chars = len(raw_text)
                raw_words = len(raw_text.split())
                nlp_words = len(text)
                nlp_lang = text._.language['language']
                nlp_score = text._.language['score']
                data.append([nlp_lang, nlp_score, nlp_words, raw_words, raw_chars])
                row_num += 1
                if not row_num % 10000:
                    print(f'page={page_num} row={row_num}')
                    with open(PATH_REVIEWS_OUT % page_num, 'a', encoding='utf-8', newline='') as f2:
                        writer = csv_writer(f2, delimiter=',')
                        writer.writerows(data)
                    data = []

prepare_review_languages()
