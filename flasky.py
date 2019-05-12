import os
from app import create_app, db
from app.models.user import User, UserLog, UserFeedback
from app.models.book import Book
from app.models.order import GoodsShopCar
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book, UserLog=UserLog, UserFeedback=UserFeedback, GoodsShopCar=GoodsShopCar)
