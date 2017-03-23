
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug import check_password_hash, generate_password_hash

from komafly.cmm.application import db
from komafly.ktr.forms import LoginForm
from komafly.ktr.model import User,TM_ISSUE02
from komafly.ktr.service import *

import numpy as np
import pandas as pd
from functools import partial
 
mode_ktr = Blueprint('ktr', __name__, url_prefix='/ktr', template_folder='templates')


@mode_ktr.route('/', methods=['GET', 'POST'])
@mode_ktr.route('/index', methods=['GET', 'POST'])
def index():
    users = select_issue02_all('USER_GROUP')
    return render_template("ktr/index.html",users=users)


@mode_ktr.route('/df', methods=['GET', 'POST'])
def show_dataframe():
    q = '''
    SELECT 
    RCEPT_ID, 
    ISGN_ORGINL_RCEPT_ID, 
    RCEPT_TOTAMT, 
   DECSN_TOTAMT, 
   RCPMNY_SE_CD, 
   RCEPT_PROGRS_STTUS_CD, 
   AGREM_ID, REGISTER_ID, REGIST_DT, 
   CHANGER_ID, CHANGE_DT, INDUST_CL_CD
FROM CP_BNCR002
    '''
    df = pd.read_sql(q,con=db.engine)
    df = df.fillna('')
    df.rename(columns=get_cnames(),inplace=True)
    return df.to_html(index=False, na_rep="NA", classes='dataframe')


@mode_ktr.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("ktr/signin.html", form=form) 