# Author:       James Bush
# Date:         March 11, 2021
# Description:  Set of classes representing game of Janggi. JanggiGame class
#               controls game flow; Piece class sets common functionality for
#               individual piece classes, which are separate and contain rules
#               for each piece.

class JanggiGame:
    """
    Represent a JanggiGame object. Take no parameters and initialize private
    data members for _game_state, _board, _player_turn, and _in_check.
    """

    def __init__(self):
        """
        Initialize JanggiGame object with _game_state, _board, _player_turn,
        and _in_check private data members.
        """

        self._game_state = 'UNFINISHED' #UNFINISHED, RED_WON, BLUE_WON
        self._board = {}
        self._player_turn = 'BLUE'
        self._in_check = None #"RED", "BLUE"

        #initialize blank board
        cols = 'abcdefghi'
        for row in range(10):
            for col in range(len(cols)):
                self._board[cols[col]+str(row+1)] = 0

        #Red initial board placement
        self._board['a1'] = Chariot("RED",'a1')
        self._board['b1'] = Elephant("RED",'b1')
        self._board['c1'] = Horse("RED",'c1')
        self._board['d1'] = Guard("RED",'d1')
        self._board['f1'] = Guard("RED",'f1')
        self._board['g1'] = Elephant("RED",'g1')
        self._board['h1'] = Horse("RED",'h1')
        self._board['i1'] = Chariot("RED",'i1')
        self._board['e2'] = General('RED','e2')
        self._board['b3'] = Cannon('RED','b3')
        self._board['h3'] = Cannon('RED','h3')
        for pos in ['a4','c4','e4','g4','i4']:
            self._board[pos] = Soldier('RED',pos)

        #Blue initial board placement
        self._board['a10'] = Chariot("BLUE",'a10')
        self._board['b10'] = Elephant("BLUE",'b10')
        self._board['c10'] = Horse("BLUE",'c10')
        self._board['d10'] = Guard("BLUE",'d10')
        self._board['f10'] = Guard("BLUE",'f10')
        self._board['g10'] = Elephant("BLUE",'g10')
        self._board['h10'] = Horse("BLUE",'h10')
        self._board['i10'] = Chariot("BLUE",'i10')
        self._board['e9'] = General('BLUE','e9')
        self._board['b8'] = Cannon('BLUE','b8')
        self._board['h8'] = Cannon('BLUE','h8')
        for pos in ['a7','c7','e7','g7','i7']:
            self._board[pos] = Soldier('BLUE',pos)

    def get_board(self):
        """
        Return the current board. For testing.
        """

        return self._board

    def get_game_state(self):
        """
        Returns _game_state data member, i.e., 'UNFINISHED' or 'RED_WON' or
        'BLUE_WON'. Also used to prevent further moves through validation in
        make_move() method if game concluded.
        """

        return self._game_state

    def is_in_check(self, side):
        """
        Take a parameter (side) either 'RED' or 'BLUE' and return True if
        that player is in check, False otherwise.
        """

        if side.upper() == self._in_check:
            return True
        else:
            return False

    def get_piece(self, origin):
        """
        Take origin, return piece object from board.
        """
        return self._board[origin]

    def make_move(self, origin, destination):
        """
        Take two parameters - strings that represent the square to
        move from (origin) and the square to move to (destination). Determine if
        passed move is appropriate. Return True if move appropriate and record
        move, False if not.
        """

        #1) Check if there is a piece at the location
        #print("Attempted move from ",origin,"to ",destination)
        if self._board[origin] == 0:
            return False

        #2) Is it the moving side's turn?
        if self._player_turn != self._board[origin].get_side():
            return False

        #3) If there is a piece there and it is player's turn update position
        #...and update status of check
        self._board[origin].set_position(origin)
        self.check_check(origin, destination)

        #4) Is the move to the same location, i.e., a pass-move
        if origin == destination:
            if self._player_turn == "BLUE":
                self._player_turn = "RED"
                return True
            elif self._player_turn == "RED":
                self._player_turn = "BLUE"
                return True

        #5) Do the rules specific to the piece prohibit the move
        if self._board[origin].check_piece_rules(destination, self._board) == False:
            return False

        #6) Considering board state, is destination available (occupy/capture) to piece?
        if destination not in self._board[origin].check_available_moves(self._board).keys():
            return False

        #7) Is the piece attempting to move diagonally outside palace and not horse or elephant?
        if self._board[origin].check_diagonal(destination) == False:
            return False

        #8) Does the move put moving party in check (first eval)
        if self.check_check(origin, destination) == False:
            return False

        #9) Hypothetically record the move to ensure it doesn't cause check,
        #...take it back if it does and return false. Otherwise, record move
        else:
            saved_board = dict(self._board) #Save the board state
            self._board[destination] = self._board[origin] #Temporarily record the move
            self._board[origin] = 0

            if self.check_check(origin, destination) == False: #Does second eval of move trigger check?
                self._board = saved_board   #Restore the prior board state
                return False #Prohibit the move
            else: #Otherwise, record the move
                self._board = saved_board #Restore the saved board
                self._board[destination] = self._board[origin] #record the move
                self._board[origin] = 0
                self._board[destination].set_position(destination) #Update piece record

        #10) If the other party is now in check/mate, record that as well.
                opposing_general = [key for key, value in self._board.items() if type(value) == General and value.get_side() != self._board[destination].get_side()]
                opposing_general[0]
                if opposing_general[0] in self._board[destination].check_available_moves(self._board).keys():
                        self._in_check = self._board[opposing_general[0]].get_side() #Update status of in_check

        #11) Switch turns
                if self._player_turn == "BLUE":
                    self._player_turn = "RED"
                elif self._player_turn == "RED":
                    self._player_turn = "BLUE"
                return True

    def check_check(self, origin, destination):
        """
        Helper function to evaluate status of check for make_move(). Take
        origin and desination, return False if move prohibited due to check
        also evaluates checkmate and ends game if it occurs.
        """
        # Find the generals
        general_positions = [key for key, value in self._board.items() if type(value) == General]
        opposing_pieces = []

        # Is moving party currently in check and needs to escape
        for general in general_positions: #Locate generals on board
            if self._board[general].get_side() == self._player_turn: #Look at general of moving side
                moving_side_general = general

        #Scan at all other board positions
        for key, value in self._board.items():
            if value != 0 and value.get_side() != self._player_turn and type(value) not in {General, Guard}:  #If a pos is occupied by opposing side

                #Exclude pieces that are too far away so as to not blow up the computer
                if self._board[moving_side_general].get_side() == "BLUE":
                    if (key[-1] not in {"1", "2", "3"} or
                        type(self._board[key]) in {Chariot, Cannon}):
                        opposing_pieces.append(value)
                elif self._board[moving_side_general].get_side() == "RED":
                    if (
                        ( len(key) != 3 or (len(key) == 2 and key[-1] not in {"9", "8"}) ) or
                        (type(self._board[key]) in {Chariot, Cannon})
                        ):
                        opposing_pieces.append(value)

        for value in opposing_pieces: #Look at the pieces that could place the general in check
            #if moving moving_side_general's curent pos subject to capture
            if moving_side_general in value.check_available_moves(self._board).keys():
                self._in_check = self._board[moving_side_general].get_side() #Update status of in_check
                if len(self._board[moving_side_general].check_available_moves(self._board).keys()) == 0: #If no immediate available moves, CHECKMATE
                    if self._player_turn == 'RED':
                        self._game_state = "BLUE_WON"
                        return False
                    elif self._player_turn == 'BLUE':
                        self._game_state = "RED_WON"
                        return False
                #No moves to another position where general would be placed in check
                elif destination in value.check_available_moves(self._board).keys():
                    return False

