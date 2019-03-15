from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from usermodel import UsersModel
from add_news_form import AddNewsForm
from db import DB
from user_model import UserModel
from news_model import NewsModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()

def exits(args):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session)
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index") 
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return redirect('/index')
    if session['username'] == 'admin':
        form = AddNewsForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            nm = NewsModel(db.get_connection())
            nm.insert(title,content,session['user_id'])
            return redirect("/index")
        return render_template('admin_add_news.html', title='Добавление новости', form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return redirect('/index')    
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        news = NewsModel(db.get_connection()).get_all(session['user_id'])
        return render_template('admin_index.html', username=session['username'], news=news)        
    news = NewsModel(db.get_connection()).get_all(None)
    return render_template('index.html', username=session['username'], news=news)


@app.route('/error', methods=['GET', 'POST'])
def error():
    return "error, unknown user"


@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')

    elif request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login not in UsersModel.get_all():
            UsersModel.insert(login, password)
            session['username'] = login
            RDB.add_user(login)
            return render_template('registration_success.html',
                                   name1=login,
                                   adress=url_for('static',
                                                  filename=filename))    

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
