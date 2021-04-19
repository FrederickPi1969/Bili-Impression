# 印象.Bili

## 简介

印象·Bili是一个Windows端的Bilibili爬虫项目。我们此项目作为SP21-CS242@UIUC的final project.

相关技术：爬虫，数据分析，统计建模，NLP, 知识图谱，前端后端/web.


针对一个用户感兴趣的话题词, (e.g. 王者荣耀，photoshop，etc.), 它具有以下的功能：

- 根据爬取相关视频的评论和弹幕生成话题印象词云，并用NLP的算法提高词云质量
- 筛选该话题下最受欢迎的UP主
- 生成对该话题感兴趣的用户的性别分布
- 用类Kernel Density Estimation的方法拟合话题的热度变化
- 提取弹;幕/评论中的 named entity 并生成关联标签/UP主/概念的知识图谱。
- More coming in the future. Stay tuned!

我们提供两种方法来运行代码: (1) 用本地的GUI的来直接运行代码。需要在本地安装所有需要的development packages (详见requirements). （2）我们提供了后端服务器及前端web application. 用户可以直接访问我们的网站来执行操作。



## Requirements

```
beautifulsoup4==4.9.3
Flask==1.1.2
Flask-Cors==3.0.10
Kivy==2.0.0
kivy-deps.angle==0.3.0
kivy-deps.glew==0.3.0
kivy-deps.gstreamer==0.3.2
kivy-deps.sdl2==0.3.1
Kivy-examples==2.0.0
Kivy-Garden==0.1.4
kiwisolver==1.3.1
lxml==4.6.2
matplotlib==3.3.3
numpy==1.20.2
pandas==1.1.4
Pygments==2.8.1
pymongo==3.11.3
pypiwin32==223
pywin32==300
python-dotenv==0.15.0
requests==2.24.0
scipy==1.5.4
Scrapy==2.4.1
```




## Project Agenda

### Part 1

**Xinyu**

- Basic Web scraping (single-thread, native) the **comments, tags, Danmaku, commenters info, video info** for search results responded by "综合排序" query topic indicated by the user. (M in MVC)
- Scrape fuzzy search suggestion used by search.bilibili.com.
- Data storage with MongoDB.

**Zihan**:

- Local App with NUI, receiving user input and executing scraper to obtain danmaku, tags, and comments of customize number of videos.
- Web App server, dealing with scraping requests from outside and run scraping functions. Send results to frontends.
- Adding functionality of customized search with options (subarea, most danmaku, most recently released)


### Part 2

**Xinyu**:

- Vanilla wordCloud generation. Do initial filtering (excluding stopwords/obvious low quality phrases) using exact matches.
- Support second-hand ranking of video results with either view counts or uploading date.
- Decide whether or not to consider a video as wordCloud generation candidate using video description/author/tags/title.
- Design the occurrence-time-enhanced total view counts based top-k author ranking algorithm (see rubric for details) and extract top authors for queries.

**Zihan**:

- Advanced web scraping - multi {processing/threading} for accelerating scraping.
- Implement an internet proxy for scraping to avoid IP getting banned by Bilibili.
- Basic web page front end for showing raw data from results got above
  (without much decoration).


### Part 3


**Xinyu**:
Implement the word cloud generation algorithm and do optimization. This includes：

- Repetitive words / reduplication words reduction + phrase group + cutting via phrase mining techniques.
- Apply idea of high quality phrase mining technique to filter out high quality phrases - *Jialu Liu, Mining Quality Phrases from Massive Text Corpora, 2015*
- Carry out case studies to demonstrate the performance of the new improvements. i.e. compare algorithm-corrected wordCloud v.s. raw generation results. Aparat from above, implement the stimulated popularity variation of query word via kernel density estimation algorithm (see rubrics-week3 for details.)

**Zihan**:

- Complete Web App frontend and Local App NUI, support new functions like showing fuzzy search selection and top k uploaders search.
- Add buttons with onclick functions to video scraping options (subarea, most danmaku, most recently released).


### Part 4

**Xinyu**

- Differentiate native Bili concepts (Uploaders) from external entities.
- Do named entity recognition in scraping results and generate related concepts recommendation using distant supervision (Possible sources: Baidu Encyclopedia, Moegirl Encyclopedia, WikiPedia).
- Attempt to link tags/authors, as well as surface mentions in corpus to remote encyclopedias.
- Generate knowledge graph based on previously detected entities via different weight algorithms for native/non-native concepts.

**Zihan**:

- Visualization of all data obtained from the backend.
- Adding interactivity to visualizations.(e.g. Line charts with nodes can show pop-ups when moving the mouse on it.)
-  Adding decorations to Web App and Local App.
