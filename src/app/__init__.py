import os
from flask import Flask
from .WordGenerator import *

path = os.path.dirname(__file__)

app = Flask('syllable-shaker', template_folder=os.path.join(path, 'templates'))
generator = WordGenerator.FromFile(os.path.join(path, 'data/syllables.csv'))

from app import routes, errors