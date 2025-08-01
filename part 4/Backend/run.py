from app import create_app, db
from app.models import User, Place, Review, Amenity

app = create_app()

# Créer les tables au démarrage de l'application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
