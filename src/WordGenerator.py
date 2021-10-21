from csv import reader
import random

from utils import log_to_console

class WordGenerator:

    _syllables = {}
    
    def __init__(self, filename):
        log_to_console('loading syllables from ' + filename)
        # open file in read mode
        with open(filename, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj, skipinitialspace=True, delimiter=',')
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                for syll in row:
                    n = len(syll)
                    self._syllables.setdefault(n, []).append(syll)
        log_to_console(self._syllables)

    def MakeWord(self, config, capitalize):
        selection = []
        for nC,nS in config.items():
            if nC in self._syllables:
                s = self._syllables[nC]
                for i in range(nS):
                    selection.append(random.choice(s))
        random.shuffle(selection)
        word = ''.join(selection)
        return word if capitalize == 'no' else word.upper()