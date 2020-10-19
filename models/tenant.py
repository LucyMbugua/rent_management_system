from main import db
from sqlalchemy import func

class TenantModel(db.Model):
    __tablename__="tenants"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(55), nullable=False)
    lname = db.Column(db.String(55), nullable=False)
    email = db.Column(db.VARCHAR(30), nullable=False,unique=True)
    property_id =db.Column(db.Integer, db.ForeignKey('properties.id'))
    house_id =db.Column(db.Integer, db.ForeignKey('houses.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    payment = db.relationship('PaymentModel', backref="tenant", lazy=True)#sales & stock are always a list of objects
    
    def create_record(self):
        db.session.add(self)
        db.session.commit()
    #fetch records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()


    @classmethod
    def update_tenant(cls, tenant_id,fname,lname,email, property_id, house_id):
        record = cls.query.filter_by(id=tenant_id).first()
        if record:
            
            record.fname=fname
            record.lname=lname
            record.email=email
            record.property_id=property_id
            record.house_id=house_id
            db.session.commit()
            return True
        else:
            return False
    