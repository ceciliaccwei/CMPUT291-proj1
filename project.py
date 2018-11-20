import sqlite3
import getpass
import time
import os
import sys

if len(sys.argv) != 2:
	print("Please run with: python PROJECT.py DATABASE.db")
	quit()
db_file_path = sys.argv[1]

if not (os.path.exists(db_file_path)):
    print("File does not exist!")
    quit()
conn = sqlite3.connect(db_file_path)
c = conn.cursor()

def main():
		conn.commit()
		start()
		

def start():
		 while True:
				print("Welcome to the carpool system!")
				print("1. Login")
				print("2. Sign up")
				print("3. Exit")
				command = raw_input("What would you like to do today?")
				if command == '1':
					 login()
				elif command == '2':
					 signup()
					 continue
				elif command == '3':
					 quit()
				else: 
					 print("Command not found!")


def signup():
		 while True:
				email = raw_input("Please enter your email (or BACK): ").lower()
				if email == 'back':
					main()
				c.execute("SELECT * FROM members WHERE email like ?;",(email,))
				dup = c.fetchone()
				if dup == None:
					 break 
				else:
					 print("This email has already been signed up.")
		 password = getpass.getpass("Enter your password: ")
		 name = raw_input("Please enter your name: ")	  
		 while True:
			try:
				phone = int(raw_input("Please enter your phone number: "))
				break
			except ValueError:
				print("Invalid input!")
				continue 
		 c.execute("INSERT INTO members VALUES ('%s', '%s', '%s', '%s');" % (email, name, phone, password))
		 conn.commit()
		 print("You have successfully signed up!")
		 main()


def login(): 
		while True:
			email = raw_input("Please enter your email (or BACK): ").lower()
			if email== 'back':			
				break
			c.execute("SELECT * FROM members WHERE email like '%s';" % email)
			username = c.fetchone()
			if username == None:
					print("Username does not exist")  
			else:
					password = getpass.getpass("Enter your password: ")
					c.execute("SELECT * FROM members WHERE email like '%s' and pwd = '%s';" % (email,password)) 
					check_login = c.fetchone()
					if check_login == None: 
							print("Incorrect email or password, please try again.")
					else:
							print("Welcome!")    
							user = email
							c.execute("SELECT msgTimestamp,sender,rno,content FROM inbox WHERE email like '%s' and seen like '%s';" % (user,'n'))
							print ("".join('%-22s'%x[0] for x in c.description))
							ar = [[str(item) for item in results] for results in c.fetchall()]
							for row in ar:
								print ("".join('%-22s'%x for x in row))
							c.execute("UPDATE inbox SET seen = '%s' where seen like '%s' and email like '%s';" % ('y','n',user))
							conn.commit()
							chooseOptionCategory(user)
							  
			break

def chooseOptionCategory(user):
	while True:
		print("1. Rides")
		print("2. Bookings")
		print("3. Requests")
		print("4. Log out")
		print("5. Exit")
		option = raw_input("Your option: ")
		if option == '1':
			RidesRelated(user)
		elif option == '2':
			BookingsRelated(user)
		elif option == '3':
			RequestRelated(user)
		elif option == '4':
			main()
		elif option == '5':
			quit()
		else:
			print("Command not found!")

def RidesRelated(user):
	while True:
		print("1. Offer a ride")
		print("2. Search rides")
		print("3. Go back")
		print("4. Log out")
		print("5. Exit")
		option = raw_input("Your option: ")
		if option == '1':
			offerRide(user)
		elif option == '2':
			searchRides(user)
		elif option== '3':
			break
		elif option=='4':
			main()
		elif option=='5':
			quit()
		else:
			print("Command not found!")

def BookingsRelated(user):
	while True:
		print("1. List all confirmed bookings on my rides")
		print("2. Book someone on my ride")
		print("3. Go back")
		print("4. Log out")
		print("5. Exit")
		option = raw_input("Your option: ")
		if option == '1':
			bookingList(user)
		elif option == '2':
			rideList(user)
		elif option == '3':
			break
		elif option == '4':
			main()
		elif option == '5':
			quit()
		else:
			print("Command not found!")

