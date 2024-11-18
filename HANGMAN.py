#Importations for code
from random import choice
from string import ascii_uppercase
from pyfonts import load_font
import math
import random

import PySimpleGUI as sg #To use the GUI to build the game visual features

Wrong_Guesses_Max = 11	#Max number of guesses according to layers of cowboy

class HANGMAN:			#hangman class defined to create variables
	
	def __init__(self):		#constructor form/ class instance
		layout = [			#layout structure of the class to be defined
			[
				self._Gameboard_Frame(),		#Frame for gameboard/canvas
				self._Letters_Frame(),			#Frame to get the letters and display the ones available
			],
			[
				self._Word_Guessed_Created_Frame(),		#Frame to the gussed word
			],
			[
				self._Buttons_Frame(),					#Frame to create the buttons for the GUI and to press
			],
		]
		
		self._window = sg.Window(title="WildWest Hangman", layout=layout, finalize=True)	#Window allows for the game to be shown, labeled WILDWEST HANGMAN
		self._Gameboard = self._window["-GAMEBOARD-"]	#the gameboard element will be accessed with the window for the other elements
		self._New_Game()		#New game method to start a new game from the board
		self.Quit_Game = False	#Quit Game method to quit the gameboard, start at false so game doesnt automatically quit
		self._Games_Won = 0		#Counter to keep track of the games won
		self._Games_Played = 0 	#Counter for number of games played
		
	def _Gameboard_Frame(self):		#Function/defines gameboard method, to create the frame and layout in frame
		return sg.Frame(
			"WildWest Hangman",		#Title of Frame
			[
				[
					sg.Graph(
						key="-GAMEBOARD-",		#identifier
						canvas_size=(300, 600),	#size of the area in pixels
						graph_bottom_left=(0,0),	#initializing where the pixels start
						graph_top_right=(300, 600),
					)
				]
			],
			font = "Arial 20",			#Font chosen
		)
	
	def _Letters_Frame(self):			#Function for the letters method
		letter_groups = [				#Groups to divide alphabet to 4 letters
			ascii_uppercase[i:i+4]		#4 letter chunks to be sliced into
			for i in range(0, len(ascii_uppercase), 4)		#goes in steps of 4
		]
		#buttons created for each letter to be chosen/guessed
		letter_buttons = [
			[
				
				sg.Button(	#For each letter
					button_text = f" {letter} ",	#the letter is set to the text
					font = "Courier 20",				#Font chosen
					border_width = 0,				#for a flat button
					button_color = ('green on white'),	#colors chosen
					key=f"-letter-{letter}-",			#the identifier for each button
					enable_events=True,					#clicked button means event occurs
				)
				for letter in letter_group	#button for each letter
			]
			for letter_group in letter_groups	#loops through the groups created
		]
		return sg.Column(	#stacks buttons vertical
			[
				[
					sg.Frame(	#holds buttons in a frame
						"Letters",	#Title
						letter_buttons,		#list of the buttons	
						font = "Any 20",	#font and size
					),
					sg.Sizer(h_pixels=300),			#Spaces out other frames
				]
			
			]
			
		)
	
	

	def _Word_Guessed_Created_Frame(self):		#define frame for the letters being guessed
		return sg.Frame(
			"",			#No visible title
			[
				[
					sg.Text(		#text element to display word			
						key="-WORD-DISPLAYED-",		#identifier for the element
						font= "Arial 20",			#Font and size
					
					)
				
				]
			],
			element_justification="center",		#Centers the guessed word in frame
		)
		
	def _Buttons_Frame(self):
		return sg.Frame(
			"",
			[
				[
					sg.Sizer(h_pixels=90),	#pixels of horizontal space on left
					sg.Button(				#button for new game
						button_text="New Game",		#Title of button
						key="-NEWGAME-",			#Identifier
						font = "Arial 20",			#Font and Size
					),
					sg.Sizer(h_pixels=60),			#Space for restart game button
					sg.Button(
						button_text="Restart Game",
						key="-RESTARTGAME-",
						font= "Arial 20",			#Has the title, font size, and unique key
					),
					sg.Sizer(h_pixels=60),			#Space for quit game button
					sg.Button(
						button_text="Quit Game",
						key="-QUITGAME-",
						font = "Arial 20",			#title, space, and fontsize
					),
					sg.Sizer(h_pixels=90),			#horizontal space on the right as well
				]
			],
			font = "Arial 20"					#Font and Size
		)
		
	def _Drawing_Post(self):				#Defines the post that will be drawn to "hang" the man
		lines = [
			((20,55),(220,55),8),			#Lines created with their respective width
			((145,40),(145,405),8),
			((180,400),(80,400),8),
			((80,405),(80,370),8),
			((80,370),(80,350),1),
		]
		for *points, width in lines:
			self._Gameboard.DrawLine(*points,color ='silver', width = width)		#allows for the lines to be called and created
	
	def _Drawing_Tumbleweed1(self):								#To create a tumbleweed to give the wildwest feeling
		center_x, center_y = 35, 120
		radius = 20
		num_spokes = 30			#amount of lines that will be randomly chosen to surround the weed
		lines = []				#initialize an empty list for the spokes
		
		for _ in range(num_spokes):			#to get the random angle and length of where the spokes go
			angle = random.uniform(0,360)
			length = random.uniform(0, radius)
			angle_radians = math.radians(angle)
			
			x_end = center_x + length * math.cos(angle_radians)		#Gives an x and y end
			y_end = center_y + length * math.sin(angle_radians)
			
			lines.append(((center_x, center_y), (x_end, y_end), random.randint(2,5)))		#append the lines from center to end with random width
			
		for *points, width in lines:		#loops through all lines to draw on gameboard
			self._Gameboard.DrawLine(*points,color ='maroon', width = width)
		
		self._Gameboard.Widget.update()		#Refresh the frame
	
	def _Drawing_Tumbleweed2(self):		#Process repeated for another tumbleweed
		center_x1, center_y1 = 240, 75
		radius1 = 20
		num_spokes1 = 50
		lines = []
		
		for _ in range(num_spokes1):
			angle1 = random.uniform(0,360)
			length1 = random.uniform(0,radius1)
			angle_radians1 = math.radians(angle1)
			
			x_end1 = center_x1 + length1 * math.cos(angle_radians1)
			y_end1 = center_y1 + length1 * math.sin(angle_radians1)
			
			lines.append(((center_x1, center_y1), (x_end1, y_end1), random.randint(2,5)))
		
		for *points, width in lines:
			self._Gameboard.DrawLine(*points, color = 'maroon', width = width)
			
		self._Gameboard.Widget.update() #refresh in case the tumbleweed doesn't form
	
	def _Drawing_Hangedman(self):
		
		head = (80,330)
		
		hat = [
			((60,350),(60,370)),		#For the line up hat
			((100,350),(100,370)),		#For the line up hate
			((100,370),(80,360)),		#For the triangle line
			((60,370),(80,360)),		#For the triangle Line
			((40,350),(120,350)),		#Horizontal Line for bottom of hat
			((30,340),(130,340)),		#Horizontal Line for Bottom of Hat
			
			
		]
		
		bandana = [
			((60,310),(100,310)),		#Horizontal line for bandana under head
			((60,310),(80,270)),		#Triangle Line
			((100,310),(80,270)),		#Triangle Line
		]
		
		torso = [((80,310),(80,210))]
		
		vest = [
			((80,210),(60,210)),		#For the rectangle for the vest stopping at shoulder inserts
			((80,210),(100,210)),
			((60,210),(60,290)),
			((100,210),(100,290)),
			((60,290),(100,290)),
			
			((60,250),(55,265)),		#To make a "semicircle" cutout of left side near shoulder
			((55,265),(60,280)),
			((60,280),(65,265)),
			((65,265),(60,250)),
			
			((100,250),(105,265)),		#To make a "semicircle" cutout of left side near shoulder
			((105,265),(100,280)),
			((100,280),(95,265)),
			((95,265),(100,250)),
		]
		
		left_arm = [
			((80,290),(60,290)),		#Coordinates for shoulder, left arm, and left hand
			((60,290),(40,250)),
			((40,250),(40,230)),
		]
		
		right_arm = [
			((80,290),(100,290)),		#Coordinates for shoulder, right arm, and right hand
			((100,290),(120,250)),
			((120,250),(120,230)),
		]
		
		left_leg = [
			((80,210),(60,210)),		#For left leg
			((60,210),(50,180)),
			((50,180),(50,120)),
			((50,120),(40,120)),
		]
		
		right_leg = [
			((80,210),(100,210)),		#To draw right leg
			((100,210),(110,180)),
			((110,180),(110,120)),
			((110,120),(120,120)),
		]
		
		left_boot = [
			((40,120),(40,110)),		#To draw little hook boots
			((40,110),(30,110)),
			((30,110),(30,120)),
		]
		
		right_boot =[
			((120,120),(120,110)),		#To draw little hook boots
			((120,110),(130,110)),
			((130,110),(130,120)),
		]
		
		body = [			#List of what body parts come after each wrong guess
			hat,
			bandana,
			torso,
			vest,
			left_arm,
			right_arm,
			left_leg,
			right_leg,
			left_boot,
			right_boot,
		]
		
		
		if self._Guessed_Wrong == 1:	#Draws the head once a guess is wrong
			self._Gameboard.DrawCircle(head, 20, line_color = 'gray', line_width = 4)
		elif self._Guessed_Wrong > 1:		#Greater than one it starts to go down the list and draw more body parts
			for Part in body[self._Guessed_Wrong - 2]:	#for loop to add another part
				self._Gameboard.DrawLine(*Part, color = 'gray', width = 4)
	
	def _Word_Selected(self):		#To choose the random word from the .txt word file
		with open("HangManWords.txt", mode="r",encoding="utf-8") as words:	#opens file with UTF-8 encoding
			Word_Choices_List = words.readlines()				#reads all lines and stores as list
		return choice(Word_Choices_List).strip().upper()		#randomly chooses the word, puts uppercase
		
	def _Word_Guessed_Created(self):	#Shows correct guessed letters and keeps underscores for blanks
		Available_Letters = []			#list to store information
		
		for letter in self._target_word:		#loops through each letter in chosen word
			if letter in self._Letters_Chosen:		#check if the letter has been guessed
				Available_Letters.append(letter)		#adds letter to list
			else:
				Available_Letters.append("_")		#adds underscore if not guessed
		return " ".join(Available_Letters)			#joins letters and underscores
		
	def _New_Game(self):			#starts a new game, resets the game drawing and letters
		self._target_word = self._Word_Selected()		#selects new word
		self._Game_Restarts()							#method to reset any other states of game
		
	def _Game_Restarts(self):	#method to restart the game
		self._Letters_Chosen = set()		#chosen letters list becomes empty
		self._Guessed_Wrong = 0				#counter back to zero for wrong guesses
		self._Word_Guessed = self._Word_Guessed_Created()		#recreates the target word
		
		self._Gameboard.erase()		#clears gameboard
		self._Drawing_Post()		#redraw drawing post
		self._Drawing_Tumbleweed1()	#redraw tumbleweed
		self._Drawing_Tumbleweed2()
		for letter in ascii_uppercase:		#Buttons on letter frame are reset
			self._window[f"-letter-{letter}-"].update(disabled=False)	
		self._window["-WORD-DISPLAYED-"].update(self._Word_Guessed)	#Updates the word with letters and underscores
		
	def _Game_Play(self, letter):		#For when a letter is selected
		if letter not in self._target_word:		#Increments the wrong guesses if chosen letter is not in word
			self._Guessed_Wrong += 1
		self._Letters_Chosen.add(letter)		#adds letter to list of chosen letters
		self._Word_Guessed = self._Word_Guessed_Created()		#updates display with current guesses
		
		self._window[f"-letter-{letter}-"].update(disabled=True)		#disables button when letter chosen
		self._window["-WORD-DISPLAYED-"].update(self._Word_Guessed)		#updates the display of the word being guessed
		self._Drawing_Hangedman()				#updates the hangman drawing
		
	def to_produce_event_read(self):		#waits for event to return identifier
		event = self._window.read()			#reads the event in the window
		event_id = event[0] if event is not None else None		#gets the identifier
		return event_id		#returns it for processing for game to progress
		
	def to_process_the_event(self, event):		#function to process events
		if event[:8] == "-letter-":				#if a button click from ltter 
			self._Game_Play(letter = event[8])		#calls the gameplay function 
		elif event == "-RESTARTGAME-":				#if restart button
			self._Game_Restarts()					#calls restart game process
		elif event == "-NEWGAME-":					# if new game button
			self._New_Game()						#calls new game function
			
	def Game_Over(self):						#function for when the game ends	
		return any(							#checks game over with max wrong guesses or winning
			[
				self._Guessed_Wrong == Wrong_Guesses_Max,		#max wrong guesses
				set(self._target_word) <= self._Letters_Chosen,		#all letters guessed
			]
		)
		
	def Game_Winner_Check(self):		#Checks if won or lost
		self._Games_Played += 1			#increments total games played
		if self._Guessed_Wrong < Wrong_Guesses_Max:		#when all letters guessed
			self._Games_Won += 1			#increments games won
			GameAnswer = sg.PopupYesNo(			#gives a statement for congratulations and if play again
				"You have won!! Proving to be the best wordslinger in the wild west ;)!\n"
				f"Making you have {self._Games_Won} wins out of {self._Games_Played} games played!\n"
				"Would You Like to PLay Another Round?",
				title = "WordSlinger",		#displays the games won out of played, title of window
			)
		else:
			GameAnswer = sg.PopupYesNo(		#when player loses, displayes statement of sorry, the word, and total of won out of played
				f"Aw darn that's too bad, you have lost this game. The word was '{self._target_word}'.\n"
				f"Making you have {self._Games_Won} wins out of {self._Games_Played} games played!\n"
				"Would You Like to PLay Another Round?",
				title = "Wanted Outlaw for Losing",	#window title
			)
		self.Quit_Game = GameAnswer == "No"	#if player selects no the game will exit
		if not self.Quit_Game:			#if yes is selected the game will restart
			self._New_Game()			#function to start new game called
			
	def Game_Close(self):				#Method to close the game
		self._window.close()			#closes the GUI window
		
if __name__ == "__main__":			#Script executed
	Game = HANGMAN()				#new instance for hangman game class 
	while not Game.Quit_Game:			#loop to continue until the quit game is selected
		while not Game.Game_Over():		#loop through game until it's over
			event_id = Game.to_produce_event_read()		#event captured
			if event_id in {sg.WIN_CLOSED,"-QUITGAME-"}:		#Clicks quit game then quit game is true and exits game
				Game.Quit_Game = True
				break											#exits the inner loop
			Game.to_process_the_event(event_id)				#processes the event
		if not Game.Quit_Game:							#checks if player will play again
			Game.Game_Winner_Check()					#checks win or lose
	Game.close()								#closes the game
