#!/usr/bin/python3

import random
from Board import Board

class Minimax():
    """ Minimax nimmt einen Zustand eines Vier Gewinnt Spielbretts """
    
    def __init__(self, gameboard):
        self.gameboard = gameboard
        self.player = [-1, 1]
            
    def bestMove(self, depth, curr_player):
        """ Gibt den besten Spielzug als eine Zahl aus {0, ..., 6} """
        
        # Festlegen des Gegenspielers
        if curr_player == self.player[0]:
            opp_player = self.player[1]
        else:
            opp_player = self.player[0]
        
        # legt den Zusammenhang zwischen Gamboard und Alpha Wert
        legal_moves = {} 
        for col in self.gameboard.selectableColumns():
            # make the move in column 'col' for curr_player
            temp = Board()
            temp = self.gameboard
            temp.enterPiece(curr_player, col)
            # Füge Spielzug an der Stelle col hinzu
            legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        print(len(legal_moves))
        # legt den niedrigsten wert fest
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move
        
    def search(self, depth, gameboard, curr_player):
        """ 
            gibt den alpha wert zurück
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for col in gameboard.selectableColumns():
            # make the move in column i for curr_player
            temp = Board()
            temp = gameboard
            temp.enterPiece(curr_player, col)
            legal_moves.append(temp)
        
        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or gameboard.checkForWinner() or gameboard.checkForDraw():
            # return the heuristic value of node
            return self.value(gameboard, curr_player)       
        
        # determine opponent's color
        if curr_player == self.player[0]:
            opp_player = self.player[1]
        else:
            opp_player = self.player[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha
    

    def value(self, gameboard, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.player[0]:
            o_color = self.player[1]
        else:
            o_color = self.player[0]
        
        my_fours = gameboard.checkForStreak(color, 4)
        my_threes = gameboard.checkForStreak(color, 3)
        my_twos = gameboard.checkForStreak(color, 2)
        opp_fours = gameboard.checkForStreak(o_color, 4)
        #opp_threes = self.checkForStreak(state, o_color, 3)
        #opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos
            

