
from Tool import app, db
import os
from Tool.forms import RegistrationForm, LoginForm, SearchForm
from Tool.models import User,Design,Adjective
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    # design=Design(location="fast_food.png")
    # db.session.add(design)
    # db.session.commit()
    # adjective=Adjective(name='cool')
    # db.session.add(adjective)
    # db.session.commit()
    # adjective=Adjective.query.filter_by(id=1).first()
    # design=Design.query.filter_by(id=1).first()
    # design.designs.append(adjective)
    # db.session.commit()
    # print(design.designs)
    return render_template("index.htm")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            print('hi')
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.htm')

@app.route('/designfind/<adjectives>', methods=['GET', 'POST'])
@login_required
def find(adjectives):
    form=SearchForm()
    if form.validate_on_submit():
        adjectives_=form.adjectives.data
        return redirect(url_for('find', adjectives=adjectives_))
    da_list = []
    if adjectives!='None':
        for i in adjectives.split(','):
            adjective=Adjective.query.filter_by(name=i).first()
            print(i)
            if adjective:
                for j in adjective.designs:
                    da_list.append(j)
    else:
        design=Design.query.order_by(Design.id.asc())
        for i in design:
            da_list.append(i)
    return render_template('find.htm',da_list=da_list,form=form,adjectives=adjectives)


@app.route('/add/<design_id>/<adjectives_>/<where>', methods=['GET', 'POST'])
@login_required
def add(design_id,adjectives_,where):
    design = Design.query.filter_by(id=int(design_id)).first()
    current_user.designs.append(design)
    db.session.commit()
    if where=='find':
        return redirect(url_for(where, adjectives=adjectives_))
    else:
        return redirect(url_for(where))

@app.route('/remove/<design_id>/<adjectives_>/<where>', methods=['GET', 'POST'])
@login_required
def remove(design_id,adjectives_,where):
    design = Design.query.filter_by(id=int(design_id)).first()
    current_user.designs.remove(design)
    db.session.commit()
    if where=='find':
        return redirect(url_for(where, adjectives=adjectives_))
    else:
        return redirect(url_for(where))


if __name__ == '__main__':
    app.run(debug=True)
