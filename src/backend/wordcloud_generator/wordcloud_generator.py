from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import os
import pickle as pkl
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

def generate_wordcloud(keyword, candiate_video_info,
                       stopwords_path=STOPWORD_PATH,
                       keep_stop_words=False,
                       width=1200, height=800,
                       bg_color="white", contour_color="steerlblue",
                       max_words=300):
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
                            stopwords=stopwords_cn
                        )

    print("=============================================================================================")
    print("\n Generating word cloud... \n")
    w.generate(corpus)
    print(w.words_)

    w.to_file(f'./wordclouds/印象-{keyword}.png')
    print("\nWord Cloud successfully generated. Check the wordclouds directory for results.\n")
    return w

if __name__ == "__main__":
    # keyword = "绵羊料理"
    # with open("./绵羊.pkl", "rb") as file:
    #     candidate_video_info = pkl.load(file)
    # generate_wordcloud(keyword, candidate_video_info)

    keyword = "特别周"
    _, candidate_video_info = start_scraping(keyword, max_pages=1, max_videos=5)
    generate_wordcloud(keyword, candidate_video_info, max_words=300)

