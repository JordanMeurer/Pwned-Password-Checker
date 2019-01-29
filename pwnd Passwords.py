# code: UTF-8
from tkinter import * 
import json
import os
import requests
import wget
import threading
import hashlib
import io


#Global variables
headers = requests.utils.default_headers()								#Creating the header object
headers.update({'User-Agent': 'Test program by Anon'})					#Updating the header information
c_url = "https://haveibeenpwned.com/api/v2/breaches"					#URL for the companies parse
url = "https://api.pwnedpasswords.com/range/"							#URL for the passwords parse

#password class, I don't think it will be used since we can't see companies
class Passwords:
	def __init__(self, company, password):
		self.company = company
		self.password = password
	
class Main:
	def __init__(self, master):
		c_response = requests.get(c_url, headers = headers)				#Checks the Rest server
		if c_response.status_code !=200:								#If there is a problem it exits
			print("There was a problem")
			exit()
		
		#Shows that everything worked
		json_companies = c_response.json()
		companies = []
		for x in range(0, len(json_companies)):
			companies.append(json_companies[x]['Name'])
		frame = Frame(master)
		frame.pack()
		
		#Drop down for companies
		value = StringVar(frame)							#Builds dropd
		value.set(companies[0])                             #Change to change the first company
		self.Options = OptionMenu(frame, value, *companies) #Change "None" to *companies
		self.Options.grid(row = 0, column = 3)
		
		#Label for companies
		self.Label0 = Label(frame, text='Companies List')
		self.Label0.grid(row = 0, column = 2)
		
		#User password input
		self.input = Entry(frame, show='*')
		self.input.bind('<Return>', self.submit)			#Allows user to hit enter to submit
		self.input.grid(row = 1, column = 3)
		
		#Submit Button
		self.Submit = Button(frame, text="Submit", command = self.submit)
		self.Submit.grid(row=2, column = 3)
		
	#Creates the thread for use	
	def submit(self, event = None):
		threading.Thread(name='API Thread', target=self.callAPI).start()
		
	#Hashes and calls the API
	def callAPI(self, event = None):
		hash = hashlib.sha1()								#Creates the hash object
		hash.update(self.input.get().encode('utf-8'))		#Hashes the user's input
		hash_text = hash.hexdigest()						#Gets the hash value
		response = requests.get(url + hash_text[0:5])		#Sends off to the API
		file_obj = io.StringIO(response.text)				#Parses the response
		lines = file_obj.readlines()						#Sets the response into lines
		for x in range(len(lines)):							#Loops looking for the match
			if(hash_text[5:].upper() == lines[x][0:35]):	#Checks the last 35 of our hash with their first 35
				print(lines[x][0:35])						#Prints the hash for now
				print("Match, found %s times" % (lines[x][36:].strip('\n'))) #Informs of match
		print("Next")
	#This won't be used (for now)
	def email_check(self, Options, value):					#I will come back to this eventually
		if self.input.get() == '':							#Checks for empty input
			print("No email set")							#Informs the user, will have to add that to the gui
		else:												#If the user has input
			url = "https://haveibeenpwned.com/api/v2/pasteaccount/" + self.input.get()#Creates the URL for the API
			headers = requests.utils.default_headers()		#Creates the header object
			headers.update({'User-Agent': 'PythonPwndPasswords/Beta'}) #Updates the header
			response=requests.post(url, headers = headers)	#Sends of the request
			if(response.status_code == 404):				#404 means it couldn't find the data, email not there
				print("Account wasn't found!")			
			elif (response.status_code == 400):				#400, the user inputted something wrong
				print("Invalid format")
			elif (response.status_code == 200):				#200, OK meaning it is apart of the list
				print("Account found")
			else:											#Any other error just in case
				print(response.status_code)
				

root = Tk()                          						#Creates the GUI object
root.title("Pwn'd passwords")								#Changes the title of the program
root.minsize(height=100, width=350)							#Creates the minimal size of the program
root.resizable(0,0)											#Doesn't allow resizing (for now I guess)
b = Main(root)												#Honestly I don't remember
root.mainloop()												#Main loop for the GUI