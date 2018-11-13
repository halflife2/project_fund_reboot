
from __future__ import print_function
from lexrankr import LexRank
from konlpy.tag import Twitter
import re
file = open('output.txt','r')
read = file.readline()
your_text_here = ''

while read:
    your_text_here += read
    read = file.readline()

def wordRank(text):
    text = text.replace('\\n','.')
    new = re.sub('[^가-힝0-9a-zA-Z\\s\\.]', '', text)

    lexrank = LexRank()
    lexrank.summarize(new)
    summaries = lexrank.probe(3)
    word = Twitter()
    out = []
    for summary in summaries:
        out += word.nouns(summary)

    out = list(set(out))
    print(out)

wordRank(your_text_here)
file.close()