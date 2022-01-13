from flask import Flask, render_template, redirect, url_for, request, send_file
from werkzeug.exceptions import *
from syllable_shaker import app, generator
from .utils import *

@app.route("/" ,methods = ['POST', 'GET'])
@app.route("/index", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        #TODO: check validity
        config = request.form['config']
        fadeout = float(request.form['fadeout'])*1000
        capitalize = 'yes' if request.form.get('capitalize') else 'no'
        page = 'make_code' if request.form.get('qr') else 'next_word'
        url = url_for(page, config=config, score=0, fadeout=fadeout, capitalize=capitalize)
        log_to_console('starting session: ' + url)
        return redirect(url)
    else:
        return render_template('index.html')

@app.route("/next/<config>/<score>")
@app.route("/next/<config>/<score>/<fadeout>")
@app.route("/next/<config>/<score>/<fadeout>/<capitalize>")
def next_word(config, score, fadeout=0.0, capitalize='no'):
    try:
        newScore = int(score) + 1
        genWord, genCode = generator.MakeWord(config, capitalize)
    except Exception as e:
        raise BadRequest(e)
    return render_template('word.html',
        templateCode=genCode,
        word=genWord,
        templateConfig=config,
        templateScore=newScore,
        templateFadeout=fadeout,
        templateCapitalize=capitalize);

@app.route("/repeat/<code>/<config>/<score>")
@app.route("/repeat/<code>/<config>/<score>/<fadeout>")
@app.route("/repeat/<code>/<config>/<score>/<fadeout>/<capitalize>")
def same_word(code, config, score, fadeout=0.0, capitalize='no'):
    try:
        newScore = int(score) - 1
        genWord = generator.MakeWordFromCode(code, capitalize)
    except Exception as e:
        raise BadRequest(e)
    return render_template('word.html',
        templateCode=code,
        word=genWord,
        templateConfig=config,
        templateScore=newScore,
        templateFadeout=fadeout,
        templateCapitalize=capitalize);

@app.route("/code/<config>/<fadeout>/<capitalize>")
def make_code(config, fadeout, capitalize):
    address = request.host_url + url_for('next_word', config=config, fadeout=fadeout, capitalize=capitalize)
    img_io = make_qr_code(address)
    return send_file(img_io, mimetype='image/png')