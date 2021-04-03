import JanggiGame as jg
import print_board as pb


################################################################################
#TESTS
def try_a_bunch_of_moves(game):
    #moves = ['f8','e8','c8','f9','e9','d9','f10','e10','d10']#Blue gen/guard
    moves = ['f1','e1','d1','f2','e2','d2','f3','e3','d3'] #Red gen/guard
    for i in moves:
        game.make_move('e2',i)
        print("red in check:",game.is_in_check('red'))
        print("blue in check:",game.is_in_check('blue'))
        print(game.get_game_state())
        print()


def check_all_available_moves(the_board):
    for key,value in the_board.items():
        if value != 0:
            i = game.get_piece(key)
            print("available moves for",i.get_position(),i.get_token(), i.check_available_moves(the_board))
            print()

game = jg.JanggiGame()
board = game.get_board()
pb.print_board(board)
#check_all_available_moves(board)
#game.make_move('e2','f1')
#pb.print_board(board)
#check_all_available_moves(board)

def test_1():
    print(game.make_move('c1', 'e3')) #should be FALSE because it's not Red's turn #PASSED
    print()
    print(game.make_move('a7','b7')) #should return TRUE #PASSED
    #print()
    print(game.is_in_check('blue')) #should return FALSE #PASSED
    #print()
    print(game.make_move('a4', 'a5')) #should return TRUE #PASSED
    #print()
    print(game.get_game_state()) #should return UNFINISHED #PASSED
    #print()
    print(game.make_move('b7','b6')) #should return TRUE    #PASSED
    #print()
    print(game.make_move('b3','b6')) #should return FALSE because it's an invalid move #PASSED
    #print()
    print(game.make_move('a1','a4')) #should return TRUE #PASSED
    #print()
    print(game.make_move('c7','d7')) #should return TRUE #PASSED
    #print()
    print(game.make_move('a4','a4')) #this will pass the Red's turn and return TRUE #PASSED
    #print()
    ######MY ADDITIONAL TESTS
    print(game.make_move('e9','e8')) #blue general up one should return TRUE

    print(game.make_move('e2','f3')) #red general up one should return TRUE

    print(game.make_move('i10','i9')) #blue chariot up one should return TRUE

    print(game.make_move('f1','e2')) #red guard to center up one should return TRUE

    print(game.make_move('i9','f9')) #blue chariot left to CHECK red gen return TRUE

    print("Blue in check:",game.is_in_check('blue'))
    print("Red in check:",game.is_in_check('red')) #SHOULD BE TRUE

    print(game.make_move('e4','e5')) #red sol to down one should return TRUE

    print(game.make_move('f9','f6')) #blue chariot left to CHECK red gen return TRUE

    print("Red in check:",game.is_in_check('red')) #SHOULD BE TRUE


def test_2():
    print(game.make_move('a7','b7'))
    print(game.make_move('a4','a5'))
    print(game.make_move('b8','b4'))


def test_3():
    print(game.make_move('c7','c6'))
    print(game.make_move('a4','a5'))
    print(game.make_move('a7','b7'))
    print(game.make_move('a5','a6'))
    print(game.make_move('b8','b6'))
    print(game.make_move('a6','a7'))
    print(game.make_move('b6','e6'))

def test_4():
    print(game.make_move('c7','c6'))
    print(game.make_move('c1','d3'))
    print(game.make_move('b10','d7'))
    print(game.make_move('b3','e3'))
    print(game.make_move('c10','d8'))
    print(game.make_move('h1','g3'))
    print(game.make_move('e7','e6'))
    print(game.make_move('e3','e6'))
    print(game.make_move('h8','c8'))
    print(game.make_move('d3','e5'))
    print(game.make_move('c8','c4'))
    print(game.make_move('e5','c4'))
    print(game.make_move('i10','i8'))
    print(game.make_move('g4','f4'))
    print(game.make_move('i8','f8'))
    print(game.make_move('g3','h5'))
    print(game.make_move('h10','g8'))
    print(game.make_move('e6','e3'))

    board = game.get_board()

    print("Blue in check:",game.is_in_check('blue'))
    e3 = game.get_piece('e3')
    print(e3.get_token(),e3.check_available_moves(board))
    print("Blue in check:",game.is_in_check('blue'))
    #for key,value in board.items():
        #print(key,value)

    #print(game.make_move('f8','f9'))
    #print(game.make_move('e3','e8'))
    #print(e3.get_available_moves())


test_4()

board = game.get_board()
pb.print_board(board)
