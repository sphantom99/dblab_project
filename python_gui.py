import tkinter as tn 
from tkinter import messagebox as msg
import mysql.connector as con
import re 

"""
The general idea for all the windows is the same. Firstly we create labels so as to mark the data that is supposed to 
be inserted in the entry fields and then I create the entry fields. Most windows created are shown by using the .grid() 
method which treats the window as an array thus by defining the values we can place them on the window.
If we wish to create a new window other than the main window we first have to create a "Toplevel" which is the basic 
window and then create an instance of the class window we wish to view extending the Toplevel.

The connection with the db is done using the mysql library. We created several more stored procedures to make 
this python programm completely without mysql involved. To call a stored procedure after we create a cursor object 
we use the .callproc() method which with the proc name and the arguments as a list executes it inside the DB. If changes
were made to the DB (inserting) we have to call the commit() method for the connection object so as to make them 
permanent
"""


#Login Window 
class login(object):
	"""
	This is the login window, three labels , two entryfields and two buttons.
	When user hits button => login we query the db for the combination of username and pass
	If found we spawn the corresponding window...
	"""
	
	def __init__(self, master):
		self.user = ""
		self.master = master
		#self.master.title("Welcome")
		self.var = tn.StringVar()
		self.var.set("Welcome\nPlease login")
		self.welcome_label = tn.Label(master,textvar=self.var)
		self.welcome_label.grid(columnspan=2,sticky=tn.N,row = 0)

		self.image = tn.PhotoImage(file="./assets/login.png")
		global imageicon
		imageicon = tn.PhotoImage(file="./assets/newspaper4.png")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.imagelabel = tn.Label(master)
		self.imagelabel.grid(columnspan = 2, row = 1 ,column = 0)
		self.imagelabel['image']= self.image
		
		self.label_username = tn.Label(master,text = "Username:")
		self.label_username.grid(row = 2 , column = 0)

		self.label_password = tn.Label(master,text = "Password:")
		self.label_password.grid(row = 3 , column = 0)

		self.entry_username = tn.Entry(master)
		self.entry_username.grid(row = 2 , column = 1)

		self.entry_password = tn.Entry(master,show="*")
		self.entry_password.grid(row = 3,column = 1)	

		self.login_button = tn.Button(master,text="Login",command = self.validation)
		self.login_button.grid(row=4,column=0)	

		self.login_button = tn.Button(master,text="Quit",command = master.quit)
		self.login_button.grid(row=4,column=1)	
		
	def validation(self): #--------------------------------------------------------------------------
		"""
		self.user = self.entry_username.get()
		password = self.entry_password.get()
		if self.user == "1234" and password == "1234":
			new = tn.Toplevel()
			newj = journalist(new)
		"""
		global pattern
		pattern = ["select","SELECT","DROP","drop","'",";"]
		
		credlist = []
		
		self.user = self.entry_username.get()
		password = self.entry_password.get()
		for x in pattern:
			if re.search(x,self.user):
				self.var.set("you are an asshole...")
				re.sub(x," ",self.user)
				pass
			pass
		curs.callproc("validatePassword",[self.user])
		for x in curs.stored_results():
			credlist = x.fetchall()
		if self.user == "Efstratios Gallopoulos" and password == "4321":
			new = tn.Toplevel(class_="Main Window")
			newpublisher = publisher(new)
		elif self.user == "Eleni Voyatzaki" and password == "4321":
			new = tn.Toplevel(class_="Main Window")
			newpublisher = publisher(new)
		elif self.user == "Maria Rigou" and password == "4321":
			new = tn.Toplevel(class_="Main Window")
			newpublisher = publisher(new)	
		elif credlist[0][0] == password :
			if credlist[0][1]=="Journalist":
				new = tn.Toplevel(class_="Main Window")      
				newemp = journalist(new)
			if credlist[0][1]=="Editor_in_chief":
				new = tn.Toplevel(class_="Main Window")
				neweditor = editor_in_chief(new)
			if credlist[0][1]=="Administrative":
				new = tn.Toplevel(class_="Main Window")
				newadmin = administrative(new)
		else:
			msg.showwarning("Incorrect","The credentials you entered are Incorrect")
		self.master.iconify()
	


#Journalist Windows

class journalist(login,object):
	"""
	docstring for employee

	if the user entered is an employee this window spawns
	prompting the user for an answer about what he wants to do.


	"""
	def __init__(self,master):
		
		
		self.var1 = tn.IntVar()
		self.var1.set(20)
		self.master = master
		master.title("Welcome")
		self.image = tn.PhotoImage(file="./assets/journalist2.png")
		self.image = self.image.subsample(5,5)
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.var = tn.StringVar()
		self.var.set("Welcome\nWhat would you like to do?")
		self.welcome_label = tn.Label(master,textvar=self.var)
		self.welcome_label.pack()  #grid(columnspan=2,sticky=tn.N,row = 0)
		self.imagelabel = tn.Label(master)
		self.imagelabel.pack()
		self.imagelabel['image'] = self.image
		options=[("Submit an article",0),("View an article",1),("Revise an article",2)]

		for text,val in options:
			tn.Radiobutton(master,text=text , value = val , variable = self.var1).pack()

		self.but = tn.Button(master,text="Select",command=self.checkans)
		self.but.pack()
		self.quit = tn.Button(master,text="Quit",command=master.quit)
		self.quit.pack()

	def checkans(self):
		if self.var1.get()==0:
			submit = tn.Toplevel(class_="Submission")
			subwin = submission(submit)
			
		elif self.var1.get()==1:
			viewer = tn.Toplevel(class_="View")
			viewwin = view(viewer)
			
		elif self.var1.get()==2:
			revision = tn.Toplevel(class_="Revision")
			revisewin = revise(revision)			