###############################################################################
#Piece class
###############################################################################
class Piece:
    """
    Represent piece master class. Contains rules for permissible moves,
    data members for _side, _position, and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_position(self):
        """
        Return position of piece outside the class.
        """
        return self._position

    def set_position(self, position):
        """
        For setting position of piece outside the class. Used in move validation
        by JanggiGame.make_move().
        """
        self._position = position

    def get_side(self):
        """
        Return the value of the self._side data member. Used in move validation
        by JanggiGame.make_move().
        """
        return self._side

    def get_available_moves(self):
        """
        Return vlaue of the self._available_moves data member for use in move
        validation by JanggiGame.make_move().
        """
        return self._available_moves

    def check_diagonal(self, destination):
        """
        Take proposed destination position. Detect whether non-horse,
        non-elephant piece is attempting to move diagonally. Return True if
        proper move within palace, False otherwise.
        """

        #Diagonal moves - should only move diagonally within fortress, as permitted there
        if type(self) in {General, Guard}:
            if self._position not in {"e2","e9"}: #not moving from center of fortress, so anywhere else on board
                    if (self._position[0] != destination[0]) and (self._position[-1] != destination[-1]): #making a diagonal move
                        #not moving from outer corners to middle
                        if  ((self._position in {"d1","d2","d3","e1","e3","f1","f2","f3"} and destination != "e2") or
                            (self._position in {"d8","d9","d10","e8","e10","f8","f9","f10"} and destination != "e9")
                            ):
                            return False
                        else:
                            return True
                    else:
                        return True
            else:
                return True

        elif type(self) not in {General, Guard, Horse, Elephant}:
            #code cannon logic here
            if self._position[0] != destination[0] and self._position[-1] != destination[-1]:
                if self._position in {"e9"} and destination in {"d8","d9","d10","e8","e10","f8","f9","f10"}:
                    return True
                elif self._position in {"e2"} and destination in {"d1","d2","d3","e1","e3","f1","f2","f3"}:
                    return True
                elif self._position in {"d1","d2","d3","e1","e3","f1","f2","f3"} and destination == "e2":
                    return True
                elif self._position in {"d8","d9","d10","e8","e10","f8","f9","f10"} and destination == "e9":
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def check_available_moves(self, board):
        """
        Take board as dictionary of all board spaces with current piece layout.
        Compile dictinoary of board spaces that can be currently occupied or
        captured by piece.
        """
        self._available_moves = {} #Reset so it checks board each time anew
        for key, value in board.items(): #Looking at the main board
            if self.check_piece_rules(key, board) == True: #Meta-allowable by piece-specific rules
                if self.check_diagonal(key) == True: #allowable diagonal within fortress
                    if value == 0:  # Pos empty
                        self._available_moves[key] = value
                    elif value != 0: #Pos occupied
                        if value.get_side() != self._side:  #Opposing side piece / capture
                            self._available_moves[key] = value
        return self._available_moves

###############################################################################
# Specific Piece Classes
###############################################################################
class General(Piece):
    """
    Represent General piece. Contains rules for permissible moves, data members
    for _side and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'GN')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        GENERAL: Only one space per move and only within palace. May move
        diagonally according to board lines within palace. May not place itself
        in check.
        """
        # Move outside bounds of fortess for RED
        if (self._side == "RED" and
            (destination[0] not in ['d','e','f'] or
            int(destination[-1]) not in (1, 2, 3))
            ):
                return False
        # Move outside bounds of fortess for BLUE
        elif (self._side == "BLUE" and
            (destination[0] not in ['d','e','f'] or
            int(destination[-1]) not in (0, 8, 9))
            ):
                return False
        # Move would be >1 space along y-axis within fortress
        elif ((int(destination[-1]) != int(self._position[-1])) and
            (((int(destination[-1]) + int(self._position[-1])) %2 ) == 0)
            ):
                return False
        # Move would be >1 space along x-axis within fortress
        elif ((destination[0] == 'f' and self._position[0] == 'd') or
            (destination[0] == 'd' and self._position[0] == 'f')
            ):
                return False
        else:
            return True

class Guard(Piece):
    """
    Represent Guard piece. Contains rules for permissible moves, data members
    for _side and _available_moves.
    """
    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'GD')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        GUARD: Only one space per move and only within palace. May move
        diagonally according to board lines within palace. May not place General
        in check.
        """
        # Move outside bounds of fortess for RED
        if (self._side == "RED" and
            (destination[0] not in ['d','e','f'] or
            int(destination[-1]) not in (1, 2, 3))
            ):
                return False
        # Move outside bounds of fortess for BLUE
        elif (self._side == "BLUE" and
            (destination[0] not in ['d','e','f'] or
            int(destination[-1]) not in (0, 8, 9))
            ):
                return False
        # Move would be >1 space along y-axis within fortress
        elif ((int(destination[-1]) != int(self._position[-1])) and
            (((int(destination[-1]) + int(self._position[-1])) %2 ) == 0)
            ):
                return False
        # Move would be >1 space along x-axis within fortress
        elif ((destination[0] == 'f' and self._position[0] == 'd') or
            (destination[0] == 'd' and self._position[0] == 'f')
            ):
                return False
        #If move within fortress and <1 space in any direction
        else:
            return True


