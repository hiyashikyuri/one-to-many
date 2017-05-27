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
    hobbies = db.relationship('Hobby', backref='person', lazy='dynamic')
    """
    hobbiesではカラムが追加しているのではなく、Hobbyに対して関連性を設定
    to_dict()メソッドはオブジェクトをjsonで返すためのメソッド
    """

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # Personに紐づいているHobbyを全部出力
            'hobby': [Hobby.to_dict(hobby) for hobby in self.hobbies.all()]
        }


class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


@app.route('/')
def index():
    return jsonify({"data": [Person.to_dict(person) for person in Person.query.all()]})


if __name__ == '__main__':
    app.run()