class submission(object):
	"""
	docstring for submission

	allows the user to enter specific values to be inserted in the db

	"""
	def __init__(self,master):
				
		self.choice = []
		self.author_check = tn.IntVar()
		self.choices_Categories = []
		curs.callproc("showAllCategories")
		for x in curs.stored_results():
			self.choice = x.fetchall()
		for y in range(len(self.choice)):
			for x in self.choice[y]:
				self.choices_Categories.append(x.encode("utf-8"))
				
		

		self.welcomevar = tn.StringVar()
		self.welcomevar.set("Please fill out the next fields..")
		self.ansstring_Category = tn.StringVar()
		
		self.master = master
		master.title("Submission")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,textvar=self.welcomevar)
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.label_Path = tn.Label(master,text="Path:")
		self.label_Path.grid(row = 1 ,column = 0)
		self.label_Title = tn.Label(master,text="Title")
		self.label_Title.grid(row = 2 , column = 0)
		self.label_Summary = tn.Label(master,text="Summary:")
		self.label_Summary.grid(row = 3 ,column = 0)
		self.label_Photo = tn.Label(master,text="Path to image:")
		self.label_Photo.grid(row = 4 ,column = 0)
		self.label_Category = tn.Label(master,text="Category:")
		self.label_Category.grid(row = 5 ,column = 0)
		self.label_Pages = tn.Label(master,text="No. of Pages:")
		self.label_Pages.grid(row = 6 ,column = 0)
		self.label_Keywords = tn.Label(master,text="Keywords:")
		self.label_Keywords.grid(row = 7 ,column = 0)

		self.entryfield_Path = tn.Entry(master)
		self.entryfield_Path.grid(row = 1, column = 1)
		self.entryfield_Title = tn.Entry(master)
		self.entryfield_Title.grid(row = 2, column = 1)
		self.entryfield_Summary = tn.Entry(master)
		self.entryfield_Summary.grid(row = 3,column = 1)
		self.entryfield_Photo = tn.Entry(master)               #No of pages to be added
		self.entryfield_Photo.grid(row = 4, column = 1)
		self.optionmenu_Category = tn.OptionMenu(master,self.ansstring_Category, *self.choices_Categories)         
		self.optionmenu_Category.grid(row = 5, column = 1)
		self.entryfield_Pages = tn.Entry(master)
		self.entryfield_Pages.grid(row = 6, column = 1)
		self.entryfield_Keywords = tn.Entry(master)
		self.entryfield_Keywords.grid(row = 7, column = 1)
		self.optionmenu_Coauthor = tn.Checkbutton(master,text="Has Coauthors ",variable = self.author_check)         
		self.optionmenu_Coauthor.grid(columnspan = 2,row = 8, column = 1)
		
		self.accept = tn.Button(master,text = "Submit",command=self.submit_article)
		self.accept.grid(row = 9 ,column = 0)

		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=9,column = 1)

	def submit_article(self):
		if int(self.entryfield_Pages.get()) < 1 or int(self.entryfield_Pages.get()) > 20:
			self.label_Pages.config(fg = "RED")
			self.welcomevar.set("Incorrect value")
			pass
		else :
			global path
			catname = []
			res = []
			path = self.entryfield_Path.get()
			
			#insert into table articles blah blah blah...
			
			curs.callproc("getCategoryCode",[self.ansstring_Category.get()])
			for i in curs.stored_results():
				res = i.fetchone()
			
			curs.callproc("insertArticleAsJournalist",[self.entryfield_Path.get(), #
													self.entryfield_Title.get(),
													self.entryfield_Summary.get(),
													self.entryfield_Photo.get(),
													res[0],
													self.entryfield_Pages.get(),
													tester.user])
			a.commit()
			if self.author_check.get() == 1 :
				coauth = tn.Toplevel()
				newcoauth = insertCoauthors(coauth)
				pass
			keywords = self.entryfield_Keywords.get()
			key_list = keywords.split()
			for i in key_list:
				curs.callproc("addKeywords",[path,i])
				a.commit()
			
			msg.showinfo("Complete","The article has been submitted..")
			self.master.destroy()

class insertCoauthors(object):
	"""docstring for insertCoauthors"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showRestJournalists",[tester.user])
		for i in curs.stored_results():
			self.listing = i.fetchall()
		for x in range(len(self.listing)):
			for y in self.listing[x]:
				self.choices.append(y.encode("utf-8"))		
		
		self.master = master
		self.master.title("Coauthors")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Please Submit a Coauthor")
		self.welcome_label.pack()
		self.menubutton = tn.Menubutton(master, text="Pick a Journalist", indicatoron=True,borderwidth=1, relief="raised")
		self.menu = tn.Menu(self.menubutton, tearoff=False)
		self.menubutton.configure(menu=self.menu)
		for choice in self.choices:
			self.menu.add_command(label=choice,command=lambda option=choice: self.set_option(option))
		self.menubutton.pack()
		self.quit_button = tn.Button(master,text="Quit",command = master.destroy)
		self.quit_button.pack()

	def set_option(self,option):
		
		curs.callproc("insertCoAuthor",[path,option])
		a.commit()
		
		self.menu.delete(option)
		pass
	
class view(object):
	"""docstring for view"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showAllJournalistArticles",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Articles")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose which article you wish to view..")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.view_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)

	def view_selected(self):
		global view_ans
		view_ans = self.ansstring1.get()
		viewresult = tn.Toplevel(class_="View Result")
		viewreswin = viewres(viewresult)
		pass

class viewres(object):
	"""docstring for viewres"""
	def __init__(self, master):
		

		curs.callproc("showArticle",[view_ans])
		for i in curs.stored_results():
			result = i.fetchall()
			pass
		curs.callproc("getCatName",[result[0][11]])
		for x in curs.stored_results():
			catname = x.fetchall()
			pass
		self.master = master
		master.title("Results")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="The article you selected has the following attributes :")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)
		
		self.label_Path = tn.Label(master,text="Path: "+ str(result[0][0]))
		self.label_Path.grid(row = 1 ,column = 0)
		self.label_Title = tn.Label(master,text="Title: "+str(result[0][1]))
		self.label_Title.grid(row = 2 , column = 0)
		self.label_Summary = tn.Label(master,text="Summary: "+str(result[0][2]))
		self.label_Summary.grid(row = 3 ,column = 0)
		self.label_Photo = tn.Label(master,text="Path to image: "+str(result[0][8]))
		self.label_Photo.grid(row = 4 ,column = 0)
		self.label_IssueNo = tn.Label(master,text="IssueNo : "+str(result[0][9]))
		self.label_IssueNo.grid(row = 5 ,column = 0)
		self.label_Category = tn.Label(master,text="Category: "+str(catname[0][0]))
		self.label_Category.grid(row = 6 ,column = 0)
		self.label_Checked = tn.Label(master,text="Status: " +str(result[0][5]))
		self.label_Checked.grid(row=7,column = 0)
		self.label_Pages = tn.Label(master,text="No. of Pages: "+str(result[0][7]))
		self.label_Pages.grid(row = 8 ,column = 0)
		self.label_Approval = tn.Label(master,text="Approval Date: "+str(result[0][12]))
		self.label_Approval.grid(row = 9 ,column = 0)
		self.label_Comments = tn.Label(master,text="Comments: "+str(result[0][4]))
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row = 10 , column = 0)
		
class revise(object):
	"""docstring for revise"""
	def __init__(self, master):
		
		self.choices = []
		curs.callproc("showAllJournalistArticles",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Revision")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose which article you wish to revise..")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.replace)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)
	def replace(self):
		global path_to_be_revised
		path_to_be_revised = self.ansstring1.get()
		resub = tn.Toplevel(class_="Revised Submission")
		resubwin = revisedsubmission(resub)
				
