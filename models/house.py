from main import db
from sqlalchemy import func

class HouseModel(db.Model):
    __tablename__="houses"
    id = db.Column(db.Integer, primary_key=True)
    property_id =db.Column(db.Integer, db.ForeignKey('properties.id'))
    house_name = db.Column(db.String(55), nullable=False)
    rent_amount = db.Column(db.String(55), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def create_record(self):
        db.session.add(self)
        db.session.commit()
    #fetch records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def update_house(cls, house_id, property_id, house_name, rent_amount):
        record = cls.query.filter_by(id=house_id).first()
        if record:
            record.property_id=property_id
            record.house_name=house_name
            record.rent_amount=rent_amount
            db.session.commit()
            return True
        else:
            return False