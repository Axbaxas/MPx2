#!/usr/bin/python3.6

#----IMPORTANT DESIGN INFORMATION----#
#Dseek is a tool used alongside MPx2 as a way to list, search, and change directories
#The top is reserved for the current directory and the eXit button.
#The X will cause dseek to return the value passed to it as an input value (EX. If the input was 'C:\Users\Bob\Music\' it would return 'C:\Users\Bob\Music\')
#The middle section will be ten lines long each listing a directory, if there is more, buttons will be available to move up and down on the right side, if there is less, the space will be there, but blank
#If a user clicks on a blank directory, it will not do anything (this will require a check for when a user clicks on an entry)
#At the top of the list, taking up 'spot' 11, will be a 'Back one directory' buttons
#The bottom will be the 'Open' and 'Choose' buttons
#Clicking a directory and selecting open will set the current directory to that directory, meaning that if you click 'Choose' right after, it will be the same as if you had only selected the directory and not opened it
#
#This dseekWindow will appear above the MPx2 dseekWindow, it will be the same width

#----GENERAL FLOW----#
#	[Setup]
#		Set the input directory as current working directory
#
#	[Main]
#Create directory list based on current working directory and store it as an array (if array is less than ten entries, fill the rest with '')
#^^Also create a variable with the number of actual directories (I'll call it 'dirCount' for now)
#Draw dseekWindow
#		Draw current working directory and X button
#		Draw the directory list and buttons (the directory list is based on a scroll variable, the entry for spot three will be along the lines of 'entry3=dirArray[scrollInt+2]' if the scrollInt is 0)
#		Draw 'Open' and 'Choose' buttons
#
#If scroll buttons are pressed:
#		Do a check along the lines of
#			For up - 'if(scrollInt>0): scrollInt-=1'
#			For down - 'if(dirCount>10){if(scrollInt<len(dirCount)){scrollInt+=1}}' I know its one line but I'm lazy with comments
#If X is pressed return input value
#If a directory is selected it sets selectedDir to that directory, then if it is opened it will set it to current directory
#Pressing choose reads the slectedDir variable, currentDir is just for saying where you are at the top





import os
from tkinter import * #This lets things be called Tk instead of tkinter.Tk
from tkinter.font import Font

#Lists directories
def listDirectories(directory):
	#print("List directories")
	#Create an empty list an a list called dirList which contains ALL items in a directory
	dir=[]
	dirList=os.listdir(directory)
	#Sees if a list item is a directory, if it is it adds it to the dir list
	for item in dirList:
		if(os.path.isdir(os.path.join(directory,item))):
			dir.insert(len(dir),item)
	#If a directory is less than ten entries it will fill the rest with ''
	while(len(dir)<10):
		dir.insert(len(dir),'')
	#Return the list
	global scrollInt
	scrollInt=0
	return(dir)
	
	
#The number of directories
def dirNumber(directory):
	#print("Directory number")
	#Create an empty list an a list called dirList which contains ALL items in a directory
	dir=[]
	dirList=os.listdir(directory)
	#Sees if a list item is a directory, if it is it adds it to the dir list
	for item in dirList:
		if(os.path.isdir(os.path.join(directory,item))):
			dir.insert(len(dir),item)
	#Returns the length of the directory list
	global scrollInt
	scrollInt=0
	return(len(dir))
	
#Required to update all text in a simple command
def updateText():
	#print("Updating Text")
	current.config(text=workingdir)
	d1.config(text=dir[0+scrollInt])
	d2.config(text=dir[1+scrollInt])
	d3.config(text=dir[2+scrollInt])
	d4.config(text=dir[3+scrollInt])
	d5.config(text=dir[4+scrollInt])
	d6.config(text=dir[5+scrollInt])
	d7.config(text=dir[6+scrollInt])
	d8.config(text=dir[7+scrollInt])
	d9.config(text=dir[8+scrollInt])
	d10.config(text=dir[9+scrollInt])
	

#Decrease scroll int if not already completely scrolled up
def scrollUp():
	#print("Scroll up")
	global dirCount
	global scrollInt
	global dir
	if(scrollInt>0):
		scrollInt-=1
		updateText()
		dseekWindow.update()
	
#Increase scroll int if not all the way down and there is more to show	
def scrollDown():
	#print("Scroll down")
	global dirCount
	global scrollInt
	global dir
	##print(str(dirCount)+" > 10")
	if(dirCount>10):
		##print(str(scrollInt)+10" != "+str(dirCount))
		if(scrollInt+10!=dirCount):
			scrollInt+=1
			updateText()
			##print(dir[scrollInt])
			dseekWindow.update()
			
#Returns current folder to MPx2
def exit():
	#print("X pressed")
	global exit_code
	exit_code=2
	dseekWindow.destroy()

	

#Exits by destrying dseekWindow
def chooseFolder():
	#print("Folder Chosen")
	dseekWindow.quit()
	
