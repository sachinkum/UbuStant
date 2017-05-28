#!/usr/bin/env python

import aiml
import os
import time, sys
import pyttsx
import speech_recognition as sr
import warnings


mode = "text"			#Setting the default input mode
if len(sys.argv) >1:		#If the number of arguments while executing from the terminal more than 1, eg:- "python bot.py voice"
	if sys.argv[1]=="--voice" or sys.argv[1]=="voice":
		mode = "voice"

terminate = ['bye','goodbye','gotosleep','byebye']		#Some keywords used for termination

def offline_speak(botresponse):		#The function for offline speech output
	engine = pyttsx.init()
	engine.say(botresponse)
	engine.runAndWait()

def hear():				#The function for offline speech input
	rss = sr.Recognizer()
	with sr.Microphone() as source:
	    print("Message:- ")
	    audio = rss.listen(source)
	try:
	    print rss.recognize_google(audio)
	    return rss.recognize_google(audio)
	except sr.RequestError as e1:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e1))
	except sr.UnknownValueError:
	    offline_speak("I could not understand what you said! Would you mind repeating?")
	    return(hear())


kernel = aiml.Kernel()			#Initializing the kernel

if os.path.isfile("./bot_brain.brn"):
	kernel.bootstrap(brainFile = "./bot_brain.brn")
else:
	print ("BOOTING KERNEL SYSTEM...")
	kernel.bootstrap(learnFiles = "./std-startup.xml", commands = "LOAD AIML B")	#Contains commands to load all the aiml files
	kernel.saveBrain("./bot_brain.brn")
	print "BOOT COMPLETED...\n SYSTEM NOW AVAILABLE"
	time.sleep(3)			#Just for a better user experience
	os.system("clear")
	
# kernel now ready for use
while True:
	if mode == "voice":		#If mode is 'voice', call the hear() function
		response = hear()
	else:				#Or else call to input text
		response = raw_input("Message:- ")
	
	if response.lower().replace(" ","") in terminate:		#Termination keywords used to break out of the script
		botresponse = "We'll catch up later then...BYE"
		print  botresponse
		offline_speak(botresponse)
		break
	botresponse = kernel.respond(response)		#Fetches the responses from the aiml by matching the patterns
	print  botresponse			#Prints the response to the stdout
	offline_speak(botresponse)		
