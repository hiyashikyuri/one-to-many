from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/one-to-many'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
    データベースの作成手順は、
    まず python コンソールで
    from app import db でインポートして
    その後、one-to-manyのデータベースを作成する
    作成し終わったら、
    db.create_all() で完成！
"""


# class にクエリをまとめるととても綺麗になる方オススメ

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pets': [Pet.to_dict(pet) for pet in self.pets.all()]

        }


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,

        }


@app.route('/')
def index():
    person = [Person.to_dict(person) for person in Person.query.all()]
    return jsonify({
        "response": person
    })


if __name__ == '__main__':
    app.run()