def rideList(user):
	print(user)
	c.execute("SELECT r.*, \
	r.seats - ifnull(sum(b.seats) ,0) as seats_avaliable \
	from rides r \
	left join \
	bookings b \
	on r.rno = b.rno \
	where r.driver like ? \
	group by r.rno;",(user,))
	print ("".join('%-13s'%x[0] for x in c.description))
	ar = [[str(item) for item in results] for results in c.fetchall()]
	prtFive(ar)
	while True:
		print("Enter the rno to book")
		rno = raw_input("Or enter Back to go back: ")
		try:
			rno = int(rno)
			c.execute("SELECT * FROM rides WHERE driver like '%s' and rno='%d';" % (user,rno))
			check_ride = c.fetchone()
			if check_ride == None:
				print("That's not your ride!")
				continue
			else:
				break
		except ValueError:
			return

	while True:
		email = raw_input("Please enter the member's email: ").lower()
		c.execute("SELECT * FROM members WHERE email like ?;",(email,))
		exist = c.fetchone()
		if exist == None:
			print("Member does not exist!")
			continue
		else:
			break

	c.execute("SELECT r.seats - ifnull(sum(b.seats) ,0) \
	from rides r \
	left join \
	bookings b \
	on r.rno = b.rno \
	where r.rno = ? \
	group by r.rno;",(rno,))
	seats_avaliable = int(c.fetchone()[0]) 
	while True:
		try:
			cost = int(raw_input("Please enter your cost: "))
			break
		except ValueError:
			print("Invalid input!")
			continue

	while True:
		try:
			seats = int(raw_input("Please enter your seats booked: "))
			break
		except ValueError:
			print("Invalid input!")
			continue

	c.execute("SELECT lcode FROM locations")
	ar = [[str(item) for item in results] for results in c.fetchall()]

	pickup = raw_input("Please enter the pickup loc: ")
	while [pickup] not in ar:
		searchLoc(pickup)
		pickup = raw_input("Please enter the pickup loc: ")

	dropoff = raw_input("Please enter the dropoff loc: ")
	while [dropoff] not in ar:
		searchLoc(dst)
		dropoff = raw_input("Please enter your dst: ")

	seen = 'n'
	c.execute("SELECT ifnull(max(bno),0) FROM bookings")
	bno = int(c.fetchone()[0])+1
	if seats <= seats_avaliable:
		c.execute("INSERT INTO bookings VALUES (?,?,?,?,?,?,?);",(bno,email,rno,cost, int(seats), pickup,dropoff))
		content = "your booking: "+str(bno)+ " is confirmed!"
		msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
		c.execute("INSERT INTO inbox VALUES (?,?,?,?,?,?);",(email,msgTimestamp,user,content,rno,seen))
		conn.commit()
		print("message sent!")
	else: 
		option = raw_input("Are you sure to overbook? [Y/N]")
		if option.upper() == 'Y':
			c.execute("INSERT INTO bookings VALUES (?,?,?,?,?,?,?);",(bno,email,rno,cost, int(seats), pickup,dropoff))
			content = "your booking: "+str(bno)+ " is confirmed!"
			msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
			c.execute("INSERT INTO inbox VALUES (?,?,?,?,?,?);",(email,msgTimestamp,user,content,rno,seen))
			conn.commit()
			print("message sent!")
		else:
			return