class Horse(Piece):
    """
    Represent Horse piece.  Contains rules for permissible moves, data members
    for _side and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'HO')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        HORSE: one step orthogonally then one step diagonally outward, with no
        jumping). A horse can be transposed with an adjacent elephant in the initial
        setup.
        """

        #Columns for indexing, algorithm for analyzing available moves, positions
        cols = 'abcdefghi'
        move_dict = {-19:[-9], -17:[-9], -11:[-1], -7:[1], 7:[-1], 11:[1], 17:[9], 19:[9]}
        pos_list = [[key, value] for key, value in board.items()]

        #Find index of origin position in index
        for i in range(len(pos_list)):
            if self._position == pos_list[i][0]:
                origin_index = i

        #Try each move in move algorithm
        for key, value in move_dict.items():
            move = origin_index + key
            if (move) in range(0,90): #Move is on the board, but possibly outside 2-space radius fence

                #are cols > 2 away in any direction?
                for i in range(len(cols)):
                    if cols[i] == pos_list[move][0][0]:
                        move_col_index = i
                    if cols[i] == self._position[0]:
                        origin_col_index = i
                if  (((origin_col_index - move_col_index) > 2) or
                    ((move_col_index - origin_col_index) > 2)):
                    if destination == pos_list[move][0]:
                        return False

                #are rows > 2 away in any direction?
                elif len(pos_list[move][0]) == 2 and len(self._position) == 2: #moves < row 10
                    if  (((int(pos_list[move][0][-1]) - int(self._position[-1])) > 2) or
                        ((int(self._position[-1]) - int(pos_list[move][0][-1])) > 2)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]:  #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0: #clear en route?
                                return True
                            else:
                                return False

                #Length of destination string is 3
                elif len(pos_list[move][0]) == 3 and len(self._position) == 2: #moves == row 10
                    if  (((int(pos_list[move][0][-2:]) - int(self._position[-1])) > 2) or
                        ((int(self._position[-1]) - int(pos_list[move][0][-2:])) > 2)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]:  #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0: #clear en route?
                                return True
                            else:
                                return False

                #Length of origin string is 3
                elif len(pos_list[move][0]) == 2 and len(self._position) == 3: #moves == row 10
                    if  (((int(pos_list[move][0][-1]) - int(self._position[-2:])) > 2) or
                        ((int(self._position[-2:]) - int(pos_list[move][0][-1])) > 2)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]: #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0:  #clear en route?
                                return True
                            else:
                                return False
                else: #not on board
                    return False

