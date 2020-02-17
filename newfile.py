check= False 
while (check== False):
	try:
		userValue= int(input("input any whole number: "))
		check=True
	except:
		print("there has been an error with your input, try again")
		check= False


for x in range(1,userValue+1):
	string="value= {0} and value squared= {1}"
	squared= x*x
	if (squared<200):
	    print(string.format(x,squared))
	    
	else:
		print("squared value cannot go over 200")
		break