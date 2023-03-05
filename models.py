from extensions import db, login_manager, admin

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView

from app import app
  


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key =True)
    Full_name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_favorite = db.relationship('Favorites_products', backref = 'user_favorite')

    def __init__(self, Full_name, Email, password):
        self.Full_name = Full_name
        self.Email = Email
        self.password = password 
        
    def __repr__(self):
        return self.Full_name
    
    def save(self):
        db.session.add(self)
        db.session.commit()    
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float,default=123.00)
    new_price = db.Column(db.Float,default=100.00)    
    description = db.Column(db.Text,nullable=True)
    image_url = db.Column(db.String(255),unique=True, nullable=False)
    size = db.Column(db.Boolean,default=True)
    color = db.Column(db.Boolean,default=True)
    comment = db.relationship('Review', backref='comment')
    color_id = db.Column(db.ForeignKey('color.id'), nullable = False)
    size_id = db.Column(db.ForeignKey('size.id'), nullable = False)
    price_id = db.Column(db.ForeignKey('price.id'), nullable = False)
    category_id = db.Column(db.ForeignKey('category.id'),nullable = False)
    detail_category_id = db.Column(db.ForeignKey('detailed.id'),nullable = False)
  
    
    def __init__ (self,name, price, new_price, description, image_url, size, color,color_id,size_id,price_id,category_id,detail_category_id):
        self.name = name
        self.price = price
        self.new_price = new_price
        self.description = description
        self.image_url = image_url
        self.size = size
        self.color = color
        self.color_id=color_id
        self.size_id=size_id
        self.price_id=price_id
        self.category_id=category_id
        self.detail_category_id=detail_category_id
        
                
    def save(self):
        db.session.add(self)
        db.session.commit()
               

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    category= db.relationship('Product', backref='category')
    def __repr__(self) :
        return self.name
    
    def __init__(self, name):
        self.name = name
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        

class Detailed(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(40), unique = True, nullable = False)
    detailed_category = db.relationship('Product', backref='detailed_category')
    def __repr__(self) :
        return self.name
    
    def __init__(self, name):
        self.name = name
        
    def save(self):
        db.session.add(self)
        db.session.commit()        


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Subject = db.Column(db.String(100))
    Message = db.Column(db.String(255))
    
    
    def __init__(self, Name, Email, Subject, Message):
        self.Name = Name
        self.Email = Email
        self.Subject = Subject
        self.Message = Message
        
    def __repr__(self):
        return self.Name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
class Newsletter(db.Model):
    __Tablename__ = 'Newsletter'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self) :
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        

class Favorites_products(db.Model):
    __tablename__ = 'favorites_products'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id'),
      )
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete = 'CASCADE'))
    product = db.relationship('Product', backref = 'favorites')

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return self.user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Color(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    product_color = db.relationship('Product', backref='product_color')
    
    def __repr__ (self):
        return self.name
    
    def __init__ (self,name):
        self.name = name
    
        
    def save(self):
        db.session.add(self)
        db.session.commit()


class Size(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    product_size = db.relationship('Product', backref='product_size')
    
    def __repr__ (self):
        return self.name
    
    def __init__ (self,name):
        self.name = name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
class Price(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price_name = db.Column(db.String(50), nullable = False)
    product_price = db.relationship('Product', backref='product_price')

    def __repr__ (self):
        return self.price_name
    
    def __init__ (self,price_name):
        self.price_name = price_name
           
    def save(self):
        db.session.add(self)
        db.session.commit()
        

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    review_text = db.Column(db.Text, nullable = False)
    date = db.Column(db.String(20), nullable = False)
    full_name = db.Column(db.String(20), nullable = False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))
    
    def __init__(self, review_text,date):
        self.review_text = review_text
        self.date = date
    
    def __repr__(self) :
        return self.review_text
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    
admin.add_view(ModelView(Product, db.session)) 
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Favorites_products, db.session))
admin.add_view(ModelView(Newsletter, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Color, db.session))  
admin.add_view(ModelView(Size, db.session))  
admin.add_view(ModelView(Price, db.session)) 
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Detailed, db.session)) 