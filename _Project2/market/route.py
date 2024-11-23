from market import app,db
from flask import render_template, redirect, url_for, flash
from market.models import Item,User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user


@app.route('/')
@app.route('/home')
def _homePage () :
    return render_template('index.html')

@app.route('/market')
def _marketPage () :
    items = Item.query.all()
    # [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    return render_template('market.html', _itemName = items)


@app.route('/register',methods=['GET', 'POST'])
def _registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password = form.password1.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('_marketPage'))
    if form.errors != {}: # if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f"Error found with Creating a User : {err_msg}", category='danger')
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def _loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You have logged in as : {attempted_user.username}', category='success')
            return redirect(url_for('_marketPage'))
        else:
            flash('Username and password did not match please try again',category='danger')
    return render_template('login.html', form = form)