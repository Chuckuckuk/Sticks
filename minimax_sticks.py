#!/usr/bin/env python3

from typing import Iterable, Tuple
from copy import copy
import sticks_game
import random
from numpy import mean, std


possible_moves = (
    'll',  # player left taps opponent left
    'lr',  # player left taps opponent right
    'rr',  # player right taps opponent right
    'rl',  # player right taps opponent left
    'sr1',
    'sr2',
    'sr3',
    'sr4',
    'sl1',
    'sl2',
    'sl3',
    'sl4',
)


class Player:
    def __init__(self):
        self.left = 1
        self.right = 1

    def alive(self):
        return self.good_hands() > 0

    def good_hands(self):
        return min(self.left, 1) + min(self.right, 1)

    def select_move(self, opponent):
        raise NotImplementedError

    def __str__(self):
        return '({}, {})'.format(self.left, self.right)


def maximize(scored_moves: Iterable[Tuple[str, int]]):
    assert scored_moves
    assert None not in scored_moves
    return max(scored_moves, key=lambda item: item[1])


def minimax(_p1, _p2, depth):
    scored_moves = []
    moves_to_score = valid_moves(_p1, _p2)
    if not moves_to_score:
        return '', _p1.good_hands() - _p2.good_hands()
    if depth == 1:
        for move in moves_to_score:
            p1, p2 = copy(_p1), copy(_p2)
            execute_move(p1, p2, move)
            score = p1.good_hands() - p2.good_hands()
            scored_moves.append((move, score))
    else:
        for move in moves_to_score:
            p1, p2 = copy(_p1), copy(_p2)
            execute_move(p1, p2, move)
            scored_move = minimax(p2, p1, depth - 1)
            if scored_move is not None:
                _, score = scored_move
                scored_moves.append((move, -score))
    return maximize(scored_moves)


class GoodPlayer(Player):
    def __init__(self, depth=4):
        super(GoodPlayer, self).__init__()
        self.depth = depth

    def select_move(self, opponent):
        move, score = minimax(self, opponent, self.depth)
        return move


class BadPlayer(Player):
    def select_move(self, opponent):
        return random.choice(valid_moves(self, opponent))


def valid_move(player, opponent, move):
    assert move[0] in 'lrs'
    assert move[1] in 'lr'
    assert len(move) in (2,3)
    if 's' in move:
        num=int(move[2])
        swapping_finger = player.left if move[1]=='l' else player.right
        swapped_to_fing = player.right if move[1]=='l' else player.left
        return (swapping_finger-num,swapped_to_fing+num-5) != (0,0) and swapping_finger-num>=0
    
    tapping_fingers = player.left if move[0] == 'l' else player.right
    tapped_fingers = opponent.left if move[1] == 'l' else opponent.right
    return tapping_fingers != 0 and tapped_fingers != 0


def valid_moves(player, opponent):
    return tuple(move for move in possible_moves if valid_move(player, opponent, move))


def execute_move(player, opponent, move,muted=True):
    """
    This is the only place we actually modify the players
    """
    assert move in possible_moves, "bad move '{}'".format(move)
    assert move in valid_moves(player, opponent), "{} - {} {}".format(player, opponent, move)
    if move == 'll':
        opponent.left += player.left
        if not muted:
            print("I tap David's left hand with my left.")
    elif move == 'lr':
        opponent.right += player.left
        if not muted:
            print("I tap David's right hand with my left.")
    elif move == 'rr':
        opponent.right += player.right
        if not muted:
            print("I tap David's right hand with my right.")
    elif move == 'rl':
        opponent.left += player.right
        if not muted:
            print("I tap David's left hand with my right.")
    elif move[:2] == 'sl':
        player.right += int(move[2])
        player.left -= int(move[2])
        if not muted:
            print("I swap",move[2],"from my left to my right.")
    elif move[:2] == 'sr':
        player.left += int(move[2])
        player.right -= int(move[2])
        if not muted:
            print("I swap",move[2],"from my right to my left.")
    opponent.left %= 5
    opponent.right %= 5


def convert_davids_to_mine(davids):
    mine = Player()
    mine.left = davids.hand_dict['left'] % 5
    mine.right = davids.hand_dict['right'] % 5
    return mine


