print('''
 The 24 Game
 
 Given any four digits in the range 1 to 9, which may have repetitions,
 Using just the +, -, *, and / operators; and the possible use of
 brackets, (), show how to make an answer of 24.
 
 An answer of "q" will quit the game.
 An answer of "!" will generate a new set of four digits.
 Otherwise you are repeatedly asked for an expression until it evaluates to 24
 
 Note: you cannot form multiple digit numbers from the supplied digits,
 so an answer of 12+12 when given 1, 2, 2, and 1 would not be allowed.
 
''')
import random, re
chars = ["(",")","/","+","-","*"]  
while True:
    charsandints, ints = [], []
    for x in range(4):
        ints.append(str(random.randrange(1,10)))
    charsandints = chars + ints
    print ("Numbers are:", ints)
    guess = input("Enter your guess:")
    if guess.lower() == "q":
        break
    elif guess.lower() == "!":
        pass
    else:
        flag = True
        for a in guess:
            if a not in charsandints or guess.count(a) > charsandints.count(a):
                flag = False
        if re.search("\d\d", guess):
            print ("You cannot combine digits.")
            break
        if flag:
            print ("Your result is: ", eval(guess))
            if eval(guess) == 24:
                print ("You won")
                break
            else:
                print ("You lost")
                break
        else:
            print ("You cannot use anthing other than", charsandints)
            break
print ("Thanks for playing")
