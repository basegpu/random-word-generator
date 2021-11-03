from csv import reader
import random

from .utils import log_to_console

class WordGenerator:

    _syllables = {}

    def __init__(self, syllableList):
        for syll in syllableList:
            n = len(syll)
            self._syllables.setdefault(n, []).append(syll)
        log_to_console(self._syllables)
    
    @classmethod
    def FromFile(cls, filename):
        log_to_console('loading syllables from ' + filename)
        # open file in read mode
        with open(filename, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj, skipinitialspace=True, delimiter=',')
            # Iterate over each row in the csv using reader object
            syllableList = []
            for row in csv_reader:
                syllableList += row
        return cls(syllableList)

    @classmethod
    def MakeWord(cls, configDict, capitalize):
        selection = []
        for nC,nS in configDict.items():
            if nC in cls._syllables:
                s = cls._syllables[nC]
                for i in range(nS):
                    selection.append(random.choice(s))
        random.shuffle(selection)
        word = ''.join(selection)
        if len(word) == 0:
            raise Exception('no success in word generation - reconfig!')
        return word if capitalize == 'no' else word.upper()

    @staticmethod
    def DecodeConfig(config):
        configDict = {}
        for g in config.split('-'):
            nC,nS = g.split(':')
            configDict[int(nC)] = int(nS)
        return configDict