#This is the seek function, it's kind of the main function, it's what should be called by MPx2
def seek(currentDir):
	#print("Seek")
	global dir
	global dirCount
	global scrollInt
	global workingdir
	global exit_code
	global windowX
	global windowY
	global finaldir
	workingdir=currentDir
	finaldir=currentDir
	#Create list of directories and the number of directories as well as the current scroll count
	dir=listDirectories(currentDir)
	dirCount=dirNumber(currentDir)
	scollInt=0
	#Draw dseekWindow
	#Use monospace font
	usedFont=Font(dseekWindow, family='Monospace', size=12)
	#Makes dseekWindow appear above all else and gets rid of the dseekWindow border as well as fill it with black
	dseekWindow.wm_attributes("-topmost", 1)
	dseekWindow.overrideredirect(1)
	dseekWindow.configure(background='black')
	
	dseekWindow.geometry("%dx%d%+d%+d" % (200, 295, windowX, windowY-295)) #dseekWindow geometry (width, height, x, y) [Will be replaced with width, height, x, and y provided by MPx2]
	
	#Draw the X at the top
	Button(dseekWindow, text="X", foreground='white', background='black', borderwidth=0, command=exit).place(y=0, x=186)
	
	#Back directory buttons
	Button(dseekWindow, text="⇐", foreground='white', background='black', borderwidth=0, command=backButton).grid(row=2, column=0, sticky=W)
	 
	#Draw initial text
	updateText()
	
	
	#Scroll buttons
	Button(dseekWindow, text="⇑", foreground='white', background='black', borderwidth=0, command=scrollUp).place(y=20, x=186)
	Button(dseekWindow, text="⇓", foreground='white', background='black', borderwidth=0, command=scrollDown).place(y=240, x=186)
	r
	#Open and Choose buttons
	Button(dseekWindow, text="Choose folder", foreground='white', background='black', borderwidth=2, width=28, command=chooseFolder).place(y=270, x=0)
	
	#Loop back up to top of dseekWindow after updating all information on the dseekWindow
	dseekWindow.update()
	mainloop()
	return finaldir
	
	
#Back one directory
def backButton():
	#print("Back")
	#Get current directory, split it by '\', then remove the first and last entry
	global workingdir
	global dir
	global dirCount
	global scrollInt
	global finaldir
	currentDir=workingdir
        ## Changed from "C:\\" to "/" for Linux version, also using '/' for dir split rather than '\\'
	newdir="/"
	tmp=currentDir.split("/")
	tmp = tmp[1:-2]
	#Rejoin everything but remove the last '\'
	for item in tmp:
		newdir=newdir+item+"/"
	#Create list of directories and the number of directories as well as the current scroll count
	workingdir=newdir
	dir=listDirectories(workingdir)
	dirCount=dirNumber(workingdir)
	scollInt=0
	finaldir=newdir
	updateText()
	
	
	
#Selects the directory when clicked, uses the scroll index and position to determine which entry
def clickDir(value):
	#print("Click")
	global dir
	global finaldir
	global workingdir
	global dirCount
	#Create new directory list
	newdir=workingdir+dir[value]+"/"
	#Create list of directories and the number of directories as well as the current scroll count
	workingdir=newdir
	dir=listDirectories(workingdir)
	dirCount=dirNumber(workingdir)
	scollInt=0
	finaldir=newdir
	updateText()
	
	
def main(directory, tmpx, tmpy):
	#print("Main")
	#Make dseekWindow global
	global dseekWindow
	global windowX
	global windowY
	windowX=tmpx
	windowY=tmpy
	dseekWindow=Tk()
	#global exit_code
	global finaldir
	finaldir=directory
	##print(finaldir)
	
	#MAKE EVERYTHING GLOBAL SO IT CAN JUST NOT RUN WHEN IMPORTED
	#print("Variable stuff")
	global current
	global d1
	global d2
	global d3
	global d4
	global d5
	global d6
	global d7
	global d8
	global d9
	global d10
	
	
	#Current directory at top
	current=Button(dseekWindow, text=workingdir, foreground='white', background='black', borderwidth=0, state=DISABLED, command=exit)
	current.grid(row=1, column=0, sticky=W)

	#Directory list | Must be called early to properly update text
	d1 = Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(0+scrollInt))
	d1.grid(row=3, column=0, sticky=W)

	d2=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(1+scrollInt))
	d2.grid(row=4, column=0, sticky=W)

	d3=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(2+scrollInt))
	d3.grid(row=5, column=0, sticky=W)

	d4=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(3+scrollInt))
	d4.grid(row=6, column=0, sticky=W)

	d5=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(4+scrollInt))
	d5.grid(row=7, column=0, sticky=W)

	d6=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(5+scrollInt))
	d6.grid(row=8, column=0, sticky=W)

	d7=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(6+scrollInt))
	d7.grid(row=9, column=0, sticky=W)

	d8=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(7+scrollInt))
	d8.grid(row=10, column=0, sticky=W)

	d9=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(8+scrollInt))
	d9.grid(row=11, column=0, sticky=W)

	d10=Button(dseekWindow, text="", foreground='white', background='black', borderwidth=0, command= lambda: clickDir(9+scrollInt))
	d10.grid(row=12, column=0, sticky=W)
	
	
	
	
	
	finaldir=seek(directory)
	dseekWindow.destroy()
	return(finaldir)
	##print("Seeking done")
	#if(exit_code==2):
	#	return(0)
	#elif(exit_code==1):
	#	return(finaldir)
	
#Makes dseekWindow global and primes it for being drawn
#Initializes global variables
dir=[]
dirCount=0
scrollInt=0
workingdir=""
finaldir=""
startdir=""

passdir=""

exit_code=0
