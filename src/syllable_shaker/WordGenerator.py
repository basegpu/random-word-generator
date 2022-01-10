from csv import reader
import random

from .utils import log_to_console

class WordGenerator:

    def __init__(self, syllableList):
        if len(syllableList) == 0:
            raise Exception('no list with syllables provided.')
        self._syllables = {}
        for syll in syllableList:
            n = len(syll)
            self._syllables.setdefault(n, []).append(syll)
        log_to_console(self._syllables)
    
    def FromList(syllableList):
        return WordGenerator(syllableList)

    def FromFile(filename):
        log_to_console('loading syllables from ' + filename)
        # open file in read mode
        with open(filename, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj, skipinitialspace=True, delimiter=',')
            # Iterate over each row in the csv using reader object
            syllableList = []
            for row in csv_reader:
                syllableList += row
        return WordGenerator(syllableList)

    def MakeWord(self, config, capitalize):
        configDict = DecodeConfig(config)
        code = self.MakeCodeFromConfig(configDict)
        return (self.MakeWordFromCode(code, capitalize), code)

    def MakeCodeFromConfig(self, configDict):
        code = []
        for nC,nS in configDict.items():
            if nC in self._syllables:
                s = self._syllables[nC]
                for i in range(nS):
                    code.append('%i.%i'%(nC, random.randint(0, len(s)-1 )))
        random.shuffle(code)
        return '-'.join(code)

    def MakeWordFromCode(self, code, capitalize):
        word = ''
        for s in code.split('-'):
            nC, pos = s.split('.')
            word += self._syllables[int(nC)][int(pos)]
        if len(word) == 0:
            raise Exception('no success in word generation - reconfig!')
        return word if capitalize == 'no' else word.upper()


def DecodeConfig(config):
    configDict = {}
    for g in config.split('-'):
        nC,nS = g.split(':')
        configDict[int(nC)] = int(nS)
    return configDict