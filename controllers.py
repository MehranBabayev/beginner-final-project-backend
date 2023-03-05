from app import app
from flask import render_template, request , redirect, url_for
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import login_user ,logout_user, current_user, login_required
 
from datetime import datetime

@app.context_processor
def general():
    category=Category.query.all()
    detailed = Detailed.query.all()
    colors=Color.query.all()
    prices=Price.query.all()
    sizes=Size.query.all()
    try:
        favorites = Favorites_products.query.filter_by(user_id=current_user.id).count()
    except:
        favorites = Favorites_products.query.all()
    return dict(color=colors,size=sizes,price=prices, favoritess = favorites,category=category,detailed=detailed )


@app.route("/shop", methods=['GET','POST'])
def shop():
    form_2= SearchForm()    
    categories=Category.query.all()
    product = Product.query.all()
    count = 2
    form_3= NewsletterForm()    
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
        
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('shop'))
    
    return render_template('shop.html', form_2 = form_2,Products = product , form_3 = form_3, category=categories, count = count)


@app.route('/filter/color/<string:name>', methods = ['GET', 'POST'])
def filter_color(name):
    product1= Color.query.filter_by(name = name).first().product_color
    count = len(product1)
    form_2= SearchForm()    
    form_3= NewsletterForm()    
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count= count)
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('filter_color', name = name))
    return render_template ('shop.html',  Products = product1, count = count,form_2=form_2,form_3=form_3)


@app.route('/filter/size/<string:name>', methods = ['GET', 'POST'])
def filter_size(name):
    product1= Size.query.filter_by(name = name).first().product_size
    count = len(product1)
    form_2= SearchForm()    
    form_3= NewsletterForm()    
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
        
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('filter_size', name = name))
    return render_template ('shop.html',  Products = product1, count = count,form_2=form_2,form_3=form_3)


@app.route('/filter/price/<string:name>', methods = ['GET', 'POST'])
def filter_price(name):
    product3= Price.query.filter_by(price_name = name).first().product_price
    count = len(product3)
    form_2= SearchForm()    
    form_3= NewsletterForm()    
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
        
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('filter_price', name = name))
    return render_template ('shop.html',  Products = product3, count = count,form_2=form_2,form_3=form_3)


@app.route("/detail/<int:id>",  methods=['GET','POST'] )
def detail(id):
    form_2= SearchForm()
    form_3= NewsletterForm()
    form_4= FavoritesForm()
    form = ReviewForm()
    reviewall = Review.query.all()
    product = Product.query.filter_by(id=id).first()
    count = 2
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3,form_4 = form_4, count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('detail', id = id))        
    
            
            
    if form_4.submit_favorite.data:
        if request.method == 'POST':
            post_data = request.form
            form_4 = FavoritesForm(data=post_data)
            if form_4.submit_favorite.data and form_4.validate_on_submit():
                try:
                    
                    favorite = Favorites_products(user_id = current_user.id, product_id=id)
                    favorite.save()
                except:
                    pass
                return redirect(url_for("favorites"))
            
            
           
 
    if request.method == 'POST':
        form = ReviewForm(request.form)
        if form.validate_on_submit():
            review = Review (review_text = form.review_text.data,date = datetime.today().strftime('%d %b %Y'))
            review.product_id = id
            review.full_name = current_user.Full_name
            review.save()
            return redirect(url_for('detail', id=id))       
                   
    return render_template('detail.html', Products = product , form_2 = form_2,form_3 = form_3, form_4 = form_4, form=form, reviewall= reviewall, count = count)


@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    form_2= SearchForm()
    form_3= NewsletterForm()
    favorite_selected = Favorites_products.query.filter_by(user_id = current_user.id)
    count = 2
    
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit: 
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('favorites'))
             
    return render_template('favorites.html' ,favorite_selected = favorite_selected, form_2 = form_2,form_3 = form_3, count = count)

@app.route('/favorite/<int:id>')
def favorite_remove(id):
        
        fav = Favorites_products.query.filter_by(id = id).first()
        fav.delete()                
        return redirect(url_for('favorites'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    form_2= SearchForm()
    form_3= NewsletterForm()
    count = 2
        
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
            
            
    if request.method == 'POST':
        form =RegisterForm(request.form)        
        if form.validate_on_submit():            
            user = User(
                Full_name = form.Full_name.data,                
                Email = form.Email.data,
                password = generate_password_hash(form.password.data)
            )
            user.save()
            return redirect(url_for('login'))              
            
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                print(1)
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('register'))    
        
    return render_template('register.html',form_2 = form_2 , form=form ,form_3 = form_3, count = count)



@app.route('/login', methods = ['GET', 'POST'])
def login():
    form_1 = LoginForm()
    form_2= SearchForm()
    form_3= NewsletterForm()    
    count = 2
    if request.method == 'POST':
        post_data = request.form
        form_1 = LoginForm(data = post_data)
        if form_1.validate_on_submit():
            user = User.query.filter_by(Email=form_1.email.data).first()            
            if user and user.check_password(form_1.password.data):
                login_user(user)
                return redirect(url_for('shop'))
            else:
                print('not loged in')

    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                print(1)
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('login'))        
            
            
    return render_template('login.html', form_1=form_1, form_2 = form_2,form_3 = form_3, count = count)


@app.route("/contact" , methods = ['GET', 'POST'])
def contact():   
    form = ContactForm()
    form_2= SearchForm()
    form_3= NewsletterForm()
    count = 2
    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate_on_submit():
            contact = Contact(
                Name = form.Name.data,
                Email = form.Email.data,
                Subject = form.Subject.data,
                Message = form.Message.data               
            )
            contact.save()
            return redirect(url_for('contact'))
        
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3, count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                print(1)
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('contact'))    
        
    return render_template('contact.html', form=form , form_2 = form_2,form_3 = form_3, count = count)


@app.route('/filter/category/<int:id>', methods = ['GET', 'POST'])
def filter_category(id):
    product4 = Category.query.filter_by(id = id).first().category
    count = len(product4)
    form_2= SearchForm()
    form_3= NewsletterForm()
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3,count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('filter_category', id=id))
    return render_template ('shop.html', Products = product4,form_2 = form_2,form_3 = form_3, count = count)


@app.route('/filter/category/detail<int:id>', methods = ['GET', 'POST'])
def filter_category_detail(id):
    detailed = Detailed.query.filter_by(id = id).first().detailed_category
    count = len(detailed)
    form_2= SearchForm()
    form_3= NewsletterForm()
    if form_2.submit_search.data and form_2.validate_on_submit:
                searchtext = form_2.searchtext.data
                searched_products = Product.query.filter(Product.name.contains(searchtext)).all()
                count = len(searched_products)
                return render_template('shop.html', Products = searched_products, form_2 = form_2,form_3 = form_3,count = count)
            
    if form_3.submit_news.data:
        if request.method == 'POST':
            post_data = request.form
            form_3 = NewsletterForm(data = post_data)
            if form_3.submit_news.data and form_3.validate_on_submit:
                print(1)
                newsletter = Newsletter(name = form_3.name.data, email = form_3.email.data)
                newsletter.save()
                return redirect(url_for('filter_category', id=id))
    return render_template ('shop.html', Products = detailed, count = count,form_2 = form_2,form_3 = form_3)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


