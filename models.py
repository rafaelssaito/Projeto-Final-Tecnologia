from extensions import db

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Evento {self.titulo}>'
