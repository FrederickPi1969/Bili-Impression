# A Web app Bili-Impression 印象.Bili
Xinyu (xinyupi2) Zihan (zshan2) | Moderator: Miner Liu (minerl2)
 
This is a web app about a project for CS242
 
## Abstract
### Project Purpose
 
The purpose of this project is to provide users with visual understanding of Chinese youngsters' impressions, as well as big-data objective observations on a topic word of interest. This is done by WordCloud generation of comments, sex distributions visualizations, top uploaders ranking for a given topic, popularity varaition through time diagram, related concepts knowledge graph demonstration.  
 
 
### Project Motivation
 
Very often, we are interested in studying the general impressions, as well as making macro-scrope observations on topics of interest - especially those from fresh bloods of the society - youngsters. This includes but not limited to their comments, thoughts towards the topic, as well as statistical facts of the community.
 
BiliBili, the Largest video website for youngsters in China, has more than 200,000,000 users, with more than 54,000,000 daily active users (https://www.sohu.com/a/452506920_153054). This provides us a fabulous platform to carry out the above studies. Through large-scale web scraping techniques, we are able to get big data and form insights from them with the techniques of natural language processing and statistics. This is the most fundamental motivation of our project.
 
Beyond that, BiliBili's current functionalities are not versatile enough - for example, it does not provide top recommended uploaders for a given topic. Suppose a random youngster wants to learn cooking, BiliBili does not currently provide a recommendation list of uploaders for him so that he can get started easily. Advanced features, such as word cloud visualization of a given topic, only exists in imagination. Therefore, we are also trying to make a more versatile version of BiliBili.
 
 
 
 
 
## Technical Specification
- Platform: Browser/Web Application
- Programming Languages: Python, Javascript, Bat
- Stylistic Conventions: PEP8 and Google Javascript Style Guide
- SDK: Anaconda3
- IDE: Pycharm and VS Code
- Tools/Interfaces: Chrome or other web browsers
- Machine Learning Libs: PyTorch, Gensim, Jieba, CocoNLP, SK-Learn, NetworkX, SciPy
- Target Audience: Broad-range audience with Chinese literacy
 
 
## Functional Specification
### Features
- Scraping danmaku, tags, and comments, view counts, author, etc. from videos on bilibili.com with various customizable filtering criterions. 
- Use the results of scraping to create word cloud optimized with NLP algorithms (High quality phrase mining, named entity recognition & entity linking)
- Visualization of sex distributions of audience (commenters) of related videos
- Parse the top K uploaders of the given topic word, using a convex-function weighted total view count.
- Visualization of the variation of popularity of the topic over time. As the extraction of all comments for every single video is intractable, we will need to stimulate the total play counts with kernel density estimation resort (gamma/exponential kernel with heuristic-corrected scale decision). Then the stimulated overall tendency will be demonstrated.
- Create a knowledge graph of related concepts of the topic word (Uploaders  & Tags for native concepts, and extra entities linking to external pedias for the non-natives.).
- **IMPORTANT!** We will provide support for two systems for Visually presenting this software: (i) Local App for running locally - implement a single application with NUI (do all scraping & run all algorithms & generate all diagrams locally). Notice this will require installation of all python development frameworks (including Pytorch, Sklearn, Jieba, WordCloud, bs4, etc.). (ii) Web application for running remotely - Implement a backend server + frontend website for users who are not able to set up the python environment locally.
 
 
### Scope of the project
- Limitations include …
  We don't have a large scope Chinese NLP dataset (neither access to sufficient computational resources) so we won't be able to train a large scale model ourselves. That being said, most of the NLP algorithms will be heuristic-based, statistical-rule-based, instead of learning based. Also, users should expect suboptimal performance because of this lack of resources. 
- Assumptions include …
1. This app only has limited capacity for synchronous request processing, which means we assume at one time there are only 1-2 users using this web app instead of thousands of users using it together. 
2. Collecting exact statistics of comment number variation by date is intractable for popularity variation calculation because it could take thousands of requests for a single video. We will assume the decaying of view counts against time for each single video follows a gamma (or exponential) distribution. We will present the stimulated (instead of precise) results.
 
 
 
 
 
## Brief Timeline
 
### Week 1:
**Xinyu**:
 
(i) Basic Web scraping (single-thread, native) the **comments, tags, Danmaku, commenters info, video info** for search results responded by "综合排序" query topic indicated by the user. (M in MVC)
(ii) Scrape fuzzy search suggestion used by search.bilibili.com. 
(iii) Data storage with MongoDB.
 
**Zihan**:
(i) Local App with NUI, receiving user input and executing scraper to obtain danmaku, tags, and comments of customize number of videos.
(ii) Web App server, dealing with scraping requests from outside and run scraping functions. Send results to frontends.
(iii) Adding functionality of customized search with options (subarea, most danmaku, most recently released).
 
### Week 2：
**Xinyu**: 
(i) Vanilla wordCloud generation. Do initial filtering (excluding stopwords/obvious low quality phrases) using exact matches.
(ii) Support second-hand ranking of video results with either view counts or uploading date. 
(iii) Decide whether or not to consider a video as wordCloud generation candidate using video description/author/tags/title.
(iv) Design the occurrence-time-enhanced total view counts based top-k author ranking algorithm (see rubric for details) and extract top authors for queries.
 
**Zihan**:
(i) Advanced web scraping - multi {processing/threading} for accelerating scraping.
(ii) Implement an internet proxy for scraping to avoid IP getting banned by Bilibili.
(iii) Basic web page front end for showing raw data from results got above 
(without much decoration).
 
### Week 3:   
 
**Xinyu**:
Implement the word cloud generation algorithm and do optimization. Goals: (i) Repetitive words / reduplication words reduction + phrase group + cutting via phrase mining techniques (ii) Apply idea of high quality phrase mining technique to filter out high quality phrases - *Jialu Liu, Mining Quality Phrases from Massive Text Corpora, 2015*  (iii) Carry out case studies to demonstrate the performance of the new improvements. i.e. compare algorithm-corrected wordCloud v.s. raw generation results. Aparat from above, implement the stimulated popularity variation of query word via kernel density estimation algorithm (see rubrics-week3 for details.) 
 
**Zihan**:
(i) Complete Web App frontend and Local App NUI, support new functions like showing fuzzy search selection and top k uploaders search.
(ii) Add buttons with onclick functions to video scraping options (subarea, most danmaku, most recently released).
 
 
 
### Week 4:
 
**Xinyu**
(i) Differentiate native Bili concepts (Uploaders) from external entities
(ii) Do named entity recognition in scraping results and generate related concepts recommendation using distant supervision (Possible sources: Baidu Encyclopedia, Moegirl Encyclopedia, WikiPedia).
(iii) Attempt to link tags/authors, as well as surface mentions in corpus to remote encyclopedias. 
(iv) Generate knowledge graph based on previously detected entities via different weight algorithms for native/non-native concepts.
 
**Zihan**:
(i) Visualization of all data obtained from the backend.
(ii) Adding interactivity to visualizations.(e.g. Line charts with nodes can show pop-ups when moving the mouse on it.)
(iii) Adding decorations to Web App and Local App. 
  
 
## Rubrics
 
### Week 1
#### Xinyu:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Scraper for Video Search Results Pages |  6  |  +1: Constructing url & Scraping one page of candidate videos urls on the search result page (e.g. https://search.bilibili.com/all?keyword=%E5%8E%9F%E7%A5%9E) based on users' query and selection of subareas. <br> +2 = 0.5*4: Collecting the author & author url & view count & uploading date on each search result page. <br> +1: Convert the string view count (Scrape result will be in format of '45.1万') to integers, and do tie breaking based on uploading date. <br> +1: Support iterating through multiple search result pages and collecting the above information.  <br> +1: Logging progress report. |
| Scraper for a Single Video Page | 5 | <br> +2: For each video url, visit the source video page (e.g. https://www.bilibili.com/video/BV1Av411a7hG), and extract 'av', 'oid', description, title, tags of the video. <br> +1: Leverage 'oid' to make requests to bili danmaku api (e.g. https://api.bilibili.com/x/v1/dm/list.so?oid=314043632), parse the response JSON and do decoding. <br> +1: Leverage 'av' of video to make requests to bili comments api (e.g. https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid=203963327). Properly Extract comment content and sex of commenters. <br> +1: Error handling for corner cases (e.g. video has multiple authors).|
|  Scraper for Fuzzy Search |  2  | +1: Recognize the url construction rule for mapping user query to related keywords suggestion by search.bilibili.com. +1: Parse the response JSON by search.bilibili.com, and correctly decode suggestion results (raw JSON is written in utf-8 string, i.e. \u8585). |
|  Database |  2  | +1: Correctly set up a database (MongoDB) <br> +1: Correctly manage data collections in database (store, delete, update, etc.) | 
|  Unit Test |  10  |  0: Didn't implement tests <br> +0.5/testcase|
 
 
#### Zihan:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Local App NUI: Basic Views| 5 | +1: Welcome + user query screen (input box, submit) <br> +1: Instruction screen (function explanation) <br> +2: enables users to actually start one round of scraping using local App, report error if input is illegal <br> +1: Presenting locally stored scraping results on screen in raw format |
| Customize Scraping Options (option words passed into search bar together) | 3 | +1: Enable scraping videos in a given subarea <br> +1: Enable scraping videos in sort of most recently released <br> +1: Enable scraping videos in sort of having most danmaku |
| Backend Server for Web Application | 7 | +1: Server can receive scrape (GET/POST) requests from frontends. <br> +2: Correctly routing requests to one of the five roots (corresponding to 5 functionalities) <br> +1: Server reports error when user’s input for scraping is illegal. <br> +2: Server can run legal scraping commands and return results <br> +1: Correctly sending scraping results to frontend |
|  Unit Test | 5 |  0: Didn't implement tests <br> +0.5/testcase|
|  Manual Test | 5 |  0: Didn't implement tests <br> +1/testcase|
 
 
 
### Week 2
 
#### Xinyu:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Candidate Videos Filtering | 5 | +1: Provide support for second-hand ranking for default video search results ("综合排序" in Bilibili) based on total view counts (most views on top).<br> +1: Provide support for second-hand ranking for default video search results ("综合排序" in Bilibili) based on updation date (latest videos on top).   <br> +2: Leveraging video tags, authors, descriptions collected in week 1 to develop an algorithm evaluating relevance between the video and user's query. <br> +1: Adding consideration for queries with multiple semantic units. (e.g. "美食 王刚"，"故事 王刚" are different people) |
|  Word Cloud Generation |  4  | +2: Successfully generated a frequency-based word cloud with the naive algorithm provided by the wordCloud framework. <br> +1: Provide interface for customizable parameters for generation. <br> +1: Filtering out stop words, low quality words (e.g. 东西，什么, 看来, 1,2,3,...) based on local static word list.|
| Extract Top K Authors | 6 |  +1: Naively get top k authors based on authors' accumulative view counts in all pages of search results. <br> +2: Design the author-occurrence-time v.s. video-weight function, experiment with multiple settings (linear, convex, concave) and pick the one with the most sense. <br> +2: Implement the occurrence-time-enhanced accumulative view counts and filter out the top k authors.  <br> +1: Create a demo on  jupyter notebook to demonstrate the intuition & validity behind the function (If A has one 100w view count video, and B has three 33w view count videos, we should prefer B more). | 
|  Unit Test |  5  |  0: Didn't implement tests <br> +0.5/testcase |
|  Manual Test |  5  |  0: Didn't implement tests <br> +1/testcase |
 
 
#### Zihan:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
|  Advanced Scraping: Proxy | 4 | +1: Successfully config one proxy to do scraping. <br> +1: construct proxy pools containing multiple IPs for scraping to avoid getting banned. <br> +1: deploy proxy pools using ScraPy framework <br> +1: Implement randome sleeping time for requests to avoid got banned |
| Advanced Scraping: Multiprocess/Multithreading | 7 | +1: Successfully applying another process/thread to accelerate scraping. <bt> +2: Support customizable number of process/thread for acceleration. <br> +2: Thread-Safe write and read for scraped results. <br> +2: Distributing proxies to child processes/threads. |
| Web App Frontend | 4 | +1: Homepage for scraping. <br> +1: loading page <br> +1: reserved blank pages for all 5 functionality. <br> +1: page navigation among pages for searching and 5 functionalities. |
|  Unit Test |  5  |  0: Didn't implement tests <br> +0.5/testcase |
|  Manual Test |  5  |  0: Didn't implement tests <br> +1/testcase |
 
### Week 3
 
#### Xinyu:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Designing Kernel Function in Kernel Density Estimation | 5 | +2: Explore and design the kernel to be used in kernel density estimation. Find the reasonable setting of ground-level parameters ( e.g. scale & rate for gamma kernel ) <br> +2: Explore and design the adjustment function for kernel functions parameters based on view-counts-decaying v.s. time. Videos with higher view counts should have lower decaying rate (thus higher right-tail probability), as they are more likely to be selected by recommendation algorithms after the video is first published. <br> +1: Create a demo on jupyter notebook to introduce the intuition behind these magical functions.|
| Statistical Modeling of Video Popularity | 5 | +1: Employ min-max scaling to mapping datetime (video uploading time as  0, today as 1) to the definition range of kernel function <br> +1: calculate the estimated view counts in a given time period using the CDF (cumulative density function) of kernel function. <br> +1: Binning (equal width) video with the unit of month (2018.1 - 2019.1 will be 12 bins). <br> +1: Add video counts into the corresponding binning with proper separation. For example, a video uploaded at 3.15 should have big contributions to  both March and April. <br> +1: Properly store the binned view counts with JSON for later visualization. |
|  Word Cloud Candidates Optimization |  5  |  +2: If there are various cases of repetitive words and reduplications of different length, keep only one of them. (e.g. keep "哈*6" if all of ["哈哈", "哈哈哈", "哈*4",...,"哈*15"] have high frequency) <br> +2: Phrase mining: Implement phrase grouping and cutting algorithm via Bayesian estimation - e.g. "Support Vector Machine" has high frequency implies "Vector Machine" also has high frequency, but we will only want "Support Vector Machine", not "vector machine" <br> +1: Carry out case studies or numerical experiments (ideally with statistical measures) to compare the new generation algorithm with the naive version in week2. |
|  Unit Test |  5  |  0: Didn't implement tests <br> +0.5/testcase |
|  Manual Test |  5  |  0: Didn't implement tests <br> +1/testcase |
 
#### Zihan:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Web App frontend Data Visualization | 6 | +2: Support displaying fuzzy search suggestions in the search page. <br> 1: Support displaying word clouds (generated as jpg in the backend). <br> +1: Support displaying top-k uploaders (generated in frontend). <br> +1: support displaying popularity variation (generated in frontend). <br> +1: Support displaying sex distribution (generated in frontend). |
| Local App Improvement Data Visualizations | 5 | +2: Support displaying fuzzy search suggestions in the search page. <br> +1: Support displaying top-k uploaders. <br> +1: Support displaying sex distribution. <br> +1: Support displaying popularity trend. |
| Adding View Components to Customize Scrape Options| 4 | +1.5: Implement buttons for sub areas in two systems with onclick calls. <br> +1.5: Implement buttons for sorting methods (most recently released/ most danmaku) in two systems with onclick calls. <br> +1: onclick functions work correctly (successfully add options to scraping) |
|  Manual Test | 10 |  0: Didn't implement tests <br> +1/testcase |
 
 
### Week 4
 
#### Xinyu:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Named Entity Recognition |  4  | +1: Recognizing whether user query is a concept native to Bilibili (e.g. Think of the famous uploader "老番茄", he might not be recorded in encyclopedias, but is surely famous in Bili).  <br> +2: Make adaptation of existing NER algorithms (e.g. O-S-B-I-E algorithm) on the comments/danmaku corpus to recognize entities' surface mentions. <br> +1: Filter out high frequency / high co-occurring probability entities for candidates of entity linking. | 
| Scraping Distant Encyclopedia | 4 | +2: Adapt distant supervision (may involve scraping) to do entity linking and confirmation. (Possible sources: Baidu Encyclopedia, Moegirl Encyclopedia, WikiPedia) <br> +1: Retrieve related concepts for a given entity in the encyclopedia. <br> +1: Cache all already-seen entities to speed-up the linking process.|
| Entity linking | 5 | +1: Filter high frequency concepts from tags for a given query. <br> +2: Filter high frequency / linkable authors for a given query. <br> +2: Filter linkable entity surface mentions recognized by NER. |
| Knowledge Graph Node Selection and Storage| 2 | +2: Select nodes for the to-be-generated knowledge graph using tags/uploaders/external-entities with different sets of weights for native/non-native concepts. Store them as adjacency matrices or JSON.| 
| Bonus! | 3 | +3: If a danmaku/comment contains at least one linkable named entity, there's a good chance that it's of higher quality. Thus, we might want to improve its weight in wordCloud generation. However, while applying the entity-weight-enhanced algorithm to a single sentence might be simple, the cruel truth is that the whole corpus is built over 3,000,000 sentences (there are around 60,000 sentences per video, we intend to take around 50 videos), and it's not possible to apply this algorithm to every single sentence (as we intend to build a real-time web application). Therefore, in order to apply this algorithm on an enormous scale, an extra greedy filtering algorithm will have to be invented, and additional speed-up resorts will have to be taken. |
|  Unit Test |  5  |  0: Didn't implement tests <br> +0.5/testcase |
|  Manual Test |  5  |  0: Didn't implement tests <br> +1/testcase |
 
#### Zihan:
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Knowledge Graph Visualization | 2 |  +2: Knowledge graph raw data visualization (in both two systems). |
| Adding Interactivity to Visualizations in Web App only | 8 | +2: Interactive pie chart for sex distribution (e.g. pop-up of detailed data). <br> +2: Add links and avatars to the personal space of top k uploaders. <br> +2: Interactive line chart for popularity trend (e.g. pop-up of viewing counts). <br> +2: Add links to term in wikis, uploader spaces, or search.bilibili.com?keyword={entity} for nodes in knowledge graph. |
| Customize Word Cloud & Related Knowledge Graph | 4 | +2: Enable users to input the customize settings for word clouds (e.g. take input of size, color, number of words contained in graph with a form and sent to the server). <br> +2: Customize settings for knowledge graph. |
| Decoration for Web App and Local App | 1 | +1: Background image and elegant layout: like using modern datatables like MUI-datatable for all tables, adding animation for navigations, and proper sound effects.|
|  Manual Test |  10  |  0: Didn't implement tests <br> +1/testcase |
 
 
## Link to grading calculator: 
 
### Week 1 : 
 
#### Xinyu:
https://docs.google.com/spreadsheets/d/1HowFWr6lE7fuWRW2wdHIYzwukn2m89WyTE-ZnN3mOhg/edit?usp=sharing
 
#### Zihan:
https://docs.google.com/spreadsheets/d/1DK-61jUX-12zbK_hfwbmC4fo0A9XKdu98AHjnMTflXA/edit?usp=sharing
 
### Week 2 : 
 
#### Xinyu:
https://docs.google.com/spreadsheets/d/1NhZ4kISGNYSAjlyF0Nd1KNH-pTQBWEiy9PzeqTGKKA8/edit?usp=sharing
 
#### Zihan:
https://docs.google.com/spreadsheets/d/1PJRyb3rX7Uiijy_WG8cspUBzznsXcurnv6EvIw0XETc/edit?usp=sharing
 
### Week 3 : 
 
#### Xinyu:
https://docs.google.com/spreadsheets/d/1ZHGZCwOFjES2agrI-zr1Uwl5pAafJFgAa1D7aD-SJWA/edit?usp=sharing
 
#### Zihan:
https://docs.google.com/spreadsheets/d/1bH0KuWhgwnRblLogPpOMQmFV_ekAKIqAmYRdqCHDLNs/edit?usp=sharing
 
### Week 4 : 
 
#### Xinyu:
https://docs.google.com/spreadsheets/d/1YnIwzcKKQhbHydR6nkFvC33GnxwJWuLIjApgcCLiueg/edit?usp=sharing
 
 
#### Zihan:
https://docs.google.com/spreadsheets/d/1BwMvr3rzuMm_-LeY34V3mnhMNWYgHl_b-kwKqSEfRBw/edit?usp=sharing
