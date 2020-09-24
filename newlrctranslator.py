from googletrans import Translator
import pykakasi

translator = Translator()

"""
ID TAGS

[ar: Lyrics artist]
[al: Album where the song is from]

[ti: Lyrics(song) title]

[au: Creator of the Songtext]
[length: How long the song is]
[by: Creator of the LRC file]

[offset: + / - Overall timestamp adjustment in milliseconds, + shifts time up, - shiftsdown]

[re: The player or editor that created the LRC file]

[ve: version of theprogram]

## [00:10.33]Des amours meurent, des amours naissent

"""

## error al final del archivo, espacio en blanco, ultima linea
# extraer, modificar y crear cabezara del archivo
#modificar exafit del archivo
class LrcFile:

    def __init__(self, lrc_name):

        self.lrc_name = lrc_name
        self.dict_lines = {}
        self.timeAndLyricsList = []
        self.keyAndList = {}
        self.newLyrics = []

    def getLines(self):

        with open(self.lrc_name, 'r+') as MyFile:
            keyIndex = 0

            for line in MyFile:
                keyIndex += 1
                self.dict_lines.update({keyIndex: line})

        return self.dict_lines

        MyFile.close()
        pass

    def getTimeAndLyrics(self):
        for key,  line in self.dict_lines.items():
            if len(line) != 1:
                if 9 == line.find(']'):
                    splitedLine = line.partition(']')
                    time = splitedLine[0]
                    lyrics = splitedLine[2]
                    myTime = time.split(':')
                    minutes = myTime[0]
                    mytime2 = myTime[1]
                    mytime3 = mytime2.split('.')
                    seconds = mytime3[0]
                    milliseconds = mytime3[1]

                    self.timeAndLyricsList.extend((minutes, seconds, milliseconds, lyrics))
                    self.keyAndList[key] = self.timeAndLyricsList.copy()
                    self.timeAndLyricsList.clear()
        return self.keyAndList
        pass

    def setJpConvertor(self):

        setConvertor = pykakasi.kakasi()
        setConvertor.setMode("H", "a")  # Hiragana to ascii, default: no conversion
        setConvertor.setMode("K", "a")  # Katakana to ascii, default: no conversion
        setConvertor.setMode("J", "a")  # Japanese to ascii, default: no conversion
        setConvertor.setMode("r", "Hepburn")  # default: use Hepburn Roman table
        setConvertor.setMode("s", True)  # add space, default: no separator
        setConvertor.setMode("C", True)  # capitalize, default: no capitalize

        jpConvertor = setConvertor.getConverter()
        return jpConvertor
        pass

    def jpTokenizer(self, lyrics):

        wakati = pykakasi.wakati()
        kanjiTokenizer = wakati.getConverter()
        kajiTokenized = kanjiTokenizer.do(lyrics)

        return kajiTokenized
        pass

    def jpConvertor(self, lyrics):

        jpConvertor = self.setJpConvertor()
        jpConverted = jpConvertor.convert(lyrics)
        katakana = ''
        hiragana = ''

        for item in jpConverted:
            katakana = katakana + ' ' + item['kana']
            hiragana = hiragana + ' ' + item['hira']
        myJpTuple = (katakana, hiragana)
        return myJpTuple

        pass

    def getNextTime(self, key):
        for nextkey, list in self.keyAndList.items():
            if key+1 == nextkey:
                nextMinute = list[0].replace('[', '')
                nextSecond = list[1]
                nextMillisecond = list[2]

                return nextMinute, nextSecond, nextMillisecond

            lastKey = sorted(self.keyAndList.keys())[-1]

            if key == lastKey:
                list = self.keyAndList.get(key)
                nextMinute = int(list[0].replace('[', ''))
                nextSecond = int(list[1])
                nextMillisecond = int(list[2])

                return nextMinute+1, nextSecond , nextMillisecond
        pass

    def setTime(self, minutes, seconds, milliseconds):
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int(milliseconds)
        milliseconds -= 1

        if milliseconds == -1:
            if seconds == 00:
                minutes -= 1
                seconds = 59
                milliseconds = 00
            else:
                milliseconds = 99
        return str("%02d" % minutes), str("%02d" % seconds), str("%02d" % milliseconds)
        pass

    def orderLines(self):
        for key, list in self.keyAndList.items():
            minutes = list[0].replace('[', '')
            seconds = list[1]
            milliseconds = list[2]
            lyrics = list[3]

            traduccion = translator.translate(lyrics, dest='es')

            self.newLyrics.extend(('[' + minutes + ':' + seconds + '.' + milliseconds + ']' + lyrics))
            nextTime = self.getNextTime(key)
            timeTra = self.setTime(nextTime[0], nextTime[1], nextTime[2])

            self.newLyrics.extend(('[' + timeTra[0] + ':' + timeTra[1] + '.' + timeTra[2] + ']' + "(" + traduccion.text + ")"))
            self.newLyrics.extend(('\n'))
            self.newLyrics.extend(('\n'))
            pass

    def writeLrcFile(self):
        MyFileToWrite = open(self.lrc_name + '.lrc', 'w+')
        self.orderLines()

        for line in self.newLyrics:
            MyFileToWrite.write(line)
        MyFileToWrite.close()
        print("lrc created successfully")
    pass


titleLrc = "files/lrc/g/Till Lindemann ft' Apocalyptica - Helden.lrc"

mylrcfile = LrcFile(titleLrc)

mylrcfile.getLines()
mylrcfile.getTimeAndLyrics()
mylrcfile.writeLrcFile()
