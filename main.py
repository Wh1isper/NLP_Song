import os
import re
import csv
import math
import pickle
from tqdm import trange,tqdm
from nltk.stem import WordNetLemmatizer

songListFile = 'songList.pic'
tf_idfFile = 'tf-idf.pic'
DATAPATH = './songlyrics'
DATANAME = 'songdata.csv'
STOPWORD = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves','ah',
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him','could',
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its','ever',
            'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
            'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am','mine',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
            'and','but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
            'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
            'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
            'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
            'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
            'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
            'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
            'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn','oh']
# from nltk.corpus import stopwords
# words = stopwords.words('english')
# print(words)


class Song():
    def __init__(self,artist,song,link,text):
        self.artist = artist
        self.song = song
        self.link = link
        self.text = text

def initSongList():
    dataFile = os.path.join(DATAPATH, DATANAME)
    content = []
    songList = []
    songNum = -1
    with open(dataFile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for item in reader:
            content.append(item)
    for song in content:
        songNum = songNum + 1
        if songNum == 0:
            continue
        songList.append(Song(song[0], song[1], song[2], song[3]))
    print("总共处理歌曲:{}".format(songNum))
    return songList

def division(targ):
    lemmatizer = WordNetLemmatizer()
    pattern = r'[a-zA-Z]+'
    targ = re.findall(pattern, targ)
    i = 0
    while (i < len(targ)):
        targ[i] = targ[i].lower()
        targ[i] = lemmatizer.lemmatize(targ[i], pos='v')
        if targ[i] in STOPWORD or len(targ[i]) == 1:
            targ.pop(i)
        else:
            i = i+1
    return targ

if __name__ == '__main__':
    tf_idfList = []
    wordInSong = {}
    songList = []
    if os.path.exists(songListFile):
        with open(songListFile, 'rb') as f:
            songList = pickle.load(f)
        print("分词文件读取完毕")
    else:
        songList = initSongList()# 文本读入，预处理
        print("未找到分词后的歌词文件，正在新建")
        for i in tqdm(range(len(songList))): # 文本处理，分词，词性还原（统一为动词）
            songList[i].text = division(songList[i].text)
        with open(songListFile,'wb') as f:
            pickle.dump(songList,f)

    print("开始构建语料库")
    for i in tqdm(range(len(songList))): # 语料库构建
        wordList = []
        for word in songList[i].text:
            if word not in wordList:
                wordList.append(word)
        for word in wordList:
            if word not in wordInSong.keys():
                wordInSong[word] = 1
            else:
                wordInSong[word] = wordInSong[word] + 1
    print("\n正在计算tf-idf值")
    for song in tqdm(songList):
        wordDir = {}
        tf_idfDir = {}
        for word in song.text:
            if word not in wordDir:
                wordDir[word] = 1
            else:
                wordDir[word] = wordDir[word] + 1
        for (word, times) in wordDir.items():
            tf_idfDir[word] = round(times/len(song.text) * math.log(len(songList)/(wordInSong[word]+1)),3)
        tf_idfDir = tf_idfDir.items()
        tf_idfDir = sorted(tf_idfDir, key=lambda x:x[1],reverse=True)[:5]
        tf_idfList.append(tf_idfDir)
    with open(tf_idfFile,'wb') as f:
        pickle.dump(tf_idfList, f)
    print('tf-idf保存完毕')