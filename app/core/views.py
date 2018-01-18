from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import core
from ..aurora import aurora


@core.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('aurora.aurora_overview'))
