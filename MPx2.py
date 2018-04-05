#!/usr/bin/python3.6

#----IMPORTANT DESIGN INFORMATION----#
#Play button is a toggle for whether a song should currently be playing, checks will be like:	[if next pressed]- > [increment current song array by one]- > [is play toggle on?] so if it is on the song will just start playing and it wont if not
#The currently selected song will be loaded into memory and THAT SONG ONLY, once a new song is chosen the previous will be flushed from memory
#The play button will change its graphic to a pause button if a song is currently playing
#The bottom bottons will be: previous, play/pause, next
#The middle section is reserved for the song name and progress bar. The song name will alternate between song title, artist, and then album
#The top section will show the current directory (will be cut off if too long but if it were like 'C:\Users\Bob\Music\MusicMusic\Artist\Songs' it would show 'Artist\Songs'), as well as the X button
#Clicking the directory will give a very basic directory switcher which will show above the top bar

#----GENERAL FLOW----#
#Load current working directory as current directory
#Filter for supported song types and creates playlist in memory as an array
#Set array 0 as current song
#Read song data and set current title, artist, album, and song length		if any are unavailable, it will be set to [UNKNOWN ARTIST]/[UNKNOWN ALBUM], for unknown song titles, it'll be set to the file name
#Load song into memory
#Draw window
#	Set all the buttons to funtions
#	Draw all that stuff idk why I made the indent
#Set the window to refresh the progress bar every second, the progress bar equation will be like 'progress_bar_width=(width/total_time_in_seconds)*current_time'
#Loop window again

#----Directory Seeker----#
#When the directory is clicked to pull up the directory seeking window, it will pause playback, then start a new python script bundled along this one, it will create a new Tkinter window above this one
#The method will be called as such
#	____MAIN PLAYER____
#		directory=dseek.seek(current_open_directory)
#	____DIRECTORY SEEKER____
#		Read current directory list
#		Draw window and allow navigation
#		Which directory is chosen:
#			return(new_directory)
#If the directory is the same it wont do anything, but if it's different it will load the new directory

#----Directory Switch Script----#
#Set playback toggle to pause
#Load new directory
#Create playlist and set current playing index to 0
#Read song data and set current title, artist, album, and song length		if any are unavailable, it will be set to [UNKNOWN ARTIST]/[UNKNOWN ALBUM], for unknown song titles, it'll be set to the file name
#Load song into memory
#That should be it! The window should already be drawn!


#----POSSIBLE BUGS TO LOOK OUT FOR----#
#	When using dseek, pressing the play button may cause music to play right away after the dseek script has finished
#		FIX:Create a wrapper IF statement around player control functions checking for a variable called something like 'canRun' which will be set to 0 while dseek is open
#		FIX 2:When a function is called from Tkinter it actually sets a variable called something like 'toFunction' which will be put into a script to call the associated funtion after checking if 'canRun' is 1

print("pre-import")
import os
from tkinter import *
from tkinter.font import Font
import dseek #Custom directory seeking script
import pyglet #Media library/player
print("post-import")

#Updates title/artist/album text
def updateText():
	songInfo.config(text=currentTitle)
	
	
#Load song and set related variables
def loadSong(song):
	print("loadSong()")
	#Links global variables and loads song into memory
	global currentPlayer
	global currentSong
	global currentTitle
	global currentArtist
	global currentAlbum
	global currentSongData
	global workingDir
	print("post globals")
	print("loading " + os.path.join(workingDir, song))

	currentSongData = pyglet.media.load(os.path.join(workingDir, song), streaming=True)
	print("post songdata definition")
	#print(os.path.join(workingDir,currentSong))
	currentPlayer.queue(currentSongData)
	##print("Loading I3D information...")
	currentTitle=currentPlayer.source.info.title.decode('UTF-8')
	currentArtist=currentPlayer.source.info.author.decode('UTF-8')
	currentAlbum=currentPlayer.source.info.album.decode('UTF-8')
	#print(currentTitle)
	#print(currentArtist)
	#print(currentAlbum)
	
	#If it can't get the I3D information, it sets the song name to the file name, then sets the artist and album information to [UNKNOWN]
	if(currentTitle == ''):
		currentTitle=song
	if(currentArtist == ''):
		currentArtist="[UNKNOWN ARTIST]"
	if(currentAlbum == ''):
		currentAlbum="[UNKNOWN ALBUM]"

