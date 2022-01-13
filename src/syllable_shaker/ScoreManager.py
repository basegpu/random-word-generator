from .utils import log_to_console

class ScoreManager:

    _sep = ':'    

    def __init__(self, score):
        comp = score.split(self._sep)
        if len(comp) != 2:
            raise Exception('bad score format.')
        s = []
        for c in comp:
            try:
                s.append(int(c))
            except:
                raise Exception('bad score format - must all be integers.')
        self.Fails = s[0]
        self.Success = s[1]

    def GetScore(self):
        return "%i%c%i"%(self.Fails, self._sep, self.Success)

    def Succeeded(self):
        self.Success += 1

    def Failed(self):
        self.Fails += 1
