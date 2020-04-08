#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Mar 16, 2020 02:36:08 AM IST  platform: Linux


import Tkinter as tk
import ttk
import numpy
import av
import cv2,cv_bridge
import sys
import time
import datetime
import os,subprocess
from subprocess import check_output
import rospy
import QuadDrop
import imutils
import PIL.Image, PIL.ImageTk
import csvio
import nofly
from std_msgs.msg import Int16
from std_msgs.msg import Int32
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image, Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray
from tello_driver.msg import TelloStatus
import getpass

global pathh
pathh="/home/"+getpass.getuser()+"/catkin_ws/src/shravas/src/"

global wificard
wc=os.listdir('/sys/class/net/')
wificard = "wlo1"
#wificard = "wlp2s0"
#for i in range(len(wc)):
#	if(wc[i]!='lo'):
#		wificard=str(wc[i])
#	else:
#		wificard="wlo1"

global delidat,ls
ls=csvio.csvread(pathh+"coordinates.csv")
delidat=csvio.csvread(pathh+"deliverydata.csv")

drobj = rospy.Publisher('/drone_init', Int32, queue_size=1)
eng = rospy.Publisher('/eng_init', Int32, queue_size=1)
def start():
	drobj.publish(1)
def emstop():
	drobj.publish(0)
def callback():
	drobj.publish(-1)

def set_Tk_var():
	global che48
	che48 = tk.IntVar()

def disable_enable_button():
	#w.Altitude.configure(text='''40.2''')
	w.EmStopButton.configure(state='normal' if che48.get() else 'disable')
	w.CallbackButton.configure(state='normal' if che48.get() else 'disable')

def create_grid(event=None):
	wid = w.fcan # Get current width of canvas
	hei = w.fcan # Get current height of canvas
	w.XYPositionalData.delete('grid_line') # Will only remove the grid_line
	#print(int(w.zmm))
	# Creates all vertical lines at intevals of 100
	for i in range(0, wid, w.zmm):
		w.XYPositionalData.create_line([(i, 0), (i, hei)], tag='grid_line')

	# Creates all horizontal lines at intevals of 100
	for i in range(0, hei, w.zmm):
		w.XYPositionalData.create_line([(0, i), (wid, i)], tag='grid_line')

def create_nos(event=None):
	wid = w.fcan 
	hei = w.fcan
	if(w.zmm==50):
		w.XNos.delete('nos_line')
		w.YNos.delete('nos_line')

		for i in range(0, hei, w.zmm):			# Y Nos
			w.YNos.create_line([(0, i), (wid, i)], tag='nos_line')
			top.YNos.create_text(10,i-6,font="Consolas 8", text=str((i/50)-20))

		for i in range(0, wid, w.zmm):				#X Nos
			w.XNos.create_line([(i, 0), (i, hei)], tag='nos_line')
			top.XNos.create_text(i-8,10,font="Consolas 8", text=str((i/50)-20))

