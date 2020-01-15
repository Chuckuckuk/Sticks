from sticks_game import hands, braindead_AI, easy_AI, med_AI
from minimax_sticks import GoodPlayer, GoodPlayer_2, execute_move, convert_davids_to_mine, sync_to_davids, convert_to_davids, sync_to_mine
from IPython.display import clear_output

print('Welcome to sticks. Type h or help for rules and commands.')
# initialize you and your opponent's hads
my_hands = hands('me')

while True:
    diff = input('Bot difficulty (braindead,easy,medium,minimax): ')
    if diff=='braindead':
        their_hands=braindead_AI('bot')
        break
    elif diff=='easy':
        their_hands=easy_AI('bot')
        break
    elif diff=='medium':
        their_hands=med_AI('bot')
        break
    elif diff=='minimax':
        dep = int(input("Minimax depth (integer>=1): "))
        their_hands = GoodPlayer(depth=dep)
        break
    print('Invalid. Try again')

# indefinitely loop a prompt to make a move against your opponent. Your opponent will react completely randomly (for now)
if diff != 'minimax':
    print(' ')
    print("You have",my_hands)
    print("They have",their_hands)
    while True:
        comm = input('What will you do? ').lower()
        print(' ') # just a line break
        if comm in {'stop','exit'}: # allow the player to quit out if they like
            break
        elif comm[0] in {'h','H'}: # if the player types anything starting with h, display the help page.
            print("-You and your opponent start with one stick on each hand.")
            print("-To tap one of your opponent's hands, type 'tap A with B', where A is your hand and B is theirs.")
            print("-When tapping an opponent's hand, the number of sticks on your hand is added to theirs. You keep your sticks.")
            print("-To swap sticks from one of your hands to the other, type 'swap A from B', where A is an integer and B is a hand.")
            print("-When swapping sticks, you transfer them, unlike tapping an opponent's hand.")
            print("-If a hand has 5 or more sticks, 5 sticks are subtracted.")
            print("-If both of a player's hands have 0 sticks, that player loses.")
            print("-If you're bored of playing, type stop or exit.")
            print(' ')
            continue
        comm = comm.split() # split apart the string entered by the player. Makes it easier to identify commands
        if comm[0].lower() == 'tap': 
            try:
                A, B = comm[1].lower(), comm[3].lower() # A and B are your hand and your opponent's, respectively
                assert A in {'left','right'}
                assert B in {'left','right'}
            except:
                print("Something went wrong with the tap command. Try again. Press h or help for rules and commands")
                continue
            # implement code to tap the opponent's hand with one of yours
            my_hands.tap(their_hands,B,A)
            print("You tap their",A,"with your",B+'.')
        elif comm[0].lower() == 'swap':
            try:
                A = int(comm[1]) # try this code, if it doesn't work then throw an exception so that the whole script doesn't crash.
            except:
                print("You didn't enter an integer to swap.") # if the player didn't enter an integer, let them try again.
                continue
            try:
                B = comm[3].lower() 
                assert(B in {'left','right'}) # makes sure that the player entered a hand and not some garbage
            except:
                print("Not a valid hand.")
                continue
            # implement code to swap sticks from one of your hands to the other
            ok = my_hands.swap(B,A)
            if ok:
                continue
            else:
                print("You swap",A,"stick from your",B,"hand.")
        else:
            print("Didn't recognize that instruction. Type h or help for rules and commands.") # for any other invalid command
            continue
        my_hands.fix_hands(), their_hands.fix_hands()
        print("You have",my_hands)
        print("They have",their_hands)
        print(' ')
        # check if the player won after their action
        if their_hands.lost:
            print("You win! The bot has no sticks left.")
            break
        elif my_hands.lost:
            print("You lose! You have no sticks left. Your last move was suicide, great job.")
            break

        # implement code to have a bot randomly take some action against the player if it hasn't lost. Later will be replaced with a neural network that learns to play
        their_hands.execute_best_action(my_hands,muted=False)

        # apply the hand-5 rule and check if either player has won
        my_hands.fix_hands(), their_hands.fix_hands()
        print("You have",my_hands)
        print("They have",their_hands)
        print(' ')
        if their_hands.lost:
            print("You win!")
            break
        elif my_hands.lost:
            print("You lose!")
            break