#Checks to see if file is an audio file
def isAudio(file):
	#Get the global supported file type list
	global fileTypes
	#Split file name to get the extension
	extension=file.split('.')[-1]
	#Checks extension with all possible file types and returns true if it matches, false if it doesn't
	for type in fileTypes:
		if(extension.lower() == type):
			return True
	return False

#Get all audio files
def createPlaylist(directory):
	#Create an empty list and a list called dirList which contains ALL items in a directory
	audioFiles=[]
	dirList=os.listdir(directory)
	#Sees if a list item is a directory, if it is it adds it to the audio file list
	for file in dirList:
		if(isAudio(file)):
			audioFiles.insert(len(audioFiles),file)
	return(audioFiles)
	
#Play pause switch
def playPause():
	#Add play/pause button global to edit text
	global btnPlayPause
	#Check if player is playing, if it is, set pause, otherwise, set play			changes button text to match current state
	if(currentPlayer.playing):
		currentPlayer.pause()
		btnPlayPause.config(text="►")
		
	else:
		currentPlayer.play()
		btnPlayPause.config(text="▐ ▌")
		
#Go back a song if not at the first song
def songBack():
	#Link song index and the current song for editing
	global songIndex
	global currentSong
	#If the player is playing, set resume playback to 1, otherwise set it to 0
	if(currentPlayer.playing):
		resumePlayback=1
	else:
		resumePlayback=0
	#Delete current player (flush songs from memory), move the song index back one if it isn't 0, set the new current song, then load it
	currentPlayer.delete()
	if(currentPlayer.time < 5):
		if(songIndex > 0):
			songIndex-=1
	else:
		pass
	currentSong=playlist[songIndex]
	loadSong(currentSong)
	#If resume playback is 1, it will immediately play the song, this is if you don't pause before you press back
	if(resumePlayback == 1):
		currentPlayer.play()
	#Update text
	updateText()
	
		
#Go to next song
def songNext():
	#Link song index and the current song for editing
	global songIndex
	global currentSong
	#If the player is playing, set resume playback to 1, otherwise set it to 0
	if(currentPlayer.playing):
		resumePlayback=1
	else:
		resumePlayback=0
	#If the song isn't the last in the playlist
	if(songIndex != len(playlist)-1):
		#Delete current player (flush songs from memory), move the song index back one if it isn't 0, set the new current song, then load it
		currentPlayer.delete()
		if(songIndex < len(playlist)-1):
			songIndex+=1
		currentSong=playlist[songIndex]
		loadSong(currentSong)
		#If resume playback is 1, it will immediately play the song, this is if you don't pause before you press back
		if(resumePlayback == 1):
			currentPlayer.play()
		#Update text
		updateText()
	#Loop back to first song
	else:
		currentPlayer.delete()
		songIndex=0
		currentSong=playlist[songIndex]
		loadSong(currentSong)
		#If resume playback is 1, it will immediately play the song, this is if you don't pause before you press back
		if(resumePlayback == 1):
			currentPlayer.play()
		#Update text
		updateText()
		
#Go to next song if the song is done playing
def songDone():
	#This looks complicated, but basically, it's because Pyglet doesn't stream the whole file, it usually stops .2 seconds before, so I made this check for it, if it passes, it'll go to the next song
	if(round(currentPlayer.time,1) > round(currentSongData.duration,1)-.2):
		songNext()
	#Run again every 10 milliseconds
	window.after(10, songDone)

#Set the progress bar	
def progressBarSet():
	#Link the global progress bar for editing
	global progressBar
	#Remake the coords, the new length is (width/totalLength)*currentTime
	canvas.coords(progressBar, 0,45,(200/currentSongData.duration)*currentPlayer.time,45)
	window.after(25, progressBarSet)
	
