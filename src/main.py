from flask import Flask, render_template, redirect, url_for, request, send_file

from utils import *
from WordGenerator import *

app = Flask('syllable-shaker', template_folder='../templates')
GENERATOR = WordGenerator('../data/syllables.csv')

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        #TODO: check validity
        config = request.form['config']
        fadeout = float(request.form['fadeout'])*1000
        capitalize = 'yes' if request.form.get('capitalize') else 'no'
        page = 'make_code' if request.form.get('qr') else 'next_word'
        url = url_for(page, config=config, fadeout=fadeout, capitalize=capitalize)
        log_to_console('starting session: ' + url)
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
    genWord = GENERATOR.MakeWord(configDict, capitalize)
    return render_template('word.html', word=genWord, templateConfig=config, templateFadeout=fadeout, templateCapitalize=capitalize);

@app.route("/code/<config>/<fadeout>/<capitalize>")
def make_code(config, fadeout, capitalize):
    address = request.host_url + url_for('next_word', config=config, fadeout=fadeout, capitalize=capitalize)
    img_io = make_qr_code(address)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)