class revisedsubmission(object):
	"""
	docstring for submission

	allows the user to enter specific values to be inserted in the db

	"""
	def __init__(self,master):
		
		self.choice = []
		self.author_check = tn.IntVar()
		self.choices_Categories = []
		curs.callproc("showAllCategories")
		for x in curs.stored_results():
			self.choice = x.fetchall()
		for y in range(len(self.choice)):
			for x in self.choice[y]:
				self.choices_Categories.append(x.encode("utf-8"))
				
		


		self.ansstring_Category = tn.StringVar()
		
		self.master = master
		master.title("Submission")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Please fill out the next fields")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.label_Title = tn.Label(master,text="Title")
		self.label_Title.grid(row = 2 , column = 0)
		self.label_Summary = tn.Label(master,text="Summary:")
		self.label_Summary.grid(row = 3 ,column = 0)
		self.label_Photo = tn.Label(master,text="Path to image:")
		self.label_Photo.grid(row = 4 ,column = 0)
		self.label_Category = tn.Label(master,text="Category:")
		self.label_Category.grid(row = 5 ,column = 0)
		self.label_Pages = tn.Label(master,text="No. of Pages:")
		self.label_Pages.grid(row = 6 ,column = 0)
		self.label_Keywords = tn.Label(master,text="Keywords:")
		self.label_Keywords.grid(row = 7 ,column = 0)

		self.entryfield_Title = tn.Entry(master)
		self.entryfield_Title.grid(row = 2, column = 1)
		self.entryfield_Summary = tn.Entry(master)
		self.entryfield_Summary.grid(row = 3,column = 1)
		self.entryfield_Photo = tn.Entry(master)               #No of pages to be added
		self.entryfield_Photo.grid(row = 4, column = 1)
		self.optionmenu_Category = tn.OptionMenu(master,self.ansstring_Category, *self.choices_Categories)         
		self.optionmenu_Category.grid(row = 5, column = 1)
		self.entryfield_Pages = tn.Entry(master)
		self.entryfield_Pages.grid(row = 6, column = 1)
		self.entryfield_Keywords = tn.Entry(master)
		self.entryfield_Keywords.grid(row = 7, column = 1)
		self.optionmenu_Coauthor = tn.Checkbutton(master,text="Has Coauthors ",variable = self.author_check)         
		self.optionmenu_Coauthor.grid(columnspan = 2,row = 8, column = 1)
		
		self.accept = tn.Button(master,text = "Submit",command=self.submit_revised_article)
		self.accept.grid(row = 9 ,column = 0)

		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=9,column = 1)

	
	def submit_revised_article(self):
		if int(self.entryfield_Pages.get()) < 1 or int(self.entryfield_Pages.get()) > 20:
			self.label_Pages.config(fg = "RED")
			self.welcomevar.set("Incorrect value")
			pass
		else :
			
			catname = []
			res = []
			
			
			#insert into table articles blah blah blah...
			
			curs.callproc("getCategoryCode",[self.ansstring_Category.get()])
			for i in curs.stored_results():
				res = i.fetchone()
			
			curs.callproc("updateArticle",[path_to_be_revised, #
													self.entryfield_Title.get(),
													self.entryfield_Summary.get(),
													self.entryfield_Pages.get(),
													self.entryfield_Photo.get(),
													res[0],
													tester.user])
			a.commit()
			if self.author_check.get() == 1 :
				coauth = tn.Toplevel()
				newcoauth = insertCoauthors(coauth)
				pass
			keywords = self.entryfield_Keywords.get()
			key_list = keywords.split()
			for i in key_list:
				curs.callproc("addKeywords",[path_to_be_revised,i])
				a.commit()
			
			msg.showinfo("Complete","The article has been revised..")
			self.master.destroy()
	
	
#Editor in chief windows

class editor_in_chief(object):
	"""docstring for editor_in_chief"""
	def __init__(self, master):
		self.master = master
		master.title("Welcome")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.image = tn.PhotoImage(file="./assets/editor.png")
		self.image = self.image.subsample(2,2)
		self.var = tn.StringVar()
		self.var.set("Welcome\nWhat would you like to do?")
		self.var1 = tn.IntVar()
		self.var1.set(100)
		self.welcome_label = tn.Label(master,textvar=self.var)
		self.welcome_label.pack()  #grid(columnspan=2,sticky=tn.N,row = 0)
		self.imagelabel = tn.Label(master)
		self.imagelabel.pack()
		self.imagelabel['image'] = self.image
		editor_options = [("view written articles",0),
						  ("set the order of articles",1),
						  ("submit an article",2),
						  ("insert a new Category",3)]
		for text,val in editor_options:
			tn.Radiobutton(master,text=text , variable = self.var1 , value = val).pack()
		
		self.select = tn.Button(master,text="Select",command=self.execute)
		self.select.pack()
		self.quit = tn.Button(master,text="Quit",command=master.quit)
		self.quit.pack()

	def execute(self):
		if self.var1.get() == 0 :
			
			viewer = tn.Toplevel(class_="View")
			viewwindow = editor_view(viewer)
			
			
		elif self.var1.get() == 1:
			ordering = tn.Toplevel(class_="Ordering")
			orderwin = order_set(ordering)
		
		elif self.var1.get() == 2:
			submis = tn.Toplevel(class_="Submission")
			subwin = editor_submission(submis)
		
		elif self.var1.get() == 3:
			categ = tn.Toplevel(class_="Categories")
			categwin = category(categ)
		
