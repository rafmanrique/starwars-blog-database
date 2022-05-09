from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)
    favorites = db.relationship('Favorite', backref="user", uselist=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Nature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nature_name = db.Column(db.String(250))
    nature_people = db.relationship('People', backref="nature", uselist=True)
    nature_planet = db.relationship('Planet', backref="nature", uselist=True)
    nature_favorite = db.relationship('Favorite', backref="nature", uselist=True)

    def __repr__(self):
        return f'<Nature > f{self.nature_name}'

    def serialize(self):
        return {
			"natureName": self.natureName,
			#do not serialize the password, it's a security breach
		}


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_name = db.Column(db.String(250), unique=True, nullable=False)
    favorite_uid = db.Column(db.Integer, nullable=False)
    favorite_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    __table_args__ = (db.UniqueConstraint(
	"user_id","favorite_name","favorite_uid", "favorite_nature",
	name="debe_tener_una_sola_coincidencia"
    ),)


    def __repr__(self):
        return f'<Favorite> f{self.id}'

    def serialize(self):
        return {
			"favorite_name": self.favorite_name,
			"favorite_nature":self.favorite_nature,
            "favorite_uid":self.favorite_uid,
            "user_id":self.user_id
			#do not serialize the password, it's a security breach
		}

class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    people_name = db.Column(db.String(250), unique=True)
    people_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    

    def __repr__(self):
        return f'<people> f{self.uid}'

    def serialize(self):
        return {
			"people_name": self.people_name,
			"people_nature":self.people_nature,
            "people_uid":self.uid
			#do not serialize the password, it's a security breach
		}


class Planet(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250), unique=True)
    planet_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))

    def __repr__(self):
        return f'<Planet> f{self.uid}'

    def serialize(self):
        return {
			"planet_name": self.planet_name,
			"planet_nature":self.planet_nature,
            "planet_uid":self.uid
			#do not serialize the password, it's a security breach
		}