def bookingList(user):
	c.execute("SELECT b.* FROM bookings b, rides r\
		where b.rno = r.rno and r.driver = ?;",(user,))
	print ("".join('%-13s'%x[0] for x in c.description))
	ar = [[str(item) for item in results] for results in c.fetchall()]
	prtFive(ar)
	print("Enter the bno to cancel")
	bno = raw_input("Or enter Back to go back: ")
	if bno.upper() == 'BACK':
		return
	else:
		bno = int(bno)
		c.execute("SELECT email,rno FROM bookings WHERE bno = ?;",(bno,))
		temp = c.fetchone()
		email = str(temp[0])
		rno = int(temp[1]) 
		c.execute("DELETE FROM bookings WHERE bno= ?;", (bno,))
		content = "Your booking "+str(bno)+" is cancelled"
		seen = 'n'
		msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
		c.execute("INSERT INTO inbox VALUES (?,?,?,?,?,?);",(email,msgTimestamp,user,content,rno,seen))
		conn.commit()
		print("Booking cancelled!")

def RequestRelated(user):
	while True:
		print("1. Post a request")
		print("2. List my own requests")
		print("3. Search requests")
		print("4. Go back")
		print("5. Log out")
		print("6. Exit")
		option = raw_input("Your option: ")
		if option == '1':
			postRequest(user)
		elif option == '2':
			myRequest(user)
		elif option == '3':
			searchRequest(user)
		elif option == '4':
			break
		elif option == '5':
			main()
		elif option == '6':
			quit()
		else:
			print("Command not found!")

def offerRide(user):
	c.execute("SELECT ifnull(max(rno),0) FROM rides")
	rno = int(c.fetchone()[0])+1
	while True:
		try:
			price = float(raw_input("Please enter the price: "))
			break
		except ValueError:
			print("Invalid input!")
			continue
	while True:
		rdate = raw_input("Please enter the date in YYYY-MM-DD format: ")
		try:
			time.strptime(rdate,"%Y-%m-%d")
			break
		except ValueError:
			print("Invalid input!")
			continue
	while True:
		seats = raw_input("Please enter the seats offered: ")
		try:
			seats = int(seats)
			break
		except ValueError:
			print("Invalid input!")
			continue
	c.execute("SELECT lcode FROM locations")
	ar = [[str(item) for item in results] for results in c.fetchall()]
	src = raw_input("Please enter your src: ")
	while [src] not in ar:
		searchLoc(src)
		src = raw_input("Please enter your src: ")

	dst = raw_input("Please enter your dst: ")
	while [dst] not in ar:
		searchLoc(dst)
		dst = raw_input("Please enter your dst: ")

	lugDesc = raw_input("Please enter the luggage description: ")
	while True:
		cno = raw_input("Please enter the car number: ")
		if cno == '':
			cno = None
			break
		else:
			try:
				cno = int(cno)
				c.execute("SELECT * FROM cars WHERE owner like '%s' and cno ='%d';" % (user,cno))
				check_car = c.fetchone()
				if check_car == None:
					print("That's not your car!")
					c.execute("SELECT * from cars where owner like '%s';"%(user,))
					print ("".join('%-20s'%x[0] for x in c.description))
					ar = [[str(item) for item in results] for results in c.fetchall()]
					for row in ar:
						print ("".join('%-20s'%x for x in row))
					continue
				else:
					break
			except ValueError:
				print("Invalid input!")
				continue
	c.execute("INSERT INTO rides VALUES (?,?,?,?,?,?,?,?,?);",(rno,price,rdate,seats,lugDesc,src,dst,user,cno))
	conn.commit()
	c.execute("SELECT lcode FROM locations")
	ar = [[str(item) for item in results] for results in c.fetchall()]
	enroute = raw_input("Please enter the enroute location: ")

	while enroute != '':
		while [enroute] not in ar:
			searchLoc(enroute)
			enroute = raw_input("Please enter your enroute location: ")
		c.execute("INSERT INTO enroute VALUES (?,?);",(rno,enroute))
		enroute = raw_input("Please enter next enroute location: ")
	conn.commit()
	print("New ride offered!")