class editor_submission(object):
	"""
	docstring for submission

	allows the user to enter specific values to be inserted in the db

	"""
	def __init__(self,master):
		
		self.choice = []
		self.author_check = tn.IntVar()
		self.choices_Categories = []
		curs.callproc("showAllCategories")
		for x in curs.stored_results():
			self.choice = x.fetchall()
		for y in range(len(self.choice)):
			for x in self.choice[y]:
				self.choices_Categories.append(x.encode("utf-8"))
				
		


		self.ansstring_Category = tn.StringVar()
		
		self.master = master
		master.title("Submission")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		
		self.welcome_label = tn.Label(master,text="Please fill out the next fields")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.label_Path = tn.Label(master,text="Path:")
		self.label_Path.grid(row = 1 ,column = 0)
		self.label_Title = tn.Label(master,text="Title")
		self.label_Title.grid(row = 2 , column = 0)
		self.label_Summary = tn.Label(master,text="Summary:")
		self.label_Summary.grid(row = 3 ,column = 0)
		self.label_Photo = tn.Label(master,text="Path to image:")
		self.label_Photo.grid(row = 4 ,column = 0)
		self.label_Category = tn.Label(master,text="Category:")
		self.label_Category.grid(row = 5 ,column = 0)
		self.label_Pages = tn.Label(master,text="No. of Pages:")
		self.label_Pages.grid(row = 6 ,column = 0)
		self.label_Keywords = tn.Label(master,text="Keywords:")
		self.label_Keywords.grid(row = 7 ,column = 0)

		self.entryfield_Path = tn.Entry(master)
		self.entryfield_Path.grid(row = 1, column = 1)
		self.entryfield_Title = tn.Entry(master)
		self.entryfield_Title.grid(row = 2, column = 1)
		self.entryfield_Summary = tn.Entry(master)
		self.entryfield_Summary.grid(row = 3,column = 1)
		self.entryfield_Photo = tn.Entry(master)               #No of pages to be added
		self.entryfield_Photo.grid(row = 4, column = 1)
		self.optionmenu_Category = tn.OptionMenu(master,self.ansstring_Category, *self.choices_Categories)         
		self.optionmenu_Category.grid(row = 5, column = 1)
		self.entryfield_Pages = tn.Entry(master)
		self.entryfield_Pages.grid(row = 6, column = 1)
		self.entryfield_Keywords = tn.Entry(master)
		self.entryfield_Keywords.grid(row = 7, column = 1)
		self.optionmenu_Coauthor = tn.Checkbutton(master,text="Has Coauthors ",variable = self.author_check)         
		self.optionmenu_Coauthor.grid(columnspan = 2,row = 8, column = 1)
		
		self.accept = tn.Button(master,text = "Submit",command=self.submit_article)
		self.accept.grid(row = 9 ,column = 0)

		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=9,column = 1)

	def submit_article(self):
		global path
		catname = []
		res = []
		path = self.entryfield_Path.get()
		
		#insert into table articles blah blah blah...
		
		curs.callproc("getCategoryCode",[self.ansstring_Category.get()])
		for i in curs.stored_results():
			res = i.fetchone()
		
		curs.callproc("insertArticleAsEditor",[ self.entryfield_Path.get(), #
												self.entryfield_Title.get(),
												self.entryfield_Summary.get(),
												self.entryfield_Pages.get(),
												self.entryfield_Photo.get(),
												res[0],
												tester.user])
		a.commit()
		if self.author_check.get() == 1 :
			coauth = tn.Toplevel()
			newcoauth = insertCoauthors(coauth)
			pass
		keywords = self.entryfield_Keywords.get()
		key_list = keywords.split()
		for i in key_list:
			curs.callproc("addKeywords",[path,i])
			a.commit()
		
		msg.showinfo("Complete","The article has been submitted..")	
		self.master.destroy()	

class editor_view(object):
	"""docstring for editor_view"""
	def __init__(self, master):

		self.choices = []
		curs.callproc("showAllArticles",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Articles")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose which article you wish to view..")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master , self.ansstring1 ,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.view_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)


	def view_selected(self):
		global view_ans
		view_ans = self.ansstring1.get()
		viewresult = tn.Toplevel(class_="View Results")
		viewreswin = editorviewres(viewresult)
		
class editorviewres(object):
	"""docstring for editorviewres"""
	def __init__(self, master):
		curs.callproc("showArticle",[view_ans])
		for i in curs.stored_results():
			result = i.fetchall()
			pass
		curs.callproc("getCatName",[result[0][11]])
		for x in curs.stored_results():
			catname = x.fetchall()
			pass
		self.master = master
		master.title("Results")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="The article you selected has the following attributes :")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)
		
		self.label_Path = tn.Label(master,text="Path: "+ str(result[0][0]))
		self.label_Path.grid(row = 1 ,column = 0)
		
		self.label_Title = tn.Label(master,text="Title: "+str(result[0][1]))
		self.label_Title.grid(row = 2 , column = 0)
		
		self.label_Summary = tn.Label(master,text="Summary: "+str(result[0][2]))
		self.label_Summary.grid(row = 3 ,column = 0)
		
		self.label_Photo = tn.Label(master,text="Path to image: "+str(result[0][8]))
		self.label_Photo.grid(row = 4 ,column = 0)
		
		self.label_IssueNo = tn.Label(master,text="IssueNo : "+str(result[0][9]))
		self.label_IssueNo.grid(row = 5 ,column = 0)
		
		self.label_Category = tn.Label(master,text="Category: "+str(catname[0][0]))
		self.label_Category.grid(row = 6 ,column = 0)
		
		self.label_Checked = tn.Label(master,text="Status: " +str(result[0][5]))
		self.label_Checked.grid(row = 7,column = 0)
		
		self.label_Pages = tn.Label(master,text="No. of Pages: "+str(result[0][7]))
		self.label_Pages.grid(row = 8 ,column = 0)
		
		
		self.assess = tn.Button(master,text="Assess",command=self.assess)
		self.assess.grid(row = 9 , column = 0)
		
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row = 9 , column = 1)

	def assess(self):
		assessment = tn.Toplevel(class_="Assessment")
		assessmentwin = assession(assessment)
		self.master.destroy()
		pass

class assession(object):
	"""docstring for assession"""
	def __init__(self, master):
		
		self.master = master
		master.title("Assession")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.ans_assessment = tn.StringVar()
		self.welcome_label = tn.Label(master,text="Choose which state you wish to put the article in..")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)
		self.choices=["APPROVED","TO BE REVISED","DENIED"]
		self.list = tn.OptionMenu(master,self.ans_assessment,*self.choices)
		self.list.grid(columnspan=2 , row = 1 , column = 0)
		self.accept = tn.Button(master,text="Accept",command=self.make_assession)
		self.accept.grid(row = 4,column=0)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row = 4,column=1)

	def make_assession(self):
		
		curs.callproc("updateCheckStatus",[view_ans,self.ans_assessment.get()])
		a.commit()
		if self.ans_assessment.get() == "TO BE REVISED":
			commenting = tn.Toplevel(class_="Comments")
			commentwin = comments(commenting)

		msg.showinfo("Success","Your assessment has been made")
		self.master.destroy()
		
class comments(object):
	"""docstring for comments"""
	def __init__(self, master):
		self.master = master
		master.title("Comments for revision")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.commentlabel = tn.Label(master,text="Comments: ")
		self.commentlabel.grid(row=1,column = 0)
		self.commententry = tn.Entry(master)
		self.commententry.grid(row=1,column=1)
		self.accept = tn.Button(master,text="Accept",command=self.send_comments)
		self.accept.grid(row = 2,column=0)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row = 2,column=1)	
	def send_comments(self):
		curs.callproc("updateComments",[view_ans,self.commententry.get()])
		a.commit()
		msg.showinfo("Success","Your comments have been noted")
		self.master.destroy()

