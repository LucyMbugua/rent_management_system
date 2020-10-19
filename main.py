from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pygal
#import config class
from settings.configs import DevelopmentConfig, ProductionConfig
# import db connection
from settings.db_connect import conn

app = Flask(__name__)
#tell flask which config settings to use
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

#import models
from models.tenant import TenantModel
from models.property import PropertyModel
from models.house import HouseModel
from models.payment import PaymentModel

@app.before_first_request
def create_tables():
    db.create_all()
    #db.drop_all()
 
@app.context_processor#used to pass functions to html using jinja
def utility_processor():# first function must be named utility_processor
    def get_property_name(property_id):
        property_details= PropertyModel.query.filter_by(id=property_id).first()
        return property_details
    return dict(get_property_name=get_property_name)

@app.context_processor#used to pass functions to html using jinja
def utility_processor():# first function must be named utility_processor
    def get_house_details(house_id):
        house_details= HouseModel.query.filter_by(id=house_id).first()
        return house_details
    return dict(get_house_details=get_house_details)

@app.context_processor#used to pass functions to html using jinja
def utility_processor():# first function must be named utility_processor
    def get_payment_details(tenant_id):
        payment_details= PaymentModel.query.filter_by(tenant_id=tenant_id).first()
        return payment_details
    return dict(get_payment_details=get_payment_details)

@app.context_processor#used to pass functions to html using jinja
def utility_processor():# first function must be named utility_processor
    def get_rent_balance(house_id, tenant_id):
        house_details= HouseModel.query.filter_by(id=house_id).first()
        payment_details= PaymentModel.query.filter_by(tenant_id=tenant_id).first()
        rent_expected=int(house_details.rent_amount) 
        rent_paid =int(payment_details.amount)
        balance=rent_expected - rent_paid
        print(balance)
    
        return balance
    return dict(get_rent_balance=get_rent_balance)




@app.route('/properties', methods=['GET','POST'])
def properties():

    properties=PropertyModel.fetch_all()
    print(properties)
    if request.method == 'POST':
        property_name = request.form['property_name']
        address = request.form['address']
        
        record = PropertyModel(property_name=property_name, address=address)
        record.create_record()
        flash("Record has been successifully created","success")
       
        return redirect(url_for('properties'))

    return render_template('properties.html', all_properties = properties)

@app.route("/edit_property/<property_id>", methods=['POST'])
def edit_property(property_id):
    if request.method =='POST':
        property_name = request.form['property_name']
        address = request.form['address']
      
        if PropertyModel.update_property(property_id=property_id,property_name=property_name, address=address):
            flash("Record has been successifully updated","success")
            return redirect(url_for('properties'))

        else:
            flash("Error occurred while editing record","success")
            return redirect(url_for('properties'))

@app.route('/delete_property/<property_id>', methods=['POST'])
def delete_property(property_id):
    record =PropertyModel.query.filter_by(id=property_id).first()
    
    if record:
        db.session.delete(record)
        db.session.commit()
        flash("Successifully deleted","warning")
        
    else:
        flash("Error!! Operation unsuccessiful", "warning")

    return redirect(url_for('properties'))

@app.route('/houses', methods=['GET','POST'])
def houses():

    houses=HouseModel.fetch_all()
    properties =PropertyModel.fetch_all()
    print(houses)
    if request.method == 'POST':
        property_id =request.form['property_id']
        house_name = request.form['house_name']
        rent_amount = request.form['rent_amount']
        
        record = HouseModel(property_id=property_id, house_name= house_name, rent_amount=rent_amount)
        record.create_record()
        flash("Record has been successifully created","success")
       
        return redirect(url_for('houses'))

    return render_template('houses.html', all_houses = houses, all_properties=properties)

@app.route("/edit_house/<house_id>", methods=['POST'])
def edit_house(house_id):
    if request.method =='POST':
        property_id =request.form['property_id']
        house_name = request.form['house_name']
        rent_amount = request.form['rent_amount']
    
        if HouseModel.update_house(house_id=house_id,property_id=property_id, house_name= house_name, rent_amount=rent_amount):
            flash("Record has been successifully updated","success")
            return redirect(url_for('houses'))

        else:
            flash("Error occurred while editing record","success")
            return redirect(url_for('houses'))

@app.route('/delete_house/<house_id>', methods=['POST'])
def delete_house(house_id):
    record =HouseModel.query.filter_by(id=house_id).first()
    
    if record:
        db.session.delete(record)
        db.session.commit()
        flash("Successifully deleted","warning")
        
    else:
        flash("Error!! Operation unsuccessiful", "warning")

    return redirect(url_for('houses'))

@app.route('/tenants', methods=['GET','POST'])
def tenants():

    tenants=TenantModel.fetch_all()
    properties =PropertyModel.fetch_all()
    houses =HouseModel.fetch_all()
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        property_id=request.form['property_id']
        house_id=request.form['house_id']
        
        record = TenantModel(fname=fname,lname=lname,email=email, property_id=property_id, house_id=house_id)
        record.create_record()
        flash("Record has been successifully created","success")
       
        return redirect(url_for('tenants'))

    return render_template('tenants.html', all_tenants = tenants,all_properties=properties,all_houses=houses)


@app.route("/edit_tenant/<tenant_id>", methods=['POST'])
def edit_tenant(tenant_id):
    if request.method =='POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        property_id=request.form['property_id']
        house_id=request.form['house_id']
        
        if TenantModel.update_tenant(tenant_id=tenant_id,fname=fname,lname=lname,email=email, property_id=property_id, house_id=house_id):
            flash("Record has been successifully updated","success")
            return redirect(url_for('tenants'))

        else:
            flash("Error occurred while editing record","success")
            return redirect(url_for('tenants'))

@app.route('/delete_tenant/<tenant_id>', methods=['POST'])
def delete_tenant(tenant_id):
    record =TenantModel.query.filter_by(id=tenant_id).first()
    
    if record:
        db.session.delete(record)
        db.session.commit()
        flash("Successifully deleted","warning")
        
    else:
        flash("Error!! Operation unsuccessiful", "warning")

    return redirect(url_for('tenants'))
  
@app.route("/make_payment/<tenant_id>", methods=['GET','POST'])
def make_payment(tenant_id):
    
    if request.method == 'POST':
        date= request.form['date']
        amount= request.form['amount']
        new_payment = PaymentModel(tenant_id=tenant_id, date=date, amount=amount)
        new_payment .create_record()
        
        flash("Payment added successifully","success")
        return redirect(url_for('tenants'))

@app.route('/about')
def about():
    return render_template('contact.html')

@app.route('/contact-us')
def contact():
    return render_template('about.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_properties=len(PropertyModel.fetch_all())
    total_houses =len(HouseModel.fetch_all())
    total_tenants =len(TenantModel.fetch_all())

    pie_chart = pygal.Pie()
    pie_chart.title = 'No of Houses vs No of Tenants'
    pie_chart.add('Houses', total_houses)
    pie_chart.add('Tenants', total_tenants)
    pie= pie_chart.render_data_uri()
    return render_template('dashboard.html', total_properties=total_properties, total_houses=total_houses, total_tenants=total_tenants, chart=pie)






