from flask import Flask
from database import db
from routers.routers import aluno_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db" # mysql:///user:passw@host:port/database
app.config["SECRET_KEY"] = 'minhachavesupersecretaqueninguemvaidescobrir'

db.init_app(app)

app.register_blueprint(aluno_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)