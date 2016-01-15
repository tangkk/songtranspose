# this is a program to combine automatic chord transcription and lyrics
# run it such as "python chordlyrics.py inlyricsfile inchordfile outfile"
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

def readlyrics(inlyrics):
    title = ''
    seclist = []
    lylist = []
    f = open(inlyrics, encoding="utf8")
    for line in f:
        sp1, sp2 = line.split(']')
        if sp1.find('ti') == 1:
            _,title = sp1.split(':')
        else:
            sec = get_sec(sp1[1:])
            ly = sp2
            seclist.append(sec)
            lylist.append(ly)
            
    f.close()
    return title, seclist, lylist
    
def readchords(inchords):
    seclist = []
    chlist = []
    f = open(inchords, encoding="utf8")
    for line in f:
        sp1,sp2,sp3 = line.split(' ')
        seclist.append(float(sp1))
        chlist.append(sp3)
        
    f.close()
    return seclist, chlist
    
# main script
title, lyseclist, lylist = readlyrics(inlyrics)
chseclist, chlist = readchords(inchords)

chcount = 0
outstr = title + '\n'
# the chord of this line of lyrics appears before the next line of lyrics
for i in range(len(lyseclist)-1):
    curlysec = lyseclist[i]
    nextlysec = lyseclist[i+1]
    curly = lylist[i]
    nextly = lylist[i+1]
    curline = ''
    while chcount < len(chseclist):
        j = chcount
        curchsec = chseclist[j]
        curch = chlist[j]
        if curchsec >= curlysec and curchsec < nextlysec:
            chcount += 1
            curline += curch.strip()
            curline += ' | '
        else:
            break
    curline += '\n'
    if len(curly.strip()) == 0:
        curly = 'Intro\n'
    curline += curly
    curline += '\n'
    outstr += curline
    

fw = open(outsheet,'w', encoding="utf8")
fw.write(outstr)
fw.close()
    
    
    
    
    
    
    
    
    
    