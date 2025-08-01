# filepath: /home/nwf/holbertonschool-hbnb/part 3/app/repositories/sqlalchemy_repository.py
class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def get(self, id):
        return self.model.query.get(id)

    def get_all(self):
        return self.model.query.all()

    def add(self, obj):
        from app import db
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, id, data):
        obj = self.get(id)
        for key, value in data.items():
            setattr(obj, key, value)
        from app import db
        db.session.commit()
        return obj

    def delete(self, id):
        obj = self.get(id)
        from app import db
        db.session.delete(obj)
        db.session.commit()
        return True
