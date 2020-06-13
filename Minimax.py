#!/usr/bin/python3

import random
from Board import Board
from copy import deepcopy

class Minimax():
    """ Minimax nimmt einen Zustand eines Vier Gewinnt Spielbretts """
    
    def __init__(self, gameboard):
        self.gameboard = gameboard
        self.players = [-1, 1]
            
    def bestMove(self, depth, curr_player):
        """ Gibt den besten Spielzug als eine Zahl aus {0, ..., 6} 
            Args:
                depth:[int] gibt die Tiefe der Suche an
                curr_player:[int] gibt den aktuellen Spieler fest
        """
        
        # Festlegen des Gegenspielers
        if curr_player == self.players[0]:
            opp_player = self.players[1]
        else:
            opp_player = self.players[0]
        
        # legt den Zusammenhang zwischen Gamboard und Alpha Wert
        legal_moves = {} 

        # gehe durch alle möglichen Spielzüge durch
        for col in self.gameboard.selectableColumns():

            # kopiere das aktuelle Spielbrett 
            temp = deepcopy(self.gameboard)

            # werfe einen chip ein
            temp.enterPiece(curr_player, col)

            # füge diesen Spielzug mit alpha Wert hinzu
            legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        # legt den niedrigsten wert fest, eigentlich minus unendlich
        best_alpha = -99999999

        best_move = None
        
        # hole alle möglichen moves, also maximal 7, in eine Liste
        moves = legal_moves.items()

        # durchmische die Liste der möglichen moves
        random.shuffle(list(moves))

        # gehe durch alle moves und ihrer zugehörigen Güte 
        for move, alpha in moves:

            # suche nach dem Spielzug mit dem größten alpha
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move
        
    def search(self, depth, gameboard, curr_player):
        """ 
            gibt den alpha wert zurück.
            Args:
                depth:[int] gibt die Tiefe der Suche an
                gameboard:[Board] gibt ein Spielbrett an
                curr_player:[int] gibt den aktuellen Spieler fest
        """

        # lege alle möglichen moves fest und speichere die zugehörigen Spielbretter
        legal_moves = []
        for col in gameboard.selectableColumns():
            # führe einen Spielzug für den aktuellen Spieler durch
            temp = gameboard
            temp.enterPiece(curr_player, col)
            legal_moves.append(temp)
        
        # gebe
        if depth == 0 or gameboard.checkForWinner() or gameboard.checkForDraw():
            # return the heuristic value of node
            return self.value(gameboard, curr_player)       
        
        # determine opponent's color
        if curr_player == self.players[0]:
            opp_player = self.players[1]
        else:
            opp_player = self.players[0]

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
        if color == self.players[0]:
            o_color = self.players[1]
        else:
            o_color = self.players[0]
        
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
            

