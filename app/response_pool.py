from random import randint
#response pools
welcome_messages = ["Hello", "Hi, want to talk?", "Good Morning", "Hi."]



def randomResponse():
	value = randint(0,(len(welcome_messages)-1))
	return welcome_messages[value]
