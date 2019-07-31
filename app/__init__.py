from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
bootstrap = Bootstrap(app)

from app import routes, models, errors
from app.scraper import scrape
from app.models import clear_posts
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


clear_scheduler = BackgroundScheduler(daemon=True)
post_scheduler = BackgroundScheduler(daemon=True)
clear_scheduler.add_job(clear_posts, 'interval', days=1)
post_scheduler.add_job(scrape, 'interval', minutes=20)
clear_scheduler.start()
post_scheduler.start()


atexit.register(lambda: post_scheduler.shutdown())
atexit.register(lambda: clear_scheduler.shutdown())