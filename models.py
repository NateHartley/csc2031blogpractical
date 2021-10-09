from app import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def init_db():  # error occurs here, there should be a self parameter but adding this also causes errors
        db.drop_all()
        db.create_all()
        new_user = User(username='user1@test.com', password='mysecretpassword')
        db.session.add(new_user)
        db.session.commit()