def searchRides(user):
	keyword1 = raw_input("Keyword1: ")
	keyword2 = raw_input("Keyword2: ")
	if keyword2 != '':
		keyword3 = raw_input("Keyword3: ")
		if keyword3 != '':
			#search by 3
			searchbyK1 = searchKeyword(keyword1)
			searchbyK2 = searchKeyword(keyword2)
			searchbyK3 = searchKeyword(keyword3)
			ar = list((set(tuple(i) for i in searchbyK1)&set(tuple(j) for j in searchbyK2)&set(tuple(k) for k in searchbyK3)))

		else:
			#search by 2
			searchbyK1 = searchKeyword(keyword1)
			searchbyK2 = searchKeyword(keyword2)
			ar = list((set(tuple(i) for i in searchbyK1)&set(tuple(j) for j in searchbyK2)))
			
	else:
		#search by 1
		ar = searchKeyword(keyword1)
	description = ['rno', 'price', 'rdate', 'seats', 'lugDesc', 'src', 'dst', 'driver', 'cno', 'make', 'model', 'year', 'seats']	
	print ("".join('%-13s'%x for x in description))
	ar = map(list,ar)
	ar = sorted(ar, key=lambda x: int(x[0]))
	prtFive(ar)
	messageDriver(user)
	
def searchKeyword(keyword):
	c.execute("SELECT r.*,c.make,c.model,c.year,c.seats FROM rides r,enroute er,locations l \
			left join cars c on r.cno = c.cno \
			where (er.lcode = l.lcode and er.rno = r.rno)\
			and\
			(l.lcode like ? or l.city like ? or l.prov like ? or l.address like ?)\
			union \
			SELECT DISTINCT r.*,c.make,c.model,c.year,c.seats FROM rides r,locations l1, locations l2\
			left join cars c on r.cno = c.cno \
			WHERE (r.src = l1.lcode and  r.dst =l2.lcode)\
			and\
			(l1.lcode like ? or l1.city like ? or l1.prov like ? or l1.address like ? or \
			l2.lcode like ? or l2.city like ? or l2.prov like ? or l2.address like ? );",
			('%'+keyword+'%','%'+keyword+'%','%'+keyword+'%','%'+keyword+'%',
				'%'+keyword+'%','%'+keyword+'%','%'+keyword+'%','%'+keyword+'%',
				'%'+keyword+'%','%'+keyword+'%','%'+keyword+'%','%'+keyword+'%'))
	result = [[str(item) for item in results] for results in c.fetchall()]
	return result

def messageDriver(user):
	while True:
		rno = raw_input("Please enter the ride where you want to book:(BACK to go back) ")
		if rno.upper() == 'BACK':
			return
		else:
			try:
				rno = int(rno)
				break
			except ValueError:
				print("Invalid input!")
		
	c.execute("SELECT driver FROM rides WHERE rno = '%d';" % (int(rno)))
	email = str(c.fetchone()[0])
	msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	while True:
		try:
			cost = int(raw_input("Please enter your cost: "))
			break
		except ValueError:
			print("Invalid input!")
			continue
	while True:
		try:
			seats = int(raw_input("Please enter your seats booked: "))
			break
		except ValueError:
			print("Invalid input!")
			continue

	c.execute("SELECT lcode FROM locations")
	ar = [[str(item) for item in results] for results in c.fetchall()]

	pickup = raw_input("Please enter the pickup loc: ")
	while [pickup] not in ar:
		searchLoc(pickup)
		pickup = raw_input("Please enter the pickup loc: ")

	dropoff = raw_input("Please enter the dropoff loc: ")
	while [dropoff] not in ar:
		searchLoc(dst)
		dropoff = raw_input("Please enter your dst: ")

	content = "cost:"+str(cost) + "; "+"seats:"+str(seats) + "; "+"pickup:"+pickup + "; "+"dropoff: "+dropoff + "; "

	seen = 'n'

	c.execute("INSERT INTO inbox VALUES (?,?,?,?,?,?)",(email,msgTimestamp,user,content,rno,seen))

	conn.commit()
	print("message sent!")

