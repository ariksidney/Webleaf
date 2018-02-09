from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import core


@core.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('aurora.aurora_overview'))


@core.route('/offline.html')
def offline():
    return core.send_static_file('offline.html')


@core.route('/service-worker.js')
def sw():
    return core.send_static_file('service-worker.js')
