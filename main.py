from flask import Flask, request, redirect, render_template
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too


@app.route("/")
@app.route("/signup")
def signup():
    template = jinja_env.get_template('signup.html')
    return template.render()


@app.route("/welcome", methods=['POST'])
def welcome():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    def validate_input(input):
        if input == '':
            return "This field is required"
        elif not 3 < len(input) < 20:
            return "Input must be between 3 and 20 characters"
        elif ' ' in input:
            return "Input cannot include whitespace"
        else:
            return ''

    username_error = validate_input(username)
    password_error = validate_input(password)
    verify_password_error = validate_input(verify_password)

    if password != verify_password and verify_password_error == '':
        verify_password_error = "Passwords must match"
    elif password != verify_password:
        verify_password_error += " and passwords must match"

    if email != '':
        if ' ' in email or not 3 < len(email) < 20 or '@' not in email or '.' not in email:
            email_error = "Invalid email"

    if username_error == password_error == verify_password_error == email_error == '':
        template = jinja_env.get_template('welcome.html')
        return template.render(name=username)
    else:
        template = jinja_env.get_template('signup.html')
        return template.render(
            name=username,
            email=email,
            username_error=username_error,
            password_error=password_error,
            verify_password_error=verify_password_error,
            email_error=email_error)


app.run()
