from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1', 'description': 'A sample Restaurant that we\'re just putting in the file for now.'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1', 'description': 'A sample Restaurant that we\'re just putting in the file for now.'}, {'name':'Blue Burgers', 'id':'2', 'description': 'A sample Restaurant that we\'re just putting in the file for now.'},{'name':'Taco Hut', 'id':'3', 'description': 'A sample Restaurant that we\'re just putting in the file for now.'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	all_restaurants = restaurants
	return render_template('restaurants.html', restaurants = all_restaurants)
	
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
	return render_template('newRestaurant.html')
	
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	edit_restaurant = restaurant
	return render_template('editRestaurant.html', restaurant = edit_restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	delete_restaurant = restaurant
	return render_template('deleteRestaurant.html', restaurant = delete_restaurant)
	
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	show_restaurant = restaurant
	menu = items
	return render_template('menu.html', restaurant = show_restaurant, items = menu)
	
@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	return "This page is for making a new menu item for restaurant %s." % restaurant_id
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "This page is for editing menu item %s." %menu_id
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "This page is for deleting menu item %s." %menu_id

if __name__== '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)