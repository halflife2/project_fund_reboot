from konlpy.tag import Twitter

def wordanaly(filename):
    meceb = Twitter()
    file = open(filename,'r')
    out = open("output_nouns.txt",'w')
    outstr = ""
    while True:
        line = file.readline()
        if not line: break
        outstr += ", ".join(meceb.nouns(line))
    out.write(outstr)
    file.close()
    out.close()

wordanaly("output.txt")

