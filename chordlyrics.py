# this is a program to combine automatic chord transcription and lyrics
# run it such as "python chordlyrics.py lyricsfile chordannotationfile outfile"
# for example run:
# python chordlyrics.py aihenjiandan.lrc aihenjiandan.txt aihenjiandan.ch
# written by tangkk

import sys
inlyrics = sys.argv[1]
inchords = sys.argv[2]
outsheet = sys.argv[3]

def get_sec(s):
    l1,l2 = s.split(':')
    l21,l22 = l2.split('.')
    ret = float(l1) * 60 + float(l21) * 1 + float(l22)*0.6 / 100
    return ret

# TODO: 1. sort the lyrics in terms of secs; 2. expand lyrics when there're multiple secs
# 3. ignore irrelavant information
def readlyrics(inlyrics):
    title = ''
    seclist = []
    lylist = []
    f = open(inlyrics, encoding="utf8")
    for line in f:
        sps = line.split(']')
        
        if len(sps)==2 and sps[0].find('ti') == 1:
            _,title = sp1.split(':')
        elif len(sps)>=2 and len(sps[1])!=0:
            # append every sec and lyrics
            ly = sps[-1]
            for i in range(len(sps)-1):
                sp1 = sps[i]
                sec = get_sec(sp1[1:])
                seclist.append(sec)
                lylist.append(ly)
    f.close()
    # sort seclist and lylist in terms of seclist
    argsortidx = sorted(range(len(seclist)), key=lambda k: seclist[k])
    newseclist = sorted(seclist)
    newlylist = [lylist[i] for i in argsortidx]
    
    return title, newseclist, newlylist

# note that the annotation does not fill the end time (only start time and the chord, separated by \t)
def readchords(inchords):
    seclist = []
    chlist = []
    f = open(inchords, encoding="utf8")
    for line in f:
        sp1,sp2 = line.split('	')
        seclist.append(float(sp1))
        chlist.append(sp2)
        
    f.close()
    return seclist, chlist
    
# main script
title, lyseclist, lylist = readlyrics(inlyrics)
chseclist, chlist = readchords(inchords)

chcount = 0
if len(title) == 0:
    outstr = ''
else:
    outstr = title + '\n'
# the chord of this line of lyrics appears before the next line of lyrics
for i in range(len(lyseclist)-1):
    curlysec = lyseclist[i]
    nextlysec = lyseclist[i+1]
    curly = lylist[i]
    nextly = lylist[i+1]
    curline = ''
    linebreak = 0
    while chcount < len(chseclist):
        j = chcount
        curchsec = chseclist[j]
        curch = chlist[j]
        if curchsec >= curlysec and curchsec < nextlysec:
            chcount += 1
            curline += curch.strip()
            curline += ' | '
            linebreak += 1
        elif curchsec < curlysec:
            chcount += 1
            linebreak = 0
        else:
            linebreak -= 1
            break
    if linebreak >= 0:
        curline += '\n'
    curline += curly
    # if linebreak >= 0:
        # curline += '\n'
    outstr += curline
    

fw = open(outsheet,'w', encoding="utf8")
fw.write(outstr)
fw.close()
    
    
    
    
    
    
    
    
    
    