from main import db
from sqlalchemy import func

class PaymentModel(db.Model):
    __tablename__="payments"
    id = db.Column(db.Integer, primary_key=True)
    tenant_id =db.Column(db.Integer, db.ForeignKey('tenants.id'))
    date = db.Column(db.DateTime(timezone=True))
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    

    def create_record(self):
        db.session.add(self)
        db.session.commit()
    #fetch records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()
    