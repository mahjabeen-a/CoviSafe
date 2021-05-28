from shop import db

#table

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(80), unique=False, nullable=False, default='profile.jpg')

    def __repr__(self):
        return '<Admin %r>' % self.username
        #this will be displayed when we do query.all

db.create_all()