class Elephant(Piece):
    """
    Represent Elephant piece.  Contains rules for permissible moves, data members
    for _side and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'EL')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        ELEPHANT: move one point orthogonally followed by two points diagonally
        away from their starting point, ending on the opposite corner of a 2×3
        rectangle. Like the horse, the elephant is blocked from moving by any
        intervening pieces.
        """
        #Columns for indexing, algorithm for analyzing available moves, positions
        cols = 'abcdefghi'
        move_dict = {   -15:[-7,1], -21:[-11,-1], -25:[-17,-9], -29:[-19,-9],
                        15:[7,-1], 21:[11,1], 25:[17,9], 29:[19,9]
                    }
        pos_list = [[key, value] for key, value in board.items()] #indexed list of positions

        #Find index of origin position in index
        for i in range(len(pos_list)):
            if self._position == pos_list[i][0]:
                origin_index = i

        #Try each move in move algorithm
        for key, value in move_dict.items():
            move = origin_index + key
            if (move) in range(0,90): #Move is on the board, but possibly outside 3-space radius fence

                #are cols > 3 away in any direction?
                for i in range(len(cols)):
                    if cols[i] == pos_list[move][0][0]:
                        move_col_index = i
                    if cols[i] == self._position[0]:
                        origin_col_index = i
                if  (((origin_col_index - move_col_index) > 3) or
                    ((move_col_index - origin_col_index) > 3)):
                    if destination == pos_list[move][0]:
                        return False

                #are rows > 3 away in any direction?
                elif len(pos_list[move][0]) == 2 and len(self._position) == 2: #moves < row 10
                    if  (((int(pos_list[move][0][-1]) - int(self._position[-1])) > 3) or
                        ((int(self._position[-1]) - int(pos_list[move][0][-1])) > 3)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]:  #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0: #clear en route?
                                if board[pos_list[origin_index+value[1]][0]] == 0: #clear en route?
                                    return True
                            else:
                                return False

                #Length of destination string is 3
                elif len(pos_list[move][0]) == 3 and len(self._position) == 2: #moves == row 10
                    if  (((int(pos_list[move][0][-2:]) - int(self._position[-1])) > 3) or
                        ((int(self._position[-1]) - int(pos_list[move][0][-2:])) > 3)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]:  #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0: #clear en route?
                                if board[pos_list[origin_index+value[1]][0]] == 0: #clear en route?
                                    return True
                            else:
                                return False

                #Length of origin string is 3
                elif len(pos_list[move][0]) == 2 and len(self._position) == 3: #moves == row 10
                    if  (((int(pos_list[move][0][-1]) - int(self._position[-2:])) > 3) or
                        ((int(self._position[-2:]) - int(pos_list[move][0][-1])) > 3)):
                        if destination == pos_list[move][0]:
                            return False
                    else:
                        if destination == pos_list[move][0]: #destination within fence
                            if board[pos_list[origin_index+value[0]][0]] == 0:  #clear en route?
                                if board[pos_list[origin_index+value[1]][0]] == 0: #clear en route?
                                    return True
                            else:
                                return False
                else: #not on board
                    return False

