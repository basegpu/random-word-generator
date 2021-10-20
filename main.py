from flask import Flask, render_template, redirect, url_for, request
from csv import reader
import sys, random

app = Flask('random-word-generator')


@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        config = request.form['config']
        fadeout = float(request.form['fadeout'])*1000
        return redirect(url_for('next_word', config=config, fadeout=fadeout))
    else:
        return render_template('index.html')

@app.route("/next/<config>/<fadeout>")
def next_word(config, fadeout):
    configDict = {}
    for g in config.split('-'):
        nC,nS = g.split(':')
        configDict[int(nC)] = int(nS)
    genWord = make_word(SYLLABLES, configDict)
    return render_template('word.html', word=genWord, templateConfig=config, templateFadeout=fadeout);

def make_word(syllables, config):
    selection = []
    for nC,nS in config.items():
        if nC in syllables:
            s = syllables[nC]
            for i in range(nS):
                selection.append(random.choice(s))
    random.shuffle(selection)
    return ''.join(selection)

def log_to_console(msg):
    print(msg, file=sys.stderr)

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

# init stuff
DATAFILE = 'syllables.csv'
log_to_console('loading syllables from ' + DATAFILE)
SYLLABLES = load_syllables(DATAFILE)
log_to_console(SYLLABLES)

if __name__ == '__main__':
    app.run(debug = True)