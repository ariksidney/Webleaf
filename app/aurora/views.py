import json
import requests
from flask_login import login_required, current_user
from flask import render_template, redirect, request, url_for, flash

from .rest.restHandler import RestHandler
from .forms import AddAuroraForm
from ..models import AuroraConfig, User
from . import aurora
from .. import db
import ast

rest = RestHandler()


@aurora.route('/')
@login_required
def aurora_overview():
    auroras = AuroraConfig.query.filter(AuroraConfig.user_id == current_user.id).order_by(AuroraConfig.name).all()
    for aurora_obj in auroras:
        aurora_obj.status = rest.get_status(aurora_obj.ip_address, aurora_obj.port, aurora_obj.token)
        if aurora_obj.status != 'Unknown':
            aurora_obj.effects = rest.get_all_effects(aurora_obj.ip_address, aurora_obj.port, aurora_obj.token)
            aurora_obj.selected_effect = rest.get_selected_effect(aurora_obj.ip_address, aurora_obj.port, aurora_obj.token)
            aurora_obj.brightness = rest.get_brightness(aurora_obj.ip_address, aurora_obj.port, aurora_obj.token)
    return render_template('aurora/overview.html', auroras=auroras)


@aurora.route('/add', methods=['GET', 'POST'])
@login_required
def add_aurora():
    form = AddAuroraForm()
    if form.validate_on_submit():
        if not form.token.data:
            token = rest.get_auth_token(form.ip.data, form.port.data)
            form.token.data = token
            return render_template('aurora/add.html', form=form)
        aurora = AuroraConfig(name=form.name.data, ip_address=form.ip.data, port=form.port.data, token=form.token.data,
                              user=current_user._get_current_object())
        if aurora is not None:
            db.session.add(aurora)
            return redirect(request.args.get('next') or url_for('.aurora_overview'))
        flash('successfully added aurora')
        return redirect(url_for(".aurora_overview"))
    return render_template('aurora/add.html', form=form)


@aurora.route('/turn-on/<ip_address>&<port>&<token>',  methods=['GET', 'POST'])
@login_required
def aurora_on(ip_address, port, token):
    rest.turn_on(ip_address, port, token)
    return '', 204


@aurora.route('/turn-off/<ip_address>&<port>&<token>',  methods=['GET', 'POST'])
@login_required
def aurora_off(ip_address, port, token):
    rest.turn_off(ip_address, port, token)
    return '', 204


@aurora.route('/set-effect/<aurora_effect>',  methods=['GET', 'POST'])
@login_required
def set_effect(aurora_effect):
    aurora_effect = ast.literal_eval(aurora_effect)
    rest.set_effect(aurora_effect[0], aurora_effect[1], aurora_effect[2], aurora_effect[3])
    return redirect(url_for(".aurora_overview"))


@aurora.route('/set-brightness',  methods=['POST'])
@login_required
def set_brightness():
    rest.set_brightness(request.form['ip_address'], request.form['port'], request.form['token'], request.form['brightness'])
    return redirect(url_for(".aurora_overview")), 204