class Chariot(Piece):
    """
    Represent Chariot piece.  Contains rules for permissible moves, data members
    for _side and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'CH')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        CHARIOT: moves and captures in a straight line either horizontally or
        vertically. Additionally, the chariot may move along the diagonal lines
        inside either palace, but only in a straight line.
        """
        ##Can move in as many spaces orthogonally as long as not blocked
        if destination[0] != self._position[0] and destination[-1] != self._position[-1]: #not orthogonal move
            return False

        #Is orthogonal in direction, is destination clear en route?

        #Moving right/increasing on row axis - this appears to be working
        if destination[0] > self._position[0]:
            cols = 'abcdefghi'
            for i in range(len(cols)):
                if len(destination) == 3: #moving along row 10
                    pos = (cols[i]+destination[-2:]) #construct position string
                elif len(destination) == 2:
                    pos = (cols[i]+destination[-1]) #construct position string
                if pos[0] > self._position[0] and cols[i] <= destination[0]:
                    if board[pos] != 0:
                        if board[pos] == board[destination]: #If the position is where we are heading
                            if board[destination].get_side() == self._side:
                                return False
                            else:
                                return True
                        else:
                            return False
            return True

        #Moving left/decreasing on row axis
        elif destination[0] < self._position[0]:
            cols = 'abcdefghi'
            cols = cols[::-1] #reverse the string, since going right to left
            for i in range(len(cols)):
                if len(destination) == 3: #moving along row 10
                    pos = (cols[i]+destination[-2:]) #construct position string
                elif len(destination) == 2:
                    pos = (cols[i]+destination[-1]) #construct position string
                if pos[0] < self._position[0] and cols[i] >= destination[0]:
                    if board[pos] != 0:
                        if board[pos] == board[destination]: #If the position is where we are heading
                            if board[destination].get_side() == self._side:
                                return False
                            else:
                                return True
                        else:
                            return False
            return True

        # Moving down/increasing on column axis
        elif ((destination[-1] > self._position[-1] and len(destination) != 3 and len(self._position) != 3) or (len(destination) == 3 and len(self._position) == 2)):
            if len(destination) == 3:
                for i in range (10 - int(self._position[-1])): #When dest is row 10 - difference of spaces between origin and destination
                    pos = (self._position[0]+str((i+1) + int(self._position[-1]))) #Construct position string
                    if board[pos] != 0: #if occupied
                        if board[pos] == board[destination]: #If the position is where we are heading
                            return True
                        else: #Intermediate position blocked
                            return False
                return True
            else:
                for i in range (int(destination[-1]) - int(self._position[-1])): # Dest is not row 10 - difference of spaces between origin and destination
                    pos = (self._position[0]+str((i+1) + int(self._position[-1]))) #Construct position string
                    if board[pos] != 0:
                        if board[pos] == board[destination]: #If the position is where we are heading
                            return True
                        else: #Intermediate position blocked
                            return False
                return True

        # Moving up/decreasing on column axis
        elif ((destination[-1] < self._position[-1] and len(destination) != 3 and len(self._position) != 3) or (len(destination) == 2 and len(self._position) == 3)):
            if len(self._position) == 3:
                for i in range (10 - int(destination[-1])): #When origin is row 10 - difference of spaces between origin and destination
                    pos = (self._position[0]+str( int(self._position[-2:]) - (i+1) )) #Construct position string
                    if board[pos] != 0: #if occupied
                        if board[pos] == board[destination]: #If the position is where we are heading
                            return True
                        else:
                            return False
                return True
            else:
                for i in range (int(self._position[-1]) - int(destination[-1])): #difference of spaces between origin and destination
                    pos = (self._position[0]+str(int(self._position[-1])-(i+1)))
                    #print(pos)
                    if board[pos] != 0:
                        if board[pos] == board[destination]:
                            return True
                        else:
                            return False
                return True
        else:
            return True

