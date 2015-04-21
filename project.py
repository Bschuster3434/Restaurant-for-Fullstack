from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:funky_monkey>/')
def restaurantMenu(funky_monkey):
	restaurant = session.query(Restaurant).filter_by(id = funky_monkey).one()
	items = session.query(MenuItem).filter_by(funky_monkey = restaurant.id)
	output = ''
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output += '</br></br>'
	return output
	
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)