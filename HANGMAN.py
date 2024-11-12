import random 

def random_word()
	with open('HangManWords.txt', 'r') as file:
		words = file.read().splitlines()
		word = random.choice(words)