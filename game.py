from random import randint
from time import sleep, time
from copy import deepcopy

class MinMaxGame:
    value = 0
    num_plus = 4
    num_minus = 6
    computermode = -1
    total=num_plus+num_minus
    min_player_curr_decision = -1
    max_player_val_list=list()
    def __init__(self):
        pass

    def min_player_decision(self, num):
        if num == 0 and self.num_minus:
            self.min_player_curr_decision = 0
            self.num_minus-=1
            return 0
        elif num == 1 and self.num_plus:
            self.min_player_curr_decision = 1
            self.num_plus-=1
            return 0
        else:
            return 1
    def max_player(self,num):
        if (type(num) == int and (num>=0 and num<=1000)):
            self.max_player_val_list.append(num)
            return 0
        else:
            return 1
        
    def compute(self):
        min_decision = 1
        if self.min_player_curr_decision == 0:
            min_decision = -1
        self.value+=self.max_player_val_list[-1]*min_decision
        self.total = self.num_minus + self.num_plus

    def show_state(self):
        print()
        print("=======CURRENT STATE==========")
        print("current_value:",self.value)
        print("minus_left:",self.num_minus)
        print("plus_left:",self.num_plus)
        print("inputs_left:",self.num_plus+self.num_minus)
        print("num_list:", self.max_player_val_list)
        print("==============   ================")

    def show_final_score(self):
        print("~~~~~~~~~~~~~~FINAL SCORE~~~~~~~~~~~~~")
        print(self.value)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def play_game(self):
        while self.total != 0:
            self.show_state()
            self.max_player(int(input("MAXIMIZING DECISION:")))
            self.min_player_decision(int(input("MINIMIZING DECISION:")))
            self.compute()
            print("\n")

    def random_game(self):
        while self.total != 0:
            list1 = [0]*self.num_minus
            list1.extend([1]*self.num_plus)
            self.show_state()
            self.max_player(randint(0, 1000))
            self.min_player_decision(list1.pop(randint(0, len(list1)-1)))
            self.compute()
            print("\n")
            sleep(4)   

    def computer_game(self, mode):
        if not mode: # computer as minimiser
            computer_depth = 8
            while self.total != 0:
                starttime = time()
                self.show_state()
                self.max_player(int(input("MAXIMIZING DECISION:")))
                bestMove = self.minimax(computer_depth, computer_depth, False)[0]
                timetaken = time() - starttime
                print(f"MINIMIZER DECISION: {bestMove}")
                self.min_player_decision(bestMove)
                self.compute()
                print("Time taken by computer:")
                print("\n")
            self.show_final_score()
        else: # computer as maximiser
            computer_depth = 10
            while self.total != 0:
                starttime = time()
                self.show_state()
                bestMove = self.minimax(computer_depth, computer_depth, True)[0]
                timetaken = time() - starttime
                print(f"MAXIMIZING DECISION: {bestMove}")
                self.max_player(bestMove)
                human = int(input("MINIMIZER DECISION: "))
                self.min_player_decision(human)
                self.compute()
                print("Time taken by computer:", timetaken)
                print("\n")
            self.show_final_score()

    def evaluate(self):
        plus_prob = self.num_plus/max(1/1000000, self.total)
        if plus_prob == 1:
            if self.value < -1*self.num_plus*1000:
                return -100000
            else:
                return 100000
        eval = 10*plus_prob + self.value/1000
        return eval

    def minimax(self, og_depth, depth, turn):
        if depth == 0 or self.total == 0:
            return self.evaluate()
        if turn:
            hash_size = 100
            bestEval = -100000
            bestMove = 0
            for x in range(0, 1001, hash_size):
                state = deepcopy(self.storeState())
                self.max_player(x)
                val = self.minimax(og_depth, depth-1, False)
                if val>bestEval:
                    bestEval = val
                    bestMove = x
                self.restoreState(state)
        else:
            state = deepcopy(self.storeState())
            self.min_player_decision(0)
            self.compute()
            val0 = self.minimax(og_depth, depth-1, True)
            self.restoreState(state)
            if self.num_minus>0 and self.num_plus==0:
                    bestMove = 0
                    bestEval = val0
            else:
                state = deepcopy(self.storeState())
                self.min_player_decision(1)
                self.compute()
                val1 = self.minimax(og_depth, depth-1, True)
                self.restoreState(state)
                if self.num_minus==0:
                    bestMove=1
                    bestEval = val1
                else:
                    if val1<val0:    
                        bestMove = 1
                        bestEval = val1
                    else:
                        bestMove=0
                        bestEval=val0
        if depth == og_depth:
            return bestMove, bestEval
        else:
            return bestEval



    def storeState(self):
        state = []
        state.append(self.value)
        state.append(self.num_plus)
        state.append(self.num_minus)
        state.append(self.computermode)
        state.append(self.total)
        state.append(self.min_player_curr_decision)
        state.append(self.max_player_val_list)
        return state
    def restoreState(self, stored_state):
        self.value = stored_state[0]
        self.num_plus = stored_state[1]
        self.num_minus = stored_state[2]
        self.num_computermode = stored_state[3]
        self.total = stored_state[4]
        self.min_player_curr_decision = stored_state[5]
        self.max_player_val_list = stored_state[6]



game = MinMaxGame()
game.computer_game(False)