class order_set(object):
	"""docstring for orderset"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showAllIssues",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		self.master.title("Issues")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose the issue: ")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.choose_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)
	def choose_selected(self):
		global issue_No
		issue_No = self.ansstring1.get()
		setting = tn.Toplevel(class_="Order")
		setwin = actual_set(setting)

class actual_set(object):
    """docstring for actual_set"""
    def __init__(self, master):
        a = []
        self.order = 0
        finlist = []
        self.textlist = []
        self.art_list = []
        self.fetch_list = []
        self.master = master
        self.pagevar = tn.IntVar() 
        curs.callproc("getNumberOfPages",[tester.user,issue_No])
        for x in curs.stored_results():
        	a = x.fetchone()
        	pass
        self.pagevar.set(a[0])
        self.welcomevar = tn.StringVar()
        self.welcomevar.set("Please select the articles in the order you wish to Print them\n Pages Remaining: "+str(self.pagevar.get()))
        self.welcome_label = tn.Label(master,textvar = self.welcomevar)
        self.welcome_label.pack()
        master.title("Orders")
        self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
        curs.callproc("showAllArticlesNotInIssue",[tester.user,issue_No])
        for x in curs.stored_results():
            self.fetch_list = x.fetchall()
            pass
        for i in range(len(self.fetch_list)):
            for y in self.fetch_list[i]:
                if type(y) == int:
                    self.art_list.append(y)
                else:
                    self.art_list.append(y.encode("UTF-8"))
        for x in range(0,len(self.art_list),2):
            self.textlist.append(str(self.art_list[x]+" "+str(self.art_list[x+1])))
            pass

        self.menubutton = tn.Menubutton(master, text="Pick an Article", indicatoron=True,borderwidth=1, relief="raised")
        self.menu = tn.Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.menu)
        for choice in self.textlist:
            self.menu.add_command(label=choice,command=lambda option=choice: self.set_option(option))
        self.menubutton.pack()
        self.quit_button = tn.Button(master,text="Quit",command = master.destroy)
        self.quit_button.pack()

    def set_option(self,option):
        self.welcome_label.config(fg="BLACK")
        ind = self.textlist.index(option)
        finlist = option.split()
        
        if self.pagevar.get()-int(finlist[1]) < 0 : 
            self.welcome_label.config(fg="RED")
            self.welcomevar.set("Cannot go above the limit... \n Pages Remaining: "+str(self.pagevar.get()))
        else:
            self.order += 1
            self.pagevar.set(self.pagevar.get()-int(finlist[1]))
            curs.callproc("insertPriorityNumber",[finlist[0],self.order,issue_No])
            a.commit()
            self.welcomevar.set("Please select the articles in the order you wish to Print them\n Pages Remaining: "+str(self.pagevar.get()))
            self.menu.delete(option)
        pass			

class category(object):
	"""docstring for Category"""
	def __init__(self, master):
		self.choices_Categories = []
		curs.callproc("showAllCategories")
		for x in curs.stored_results():
			self.choice = x.fetchall()
		for y in range(len(self.choice)):
			for x in self.choice[y]:
				self.choices_Categories.append(x.encode("utf-8"))
		self.master = master
		master.title("Insert Category")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.childcheck = tn.IntVar()
		self.answer = tn.StringVar()
		self.label_name = tn.Label(master,text="New Category: ")
		self.label_name.grid(row = 1 ,column = 0)
		self.entryfield_name = tn.Entry(master)
		self.entryfield_name.grid(row = 1, column = 1)
		self.label_description = tn.Label(master,text="Description: ")
		self.label_description.grid(row = 2,column = 0)
		self.entryfield_description = tn.Entry(master)
		self.entryfield_description.grid(row = 2, column = 1)
		self.childcheckbutton = tn.Checkbutton(master,text="Is a sub",variable = self.childcheck)
		self.childcheckbutton.grid(row = 3 , column = 0)
		self.optionmenu_Category = tn.OptionMenu(master,self.answer,*self.choices_Categories)
		self.optionmenu_Category.grid(row = 3 , column = 1)
		self.button = tn.Button(master,text="Select",command=self.insert)
		self.button.grid(row=4 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 4 , column = 1)
	def insert(self):
		if self.childcheck.get() == 0:
			curs.callproc("insertNewCategory",[self.entryfield_name.get(),self.entryfield_description.get(),0])
			msg.showinfo("Success","Category inserted")
		else :
			curs.callproc("getCategoryCode",[self.answer.get()])
			for x in curs.stored_results():
				result = x.fetchone()
			curs.callproc("insertNewCategory",[ self.entryfield_name.get(),
												self.entryfield_description.get(),
												result[0]])
			msg.showinfo("Success","Category inserted")
		a.commit()
		
		self.master.destroy()#-------------------
	

#Administrative windows

class administrative(object):
	"""docstring for administrative"""
	def __init__(self, master):
		self.var1 = tn.IntVar()
		self.var1.set(20)
		self.master = master
		master.title("Welcome")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.image = tn.PhotoImage(file="./assets/admin.png")
		self.image = self.image.subsample(2,2)
		self.var = tn.StringVar()
		self.var.set("Welcome\nWhat would you like to do?")
		self.welcome_label = tn.Label(master,textvar=self.var)
		self.welcome_label.pack()  #grid(columnspan=2,sticky=tn.N,row = 0)
		self.imagelabel = tn.Label(master)	
		self.imagelabel.pack()
		self.imagelabel['image'] = self.image
		options=[("Enter number of returned Pages",0),("View financial data",1)]

		for text,val in options:
			tn.Radiobutton(master,text=text , value = val , variable = self.var1).pack()

		self.but = tn.Button(master,text="Select",command=self.checkans)
		self.but.pack()
		self.quit = tn.Button(master,text="Quit",command=master.quit)
		self.quit.pack()
	def checkans(self):
		if self.var1.get()==0:
			issue = tn.Toplevel(class_="Issue")
			issuewin = issuechoose(issue)
			
		elif self.var1.get()==1:
			financial = tn.Toplevel(class_="Financial Data")
			finwin = financial_data(financial)
			
class issuechoose(object):
	"""docstring for issuechoose"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showAllIssues",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Articles")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose the issue: ")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.choose_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)
	def choose_selected(self):
		global issue_No
		issue_No = self.ansstring1.get()
		num = tn.Toplevel(class_="Pages Returned")
		numwin = pages_returned(num)

class pages_returned(object):
	"""docstring for pages_returned"""
	def __init__(self, master):
		self.master = master
		master.title("Returned Pages")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text= "Please enter the number of returned Pages")
		self.welcome_label.grid(columnspan=3 ,row = 0 , column = 0)
		self.entryfield = tn.Entry(master)
		self.entryfield.grid(columnspan=3 ,row = 1 , column = 0)
		self.accept = tn.Button(master,text = "Submit",command=self.submit_number)
		self.accept.grid(row = 2 ,column = 0)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=2,column = 1)
	def submit_number(self):
		curs.callproc("insertReturnedCopies",[issue_No,self.entryfield.get(),tester.user])
		a.commit()
		msg.showinfo("Success","The number has been inserted")
		self.master.destroy() #-----------------------------------
		