def dmode():
	if(w.colorflag == 0):
		col1= "#333333"#dark
		altcol1="#d9d9d9"
		col2= "#ffffff"
		col3= "#000000"
		logo= pathh+"gui/logoo.png"
		about= pathh+"gui/about-dark.png"
		credits= pathh+"gui/credits-dark.png"
		gridcol= "#4a4a4a"
		fbarcol,bbarcol="#0078ff","#4a4a4a"
		fsccol,bsccol="#333333","#4a4a4a"
		w.colorflag=1
	elif(w.colorflag == 1):
		col1= "#d9d9d9"#light
		altcol1="#333333"
		col2= "#000000"
		col3= "#ffffff"
		logo= pathh+"gui/logoo.png"
		about= pathh+"gui/about-light.png"
		credits= pathh+"gui/credits-light.png"
		gridcol= "#ffffff"
		fbarcol,bbarcol="#0078ff","#d9d9d9"
		fsccol,bsccol="#d9d9d9","#d9d9d9"
		w.colorflag=0
	w.dmodeButton.configure(activebackground=altcol1)		
	root.configure(bg=col1)
	w.style.configure('.',background=col1)
	w.style.configure('.',foreground=col2)
	w.style.configure('Horizontal.TProgressbar',foreground=fbarcol, background=fbarcol,troughcolor=bbarcol)
	w.style.configure('Horizontal.TScale',foreground=fsccol, background=fsccol,troughcolor=bsccol)
	w.style.map('.', background=[('selected', col1), ('active',col1)])
	w.Logo.configure(background=col1 , foreground=col2)
	w.StatusLabel.configure(background=col1 , foreground=col2) 
	w.Status.configure(background=col1)
	w.BatteryLabel.configure(background=col1 , foreground=col2)
	#w.Battery.configure(background=col1 , foreground=col2)
	w.WifiLabel.configure(background=col1 , foreground=col2)
	#w.Battery.configure(background=col1 , foreground=col2)
	#w.AlitutdeBar.configure(background=col1 , foreground=col2)
	#w.SpeedBar.configure(background=col1 , foreground=col2)
	w.AltitudeLabel.configure(background=col1 , foreground=col2)
	w.SpeedLabel.configure(background=col1 , foreground=col2)
	w.ModeLabel.configure(background=col1 , foreground=col2)
	w.Mode.configure(background=col1 , foreground=col2)
	w.Wifi.configure(background=col1 , foreground=col2)
	w.Altitude.configure(background=col1 , foreground=col2)
	w.Speed.configure(background=col1 , foreground=col2)

	w.XYPositionalData.configure(background=gridcol)
	w.XNos.configure(background=gridcol)
	w.YNos.configure(background=gridcol)
	w.DroneLiveFeed.configure(background=col1)


	w.vsb.configure(bg=col1,activebackground=col1, highlightcolor=col1)


	ph = PIL.ImageTk.PhotoImage(PIL.Image.open(logo).resize((200, 50), PIL.Image.ANTIALIAS))
	w.Logo.configure(image = ph)
	w.Logo.image = ph

	ph = PIL.ImageTk.PhotoImage(PIL.Image.open(about).resize((857, 408), PIL.Image.ANTIALIAS))
	w.AboutSlide.configure(image = ph)
	w.AboutSlide.image = ph

	ph = PIL.ImageTk.PhotoImage(PIL.Image.open(credits).resize((857, 408), PIL.Image.ANTIALIAS))
	w.CreditsSlide.configure(image = ph)
	w.CreditsSlide.image = ph
	
	w.Error.configure(background=col1)
	w.Error.configure(foreground=col1)
	w.ConnectButton.configure(background=col1)
	w.ConnectButton.configure(foreground=col2)

	w.ConnectButton.configure(activebackground=col3)
	w.ConnectButton.configure(activeforeground=col2)

	#w.CallbackButton.configure(background=col1)
	#w.CallbackButton.configure(foreground=col2)
	#w.CallbackButton.configure(activebackground=col3)
	#w.CallbackButton.configure(activeforeground=col2)
	w.dmodeButton.configure(background=col1)
	w.dmodeButton.configure(foreground=col2)
	#w.ConnectButton.configure(activebackground=col3)
	#w.ConnectButton.configure(activeforeground=col2)
	w.EmLock.configure(background=col1)
	w.EmLock.configure(activebackground=col1)
	
	w.DeliveryDetailsPage.configure(background=col1)
	w.DroneFlightDataPage.configure(background=col1)
	w.AboutPage.configure(background=col1)
	w.CreditsPage.configure(background=col1)
	w.style.configure('TNotebook.Tab', background=col1)
	w.style.configure('TNotebook.Tab', foreground=col2)
	w.style.map('TNotebook.Tab', background=[('selected', col1), ('active',col1)])

	w.DeliveryList.configure(background=col3)
	w.DeliveryList.configure(foreground=col2)

	w.DeliveryDetails.configure(background=col3)
	w.DeliveryDetails.configure(foreground=col2)

	w.mvo.configure(background=col3)
	w.mvo.configure(foreground=col2)

	w.imu.configure(background=col3)
	w.imu.configure(foreground=col2)

	w.WhyconCoords.configure(background=col3)
	w.WhyconCoords.configure(foreground=col2)

	w.FlightData.configure(background=col3)
	w.FlightData.configure(foreground=col2)

def delidetails(event):
	t=w.DeliveryList.curselection()
	n=int(t[0])-2
	if n<0:
		return
	w.DeliveryDetails.configure(state='normal')
	w.DeliveryDetails.delete('3.0', 'end')
	strr="Name\t\t:  "+str(delidat[n]['Name'])
	strr+="\nAddress\t\t:  "+str(delidat[n]['Address'])
	strr+="\nItemName\t\t:  "+str(delidat[n]['ItemName'])
	strr+="\nItemWeight\t\t:  "+str(delidat[n]['ItemWeight'])
	strr+="\nDeliveryId\t\t:  "+str(delidat[n]['DeliveryId'])
	strr+="\nCustomerId\t\t:  "+str(delidat[n]['CustomerId'])
	strr+="\nCoordinate Location\t\t:  "+str(delidat[n]['X'])+",\t"+str(delidat[n]['Y'])+",\t"+str(delidat[n]['Z'])
	w.DeliveryDetails.insert('3.0',strr)
	w.DeliveryDetails.update()
	w.DeliveryDetails.configure(state='disabled')