class Cannon(Piece):
    """
    Represent Cannon piece. Contains rules for permissible moves, data members
    for _side and _available_moves.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'CN')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.

        CANNON: Moves by jumping another piece horizontally or vertically.
        The jump can be performed over any distance provided that there is exactly
        one piece anywhere between the original position and the target. In order to
        capture a piece, there must be exactly one piece (friendly or otherwise)
        between the cannon and the piece to be captured. The cannon then moves to
        that point and captures the piece. They may also move or capture diagonally
        along the diagonal lines in either palace, provided there is an intervening
        piece in the centre (i.e. it can only happen if the cannon is at a corner of
        the palace).
        """
        #Set up list of positions
        pos_list = [[key, value] for key, value in board.items()] #indexed list of positions
        for i in range(len(pos_list)): #find index of origin position in index
            if self._position == pos_list[i][0]:
                origin_index = i

        #Create list of moves down y-axis
        below_list = []
        below = origin_index + 9
        while below < len(pos_list):
            below_list.append(below)
            below += 9
        below_list.sort()

        #Create list of moves up y-axis
        above_list = []
        above = origin_index - 9
        while above > 0:
            above_list.append(above)
            above -= 9
        above_list.sort(reverse=True)

        #Create list of moves left on x-axis
        left_list = []
        left = (origin_index % 9) #e.g., will be 4 when orig is 50
        while left > -1  : #the origin % 9 will give you how many spaces from left it is
            if left != 0:
                left_list.append(origin_index - left)
            left -= 1
        left_list.sort(reverse=True)

        #Create list of moves left on x-axis
        right_list = []
        right = (9 - (origin_index% 9)) #e.g., will be 7 when oi is 20
        while right > 0  : #the origin % 9 will give you how many spaces from left it is
            if right != 0:
                right_list.append(origin_index + right)
            right -= 1
        right_list.sort()

        mega_cannon_move_list = [above_list, below_list, left_list, right_list]
        for list in mega_cannon_move_list:
            intermediate_count = 0
            for i in list:
                if pos_list[i][1] != 0 and pos_list[i][0] != destination: #there is something there, but not yet at destination
                    intermediate_count += 1
                elif pos_list[i][0] == destination and intermediate_count == 1:
                    return True
                elif intermediate_count > 1 or (pos_list[i][0] == destination and intermediate_count == 0):
                    return False

