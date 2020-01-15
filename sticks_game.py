from random import randint, choice

class hands:
    def __init__(self,name):
        self.name=name
        self.lost = False
        self.hand_dict = {'left':1,'right':1}
        
    def __repr__(self):
        return '{} on the right hand, {} on the left.'.format(self.hand_dict['right'],self.hand_dict['left'])
    
    def tap(self,opp,your_hand,their_hand):
        opp.hand_dict[their_hand] += self.hand_dict[your_hand]
        return 0
    
    def swap(self,side,number,muted=True):
        if side == 'right':
            if (self.hand_dict['left']+number!=5) and (self.hand_dict['right']-number>=0):
                self.hand_dict['left'] += number
                self.hand_dict['right'] -= number
                return 0

            if not muted:
                print("You can't swap that many sticks from that hand.")
            return 1
        elif side == 'left':
            if (self.hand_dict['right']+number!=5) and (self.hand_dict['left']-number>=0):
                self.hand_dict['right'] += number
                self.hand_dict['left'] -= number
                return 0
            
            if not muted:
                print("You can't swap that many sticks from that hand.")
            return 1
        if not muted:
            print("something went wrong with the swap command")
        return 0
    
    def fix_hands(self):
        self.hand_dict['right'] %= 5
        self.hand_dict['left'] %= 5
        if not (self.hand_dict['right'] or self.hand_dict['left']):
            self.lost = True
    
    def act(self,opp,muted=True):
        actions = [self.swap,self.tap]
        hands = ['left','right']
        failed = True
        while failed:
            action = choice(actions)
            hand = choice(hands)
            if action == self.swap:
                if self.hand_dict[hand]==0:
                    continue
                num = randint(1,self.hand_dict[hand])
                failed = action(hand,num,muted=True)
                continue
            if self.hand_dict[hand] == 0:
                continue
            opp_hand = choice(hands)
            failed = action(opp,hand,opp_hand)
        if action == self.swap and not muted:
            print(self.name,'swaps',num,'from their',hand,'hand.')
        elif not muted:
            print(self.name,'taps your',opp_hand,'hand with their',hand+'.')
    
    def forfeit(self):
        self.lost = True
          
            
class braindead_AI(hands):
    def execute_best_action(self,opp,muted):
        self.act(opp,muted=False)
        
class easy_AI(hands):
    def choose_action(self,opp):
        myleft = self.hand_dict['left']
        myright = self.hand_dict['right']
        opleft = opp.hand_dict['left']
        opright = opp.hand_dict['right']
        for hand1 in self.hand_dict:
            for hand2 in opp.hand_dict:
                if self.hand_dict[hand1]+opp.hand_dict[hand2] == 5:
                    action = self.tap
                    return self.tap, hand1, hand2
        if (myleft!=myright) and (myleft+myright)%2 == 0:
            if myleft > myright:
                hand = 'left'
            else:
                hand = 'right'
            return self.swap, hand, abs(myleft-myright)//2
        else:
            return self.act, 0, 0
    
    def execute_best_action(self,opp,muted=True):
        best_action, arg1, arg2 = self.choose_action(opp)
        if best_action == self.tap:
            self.tap(opp,arg1,arg2)
            if not muted:
                print(self.name,'taps your '+arg2+' hand with their '+arg1+'.')
        elif best_action == self.swap:
            self.swap(arg1,arg2,muted=True)
            if not muted:
                print(self.name,'swaps',arg2,'from their',arg1,'hand.')
        elif best_action == self.forfeit:
            self.forfeit()
        else:
            self.act(opp)
            
class med_AI(hands):
    def choose_action(self,opp):
        myleft = self.hand_dict['left']
        myright = self.hand_dict['right']
        opleft = opp.hand_dict['left']
        opright = opp.hand_dict['right']
        
        # opponent conditions
        oleft_oright_eq = opleft==opright
        
        # AI conditions
        AI_has_zero = (0 in (myleft,myright))
        AI_has_one = (1 in (myleft,myright))
        AI_can_equalize = (myleft+myright)%2==0
        
        # check for possibility of elimination
        for hand1 in self.hand_dict:
            for hand2 in opp.hand_dict:
                # condition: elimination is possible
                if self.hand_dict[hand1]+opp.hand_dict[hand2]==5:
                    
                    if oleft_oright_eq and AI_has_zero:
                        if AI_has_one:
                            return self.forfeit, 0, 0
                        return self.swap, hand1, randint(1, self.hand_dict[hand1]-1)
                        
                    
                    return self.tap, hand1, hand2
        if AI_can_equalize and (myleft!=myright):
            
            if oleft_oright_eq and (myleft+myright)//2+opleft==5:
                if myleft>myright:
                    return self.swap, 'left', randint(1,self.hand_dict['left']-1)
                return self.swap, 'right', randint(1,self.hand_dict['right']-1)
            
            if myleft>myright:
                return self.swap, 'left', (myleft-myright)//2
            return self.swap, 'right', (myright-myleft)//2
        else:
            return self.act, 0, 0
        
    def execute_best_action(self,opp,muted=True):
        best_action, arg1, arg2 = self.choose_action(opp)
        if best_action == self.forfeit:
            self.forfeit()
            if not muted:
                print(self.name,"forfeits.")
        elif best_action == self.tap:
            self.tap(opp,arg1,arg2)
            if not muted:
                print(self.name,'taps your '+arg2+' hand with their '+arg1+'.')
        elif best_action == self.swap:
            self.swap(arg1,arg2)
            if not muted:
                print(self.name,'swaps',arg2,'from their',arg1,'hand.')
        else:
            self.act(opp)