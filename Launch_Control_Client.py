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


		#Safety Frame code
		self.safety_button = Tk.Button(safety_frame, text = 'Toggle Safety: ', font = FONT,command = self.safety_switch)
		self.safety_label = Tk.Label(safety_frame, text = 'Safety Status: Disarmed', font = FONT, bg = 'red')
		self.connection_status_label1 = Tk.Label(safety_frame, text = 'Connection Status: ',font = FONT)
		self.connection_status_label2 = Tk.Label(safety_frame, text = 'Not Connected',bg = 'green',font = FONT)
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
		listen_button = Tk.Button(connection_frame, text = "Read Statuses",font = FONT, bg = "firebrick",command = self.get_info)
		listen_button.pack(fill = 'both')

		#launch_frame code
		self.ignite_button = Tk.Button(launch_frame, text="Ignite!", font=FONT, bg = "indian red", command=lambda: self.send_info('Ig'),state = 'disabled')
		self.ignite_button.pack(fill='both')
		self.launch_button = Tk.Button(launch_frame,text = "Launch!", font = FONT, bg = "indian red", command =lambda:self.send_info('L'),state = 'disabled')
		self.launch_button.pack(fill = 'both')
		self.abort_button = Tk.Button(launch_frame,text = "Abort!",font = FONT, bg = "indian red", command = lambda:self.send_info('A'),state = 'disabled')
		self.abort_button.pack(fill = 'both')

		#valve frame
		breakwire_label = Tk.Label(valve_frame, text = "Breakwire Status",font = FONT)
		breakwire_label.grid(row = 1, column = 0 ,sticky = 'E')
		#breakwire_label.pack(fill='both')
		main_label = Tk.Label(valve_frame,text = 'Main Valve',font = FONT)
		main_label.grid(row = 2, column = 0,sticky = 'E')
		lox_label = Tk.Label(valve_frame,text = 'Lox Valve',font = FONT)
		lox_label.grid(row = 3, column = 0,sticky = 'E')
		kero_label = Tk.Label(valve_frame,text = 'Kero Valve', font = FONT)
		kero_label.grid(row = 4, column = 0,sticky = 'E')
		ignitor_label = Tk.Label(valve_frame, text = "Ignitor Status",font = FONT)
		ignitor_label.grid(row = 5, column = 0, sticky = 'E')

		#status displyed
		self.b_wire_status_label = Tk.Label(valve_frame,text = 'Intact', font = FONT,bg = 'green')
		self.b_wire_status_label.grid(row = 1, column = 1, sticky = 'W' + 'E')
		self.main_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'green')
		self.main_status_label.grid(row = 2, column = 1, sticky = 'W' + 'E')
		self.kero_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'green')
		self.kero_status_label.grid(row = 4, column = 1, sticky = 'W' + 'E')
		self.lox_status_label = Tk.Label(valve_frame,text = 'Open', font = FONT,bg = 'green')
		self.lox_status_label.grid(row = 3, column = 1, sticky = 'W' + 'E')
		self.ignitor_status_label = Tk.Label(valve_frame,text = 'Not Lit', font = FONT,bg = 'green')
		self.ignitor_status_label.grid(row = 5, column = 1, sticky = 'W' + 'E')

		self.vent_open_button = Tk.Button(valve_frame, text = "Open Vents",font = FONT,command = lambda:self.send_info('VO'))
		self.vent_open_button.grid(row = 6 , column = 0, stick = 'W' + 'E')
		self.vent_close_button = Tk.Button(valve_frame, text = "Close Vents",font = FONT,command = lambda:self.send_info('VC'))
		self.vent_close_button.grid(row = 6 , column = 1, stick = 'W' + 'E')

		self.time_label = Tk.Label(time_frame,font = FONT,relief = Tk.RAISED, bg="red",bd = 5)#This label handles the time, and is updated more than once a second in the time_thread
		self.time_label = Tk.Label(time_frame,font = FONT,relief = Tk.RAISED,borderwidth = 3)#This label handles the time, and is updated more than once a second in the time_thread
		self.time_label.pack()

		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server_address = (server_IP,port)
		self.connection_status = False #initialzing to a false state

	def safety_switch(self): 

		if self.connection_status == True:
			self.ignite_button.config(state = 'normal')
			self.launch_button.config(state = 'normal')
			self.abort_button.config(state = 'normal')
			self.safety_label.config(text = "Safety Staus: Armed", bg = 'green')

		elif self.connection_status == False:
			msg = tkMessageBox.showerror('Connection Error','Safety will not toggle unless client is connected to server')

	def create_connection(self):

		try: 
			self.s.connect(self.server_address)
			tkMessageBox.showinfo('Connection Results','Socket Successfully Bound.\nClick "Read Statuses " to start')
			self.connection_status = True
			self.connection_status_label.config (text = 'Connection Status: Connected',bg = 'green')

		except socket.error as e: 
			msg = tkMessageBox.showerror("Connection Results", "Couldn't connect to {} at {}: error is {}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1],e))

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
		if data == 'Ignitor 1 Lit':
			self.ignitor_status_label.config(text = 'Lit af', bg = 'red')
		elif data == 'Ignitor 1 Off':
			self.ignitor_status_label.config(text = 'Not Lit', bg = 'green')


	def get_info(self):

		try: 
			self.s.send('bwire_status')
			data = self.s.recv(BUFF)
			if data == 'Broken':
				self.b_wire_status_label.config(text = 'Broken',bg = 'red')
			elif data == 'Intact':
				self.b_wire_status_label.config(text = 'Intact',bg = 'green')

			self.s.send('main_status')
			mdata = self.s.recv(BUFF)
			if mdata == 'Closed':
				self.main_status_label.config(text = 'Closed',bg = 'red')
			elif mdata == 'Open':
				self.main_status_label.config(text = 'Open',bg = 'green')

			self.s.send('kero_status')
			kdata = self.s.recv(BUFF)
			if kdata == 'Closed':
				self.kero_status_label.config(text = 'Closed',bg = 'red')
			if kdata == 'Open':
				self.kero_status_label.config(text = 'Open',bg = 'green')

			self.s.send('LOX_status')
			ldata = self.s.recv(BUFF)
			if ldata == 'Closed':
				self.lox_status_label.config(text = 'Closed',bg = 'red')
			if ldata == 'Open':
				self.lox_status_label.config(text = 'Open',bg = 'green')

		except socket.error as err:
			print err

		#if not err:
		#	self.master.after(200,self.get_info) #If there is not a connection issue, update info every 200 ms

	def get_time(self):

		time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		self.time_label.config(text = time_now)
		self.master.after(800,self.get_time) #Call this method every 800 ms to update the time label

	def exit(self,master):

		msg = tkMessageBox.askquestion("","Do you really want to quit?")

		if msg == 'yes':
			try:
				self.s.shutdown(socket.SHUT_RDWR) #Closes and destroys sockets.
				self.s.close()
			except socket.error as e: #If the connection wasn't made, then this path is taken.
				pass

			master.quit()
			master.destroy() #Need both for some reason

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk.Tk()
app = GUI(root)
app.get_time()
root.mainloop()