class Soldier(Piece):
    """
    Represent Soldier piece.  Contains rules for permissible moves, data members
    for _side and _available_moves.

    SOLDIER: move and capture one point either straight forward or sideways
    (unlike xiangqi, where soldiers must cross the "river" to be able to move
    sideways.) There is no promotion; once they reach the end of the board they
    may only move sideways. Soldiers may also move one point diagonally forward
    when within the enemy palace.
    """

    def __init__(self, side, position):
        """
        Initalize piece with private data members _side, _position, and
        _available_moves.
        """
        Piece.__init__(self, side, position)
        self._side = side
        self._position = position
        self._available_moves = {}

    def get_token(self):
        """Testing: Tokens for printing board"""
        return (self._side[0].lower()+'SO')

    def check_piece_rules(self, destination, board):
        """
        Take destination, which is a string of algebraic notation of intended
        move. Check rules specific to piece. Return True if move allowable,
        False if not.
        """

        cols = 'abcdefghi'

        #No moves to own-side position - not really sure why this is here
        if board[destination] != 0 and board[destination].get_side() == self._side:
            return False

        #Both on row 10
        elif len(self._position) == 3:
            if len(destination) == 3: #both on row 10
                for i in range(len(cols)-1): #going right up to last col
                    if (board[destination] != 0 and board[destination].get_side() != self._position) or board[destination] == 0:
                        if cols[i] == self._position[0] and cols[i+1] == destination[0]:  #dest is 1 to right of position
                            return True
                        elif cols[i] == destination[0] and cols[i+1] == self._position[0]: #dest is 1 to left of position
                            return True
            elif destination[0] == self._position[0]: #same column
                if destination[1] == '9':
                    if (board[destination] != 0 and board[destination].get_side() != self._position) or board[destination] == 0:
                        return True

        elif len(self._position) == 2:

            if board[self._position].get_side() == 'BLUE':
                if int(self._position[-1]) == int(destination[-1])+1 and len(destination) != 3: # dest is one row above
                    return True

            elif board[self._position].get_side() == 'RED':
                if int(self._position[-1]) == (int(destination[-1])-1):  # dest is one row below
                    return True

            for i in range(len(cols)-1): #going right up to last col
                if (board[destination] != 0 and board[destination].get_side() != self._position) or board[destination] == 0:
                    if cols[i] == self._position[0] and cols[i+1] == destination[0]:  #dest is 1 to right of position
                        return True
                    elif cols[i] == destination[0] and cols[i+1] == self._position[0]: #dest is 1 to left of position
                        return True
