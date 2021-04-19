from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import os
import pickle as pkl
import numpy as np
import re
from scipy.stats import percentileofscore
from src.backend.scraper.scraper import start_scraping

STOPWORD_PATH = "./assets/stopwords.txt"
def load_stopwords(path):
    """
    Load the pre-stored stop word and return them as a list.
    :return: stopwords as list.
    """
    try:
        with open(path, encoding="utf-8", mode="r+") as f:
            stopwords = []
            for line in f.readlines():
                stopwords.append(line.strip())
            return stopwords
    except:
        # do not strop stopwords
        return []


def load_corpus_txt(path):
    """
    Load a txt format corpus. Rquest .txt corpus,
    each line as single danmaku/comment.
    :param path: path to the .txt corpus.
    """
    try:
        with open(path, encoding="utf-8", mode="r+") as f:
            text = ""
            for line in f.readlines():
                text += line.strip()
                text += "\n"
            return text
    except:
        logger.error("Text file not found in corpus")
        exit


def construct_corpus(candidate_video_info):
    """
    Connect all danmaku & comments with "\n".
    :return: a huge corpus (str).
    """
    comment_list = []
    danmaku_list = []
    for bv in candidate_video_info.keys():
        danmakus = candidate_video_info[bv]["danmaku_list"]
        danmaku_list.extend(danmakus)
        comments = candidate_video_info[bv]["comment_list"]
        comment_list.extend(comments)
    comment_list.extend(danmaku_list)
    return "\n".join(comment_list)


def calc_tfidf(candidate_words, corpus):
    documents = corpus.split("\n")
    word2tf = {word :  0 for word in candidate_words} # word freq
    word2df = {word : 0 for word in candidate_words} # document freq
    word2tfidf = {word : 0 for word in candidate_words} # document freq
    for doc in documents:
        for word in candidate_words:
            freq_count = doc.count(word)
            word2tf[word] += freq_count
            if word in doc:
                word2df[word] += min(1, freq_count)

    # calc tf-idf
    trimed_corpus = corpus.replace("\n", "")
    for word in candidate_words:
        tf, df =  word2tf[word], word2df[word]
        word2tfidf[word] = ((tf / (len(trimed_corpus) / 2)) * ((np.log((len(documents) + 1) / (df + 1)) + 1)) ** 5)
        if re.match(r"(\w+)\s*\1+", word): word2tfidf[word] *= 0.25  # lower weight of aaa, abab, etc.
        if len(word) > 5: word2tfidf[word] *= 2  # Compensation for longer words
    return word2tfidf

def min_max_scale_dict(score_dic):
    scores = np.array(list(score_dic.values()))
    max_score = np.max(scores)
    min_score = np.min(scores)
    for k,v in score_dic.items():
        mapped_score = (score - min_score) / (max_score - min_score) # mapped to range [0, 1]
        score_dic[k] = mapped_score
    return score_dic


def percentile_scale_dict(score_dic):
    scores = np.array(list(score_dic.values()))
    for k, v in score_dic.items():
        per = percentileofscore(scores, v)
        score_dic[k] = (per / 100) ** 1.2
    return score_dic


def heuristic_postprocess(candidate_words, keyword):
    candidate_words_copy = candidate_words.copy()
    def is_substring_of_other_high_quality_word(word, words):
        for w in words:
            if w == word: continue
            if word in w and candidate_words[w] >= 0.5 * candidate_words[word]: return True
        return False

    for word in candidate_words_copy:
        first_char = word[0]
        if is_substring_of_other_high_quality_word(word, candidate_words.keys()):
            candidate_words.pop(word, None)
            continue

        if len(word) <= 3:
            if word.lower() in keyword.lower():
                candidate_words.pop(word, None)
        else:
            if re.match(r"\w*_\w*", word):    # Remove abc_def as they are mostly memes
                candidate_words.pop(word, None)
            elif re.match(r"(\w)\1+\w", word):  # remove aaaa...b as they are less informative
                candidate_words.pop(word, None)
            elif re.match(r"\w(\w)\1+", word):  # remove abbbb...
                candidate_words.pop(word, None)
    return candidate_words



def generate_wordcloud(keyword, candiate_video_info,
                       stopwords_path=STOPWORD_PATH,
                       keep_stop_words=False,
                       width=1200, height=800,
                       bg_color="white", contour_color="steerlblue",
                       max_words=300,
                       custom_stopwords=[]):
    """
    Word cloud generator interface, will generate impression wordcloud for a keywod.
    :param keyword: topic being explored interested.
    :param candiate_video_info: SECOND return value of backend/scraper/scraper.py/start_scraping.
        usually we collect 50-80 for one query.
    :param stopwords_path: the path of "\src\backend\wordcloud_generator\assets\stopword.txt"
    :keep_stop_words: whether or not to keep stopwords in the generated wordcloud.
    :param width, height, bg_color, contour_color, max_words: parameters for styling the generated wordcloud.
        check https://amueller.github.io/word_cloud/ for details.
    """
    if not os.path.isdir("wordclouds"):
        os.mkdir("wordclouds")
    if not keep_stop_words:
        stopwords_cn = load_stopwords(stopwords_path)
        stopwords_cn.append(keyword) # exlude topic itself from wordcloud
        stopwords_cn.extend(custom_stopwords)
    else:
        stopwords_cn = []
    corpus = construct_corpus(candiate_video_info)
    print("=============================================================================================")
    print("\n Starting to Generate word cloud\n")
    w = WordCloud(width=width, height=height,
                            background_color=bg_color,
                            contour_width=1,
                            contour_color=contour_color,
                            font_path="msyh.ttc",
                            max_words=max_words,
                            collocations=True,
                            stopwords=stopwords_cn,
                            min_word_length=2,
                        )

    print("=============================================================================================")
    print("\n Generating word cloud... \n")
    w.generate(corpus)
    candidate_words = heuristic_postprocess(w.words_, keyword)
    word2tfidf = calc_tfidf(candidate_words, corpus)
    w.generate_from_frequencies(word2tfidf)
    # print(word2tfidf)
    w.to_file(f'./wordclouds/印象-{keyword}-adv.png')
    print("\nWord Cloud successfully generated. Check the wordclouds directory for results.\n")
    return w

if __name__ == "__main__":
    # query = "绵羊料理"
    # with open("./绵羊.pkl", "rb") as file:
    #     candidate_video_info = pkl.load(file)
    keyword = "特别周"
    _, candidate_video_info = start_scraping(keyword, max_pages=1, max_videos=5)
    generate_wordcloud(keyword, candidate_video_info)

