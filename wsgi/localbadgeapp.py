# -*- coding: utf-8 -*-
#
# Copyright © 2015  Patrick Uiterwijk <patrick@puiterwijk.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import os
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy.exc import IntegrityError

BADGE = os.environ['BADGE']
AUTH_KEY = os.environ['AUTH_KEY']
ADMIN_KEY = os.environ['ADMIN_KEY']

app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'FAKDSLFAJES%KLAJerlkwjer'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ[
    'OPENSHIFT_POSTGRESQL_DB_URL']
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    badge = db.Column(db.String(255), primary_key=True)
    issued = db.Column(db.Boolean)

    def __init__(self, username, badge):
        self.username = username
        self.badge = badge
        self.issued = False

    def __repr__(self):
        return '<User(%s, issued=%s)>' % (self.username, self.issued)


db.create_all()


def add_user(username):
    try:
        user = User(username, BADGE)
        db.session.add(user)
        db.session.commit()
        return True
    except IntegrityError:
        return False


def done_user(username, badge):
    user = User.query.filter_by(username=username, badge=badge).first()
    user.issued = True
    db.session.add(user)
    db.session.commit()
    return user


@app.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if request.form['password'] == AUTH_KEY:
            flask.session['authed'] = True
            return flask.redirect(flask.url_for('claim'))
        elif request.form['password'] == ADMIN_KEY:
            flask.session['authed'] = True
            flask.session['admin'] = True
            return flask.redirect(flask.url_for('waiting'))
    return flask.render_template('password.html')


@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('claim'))


@app.route('/claim', methods=['GET', 'POST'])
def claim():
    if 'authed' not in flask.session or not flask.session['authed']:
        return flask.redirect(flask.url_for('auth'))
    if request.method == 'POST':
        if 'username' in request.form \
                and request.form['username'].strip() != '':
            # Handle
            if add_user(request.form['username'].strip()):
                flask.flash('User %s has been put in the queue for the badge. '
                            'The badge will be issued later today. '
                            'Current queue size: %i'
                            % (request.form['username'],
                               User.query.filter_by(issued=False).count()))
            else:
                flask.flash('User %s was already in the queue'
                            % request.form['username'],
                            'error')
        else:
            flask.flash('Enter a username', 'warning')
        return flask.redirect(flask.url_for('claim'))
    else:
        return flask.render_template(
            'index.html',
            badge=BADGE)


@app.route('/count')
def count():
    users = User.query.count()
    waiting = User.query.filter_by(issued=False).count()
    return 'Currently waiting: %i (%i total)' % (waiting, users)


@app.route('/waiting')
def waiting():
    if 'admin' not in flask.session or not flask.session['admin']:
        return flask.redirect(flask.url_for('auth'))
    users = User.query.filter_by(issued=False).all()
    printing = ''
    for user in users:
        printing += '%s (%s)<br />' % (user.username, user.badge)
    return printing


@app.route('/done/<username>/<badge>')
def done(username, badge):
    if 'admin' not in flask.session or not flask.session['admin']:
        return flask.redirect(flask.url_for('auth'))
    return done_user(username, badge).__repr__()


@app.route('/clear/sure/yes')
def clear():
    if 'sure' not in request.args:
        return 'Are you sure?'
    db.drop_all()
    db.create_all()
    return 'Cleared'
