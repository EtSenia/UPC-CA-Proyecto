from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>log in</p>"

@auth.route('/logout')
def logout():
    return "<p>log out</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 1:
            flash('Pon algo en el email', category='error')
        elif len(username) < 1:
            flash('el username ps', category='error')
        elif len(password1) < 1:
            flash('oe la contra', category='error')
        elif password1 != password2:
            flash('no coinciden alv', category='error')
        else:
            flash("Bien", category='success')
    return render_template("signup.html")