elif diff=='minimax':
    t = input("Minimax generation: ")
    if t == '2':
        me = GoodPlayer_2(depth=dep)
    else:
        me = GoodPlayer(depth=dep)
    david = hands('Me')
    print(' ')
    print("You have",david)
    print("They have",convert_to_davids(me))
    while True:
        
        # make a hands object with the opponent's score
        me_as_davids_type = convert_to_davids(me)
        david_as_my_type = convert_davids_to_mine(david)
        
        
        # the move itself
        comm = input('What will you do? ').lower()
        print(' ') # just a line break
        if comm in {'stop','exit'}: # allow the player to quit out if they like
            break
        elif comm[0] in {'h','H'}: # if the player types anything starting with h, display the help page.
            print("-You and your opponent start with one stick on each hand.")
            print("-To tap one of your opponent's hands, type 'tap A with B', where A is your hand and B is theirs.")
            print("-When tapping an opponent's hand, the number of sticks on your hand is added to theirs. You keep your sticks.")
            print("-To swap sticks from one of your hands to the other, type 'swap A from B', where A is an integer and B is a hand.")
            print("-When swapping sticks, you transfer them, unlike tapping an opponent's hand.")
            print("-If a hand has 5 or more sticks, 5 sticks are subtracted.")
            print("-If both of a player's hands have 0 sticks, that player loses.")
            print("-If you're bored of playing, type stop or exit.")
            print(' ')
            continue
        comm = comm.split() # split apart the string entered by the player. Makes it easier to identify commands
        if comm[0].lower() == 'tap': 
            try:
                A, B = comm[1].lower(), comm[3].lower() # A and B are your hand and your opponent's, respectively
                assert A in {'left','right'}
                assert B in {'left','right'}
            except:
                print("Something went wrong with the tap command. Try again. Press h or help for rules and commands")
                continue
            # implement code to tap the opponent's hand with one of yours
            david.tap(me_as_davids_type,B,A)
            print("You tap their",A,"with your",B+'.')
        elif comm[0].lower() == 'swap':
            try:
                A = int(comm[1]) # try this code, if it doesn't work then throw an exception so that the whole script doesn't crash.
            except:
                print("You didn't enter an integer to swap.") # if the player didn't enter an integer, let them try again.
                continue
            try:
                B = comm[3].lower() 
                assert(B in {'left','right'}) # makes sure that the player entered a hand and not some garbage
            except:
                print("Not a valid hand.")
                continue
            # implement code to swap sticks from one of your hands to the other
            ok = david.swap(B,A)
            if ok:
                continue
            else:
                print("You swap",A,"stick from your",B,"hand.")
        else:
            print("Didn't recognize that instruction. Type h or help for rules and commands.") # for any other invalid command
            continue
        david.fix_hands(), me_as_davids_type.fix_hands()
        
        print("You have",david)
        print("They have",me_as_davids_type)
        print(' ')
        
        # check if the player won after their action
        if me_as_davids_type.lost:
            print("You win!")
            break
        elif not me.alive():
            print("You lose")
            break
        
        # after the move
        sync_to_mine(me_as_davids_type, me)
        david_as_my_type = convert_davids_to_mine(david)
                
        
        # minimax player's move: AI, move second
        my_move = me.select_move(david_as_my_type)
        clear_output()
        if len(my_move) == 2:
            print('The bot taps your','left' if my_move[1]=='l' else 'right','with its','left.' if my_move[0]=='l' else 'right.')
        elif len(my_move) == 3:
            print('The bot swaps',my_move[2],'from its','left' if my_move[1]=='l' else 'right','hand.')
        
        execute_move(me, david_as_my_type, my_move)
        sync_to_davids(david_as_my_type,david)
        
        if not me.alive():
            print("You win!")
            break
        elif david.lost:
            print("You lose!")
            break
        print("You have",david)
        print("They have",convert_to_davids(me))