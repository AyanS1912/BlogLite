import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db,db_init
from flask_login import login_required,login_user,logout_user
from flask_login import current_user,LoginManager

app = None

def create_app():
  app = Flask(__name__, template_folder="templates")
  app.config['SECRET_KEY'] = 'passwordgeneration'
  if os.getenv('ENV', "development") == "production":
    raise Exception("Currently no production config is setup.")
  else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app)
  app.app_context().push()
  
  from application.models import User
  login_manager = LoginManager()
  login_manager.init_app(app)
  
  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))
  db_init(app)
  return app


app = create_app()

from application.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)