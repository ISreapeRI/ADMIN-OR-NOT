from db import DB
from user_model import UserModel
from news_model import NewsModel


db = DB()
users_model = UserModel(db.get_connection())
users_model.init_table()
users_model.insert("admin", "123456789")
users_model.insert("usual_user", "user")
news_model = NewsModel(db.get_connection())
news_model.init_table()
