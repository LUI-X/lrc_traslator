from googletrans import Translator
translator = Translator()


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
                if line != '\n':
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

    def getArabize(self, traductionData):
        arabize = " "

        for item in traductionData:
            try:
                if 'None' != item[3]:
                    arabize = item[3]
            except:
                pass
        return arabize
        pass

    def getReverseArabize(self, arabize):
        leftArabize = []
        list_arabize = arabize.split()
        rightArabize = list_arabize[::-1]

        for word in rightArabize:
            list_letters = list(word)
            reversed_letters = list_letters[::-1]
            reversedWord = "".join(reversed_letters)
            reversedWord = reversedWord + " "
            leftArabize.append("".join(reversedWord))
        return " ".join(rightArabize), " ".join(leftArabize)
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

                return nextMinute+1, nextSecond, nextMillisecond
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
            traductionData = traduccion.extra_data["translation"]
            arabize = self.getArabize(traductionData)
            arabize = self.getReverseArabize(arabize)

            self.newLyrics.extend(('[' + minutes + ':' + seconds + '.' + milliseconds + ']' + lyrics.rstrip("\n") + ' ←'))
            self.newLyrics.extend(('\n'))

            nextTime = self.getNextTime(key)
            timeTra = self.setTime(nextTime[0], nextTime[1], nextTime[2])
            timeLara = self.setTime(timeTra[0], timeTra[1], timeTra[2])
            timeRara = self.setTime(timeLara[0], timeLara[1], timeLara[2])


            self.newLyrics.extend(('[' + timeLara[0] + ':' + timeLara[1] + '.' + timeLara[2] + ']' + arabize[1] + '←'))
            self.newLyrics.extend(('\n'))
            self.newLyrics.extend(('[' + timeRara[0] + ':' + timeRara[1] + '.' + timeRara[2] + ']' + "→ " + arabize[0]))
            self.newLyrics.extend(('\n'))
            self.newLyrics.extend(('[' + timeTra[0] + ':' + timeTra[1] + '.' + timeTra[2] + ']' + traduccion.text))
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




titleLrc = 'files/Frozen - Let It Go (Arabic) w Lyrics + Translation - أطلقي سرك.lrc'

mylrcfile = LrcFile(titleLrc)
mylrcfile.getLines()
mylrcfile.getTimeAndLyrics()
mylrcfile.writeLrcFile()