def postRequest(user):
	c.execute("SELECT ifnull(max(rid),0) FROM requests")
	rid = int(c.fetchone()[0])+1
	while True:
		rdate = raw_input("Please enter the date in YYYY-MM-DD format: ")
		try:
			time.strptime(rdate,"%Y-%m-%d")
			break
		except ValueError:
			print("Invalid input!")
			continue
	c.execute("SELECT lcode FROM locations")
	ar = [[str(item) for item in results] for results in c.fetchall()]
	
	pickup = raw_input("Please enter the pickup loc: ")
	while [pickup] not in ar:
		searchLoc(pickup)
		pickup = raw_input("Please enter the pickup loc: ")

	dropoff = raw_input("Please enter the dropoff loc: ")
	while [dropoff] not in ar:
		searchLoc(dst)
		dropoff = raw_input("Please enter your dst: ")

	while True:
		try:
			amount = int(raw_input("Please enter the amount you are willing to pay per seat: "))
			break
		except ValueError:
			print("Invalid input!")
			continue
	
	c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?)",(rid,user,rdate,pickup,dropoff,amount))
	conn.commit()
	print("Request posted!")

def searchLoc(word):
	c.execute("SELECT * FROM locations where lcode like ? or city like ?\
		or prov like ? or address like ?;",('%'+word+'%','%'+word+'%','%'+word+'%','%'+word+'%'))
	print ("".join('%-13s'%x[0] for x in c.description))
	ar = [[str(item) for item in results] for results in c.fetchall()]
	prtFive(ar)

def myRequest(user):
	c.execute("SELECT * FROM requests where email like ?;",(user,))
	print ("".join('%-13s'%x[0] for x in c.description))
	ar = [[str(item) for item in results] for results in c.fetchall()]
	for row in ar:
		print ("".join('%-13s'%x for x in row))
	while True:
		print("Enter the rid to delete")
		rid = raw_input("Or enter Back to go back: ")
		try:
			rid = int(rid)
			c.execute("SELECT * FROM requests WHERE email like '%s' and rid='%d';" % (user,rid))
			check_ride = c.fetchone()
			if check_ride == None:
				print("That's not your request!")
				continue
			else:
				c.execute("DELETE FROM requests WHERE rid = ?;", (rid,))
				conn.commit()
				print("Request deleted!")
				break
		except ValueError:
			return

def searchRequest(user):
	keyword = raw_input("Please enther the pickup location to search: ")
	c.execute("SELECT r.* FROM requests r, locations l\
		WHERE (r.pickup = l.lcode and (\
		l.lcode like ? or l.city like ?\
		));",
		('%'+keyword+'%','%'+keyword+'%'))
	print ("".join('%-13s'%x[0] for x in c.description))
	ar = [[str(item) for item in results] for results in c.fetchall()]
	prtFive(ar)
	print("Enter the rid to select")
	rid = raw_input("Or enter Back to go back: ")
	if rid.upper() == 'BACK':
		return
	else:
		rid = int(rid)
		c.execute("SELECT email FROM requests where rid = ?;",(rid,))
		email = str(c.fetchone()[0])
		content = raw_input("Enter your message to the person: ")
		seen = 'n'
		msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
		rno = raw_input("Please enter the ride number: ")
		c.execute("INSERT INTO inbox VALUES (?,?,?,?,?,?)",(email,msgTimestamp,user,content,rno,seen))
		conn.commit()
		print("Message sent!")

def prtFive(ar):
	start = 5
	for row in ar[0:start]:
		print ("".join('%-13s'%x for x in row))
	while len(ar)>5:
		option = raw_input("enter Y to see more: ")
		if option.upper() == 'Y':
			end = start+5
			if end > len(ar):
				for row in ar[start:len(ar)]:
					print ("".join('%-13s'%x for x in row))
				break
			else:
				for row in ar[start:end]:
					print ("".join('%-13s'%x for x in row))
			start = end
		else:
			break

main()



	






