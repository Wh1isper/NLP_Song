from main import songListFile,tf_idfFile,Song
import pickle
from pyecharts import WordCloud, Page, Style
import os
import re
from tqdm import tqdm

WORD_CLOUD_PATH = './worldCloud'

def read_data():
    with open(songListFile,'rb') as f:
        songList = pickle.load(f)
    with open(tf_idfFile,'rb') as f:
        tf_idfList = pickle.load(f)
    for i in range(len(songList)):
        songList[i].text = tf_idfList[i]
    return songList,tf_idfList

def creat_charts(name, key_value):
    page = Page()

    style = Style(
        width=1100, height=600
    )
    chart = WordCloud(name,**style.init_style)
    key,value = [x[0] for x in key_value], [x[1] for x in key_value]
    chart.add("", key, value, word_size_range=[30,100], rotate_step=66)
    page.add(chart)

    return page

def divisionSong(songList):
    pattern = r'[^a-zA-z0-9]'
    for song in songList:
        song.song = re.sub(pattern,' ',song.song)

    return songList


if __name__ == '__main__':
    songList, tf_idfList = read_data()
    songList = divisionSong(songList)

    for song in tqdm(songList):
        path = os.path.join(WORD_CLOUD_PATH,song.song)
        creat_charts(song.song, song.text).render(path=path+".html")
    print("词云构建完成")