def scal(x,y):
	return x*top.sca+(top.fcan/2),(-1*y)*top.sca+(top.fcan/2)

def draw_deliv():
	for i in range(1,len(ls)-1):
		x,y=scal(float(ls[i]['x']),float(ls[i]['y']))
		top.XYPositionalData.create_oval(x-15, y-15, x+15, y+15,outline="#0078ff", width=2)

def chk_conn():
		scanoutput = check_output(["iwlist", wificard, "scan"])
		ssid = "WiFi not found"
		for line in scanoutput.split():
		  line = line.decode("utf-8")
		  if line[:5]  == "ESSID":
			ssid = line.split('"')[1]

		if(ssid=="rn7p"):
			w.Status.configure(text='''Connected''', foreground="#2cbc00")
			w.ConnectButton.place_forget()
			draw_deliv()
			eng.publish(1)
		else:
			w.ConnectButton.place(relx=0.886, rely=0.019, height=28, width=189)
			w.Status.configure(text="Disconnected",foreground="#ff0000")
			w.Error.configure(foreground="#ff0000")

def conn():
	if(os.system("nmcli device wifi connect QuadDrop password qwertyuiop")==0):
		w.ConnectButton.place_forget()
		w.Status.configure(text="Connected",foreground="#2cbc00")
		w.Error.place_forget()
		draw_deliv()
		eng.publish(1)
	else:
		w.ConnectButton.place(relx=0.886, rely=0.019, height=28, width=189)
		w.Status.configure(text="Disconnected",foreground="#ff0000")
		w.Error.configure(foreground="#ff0000")

def destroy_window():
	# Function which closes the window.
	global top_level
	top_level.destroy()
	top_level = None
	sys.exit(1)

def init(top, gui, *args, **kwargs):
	global w, top_level, root
	w = gui
	top_level = top
	root = top

