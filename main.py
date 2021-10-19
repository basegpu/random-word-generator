from flask import Flask, render_template
from csv import reader
import sys, random

app = Flask('random-word-generator')

@app.route('/')
def index():
    genWord = make_word(SYLLABLES, {N_CHARS: N_SYLLABLES})
    # Render HTML with count variable
    return render_template("index.html", word=genWord)


def load_syllables(filename):
    syllables = {}
    # open file in read mode
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj, skipinitialspace=True, delimiter=',')
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            for syll in row:
                n = len(syll)
                syllables.setdefault(n, []).append(syll)
    return syllables

def make_word(syllables, n):
    selection = []
    for nC,nS in n.items():
        for i in range(nS):
            selection.append(random.choice(syllables[nC]))
    random.shuffle(selection)
    word = ''
    for s in selection:
        word += s
    return word

def log_to_console(msg):
    print(msg, file=sys.stderr)

# init stuff
DATAFILE = 'syllables.csv'
N_CHARS = 2
N_SYLLABLES = 2
log_to_console('loading syllables from ' + DATAFILE)
SYLLABLES = load_syllables(DATAFILE)
log_to_console(SYLLABLES)

if __name__ == '__main__':
    app.run()