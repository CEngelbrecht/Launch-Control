import Tkinter as Tk 
import socket 
import subprocess
import tkMessageBox
import time
import logging
import threading

'''
A reverse engineered client based on the Launch Control Server rev3.py
Current things that need working on: 

logging
perhaps adding a terminal in the main window to show history? 
prettification/organization
code organization	
Making a stand alone executable from this

'''

server_IP = '192.168.1.33' #This is the IP of the ESB Pi. It is a static IP. 
port = 5000
BUFF = 1024

logging.basicConfig(filename = 'LC_Client_Log.txt',level = logging.INFO)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GUI:

	def __init__(self,master):
		
		FONT = ('Helvetica',22)
		self.master = master 
		#master.wm_attributes('-zoomed',True)
		master.title("Launch Control GUI")
		master.configure(bg='black',bd = 10)

		time_frame= Tk.Frame(master)
		time_frame.pack(fill = 'x',side = 'top',expand = False)
		time_frame.config(bd = 10, relief = Tk.FLAT, bg="black")

		safety_frame = Tk.Frame(master)
		safety_frame.pack(fill = 'x', side = 'top',expand = True)
		safety_frame.config(bd = 10,relief = Tk.RIDGE)

		valve_frame = Tk.Frame(master)
		valve_frame.pack(fill = 'x',side = 'left',expand = True)
		#valve_frame.grid(row = 2, column = 0, sticky = 'SW')
		valve_frame.config(bd = 10, relief = Tk.RIDGE)

		connection_frame = Tk.Frame(master)
		connection_frame.pack(fill = 'x',side = 'top',expand = True)
		#connection_frame.grid(row = 0 ,column = 1,sticky= 'E')
		connection_frame.config(bd = 10, relief = Tk.RIDGE)

		launch_frame = Tk.Frame(master)
		launch_frame.pack(fill = 'x', side = 'right',expand = True)
		#launch_frame.grid(row = 1,column = 1,sticky= 'E')
		launch_frame.config(bd = 10, relief = Tk.RIDGE)

		def empty_Label_Method():
			self.empty_label = Tk.Label(launch_frame)
			self.empty_label.pack(fill = 'both')

		#Safety Frame code
		self.safety_button = Tk.Button(safety_frame, text = 'Toggle Safety: ', font = FONT,command = self.safety_switch)
		self.safety_label = Tk.Label(safety_frame, text = 'Safety Status: Disarmed', font = FONT, bg = 'red')
		self.connection_status_label1 = Tk.Label(safety_frame, text = 'Connection Status: ',font = FONT)
		self.connection_status_label2 = Tk.Label(safety_frame, text = 'Not Connected',bg = 'red',font = FONT)
		self.connection_status_label1.grid(row = 1, column = 0, sticky = 'W' + 'E')
		self.connection_status_label2.grid(row = 1 ,column = 1, sticky = 'W' + 'E')
		self.safety_button.grid(row = 0, column = 0,sticky = 'W' + 'E')
		self.safety_label.grid(row = 0 , column = 1,sticky = 'W' + 'E')

		#connection_frame code
		close_button = Tk.Button(connection_frame, text = "Quit Application",font = FONT, bg = "firebrick", command = lambda:self.exit(master))
		close_button.pack(fill = 'both')
		create_connection_button = Tk.Button(connection_frame,text = "Create Connection", bg = "firebrick", font = FONT, command = self.create_connection)
		create_connection_button.pack(fill = 'both')
		ping_button = Tk.Button(connection_frame,text = "Ping Server",font = FONT, bg = "firebrick",command = self.ping_server)
		ping_button.pack(fill = 'both')
		listen_button = Tk.Button(connection_frame, text = "Start Reading Statuses",font = FONT, bg = "firebrick",command = self.get_info)
		listen_button.pack(fill = 'both')

		#launch_frame code
		self.ignite_button = Tk.Button(launch_frame, text="Ignite!", font=FONT, bg = "indian red", command=lambda: self.send_info('Ig'),state = 'disabled')
		self.ignite_button.pack(fill='both')
		empty_Label_Method()
		self.launch_button = Tk.Button(launch_frame,text = "Launch!", font = FONT, bg = "indian red", command =lambda:self.send_info('L'),state = 'disabled')
		self.launch_button.pack(fill = 'both')
		empty_Label_Method()
		self.abort_button = Tk.Button(launch_frame,text = "Abort!",font = FONT, bg = "indian red", command = lambda:self.send_info('A'),state = 'disabled')
		self.abort_button.pack(fill = 'both')

		#valve frame
		breakwire_label = Tk.Label(valve_frame, text = "Breakwire Status",font = FONT)
		breakwire_label.grid(row = 1, column = 0 ,sticky = 'E')
		main_label = Tk.Label(valve_frame,text = 'Main Valve',font = FONT)
		main_label.grid(row = 2, column = 0,sticky = 'E')
		lox_label = Tk.Label(valve_frame,text = 'Lox Valve',font = FONT)
		lox_label.grid(row = 3, column = 0,sticky = 'E')
		kero_label = Tk.Label(valve_frame,text = 'Kero Valve', font = FONT)
		kero_label.grid(row = 4, column = 0,sticky = 'E')
		ignitor_label = Tk.Label(valve_frame, text = "Ignitor Status",font = FONT)
		ignitor_label.grid(row = 5, column = 0, sticky = 'E')

		#status displyed
		self.b_wire_status_label = Tk.Label(valve_frame,text = 'Intact', font = FONT,bg = 'red')
		self.b_wire_status_label.grid(row = 1, column = 1, sticky = 'W' + 'E')
		self.main_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'red')
		self.main_status_label.grid(row = 2, column = 1, sticky = 'W' + 'E')
		self.kero_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'red')
		self.kero_status_label.grid(row = 4, column = 1, sticky = 'W' + 'E')
		self.lox_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'red')
		self.lox_status_label.grid(row = 3, column = 1, sticky = 'W' + 'E')
		self.ignitor_status_label = Tk.Label(valve_frame,text = 'Not Lit', font = FONT,bg = 'red')
		self.ignitor_status_label.grid(row = 5, column = 1, sticky = 'W' + 'E')

		self.vent_open_button = Tk.Button(valve_frame, text = "Open Vents",font = FONT,command = lambda:self.send_info('VO'))
		self.vent_open_button.grid(row = 6 , column = 0, stick = 'W' + 'E')
		self.vent_close_button = Tk.Button(valve_frame, text = "Close Vents",font = FONT,command = lambda:self.send_info('VC'))
		self.vent_close_button.grid(row = 6 , column = 1, stick = 'W' + 'E')
		self.main_close_button = Tk.Button(valve_frame, text = "Close Main", font = FONT,command = lambda:self.send_info('MC'))
		self.main_close_button.grid(row = 7, column = 1, stick = 'W' + 'E')

		self.time_label = Tk.Label(time_frame,font = FONT,relief = Tk.RAISED, bg="red",bd = 5)#This label handles the time, and is updated more than once a second in the time_thread
		self.time_label = Tk.Label(time_frame,font = FONT,relief = Tk.RAISED,borderwidth = 3)#This label handles the time, and is updated more than once a second in the time_thread
		self.time_label.pack()

		#Initial values
		self.kdata = "Open"
		self.mdata = "Open"
		self.ldata = "Open"
		self.bdata = "Intact"

		time_thread = threading.Thread(target = self.get_time)
		time_thread.start()

		#self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server_address = (server_IP,port)
		self.connection_status = False #initialzing to a false connection state
		self.arm_status = False

	def safety_switch(self): 

		if self.connection_status == True:
			if self.arm_status == False: 
				self.ignite_button.config(state = 'normal')
				self.launch_button.config(state = 'normal')
				self.abort_button.config(state = 'normal')
				self.safety_label.config(text = "Safety Staus: Armed", bg = 'green')
				self.arm_status = True

			elif self.arm_status == True:
				self.ignite_button.config(state = 'disabled')
				self.launch_button.config(state = 'disabled')
				self.abort_button.config(state = 'disabled')
				self.safety_label.config(text = "Safety Staus: Disarmed", bg = 'red')
				self.arm_status = False #Switch arm state

		elif self.connection_status == False:
			msg = tkMessageBox.showerror('Connection Error','Safety will not toggle unless client is connected to server')

	def create_connection(self):

		try: 
			self.s = socket.create_connection(self.server_address,timeout = 1.5)
			tkMessageBox.showinfo('Connection Results','Socket Successfully Bound.\nClick "Read Statuses " to start')
			self.connection_status = True
			self.connection_status_label2.config (text ='Connected',bg = 'green')

		except socket.error as e: 
			msg = tkMessageBox.showerror("Connection Results", "Couldn't connect to {} at {}. Error is: \n{}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1],e))

	def ping_server(self):

		msg = tkMessageBox.showinfo('','Pinging...')
		response  = subprocess.call(["ping", server_IP,"-c1", "-W1","-q"]) #This is Linux syntax.
		#response = subprocess.call("ping {} -n 1 -w 1".format(server_IP)) #This is Windows syntax. 

		if response == 0: 
			msg = tkMessageBox.showinfo("Ping Results","Ping to {} sucessful!\nGo ahead and connect.".format(server_IP))
		else:
			msg = tkMessageBox.showerror("Ping Results","Ping to {} unsuccessful.\nCheck the IP you're connecting to, or if server is online.".format(server_IP))

	def send_info(self,command):
		#These messages are taken directly from the 'Launch Control Server rev3.py' server script on the ESB Pi. 

		if command == 'MO':
			message = 'main_open'
		elif command == 'MC':
			message = 'main_close'
		elif command == 'VO':
			message = 'vents_open'
		elif command == 'VC':
			message = 'vents_close'
		elif command == 'L':
			message = 'launch'
		elif command == 'A':
			message = 'abort'
		elif command == "Ig":
			message = "ign1_on"

		self.s.send(message)
		data = self.s.recv(BUFF)
		time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		if data == 'Ignitor 1 Lit':
			time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
			self.ignitor_status_label.config(text = 'Lit af', bg = 'red')
			logging.info("Ignitor 1 lit: {}".format(time_now))
		elif data == 'Ignitor 1 Off':
			self.ignitor_status_label.config(text = 'Not Lit', bg = 'green')			


	def switch_label(self,label):

		#These statements change the status of the labels 
		if label == 'bwire':
			if self.b_wire_status_label['text'] == 'Intact':
				self.b_wire_status_label.config(text = 'Broken',bg = 'green')
			elif self.b_wire_status_label['text'] == 'Broken':
				self.b_wire_status_label.config(text = 'Intact',bg = 'red')

		if label == 'main':
			if self.main_status_label['text'] == 'Open':
				self.main_status_label.config(text = 'Closed',bg = 'green')
			elif self.main_status_label['text'] == 'Closed':
				self.main_status_label.config(text = 'Open',bg = 'red')

		if label == 'kero':
			if self.kero_status_label['text'] == 'Open':
				self.kero_status_label.config(text = 'Closed',bg = 'green')
			elif self.kero_status_label['text'] == 'Closed':
				self.kero_status_label.config(text = 'Open',bg = 'red')

		if label == "lox":
			if self.lox_status_label['text'] == 'Open':
				self.lox_status_label.config(text = 'Closed',bg = 'green')
			elif self.lox_status_label['text'] == 'Closed':
				self.lox_status_label.config(text = 'Open',bg = 'red')

	def get_info(self):
		
		try: 
			self.s.send('bwire_status')
			self.bdata = self.s.recv(BUFF)

			self.s.send('main_status')
			self.mdata = self.s.recv(BUFF)

			self.s.send('kero_status')
			self.kdata = self.s.recv(BUFF)

			self.s.send('LOX_status')
			self.ldata = self.s.recv(BUFF)

		except (socket.error,AttributeError) as err:
			time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
			logging.error("{},{}".format(time_now,err))

		#The following if statements call the label to be changed only if the server sends a message that contradicts the current status of the label 
		if self.bdata != self.b_wire_status_label['text']:
			self.switch_label("bwire")

		if self.mdata != self.main_status_label['text']:
			self.switch_label('main')

		if self.kdata != self.kero_status_label['text']:
			self.switch_label('kero')

		if self.ldata != self.lox_status_label['text']:
			self.switch_label('lox')

		self.master.after(200,self.get_info)

	def get_time(self):

		time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		self.time_label.config(text = time_now)
		self.master.after(400,self.get_time) #Call this method every 800 ms to update the time label

	def exit(self,master):

		msg = tkMessageBox.askquestion("","Do you really want to quit?")

		if msg == 'yes':
			try:
				self.s.shutdown(socket.SHUT_RDWR) #Close and destroy 
				self.s.close()
			except (socket.error, AttributeError) as e: #If the connection wasn't made, then this path is taken.
				print e

			master.quit()
			master.destroy() #Need both for some reason

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk.Tk()
app = GUI(root)
root.mainloop()