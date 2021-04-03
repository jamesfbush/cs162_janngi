#print_board module

def print_board(board):
    """
    Take board as dict and print the board to terminal window.
    NOTE: Going to need to access the values
    """
    print('\n    a     b     c     d     e     f     g     h     i\n')
    x = 0
    for key, value in board.items():
        if x == 0:                      #very first row/col = a1
            if value != 0:
                print(key[1],"",value.get_token(),end=" - ") #***NOTE this is the thing I changed
            else:
                print(key[1],"","",value,"", end=" - ")
        elif x == 9:                    #new row, print lines between
            if int(key[1]) == 9 or int(key[1]) == 2: #for fortress rows
                print("\n","   |     |     |     |   \ | /   |     |     |     | ")
            elif len(key) == 3 or int(key[1]) == 3:  #for fortress rows
                print("\n","   |     |     |     |   / | \   |     |     |     | ")
            else:                                     #regular rows
                print("\n","   |     |     |     |     |     |     |     |     | ")
            if len(key) == 2:   #for printing where keys below row 10
                if value != 0:
                    print(key[1:],"",value.get_token(),end=" - ")
                else:
                    print(key[1:],"","",value,"", end=" - ")
            else:               #for printing where key is row 10
                if value != 0:
                    print(key[1:],value.get_token(),end=" - ")
                else:
                    print(key[1:],"",value,"", end=" - ")
            x = 0
        else:                   #all in-between values that are not at beginning or end of row
            if x <8:
                if value != 0:
                    print(value.get_token(),end=" - ")
                else:
                    print("",value,"", end=" - ")
            else:
                if value != 0:
                    print(value.get_token(),end=" - ")
                else:
                    print("",value,"",end="")
        x += 1
    print('\n    a     b     c     d     e     f     g     h     i\n')

    return board
