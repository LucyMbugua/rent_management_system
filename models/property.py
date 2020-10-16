from main import db
from sqlalchemy import func

class PropertyModel(db.Model):
    __tablename__="properties"
    id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(55), nullable=False)
    address = db.Column(db.String(55), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    

    def create_record(self):
        db.session.add(self)
        db.session.commit()
    #fetch records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def update_property(cls, property_id, property_name, address):
        record = cls.query.filter_by(id=property_id).first()
        if record:
            record.property_name=property_name
            record.address=address
            db.session.commit()
            return True
        else:
            return False