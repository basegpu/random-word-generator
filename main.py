from flask import Flask, render_template, redirect, url_for, request, send_file
from csv import reader
import sys, random, io
import qrcode

app = Flask('random-word-generator')


@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        #TODO: check validity
        config = request.form['config']
        fadeout = float(request.form['fadeout'])*1000
        capitalize = 'yes' if request.form.get('capitalize') else 'no'
        page = 'make_code' if request.form.get('qr') else 'next_word'
        url = url_for(page, config=config, fadeout=fadeout, capitalize=capitalize)
        log_to_console('calling ' + url)
        return redirect(url)
    else:
        return render_template('index.html')

@app.route("/next/<config>")
@app.route("/next/<config>/<fadeout>")
@app.route("/next/<config>/<fadeout>/<capitalize>")
def next_word(config, fadeout=0.0, capitalize='no'):
    configDict = {}
    for g in config.split('-'):
        nC,nS = g.split(':')
        configDict[int(nC)] = int(nS)
    genWord = make_word(SYLLABLES, configDict, capitalize)
    return render_template('word.html', word=genWord, templateConfig=config, templateFadeout=fadeout, templateCapitalize=capitalize);

@app.route("/code/<config>/<fadeout>/<capitalize>")
def make_code(config, fadeout, capitalize):
    address = request.host_url + url_for('next_word', config=config, fadeout=fadeout, capitalize=capitalize)
    img = qrcode.make(address)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=60)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def make_word(syllables, config, capitalize):
    selection = []
    for nC,nS in config.items():
        if nC in syllables:
            s = syllables[nC]
            for i in range(nS):
                selection.append(random.choice(s))
    random.shuffle(selection)
    word = ''.join(selection)
    return word if capitalize == 'no' else word.upper()

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