from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				# Get a list of all restaurants
				restaurants = session.query(Restaurant).all()
				
				# Server Response Information
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<a href=\"/restaurants/new\">Make a New Restaurant Here</a>"
				output += "<br><br>"
				for r in restaurants:
					output += r.name + "<br>"
					output += "<a href=\"" + str(r.id) + "/edit\">Edit</a><br>"
					output += "<a href=\"" + str(r.id) + "/delete\">Delete</a><br>"""
					output += "<br>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
				
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += '''<form method='POST' enctype='multipart/form-data' 
				action='/restaurants/new'><h2>Please Enter New Restaurant</h2>
				<input name="newRestaurantName" type="text" placeholder = 'New Restaurant Name' >
				<input type="submit" value="Create"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
				
			if self.path.endswith("/edit"):
				# Get the id from the path, which will be the first number
				link_id = [int(s) for s in self.path.split('/') if s.isdigit()][0]
				# then go and get the name of the restaurant
				restaurant = session.query(Restaurant).filter_by(id= link_id).one()
				
				if restaurant !=[]:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h2>" + restaurant.name + "</h2>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % link_id
					output += "<input name=\"updateRestaurantName\" type=\"text\" placeholder = 'Update Restaurant Name' ><input type=\"submit\" value=\"Update\"></form>"	
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return
					
			if self.path.endswith("/delete"):
				# Get the id from the path, which will be the first number
				link_id = [int(s) for s in self.path.split('/') if s.isdigit()][0]
				# then go and get the name of the restaurant
				restaurant = session.query(Restaurant).filter_by(id= link_id).one()
				
				if restaurant !=[]:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1> Are you sure you want to delete " + restaurant.name + " ?</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % link_id
					output += "<input name=\"delete\" type=\"submit\" value=\"Delete\">"
					output += "<input href='/restaurants' type=\"submit\" value=\"Return to Restaurants Page\"></a>"
					output += "</form>"	
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return					
			
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')
				
				# Create new Restaurant Class
				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()	

			elif self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('updateRestaurantName')	

				# Update Restaurant Record
				# Get the Id Again
				link_id = [int(s) for s in self.path.split('/') if s.isdigit()][0]
				# then go and get the name of the restaurant
				restaurant = session.query(Restaurant).filter_by(id= link_id).one()
				restaurant.name = messagecontent[0]
				session.add(restaurant)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()						

			elif self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				
				# Update Restaurant Record
				# Get the Id Again
				link_id = [int(s) for s in self.path.split('/') if s.isdigit()][0]
				# then go and get the name of the restaurant
				restaurant = session.query(Restaurant).filter_by(id= link_id).one()
				session.delete(restaurant)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()	
				
			# self.send_response(301)
			# self.send_header('Content-type', 'text/html')
			# self.end_headers()
			# ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			# fields=cgi.parse_multipart(self.rfile, pdict)
			# messagecontent = fields.get('message')
			# if ctype == 'multipart/form-data':
				# output = ""
				# output +=  "<html><body>"
				# output += " <h2> Okay, how about this: </h2>"
				# output += "<h1> %s </h1>" % messagecontent[0]
				# output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				# output += "</body></html>"
				# self.wfile.write(output)
				# print output
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()