import numpy
import hashlib
from pieces import *
from graphics import *
class Position:
    def __init__(self, cb, back, move, piece):
        self.cb = cb
        self.total = '+'
        self.vals = []
        self.back = back
        self.front = []
        self.pruned = False
        self.temp = 0
        self.move = move
        self.piece = 0
        self.enpassant = False
        self.castle = True

def to_fen(cb):
    s = ''
    b = []
    co = 0
    for r in reversed(range(8)):
        for c in reversed(range(8)):
            p = cb[r][c]
            if (p == 0):
                co+=1
            else:
                if (co > 0):
                    b.append(str(co))
                    co = 0
                b.append(num_to_letter(cb[r][c]))
        if (co > 0):
            b.append(str(co))
        co = 0
        b.append("/")
    return (s.join(b))

def make_move(chessboard, move):
    if (move[0] == 'p'):
        pass
    elif (move[0] == 'c'):
        pass
    elif (move[0] == 'e'):
        pass
    else:
        chessboard[move[2]][move[3]] = chessboard[move[0]][move[1]]
        chessboard[move[0]][move[1]] = 0
    return chessboard

def reverse_position(chessboard, move, piece):
    if (move == 0):
        pass
    elif(move[0] >=0 and move[0] <= 7):
        chessboard[move[0]][move[1]] = chessboard[move[2]][move[3]]
        chessboard[move[2]][move[3]] = piece
    elif (move[0] == 'p'):
        pass
    elif (move[0] == 'c'):
        pass
    elif (move[0] == 'e'):
        pass
    return chessboard

def prune(node, color):
    # highly recommend drawing a diagram and looking at this function at the same time
    value = node.total # node.total is basically summing all the pieces
    temp_node = node # creates a temp because the node reference will be modified
    new_node = node.back # reference to the parent node
    to_prune = False # default prunability is false
    p_list = []
    new_color = color # new color variable because we're going up the tree and color changes
    if (new_node != 0): #checks if you're the head node and went back
        while (new_node.back != 0): #going back up the tree until you hit the head node
            if (value != '+'): # if the node has some value, then we proceed (otherwise you can't compare)
                i = 0
                #kinda of hard to explain how this loops works without a diagram
                #basically it goes back to the parent and loops through the children until you hit the child that is being analyzed
                while ((new_node.back.front)[i] != new_node):
                    if ((new_node.back.front)[i].total != '+'): #again makes sure that there's actually a value to compare
                        #we add to the list its parent node (and the parent's parent node and so on) so we can prune them all in one go
                        p_list.append(new_node)
                        p_list.append(temp_node)
                        #these if statements check if we should prune by comparing summed values
                        if (new_color % 2 == 0):
                            if (value < (new_node.back.front)[i].total):
                                to_prune = True
                        else:
                            if (value > (new_node.back.front)[i].total):
                                to_prune = True
                    new_node.temp = value #sets the parent node to a temp value so we can compare further up the tree
                    i += 1
            new_color += 1
            if (new_node.back == 0): #if it hits the head node by accident
                break
            else: #moves up the tree
                new_node = new_node.back
                temp_node = temp_node.back
    for p in p_list: #prunes every parent and parent's parent node and so on
        if (to_prune):
            p.pruned = True

def traverse(node, color, depth):
    color = color % 2 #checks if white or black (min or maxing)
    if (depth < 6):
        #piece_map_move() generates a list of moves and this loops through it
        for move in (piece_map_move(node.cb, color)):
            #moved_piece is the piece used for reversing a position
            moved_piece = (node.cb)[move[2]][move[3]]
            #creates a child node and makes a move at the same time
            child = Position(make_move(node.cb, move), node, move, moved_piece)
            (node.front).append(child) #adds child to the front of the node
            prune(child, color)
            if (not node.pruned): #if it isn't pruned, then it goes deeper into the tree
                node.vals.append(traverse(child, color + 1, depth + 1))
            else:
                #this means it was pruned,
                #so it reverses the position and returns a value it got from the pruning to its parent
                node.total = node.temp
                reverse_position(node.cb, move, moved_piece)
                return (node.total)

            reverse_position(node.cb, move, moved_piece)
        # from here, pruning has failed, so it has to take the min/max of its values and return that
        if (color == 0):
            node.total = min(node.vals)
            return (node.total)
        else:
            node.total = max(node.vals)
            return (node.total)
    else:
        #max depth is reached here so it sums the position, reverses and returns it
        node.total = numpy.sum(numpy.sum(node.cb))
        return node.total

def choose_move(node):
    i = 0
    for n in (node.front):
        if (n.total == node.total):
            return i
        i+=1












#