class Gui():
	def __init__(self,obj=None):
		global top
		top=obj
		self.ros_bridge = cv_bridge.CvBridge()
		self.point=None
		#self.draw_deliv()
		self.delivery_data()
		self.nxt=None
		self.progbarvalue=0
		#self.fac=1000/len(nofly.main(ls))
		fc=0
		for i in range(len(ls)):
			if ls[i]['delivery']>0:
				fc+=3
			else:
				fc+=1
		self.fac=1000/fc
		#self.ctr=0

		rospy.Subscriber('whycon/poses', PoseArray, self.draw_point)
		rospy.Subscriber('drone_feed', Image, self.show_feed)
		rospy.Subscriber('tello/status', TelloStatus, self.tello_status)
		rospy.Subscriber('tello/odom', Odometry, self.tello_odom)
		rospy.Subscriber('tello/imu', Imu, self.tello_imu)
		rospy.Subscriber('status_msg', String, self.prnt_msg)
		rospy.Subscriber('/wp_cords', PoseArray, self.draw_nxt)
		rospy.Subscriber('/progbar', Int16, self.upd_prog_bar)

		Lphoto = PIL.ImageTk.PhotoImage(PIL.Image.open(pathh+"gui/logoo.png").resize((200, 50), PIL.Image.ANTIALIAS))
		top.Logo.configure(image = Lphoto)
		top.Logo.image = Lphoto

		Cphoto = PIL.ImageTk.PhotoImage(PIL.Image.open(pathh+"gui/credits-light.png").resize((857, 408), PIL.Image.ANTIALIAS))
		top.CreditsSlide.configure(image = Cphoto)
		top.CreditsSlide.image = Cphoto

		Aphoto = PIL.ImageTk.PhotoImage(PIL.Image.open(pathh+"gui/about-light.png").resize((857, 408), PIL.Image.ANTIALIAS))
		top.AboutSlide.configure(image = Aphoto)
		top.AboutSlide.image = Aphoto

		Dphoto = PIL.ImageTk.PhotoImage(PIL.Image.open(pathh+"gui/dmode.png").resize((15, 15), PIL.Image.ANTIALIAS))
		top.dmodeButton.configure(image = Dphoto)
		top.dmodeButton.image = Dphoto

		fbarcol,bbarcol="#0078ff","#d9d9d9"
		fsccol,bsccol="#d9d9d9","#d9d9d9"
		top.style.configure('Horizontal.TProgressbar',foreground=fbarcol, background=fbarcol,troughcolor=bbarcol)
		top.style.configure('Horizontal.TScale',foreground=fsccol, background=fsccol,troughcolor=bsccol)

		top.StatusMesaages.configure(state='normal')
		top.StatusMesaages.insert('end', 'Status Messages\n- - - - - - - - - - - - - - - - - - - - - - - -')
		top.StatusMesaages.configure(state='disabled')
		top.StatusMesaages.see("end")

		top.FlightData.configure(state='normal')
		top.FlightData.insert('end', 'Flight Data\n- - - - - - - - - - - - - - - - - - - - - - - -\n')
		top.FlightData.configure(state='disabled')

		top.mvo.configure(state='normal')
		top.mvo.insert('end'," Odometry Data")
		top.mvo.configure(state='disabled')

		top.imu.configure(state='normal')
		top.imu.insert('end'," Gyroscope and IMU Data")
		top.imu.configure(state='disabled')

		top.DeliveryDetails.configure(state='normal')
		top.DeliveryDetails.insert('end'," Delivery Information\n- - - - - - - - - - - - - - - - - - - - - - - -\n")
		top.DeliveryDetails.configure(state='disabled')

		top.WhyconCoords.configure(state='normal')
		top.WhyconCoords.insert('end',"Current Whycon Coordinates\n- - - - - - - - - - - - - - - - - - - - - - - -\n")
		top.WhyconCoords.configure(state='disabled')

		#draw_deliv()

		scanoutput = check_output(["iwlist", wificard, "scan"])
		ssid = "WiFi not found"
		for line in scanoutput.split():
		  line = line.decode("utf-8")
		  if line[:5]  == "ESSID":
			ssid = line.split('"')[1]

		if(ssid=="QuadDrop"):
			top.ConnectButton.place_forget()
			top.Status.configure(text='''Connected''', foreground="#2cbc00")
			draw_deliv()
			eng.publish(1)
		else:
			top.Status.configure(text="Disconnected",foreground="#ff0000")

		'''if self.nxt!=None:
		top.XYPositionalData.delete(self.nxt)
		self.nxt.configure(outline="#ff7b00")'''
	
	def upd_prog_bar(self,data):
		#if self.ctr<6:
		#	self.ctr+=1
		#	return
		if(self.progbarvalue>=991):
			self.progbarvalue=0
			top.Progressbar.configure(value=self.progbarvalue)
		self.progbarvalue=self.progbarvalue+self.fac
		prev=100*(self.progbarvalue-self.fac)
		nextt=100*(self.progbarvalue)
		for i in range(prev,nextt):
			#time.sleep(0.00001)
			#print((i+1)/1000.0)
			top.Progressbar.configure(value=((i+1)/1000.0))

	def draw_nxt(self, pose):
		self.prevx,self.prevy=x,y=scal(pose.poses[0].position.x, pose.poses[0].position.y)
		if self.nxt!=None:
			top.XYPositionalData.delete(self.nxt)
			self.nxt=top.XYPositionalData.create_oval(self.prevx-15, self.prevy-15, self.prevx+15, self.prevy+15, outline="#ff7b00", width=2)
		self.nxt=top.XYPositionalData.create_oval(x-15, y-15, x+15, y+15, outline="#64eb34", width=2)
		

	def draw_point(self,pose):
		#fcan_x=fcan_y=2000/2
		can_x,can_y=888,491
		#scalex=scaley=100
		if self.point!=None:
			top.XYPositionalData.delete(self.point)
		x,y=scal(pose.poses[0].position.x, pose.poses[0].position.y)
		self.point=top.XYPositionalData.create_oval(x-5, y-5, x+5, y+5, fill="#0078ff", outline="#0078ff", width=2)

		top.WhyconCoords.configure(state='normal')
		top.WhyconCoords.delete('3.0', 'end')
		top.WhyconCoords.update()
		strr="   Position:\n   x: "+str(pose.poses[0].position.x)+"\t\t\t\ty: "+str(pose.poses[0].position.y)+"\t\t\t\tz: "+str(pose.poses[0].position.z)
		#strr+="\n   Orientation:\n   w: "+str(data.pose.pose.orientation.w)+"\tx: "+str(data.pose.pose.orientation.x)+"\n   y: "+str(data.pose.pose.orientation.y)+"\tz: "+str(data.pose.pose.orientation.z)
		top.WhyconCoords.insert('3.0',strr)
		top.WhyconCoords.configure(state='disabled')

	def delivery_data(self):
		top.DeliveryList.insert('end',"Customer Id")
		top.DeliveryList.insert('end',"- - - - - - - - - - - - - - - - - - - - - - - -")
		for i in range(len(delidat)):
			top.DeliveryList.insert('end',delidat[i]['CustomerId'])
		#self.DeliveryDetails.configure()

	def prnt_msg(self,msg):
		if(msg.data=="Tello Connected"):
			self.progbarvalue=0
			top.Progressbar.configure(value=self.progbarvalue)
		top.StatusMesaages.configure(state='normal')
		top.StatusMesaages.configure(foreground="white")
		top.StatusMesaages.insert('end', "\n"+msg.data)
		top.StatusMesaages.configure(state='disabled')
		top.StatusMesaages.see("end")

	def show_feed(self, image):
		frame = self.ros_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = imutils.resize(frame, width=656,height=405)
		photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
		#top.Status.configure(text="Hello")
		top.DroneLiveFeed.configure(image = photo)
		top.DroneLiveFeed.image = photo
	
	def tello_status(self,data):
		top.Status.configure(foreground="#2cbc00")
		top.Status.configure(text='''Connected''')

		if(data.battery_percentage<=30):
			top.style.configure('batt.Horizontal.TProgressbar',foreground='red', background='red')
		elif(data.battery_percentage<=80 and data.battery_percentage>30):
			top.style.configure('batt.Horizontal.TProgressbar',foreground='#0078ff', background='#0078ff')
		elif(data.battery_percentage>80):
			top.style.configure('batt.Horizontal.TProgressbar',foreground='#2cbc00', background='#2cbc00')

		top.Battery.configure(value=str(data.battery_percentage))
		top.Altitude.configure(text=str(100*data.height_m))
		top.AltitudeBar.configure(value=str(100*data.height_m))
		top.Speed.configure(text=str(100*data.speed_horizontal_mps))
		top.SpeedBar.configure(value=str(100*data.speed_horizontal_mps))

		
		top.Mode.configure(text=str(data.fly_mode))
		top.Wifi.configure(text=str(data.cmd_roll_ratio)+"%")

		top.FlightData.configure(state='normal')
		top.FlightData.delete('3.0', 'end')
		strr="Flight Time : "+str(data.flight_time_sec)
		strr+="\nBattery Percentage : "+str(data.battery_percentage)
		strr+="\nFlight time left : "+str(data.drone_fly_time_left_sec)
		strr+="\nTemperature : "+str(data.temperature_height_m)
		strr+="\nWind State : "+("Windy " if data.wind_state==1 else "Not Windy")
		top.FlightData.insert('3.0',strr)
		top.FlightData.update()
		top.FlightData.configure(state='disabled')

	def tello_odom(self,data):
		top.mvo.configure(state='normal')
		top.mvo.delete('2.0', 'end')
		top.mvo.update()
		strr="   Position:\n   x: "+str(data.pose.pose.position.x)+"\ty: "+str(data.pose.pose.position.y)+"\n   z: "+str(data.pose.pose.position.z)
		strr+="\n   Orientation:\n   w: "+str(data.pose.pose.orientation.w)+"\tx: "+str(data.pose.pose.orientation.x)+"\n   y: "+str(data.pose.pose.orientation.y)+"\tz: "+str(data.pose.pose.orientation.z)
		top.mvo.insert('2.0',strr)
		top.mvo.configure(state='disabled')

	def tello_imu(self,data):
		top.imu.configure(state='normal')
		top.imu.delete('2.0', 'end')
		top.imu.update()
		strr="   Angular Velocity:\n   x: "+str(data.angular_velocity.x)+"\ty: "+str(data.angular_velocity.y)+"\n   z: "+str(data.angular_velocity.z)
		strr+="\n   Linear Acceleration:\n   x: "+str(data.linear_acceleration.x)+"\ty: "+str(data.linear_acceleration.y)+"\n   z: "+str(data.linear_acceleration.z)
		top.imu.insert('2.0',strr)
		top.imu.configure(state='disabled')
		#top.odm.see("end")

	def tello_events(self,msg):
		top.WhyconCoords.configure(state='normal')
		top.WhyconCoords.configure(foreground="white")
		top.WhyconCoords.insert('end', "\n"+msg.data)
		top.WhyconCoords.configure(state='disabled')
		top.WhyconCoords.see("end")

if __name__ == '__main__':
	import QuadDrop
	QuadDrop.vp_start_gui()
	




