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
        
        # gebe die Güte des Spielbrett zurück
        if depth == 0 or gameboard.checkForWinner() or gameboard.checkForDraw():
            # gebe den Wert des Spielbrettes zurück
            return self.value(gameboard, curr_player)       
        
        # Festlegen des Gegenspielers
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
    

    def value(self, gameboard, player):
        """ Einfache Heuristik um ein Spielbrett auf Güte zu bewerten
            Args:
                gameboard[Board] : Das Spielbrett das untersucht wird

            Returns:
                (num of 4-in-a-rows) * 1000 
                + (num of 3-in-a-rows) * 10 
                + (num of 2-in-a-rows)
                - (num of opponent 4-in-a-rows) * 10000
        """
        # Festlegen des Gegenspielers
        if player == self.players[0]:
            o_player = self.players[1]
        else:
            o_player = self.players[0]
        
        # Berechne die Reihen in dem Spielbrett
        my_fours = gameboard.checkForStreak(player, 4)
        my_threes = gameboard.checkForStreak(player, 3)
        my_twos = gameboard.checkForStreak(player, 2)
        opp_fours = gameboard.checkForStreak(o_player, 4)

        return my_fours*1000 + my_threes*10 + my_twos - opp_fours*10000
            