def sync_to_davids(my_type, davids):
    davids.hand_dict['left'] = my_type.left if my_type.left != 0 else 5
    davids.hand_dict['right'] = my_type.right if my_type.right != 0 else 5
    davids.fix_hands()


def convert_to_davids(mine):
    davids = sticks_game.hands('David')
    davids.hand_dict['left'] = mine.left if mine.left != 0 else 5
    davids.hand_dict['right'] = mine.right if mine.right != 0 else 5
    davids.fix_hands()
    return davids


def sync_to_mine(davids_type, me):
    me.left = davids_type.hand_dict['left'] % 5
    me.right = davids_type.hand_dict['right'] % 5


def sim_1k():
    me_wins, dave_wins = (0,0)
    me_tot = []
    d_tot = []

    dep = int(input("Depth for Bob's AI: "))
    
    for i in range(10):
        me_wins, dave_wins = (0,0)
        for _ in range(100):
            me = GoodPlayer(depth=dep)
            david = sticks_game.med_AI('David')
            while True:
                david_as_my_type = convert_davids_to_mine(david)
                #print("me: {} v {} :david".format(me, david_as_my_type))
                if not me.alive():
                    #print("I lose!")
                    dave_wins+=1
                    break
                my_move = me.select_move(david_as_my_type)
                execute_move(me, david_as_my_type, my_move)
                #print("me: {} v {} :david".format(me, david_as_my_type))
                me.select_move(david_as_my_type)
                if not david_as_my_type.alive():
                    #print("I win!")
                    me_wins+=1
                    break
                sync_to_davids(david_as_my_type, david)
                me_as_davids_type = convert_to_davids(me)
                david.execute_best_action(me_as_davids_type)
                sync_to_mine(me_as_davids_type, me)

        print("I won",me_wins,"games. David won",dave_wins,"games.")
        me_tot.append(me_wins)
        d_tot.append(dave_wins)
        #input("Press enter to continue")

    print("Average wins for me:",mean(me_tot))
    print("Average wins for David:",mean(d_tot))
    print("Standard deviation:",std(me_tot))
    
    
def sim_100():
    me_wins, dave_wins = (0,0)
    dep = int(input("Depth for Bob's AI: "))
    for _ in range(100):
        me = GoodPlayer(depth=dep)
        david = sticks_game.med_AI('David')
        while True:
            # allow it to print non-minimax score
            david_as_my_type = convert_davids_to_mine(david)
            
            # print score
            print("me: {} v {} :david".format(me, david_as_my_type))
            
            # check if minimax player has lost
            if not me.alive():
                print("I lose!")
                dave_wins+=1
                break
            
            # minimax player's move
            my_move = me.select_move(david_as_my_type)
            execute_move(me, david_as_my_type, my_move)
            
            # print score
            print("me: {} v {} :david".format(me, david_as_my_type))
            
            # check if non-minimax player has lost
            if not david_as_my_type.alive():
                print("I win!")
                me_wins+=1
                break
                
            # non-minimax player's move
            sync_to_davids(david_as_my_type, david)
            me_as_davids_type = convert_to_davids(me)
            david.execute_best_action(me_as_davids_type)
            sync_to_mine(me_as_davids_type, me)

    print("I won",me_wins,"games. David won",dave_wins,"games.")

def sim_1():
    dep = int(input("Depth for Bob's AI: "))
    me = GoodPlayer(depth=dep)
    david = sticks_game.med_AI('David')
    while True:
        david_as_my_type = convert_davids_to_mine(david)
        print("me: {} v {} :david".format(me, david_as_my_type))
        if not me.alive():
            print("I lose!")
            #dave_wins+=1
            break
        my_move = me.select_move(david_as_my_type)
        execute_move(me, david_as_my_type, my_move,muted=False)
        print("me: {} v {} :david".format(me, david_as_my_type))
        me.select_move(david_as_my_type)
        if not david_as_my_type.alive():
            print("I win!")
            #me_wins+=1
            break
        sync_to_davids(david_as_my_type, david)
        me_as_davids_type = convert_to_davids(me)
        david.execute_best_action(me_as_davids_type)
        sync_to_mine(me_as_davids_type, me)

#sim = input("Sim how many (1,100,1000): ")
#if sim == '100':
#    sim_100()
#elif sim=='1000':
#    sim_1k()
#else:
#    sim_1()