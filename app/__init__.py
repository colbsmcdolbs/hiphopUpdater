from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_select2 import Select2


db = SQLAlchemy()
select2 = Select2()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    select2.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)



    if not app.debug and not app.testing:
        from app.scraper import scrape
        from app.models import clear_posts
        import atexit
        from apscheduler.schedulers.background import BackgroundScheduler
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        clear_scheduler = BackgroundScheduler(daemon=True)
        post_scheduler = BackgroundScheduler(daemon=True)

        clear_scheduler.add_job(clear_posts, 'interval', days=1)
        post_scheduler.add_job(scrape, 'interval', minutes=5)
        clear_scheduler.start()
        post_scheduler.start()
        atexit.register(lambda: post_scheduler.shutdown())
        atexit.register(lambda: clear_scheduler.shutdown())

    return app

from app import models