class financial_data(object):
    """docstring for financial_data"""
    def __init__(self, master):
        self.intvar = tn.IntVar()
        self.intvar.set(20)
        self.master = master
        master.title("Finance")
        self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
        self.textvar = tn.StringVar()
        self.textvar.set("Please enter the dates you wish to see the data for")
        self.label = tn.Label(master,textvar=self.textvar)
        self.label.grid(columnspan=3 , row = 0 , column = 0)
        self.label_from = tn.Label(master,text="From: ")
        self.label_from.grid(row = 1 , column = 0)
        self.label_fromday = tn.Label(master,text = "Day : ")
        self.label_fromday.grid(row = 2 , column = 0)
        self.label_frommonth = tn.Label(master,text = "Month : ")
        self.label_frommonth.grid(row = 3 , column = 0)
        self.label_fromyear = tn.Label(master,text = "Year : ")
        self.label_fromyear.grid(row = 4 , column = 0)
        self.label_to = tn.Label(master,text="To :")
        self.label_to.grid(row = 5 , column = 0)
        self.label_today = tn.Label(master,text = "Day : ")
        self.label_today.grid(row = 6 , column = 0)
        self.label_tomonth = tn.Label(master,text = "Month : ")
        self.label_tomonth.grid(row = 7 , column = 0)
        self.label_toyear = tn.Label(master,text = "Year : ")
        self.label_toyear.grid(row = 8 , column = 0)
        self.entry_fromday = tn.Spinbox(master,from_=1,to=31)
        self.entry_fromday.grid(row = 2, column = 1)
        self.entry_frommonth = tn.Spinbox(master,from_=1,to=12)
        self.entry_frommonth.grid(row = 3, column = 1)
        self.entry_fromyear = tn.Spinbox(master,from_=1995,to=2020)
        self.entry_fromyear.grid(row = 4, column = 1)
        self.entry_today = tn.Spinbox(master,from_=1,to=31)
        self.entry_today.grid(row = 6, column = 1)
        self.entry_tomonth = tn.Spinbox(master,from_=1,to=12)
        self.entry_tomonth.grid(row = 7, column = 1)
        self.entry_toyear = tn.Spinbox(master,from_=1995,to=2020)
        self.entry_toyear.grid(row = 8, column = 1)
        self.RadiobuttonPerEmployee = tn.Radiobutton(master,text="Show results per employee" , variable = self.intvar , value = 0)
        self.RadiobuttonPerEmployee.grid(columnspan = 2,row = 9,column = 0)
        self.RadiobuttonTotal = tn.Radiobutton(master,text="Show Total Results",variable = self.intvar , value = 1)
        self.RadiobuttonTotal.grid(columnspan = 2,row = 10,column = 0)
        self.accept = tn.Button(master,text = "Submit",command=self.submit_time)
        self.accept.grid(row = 11 ,column = 0)
        self.quit = tn.Button(master,text="Quit",command=master.destroy)
        self.quit.grid(row=11,column = 1)

    def validate(self):
		flag = 0
		if int(self.entry_fromday.get())>31 or int(self.entry_fromday.get()) < 0:
			self.label_fromday.config(fg='RED')
			flag = 1
		if int(self.entry_frommonth.get())>12 or int(self.entry_frommonth.get()) < 0:
			self.label_frommonth.config(fg='RED')
			flag = 1
		if int(self.entry_fromyear.get())>1995 or int(self.entry_fromyear.get()) < 0:
			self.label_fromyear.config(fg='RED')
			flag = 1
		if int(self.entry_today.get())> 31 or int(self.entry_today.get()) < 0:
			self.label_today.config(fg='RED')
			flag = 1
		if int(self.entry_tomonth.get())>12 or int(self.entry_tomonth.get()) < 0:
			self.label_tomonth.config(fg='RED')
			flag = 1
		if int(self.entry_toyear.get())> 2020 or int(self.entry_toyear.get()) < 1995:
			self.label_toyear.config(fg='RED')
			flag = 1
		if flag == 1:
			self.textvar.set("Wrong data")
			return False
		return True
    def submit_time(self):
        self.listing = []
        from_date = ""
        to_date = ""
        if self.validate() :
            string=""
            from_date = self.entry_fromyear.get()+"-"+self.entry_frommonth.get()+"-"+self.entry_fromday.get()
            to_date = self.entry_toyear.get()+"-"+self.entry_tomonth.get()+"-"+self.entry_today.get()
            
            if self.intvar.get() == 1:
            	curs.callproc("showAllNewspaperExpenses",[str(from_date),str(to_date),tester.user])
            	for x in curs.stored_results():
            		result = x.fetchall()
            	
            	self.listing.append(result[0])
            	msg.showinfo("Results","The total is: "+str(self.listing[0][0]))
            	
            elif self.intvar.get() == 0:
            	curs.callproc("showNewspaperExpensesPerEmployee",[from_date,to_date,tester.user])
            	for x in curs.stored_results():
            		result = x.fetchall()
            	for y in result:
            		for i in range(len(y)/3):
            			self.listing.append(y[i].encode("utf-8")+" "+y[i+1].encode("utf-8")+" "+str(y[i+2]))
            	for i in range(len(self.listing)):
            		string = string + self.listing[i]+"\n"
            	msg.showinfo("Results"," The results are: \n"+string)		
            		
            	
#Publisher Windows

class publisher(object):
	"""docstring for publisher"""
	def __init__(self, master):
		self.var1 = tn.IntVar()
		self.var1.set(20)
		self.master = master
		self.master.title("Welcome")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.master.minsize(200,200)
		self.var = tn.StringVar()
		self.var.set("Welcome\nWhat would you like to do?")
		self.welcome_label = tn.Label(master,textvar=self.var)
		self.welcome_label.pack()  #grid(columnspan=2,sticky=tn.N,row = 0)
		self.image = tn.PhotoImage(file="./assets/publisher.png")
		self.image = self.image.subsample(3,3)
		self.imagelabel = tn.Label(master)
		self.imagelabel.pack()
		self.imagelabel['image'] = self.image
		options=[("Change Papers attributes",0),
				("Set the number of issues to be printed",1),
				("Set the editor in chief",2),
				("Check sold copies of an issue",3),
				("Hire a new Worker",4)]

		for text,val in options:
			tn.Radiobutton(master,text=text , value = val , variable = self.var1).pack()

		self.but = tn.Button(master,text="Select",command=self.checkans)
		self.but.pack()
		self.quit = tn.Button(master,text="Quit",command=master.quit)
		self.quit.pack()
	

	def checkans(self):
		global answer
		answer = self.var1.get()
		if self.var1.get()==0:
			pap = tn.Toplevel(class_="Newspaper")
			paperwin=chooseNpPub(pap)
			
		elif self.var1.get()==1:
			page = tn.Toplevel(class_="Newspaper")
			pagewin = chooseNpPub(page)
		
		elif self.var1.get()==2:
			edit = tn.Toplevel(class_="Newspaper")
			editwin = chooseNpPub(edit)
		
		elif self.var1.get()==3:
			sale = tn.Toplevel(class_="Newspaper")
			salewin = chooseNpPub(sale)

		elif self.var1.get()==4:
			hire = tn.Toplevel(class_="Hire")
			hirewin = hiring(hire)
			
