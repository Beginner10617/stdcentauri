from flask import Blueprint, render_template
import os
from dotenv import load_dotenv
load_dotenv()
index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')

