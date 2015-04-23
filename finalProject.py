from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	all_restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = all_restaurants)
	
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		new_restaurant = Restaurant(name = request.form['name'], description = request.form['description'])
		session.add(new_restaurant)
		session.commit()
		return redirect( url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')
	
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name'] != '':
			edit_restaurant.name = request.form['name']
		if request.form['description'] != '':
			edit_restaurant.description = request.form['description']
		session.add(edit_restaurant)
		session.commit()
		return redirect( url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = edit_restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	delete_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(delete_restaurant)
		session.commit()
		return redirect( url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = delete_restaurant)
	
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	show_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	#menu = session.query(MenuItem).filter_by(restaurant_id = show_restaurant.id).all()
	course_order = ["Appetizer", "Beverage", "Entree", "Dessert"]
	courses_dict = {}
	for c in course_order:
		menu_items = session.query(MenuItem).filter_by(restaurant_id = show_restaurant.id, course = c).all()
		if len(menu_items) == 0:
			continue
		courses_dict[c] = menu_items
	return render_template('menu.html', restaurant = show_restaurant, items = menu)
	
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	restaurant_item = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		new_menu_item = MenuItem( name = request.form['name'], description = request.form['description'],
								 price = request.form['price'], course = request.form['course'],
								 restaurant_id = restaurant_id)
		session.add(new_menu_item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant = restaurant_item)
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	edit_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	if request.method == 'POST':
		print request.form
		if request.form['name'] != '':
			edit_item.name = request.form['name']
		if request.form['description'] != '':
			edit_item.description = request.form['description']
		if request.form['course'] != '':
			edit_item.course = request.form['course']
		if request.form['price'] != '':
			edit_item.price = request.form['price']
		session.add(edit_item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant = edit_restaurant, item = edit_item)
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	delete_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	delete_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	if request.method == 'POST':
		session.delete(delete_item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant = delete_restaurant, item = delete_item)

if __name__== '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)