#Change directory
def changeDirectory():
	#Link global variables
	global workingDir
	global screenWidth
	global screenHeight
	global playlist
	global songIndex
	global currentSong
	#global currentTitle
	#global currentArtist
	#global currentAlbum
	global currentPlayer
	workingDir=dseek.main(workingDir, screenWidth-225, screenHeight-130)
	currentPlayer.play()
	playPause()
	currentPlayer.delete()
	playlist=createPlaylist(workingDir)
	##print(playlist)
	#Sets the currently playing song to the first item in the playlist and sets the artist information
	songIndex=0
	currentSong=playlist[songIndex]
	#print(currentSong)
	#Queue song to player and get information (sets song title, artist, and album variables)
	loadSong(currentSong)
	updateText()
	
def drawWindow():
	#Set play/pause button to a global object so the text can be edited as well as songInfo and progressBar
	global btnPlayPause
	global songInfo
	global progressBar
	global canvas
	global screenWidth
	global screenHeight
	screenWidth=window.winfo_screenwidth()
	screenHeight=window.winfo_screenheight()
	#Use monospace font
	usedFont=Font(window, family='Monospace', size=12)
	buttonFont=Font(window, family='Monospace', size=18)
	#Makes window appear above all else and gets rid of the window border as well as fill it with black
	window.wm_attributes("-topmost", 1)
	window.overrideredirect(1)
	window.configure(background='black')
	window.geometry("%dx%d%+d%+d" % (200, 90, screenWidth-225, screenHeight-130)) #Window geometry (width, height, x, y)
	
	#Replace window with canvas (needed for progess bar)
	canvas = Canvas(window, width=200, height=90, highlightthickness=0, highlightcolor="black", background="black")
	canvas.pack()
	
	#Draw X button as well as the current working directory
	
	Button(canvas, text=workingDir, foreground='grey', background='black', borderwidth=0, highlightthickness=0, highlightcolor="black", command=changeDirectory).place(y=0, x=0)
	Button(canvas, text="X", foreground='white', background='black', borderwidth=0, highlightthickness=0, highlightcolor="black", command=exit).place(y=0, x=186)
	songInfo = Label(canvas, text=currentTitle, foreground='white', background='black', borderwidth=0)
	songInfo.place(y=24, x=0)
	
	#Progress bar
	progressBar = canvas.create_line(0, 45, 0, 45, fill="white", width=2)
	
	#Previous, play/pause, and next buttons
	Button(canvas, text="◁", foreground='white', background='black', borderwidth=0, font=buttonFont, width=2, command=songBack).place(y=47, x=30)
	btnPlayPause = Button(canvas, text="►", foreground='white', background='black', borderwidth=0, font=buttonFont, width=2, command=playPause)
	btnPlayPause.place(y=47, x=80)
	Button(canvas, text="▷", foreground='white', background='black', borderwidth=0, font=buttonFont, width=2, command=songNext).place(y=47, x=130)
	
	#Start script that will run in the background to check the song progress
	window.after(0, songDone)
	#Start script to make the progress bar move with the song
	window.after(0, progressBarSet)
	
	#Update window and loop to start of draw script
	window.update()
	mainloop()

print("pre-init")
#Initialization - Creates list of supported files, sets the curent directory to the working one, and creates the global empty player
fileTypes=['mp3', 'wav', 'aiff', 'flac', 'alac', 'ape', 'acc', 'dts']
workingDir=os.getcwd()+"/"
currentPlayer=pyglet.media.Player()
print("post-init")

#Gets important variables for positioning
global screenWidth
global screenHeight
global currentSongData
print("post globals")

#Makes window global and primes it for being drawn
global window
window=Tk()
print("post window init")

#Create playlist of audio files
playlist=createPlaylist(workingDir)
print("post playlist init")

#Sets the currently playing song to the first item in the playlist and sets the artist information
songIndex=0
currentSong=playlist[songIndex]
print("post song init")

#Queue song to player and get information (sets song title, artist, and album variables)
print(currentSong)
loadSong(currentSong)
print("post loadsong")

#Draws window, the rest of the program is handled here
drawWindow()
print("post draw")

#currentPlayer.play()

#string=input("")
#currentPlayer.delete()
