# encoding=utf-8

from flask import (
    Blueprint, flash, g, redirect, request, current_app as app, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('hello', __name__)


@bp.route('/')
def index():
    return "hello world"
