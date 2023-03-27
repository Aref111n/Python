import random

def gamewin(comp, you):
    if comp==you:
        return "Draw"
    elif comp=='r' and you=='p':
        return "You Won"
    elif comp=='p' and you=='s':
        return "you Won"
    elif comp=='s' and you=='r':
        return "You Won"
    else:
        return "You Lost"
    

while True:
    print("Comp Turn: Rock(r) Paper(p) or Scissor(s)?")
    r = random.randint(1, 3)
    if r==1:
        comp = 'r'
    elif r==2:
        comp = 'p'
    elif r==3:
        comp = 's'
    print("Computer choosed it's turn")
    print("Your Turn: Rock(r) Paper(p) or Scissor(s)")
    a = input() 

    print(gamewin(comp, a))
    print("Press 0 to exit, and press 1 for next turn")
    turn = int(input())
    if turn==0:
        break
    