class Paper(object):
	"""docstring for Paper"""
	def __init__(self, master):
		self.master = master
		master.title("Paper")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.label = tn.Label(master,text="Please enter the attributes:")
		self.label.grid(columnspan=3 , row = 0 , column = 0)
		self.label_freq = tn.Label(master,text="Frequency :")
		self.label_freq.grid(row = 2 , column = 0)
		self.label_owner = tn.Label(master,text="Owner :")
		self.label_owner.grid(row = 3 , column = 0)
		self.entry_freq = tn.Entry(master)
		self.entry_freq.grid(row = 2 , column = 1 )
		self.entry_owner = tn.Entry(master)
		self.entry_owner.grid(row = 3, column = 1)
		self.accept = tn.Button(master,text = "Submit",command=self.submit_attributes)
		self.accept.grid(row = 4 ,column = 1)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=4,column = 2)

	def submit_attributes(self):
		curs.callproc("updateNewspaper",[newspaper_name,self.entry_freq.get(),self.entry_owner.get()])
		a.commit()
		msg.showinfo("Success","Attributes updated")
		self.master.destroy()
		pass

class chooseNpPub(object):
	"""docstring for chooseNpPub"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showAllOwnedNewspapers",[tester.user])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Newspapers")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.master.minsize(200,200)
		self.welcome_label = tn.Label(master,text="Choose the Newspaper: ")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(self.master , self.ansstring1, *self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.choose_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)
	def choose_selected(self):
		global newspaper_name
		newspaper_name = self.ansstring1.get()	
		if answer == 0:
			paperatt = tn.Toplevel(class_ = "Attributes")
			att = Paper(paperatt)
			pass
		elif answer == 1:
			issuechoice = tn.Toplevel(class_="Issue")
			choice = issuechoosepub(issuechoice)

		elif answer == 2:
			editor = tn.Toplevel(class_="New Editor")
			editorwin = set_editor(editor)
		elif answer == 3:
			issuechoice = tn.Toplevel(class_="Issue")
			choice = issuechoosepub(issuechoice)
			pass

class issuechoosepub(object):
	"""docstring for issuechoosepub"""
	def __init__(self, master):
		self.choices = []
		curs.callproc("showAllIssuesPub",[newspaper_name])
		for i in curs.stored_results():
			results = i.fetchall()
		
		for x in range(len(results)):
			for y in results[x]:
				self.choices.append(str(y).encode("utf-8"))
			
		self.ansstring1= tn.StringVar()
		self.master = master
		master.title("Issues")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.welcome_label = tn.Label(master,text="Choose the issue: ")
		self.welcome_label.grid(columnspan=2 , row = 0 , column = 0)

		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=2 , row = 1 , column = 0)

		self.button = tn.Button(master,text="Select",command=self.choose_selected)
		self.button.grid(row=2 , column=0)
		self.button1 = tn.Button(master,text="Quit",command= master.destroy)
		self.button1.grid(row = 2 , column = 1)
	def choose_selected(self):
		global issue_selected
		issue_selected = self.ansstring1.get()
		if answer == 1:
			pageselect = tn.Toplevel()
			pagewin = pages_created(pageselect)
		elif answer == 3:
			curs.callproc("totalSold",[newspaper_name,issue_selected])
			for x in curs.stored_results():
				result = x.fetchone()
			msg.showinfo("Result","The number of sold copies is : "+str(result[0]))	

class pages_created(object):
	"""docstring for pages_created"""
	def __init__(self, master):
		self.master = master
		master.title("Number of pages")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.label = tn.Label(master,text="Please enter the number of Copies you want to print:")
		self.label.grid(columnspan=3 , row = 0 , column = 0)
		self.entry_num = tn.Entry(master)
		self.entry_num.grid(columnspan = 3, row = 1, column = 0)
		self.accept = tn.Button(master,text = "Submit",command=self.submit_pages)
		self.accept.grid(row = 2 ,column = 1)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=2,column = 2)
	def submit_pages(self):
		curs.callproc("insertNumberOfCopies",[issue_selected,self.entry_num.get(),newspaper_name])
		a.commit()
		msg.showinfo("Success","The number of copies has been inserted")
		self.master.destroy()
		pass
		
class set_editor(object):
	"""docstring for set_editor"""
	def __init__(self, master):
		self.choices = []
		listing = []
		curs.callproc("showOldEditor",[newspaper_name])
		for x in curs.stored_results():
			listing = x.fetchone()
		oldeditor = listing[0]+" "+listing[1]
		curs.callproc("showAllNewspaperJournalists",[newspaper_name])
		for x in curs.stored_results():
			listing = x.fetchall()
			pass

		for x in listing:
			for i in range(len(x)/2):
				self.choices.append(x[i].encode("UTF-8")+" "+x[i+1].encode("UTF-8"))
				pass
			pass
		
		self.ansstring1 = tn.StringVar()
		self.master = master 
		master.title("New Chief")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.label_oldEditor = tn.Label(master,text="The current editor is: "+oldeditor)
		self.label_oldEditor.grid(columnspan=3 , row = 0 , column = 0)
		self.label = tn.Label(master,text="Please choose the new editor in chief:")
		self.label.grid(columnspan=3 , row = 1 , column = 0)
		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=3 , row = 2 , column = 0)
		self.accept = tn.Button(master,text = "Submit",command=self.submit_editor)
		self.accept.grid(row = 3 ,column = 1)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=3,column = 2)

	def submit_editor(self):
		ans = self.ansstring1.get()
		ans = ans.split()

		curs.callproc("nameToEmail",[ans[0],ans[1]])
		for i in curs.stored_results():
			email = i.fetchone()
		pass
		curs.callproc("promotion",[email[0]])
		a.commit()
		msg.showinfo("Success","The Editor in chief has been changed")
		self.master.destroy()

class sales(object):
	"""docstring for sales"""
	def __init__(self, master):
		self.master = master
		master.title("Sales")
		self.master.tk.call('wm','iconphoto',self.master._w,imageicon)
		self.choices = [1,2,3,4,5]
		self.ansstring1 = tn.IntVar()
		self.label = tn.Label(master,text="Please choose the issue you want to see the sales for:")
		self.label.grid(columnspan=3 , row = 0 , column = 0)
		self.optionmenu1 = tn.OptionMenu(master,self.ansstring1,*self.choices)
		self.optionmenu1.grid(columnspan=3 , row = 1 , column = 0)
		self.accept = tn.Button(master,text = "Submit",command=self.submit_issue)
		self.accept.grid(row = 2 ,column = 1)
		self.quit = tn.Button(master,text="Quit",command=master.destroy)
		self.quit.grid(row=2,column = 2)
	def submit_issue(self):
		msg.showinfo("Result",self.ansstring1.get())
		pass

class hiring(object):
	"""docstring for hiring"""
	def __init__(self, master):
		self.Choices = ["Administrative","Journalist"]
		self.first = []
		self.last = []
		curs.callproc("showAllOwnedNewspapers",[tester.user])
		for i in curs.stored_results():
			self.first = i.fetchall()
		
		for x in range(len(self.first)):
			for y in self.first[x]:
				self.last.append(str(y).encode("utf-8"))

		self.master = master
		self.master.title("Hire")
		self.welcomevar = tn.StringVar()
		self.welcomevar.set("Please fill out the next fields..")
		self.ansvar = tn.StringVar()
		self.ansvar1 = tn.StringVar()
		self.welcome_label = tn.Label(master,textvar=self.welcomevar)
		self.welcome_label.grid(columnspan=2,row = 0,column = 0)

		self.name_label = tn.Label(master,text = "Name :")
		self.name_label.grid(row = 1,column = 0)
		self.lastname_label = tn.Label(master,text = "Last Name :")
		self.lastname_label.grid(row = 2,column = 0)
		self.email_label = tn.Label(master,text = "Email :")
		self.email_label.grid(row = 3,column = 0)
		self.salary_label = tn.Label(master,text = "Salary :")
		self.salary_label.grid(row = 4,column = 0)
		self.newspaper_label = tn.Label(master,text = "Assigned Newspaper :")
		self.newspaper_label.grid(row = 5,column = 0)
		self.specialty_label = tn.Label(master,text="Hired as a :")
		self.specialty_label.grid(row = 6,column = 0)
		
		self.name_entry = tn.Entry(master)
		self.name_entry.grid(row = 1, column = 1)
		self.lastname_entry = tn.Entry(master)
		self.lastname_entry.grid(row = 2, column = 1)
		self.email_entry = tn.Entry(master)
		self.email_entry.grid(row = 3, column = 1)
		self.salary_entry = tn.Entry(master)
		self.salary_entry.grid(row = 4, column = 1)
		self.newspaper_option = tn.OptionMenu(master,self.ansvar,*self.last)
		self.newspaper_option.grid(row = 5,column = 1)
		self.specialty_option = tn.OptionMenu(master,self.ansvar1,*self.Choices)
		self.specialty_option.grid(row = 6,column = 1)
		
		self.accept = tn.Button(master,text="Accept",command = self.set_attributes)
		self.accept.grid(row = 7,column = 0)
		self.quit = tn.Button(master,text="Cancel",command = self.master.destroy)
		self.quit.grid(row = 7, column = 1)	
	def set_attributes(self):
		global name
		name = self.name_entry.get()
		global lastname
		lastname = self.lastname_entry.get()
		global email
		email = self.email_entry.get()
		global salary 
		salary = self.salary_entry.get()
		global newspaper 
		newspaper = self.ansvar.get()
		if self.ansvar1.get()== "Journalist" :
			j_hire = tn.Toplevel(class_="Journalist")
			j_hirewin = journalist_hire(j_hire)
			pass
		elif self.ansvar1.get()== "Administrative":
			A_hire = tn.Toplevel(class_="Administrative")
			A_hirewin = administrative_hire(A_hire)
			pass
		self.master.destroy()							

class journalist_hire(object):
	"""docstring for journalist_hire"""
	def __init__(self, master):
		self.master = master
		self.master.title("New Journalist")
		self.textvar = tn.StringVar()
		self.textvar.set("Please fill out the next fields \nfor your new Journalist")

		self.welcome_label = tn.Label(master,textvar = self.textvar)
		self.welcome_label.grid(columnspan = 2,row = 0, column = 0)
		self.preocc_label = tn.Label(master,text="Months in Previous Occupation")
		self.preocc_label.grid(row=1,column=0)
		self.short_bio_label = tn.Label(master,text="Short Bio:")
		self.short_bio_label.grid(row = 2, column = 0)

		self.preocc_listbox = tn.Spinbox(master,from_=0,to=1000)
		self.preocc_listbox.grid(row=1,column=1)
		self.short_bio_entry = tn.Entry(master)
		self.short_bio_entry.grid(row=2,column=1)
		self.accept = tn.Button(master,text="Accept",command = self.hire)
		self.accept.grid(row = 3,column = 0)
		self.quit = tn.Button(master,text="Cancel",command = self.master.destroy)
		self.quit.grid(row = 3, column = 1)

	def hire(self):
		self.textvar.set("Please fill out the next fields \nfor your new Journalist")
		self.welcome_label.config(fg="BLACK")
		if self.preocc_listbox.get() < 0 or self.preocc_listbox.get() > 1000 :
			self.welcome_label.config(fg="RED")
			self.textvar.set("Please use only numeric values..")
			pass
		curs.callproc("insert_journalist",[self.preocc_listbox.get(),
											self.short_bio_entry.get(),
											name,
											lastname,
											email,
											salary,
											newspaper])
		a.commit()
		self.master.destroy()
		pass

class administrative_hire(object):
	"""docstring for administrative_hire"""
	def __init__(self, master):
		self.dutyans = tn.StringVar()
		self.master = master
		self.master.title("New Administrative")
		self.textvar = tn.StringVar()
		self.textvar.set("Please fill out the next fields \nfor your new Administrative")

		self.welcome_label = tn.Label(master,textvar = self.textvar)
		self.welcome_label.grid(columnspan = 2,row = 0, column = 0)
		self.duties_label = tn.Label(master,text="Duties:")
		self.duties_label.grid(row=1,column=0)
		self.street_label = tn.Label(master,text="Street:")
		self.street_label.grid(row = 2, column = 0)
		self.streetNo_label = tn.Label(master,text="Street Number:")
		self.streetNo_label.grid(row = 3, column = 0)
		self.city_label = tn.Label(master,text="City:")
		self.city_label.grid(row = 4, column = 0)

		self.duties_option = tn.OptionMenu(master,self.dutyans,*["Secretary","Logistics"])
		self.duties_option.grid(row = 1, column = 1)
		self.street_entry = tn.Entry(master)
		self.street_entry.grid(row = 2, column = 1)
		self.streetNo_list = tn.Spinbox(master,from_=1,to=500)
		self.streetNo_list.grid(row = 3, column = 1)
		self.city_entry = tn.Entry(master)
		self.city_entry.grid(row = 4, column = 1)
		
		self.accept = tn.Button(master,text="Accept",command = self.hire)
		self.accept.grid(row = 5,column = 0)
		self.quit = tn.Button(master,text="Cancel",command = self.master.destroy)
		self.quit.grid(row = 5, column = 1)

	def hire(self):
		if self.streetNo_list.get() < 1 or self.streetNo_list.get() > 500:
			self.welcome_label.config(fg="RED")
			self.textvar.set("Please enter only a number in the Street Number section..")
			pass
		else:
			curs.callproc("insert_administrative",[self.dutyans.get(),
													self.street_entry.get(),
													self.streetNo_list.get(),
													self.city_entry.get(),
													name,
													lastname,
													email,
													salary,
													newspaper])
			a.commit()
			msg.showinfo("Success","The employee has been hired")
			pass

		

a = con.connect(user ="root",password="",host="localhost",database ="whatever")
curs = a.cursor()

root = tn.Tk(className = "Login")

tester = login(root)
root.mainloop()
"""
new = tn.Tk()
test = hiring(new)
new.mainloop()	

"""