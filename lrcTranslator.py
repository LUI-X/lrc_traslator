from googletrans import Translator
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
class LrcFile:

    def __init__(self, lrc_name):

        self.lrc_name = lrc_name

    def openlrc(self):

        self.lrc_name

        MyLrc = open(self.lrc_name, 'r+')
        self.MyLrc = MyLrc

        return MyLrc

        pass

    def getLrcDict(self):

        self.timeAndLyrics = {}

        for line in self.MyLrc:

            if len(line) != 1:

                if 9 == line.find(']'):

                    splitedLine = line.partition(']')

                    self.timeAndLyrics[splitedLine[0]] = splitedLine[2]

        return (self.timeAndLyrics)

        pass

    def createLrcFile(self):

        MyFileToWrite = open(self.lrc_name, 'w+')

        for time, lyrics in self.timeAndLyrics.items():


            MyFileToWrite.write(time + ']'+lyrics)

            splitedTime = time.partition('.')

            traduccion = translator.translate(lyrics, dest='es')

            MyFileToWrite.write((splitedTime[0] + '.' + str(int(splitedTime[2])+1)+']' + "(" + traduccion.text + ")"))

            MyFileToWrite.write('\n')
            MyFileToWrite.write('\n')

        MyFileToWrite.close()
        return


    pass




titleLrc = "files/eros-ramazzotti-unaltra-teotra-como-tu.lrc"

mylrcfile = LrcFile(titleLrc)

mylrcfile.openlrc()
mylrcfile.getLrcDict()
mylrcfile.createLrcFile()


