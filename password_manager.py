import hashlib
import os

# An object that represents each account
class Account:
	# Constructor method, each Account instance/object will have a username and password
	def __init__(self, username, password):
		self.username = username
		self.password = password

		# Hashing using md5 message digest algorithm
		hash1 = hashlib.md5(self.password.encode('utf-8'))
		self.key = hash1.hexdigest()

	# Method has not yet been implemented, algorithm and features still need work
	def change_password(self, new_password):
		self.password = new_password
		self.hash_password(self.new_password)

# Function that takes on the process of creating a new user
def create_new_user(username = None):
	if username == None:
		username = input("Please enter a username: ")

		f = open('database.txt', 'r')
		lines = f.readlines()
		f.close()

		# Checks to see if a user with the same username already exists, and does not allow creation of another user with the same username
		if (username+'\n') in lines:
			while (username+'\n') in lines:
				print("An account already exists under this username. Please enter a new username.")
				username = input("Please enter a username: ")
	
	# Asks the user to enter and re-enter a password for their new account

	while True:
		password = input("Please enter a password: ")
		password_reenter = input("Please re-enter your password: ")
		if password == password_reenter:
			break
		print("Your passwords do not match. Please try again.")

	# If user enters a valid username and successfully enters their password twice, an Account instance is created using the entered credentials
	new_user = Account(username, password)

	# Write to database.txt all the new account's info
	'''Notice that the password is not stored in plain text in the textile, it is hashed and stored
		like how passwords are really stored in databases'''
	lines_to_write = ["username:"+"\n"+new_user.username+"\n", "password hash:"+"\n"+str(new_user.key)+"\n\n"]
	f = open('database.txt', 'a')
	f.writelines(lines_to_write)
	f.close()

	# Return the new_user instance of Account
	return new_user

# Function for checking if user login credentials are valid
def valid_login(username, password):
	f = open('database.txt', 'r')
	lines = f.readlines()
	f.close()

	'''If the user enters a username that does not already exist, they will be given the option to create an account using that username
	 	that they just entered'''
	if (username+'\n') not in lines:
		y_or_n = input("An account with this username does not currently exist. Would you like to create a new account with this username? ('yes' or 'no') ")
		if y_or_n == 'yes':
			# The create_new_user function takes over from here, passing in an optional username argument
			create_new_user(username)
		else:
			y_or_n = input("Would you like to try again with an existing username? ('yes' or 'no') ")
			if y_or_n == 'yes':
				while True:
					# Check again for existing username, if it exists then break out of the loop
					username = input("Enter your username: ")
					if (username+'\n') in lines:
						break
					print("An account with this username does not currently exist. Please try again.")

			# Some room for improvement/new features/options if the user chooses to say no, will add later once core functions are completed
			else:
				print("Okay, bye.")
				quit()

	f = open('database.txt', 'r')
	lines = f.readlines()
	f.close()

	# Recreate an md5 hash of the entered password
	key_index = lines.index((username+'\n')) + 2
	key = lines[key_index]

	hash2 = hashlib.md5(password.encode('utf-8'))

	new_key = hash2.hexdigest()
	
	# If the existing password hash in the text file matches the newly created password has of the password that was just entered, return True
	if str(new_key) == str(key)[:len(str(key)) - 1]:
		return True

	# If the hashes do not match, return false
	return False

# Function that creates the text file database in case it does not already exist in the same directory as the Python file
def check_db_existence():
	try:
		f = open('database.txt', 'r')
	except:
		f = open('database.txt', 'w')
	finally:
		f.close()

# Print the greeting message
greeting = "WELCOME"
print(greeting)

new_or_existing = input("Create new account or login with existing account? (Type 'new' or 'existing') ")

check_db_existence()

if new_or_existing == 'new':
	# User will be assigned the Account instance that is returned by the create_new_user() function
	user = create_new_user()
	print("Your account has been created. Welcome.")

else:
	username = input("Enter your username: ")
	password = input("Enter your password: ")
	if valid_login(username, password):
		user = Account(username, password)
		print("Welcome,", user.username)
	else:
		print("Incorrect username and/or password.")
		quit()
