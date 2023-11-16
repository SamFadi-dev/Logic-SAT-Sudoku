#!/usr/bin/python3

import sys
import subprocess
"""
    The above code is a Python script that can solve, check the uniqueness of solution, and generate
    Sudoku puzzles of different sizes. 
    
"""

# reads a sudoku from file
# columns are separated by |, lines by newlines
# Example of a 4x4 sudoku:
# |1| | | |
# | | | |3|
# | | |2| |
# | |2| | |
# spaces and empty lines are ignored
def sudoku_read(filename):
    myfile = open(filename, 'r')
    sudoku = []
    N = 0
    for line in myfile:
        line = line.replace(" ", "")
        if line == "":
            continue
        line = line.split("|")
        if line[0] != '':
            exit("illegal input: every line should start with |\n")
        line = line[1:]
        if line.pop() != '\n':
            exit("illegal input\n")
        if N == 0:
            N = len(line)
            if N != 4 and N != 9 and N != 16 and N != 25:
                exit("illegal input: only size 4, 9, 16 and 25 are supported\n")
        elif N != len(line):
            exit("illegal input: number of columns not invariant\n")
        line = [int(x) if x != '' and int(x) >= 0 and int(x) <= N else 0 for x in line]
        sudoku += [line]
    return sudoku

# print sudoku on stdout
def sudoku_print(myfile, sudoku):
    if sudoku == []:
        myfile.write("impossible sudoku\n")
    N = len(sudoku)
    for line in sudoku:
        myfile.write("|")
        for number in line:
            if N > 9 and number < 10:
                myfile.write(" ")
            myfile.write(" " if number == 0 else str(number))
            myfile.write("|")
        myfile.write("\n")

# get number of constraints for sudoku
def sudoku_constraints_number(sudoku):
    N = len(sudoku)
    # Here generate the number of constraints
    count = N*N + (N*N) + (N*N) + (N*N)
    return count



# prints the generic constraints for sudoku of size N
def sudoku_generic_constraints(myfile, N):
    """
    The function `sudoku_generic_constraints` generates generic constraints for a Sudoku puzzle of size
    N.
    
    :param myfile: The parameter `myfile` is a file object that represents the file where the output
    will be written. It is used by the `output` function to write strings to the file
    :param N: The parameter N represents the size of the Sudoku grid or the number of rows and columns
    in the grid. It is used to define the range of the loops and to set the possible values for each
    case in the grid
    """

    def output(s):
        """
        The function "output" writes the string "s" to a file.
        
        :param s: The parameter "s" is a string that represents the content that will be written to a
        file
        """
        myfile.write(s)

    # Notice that the following function only works for N = 4 or N = 9
    def newlit(i,j,k):
        """
        The function `newlit` takes three arguments `i`, `j`, and `k`, and outputs their concatenated
        string representation followed by a space.
        
        :param i: The parameter "i" is a variable that represents the first value to be concatenated
        into the output string
        :param j: The parameter "j" is a variable that is being passed into the function "newlit"
        :param k: The parameter "k" is a variable that is being passed into the function "newlit"
        """
        output(str(i)+str(j)+str(k)+ " ")
    
    def new_not():
        """
        The function "new_not" outputs a hyphen ("-").
        """
        output("-")

    def newcl():
        """
        The function `newcl` outputs the number 0 followed by a newline character.
        """
        output("0\n")

    def newcomment(s):
#        output("c %s\n"%s)
        output("")
    
    def row_constraint(N):
        """
        The function `row_constraint` sets up constraints for a Sudoku puzzle, ensuring that each row
        contains unique values.
        
        :param N: The parameter N represents the size of the grid or the number of rows and columns in
        the grid. It is used to define the range of the loops and to set the possible values for each
        case in the grid
        """
        #Set all the possible value for a case
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                for k in range(1, N + 1):
                    newlit(i, j, k)
                newcl()
                #Only one value in a case
                for k in range(1, N + 1):
                    for kAlt in range(k + 1, N + 1):
                        new_not()
                        newlit(i, j, k)
                        new_not()
                        newlit(i, j, kAlt)
                        newcl()
            #Must be different values in a row
            for kRow in range(1, N + 1):
                for jRow in range(1, N + 1):
                    for jRowAlt in range(jRow + 1, N + 1):
                        new_not()
                        newlit(i, jRow, kRow)
                        new_not()
                        newlit(i, jRowAlt, kRow)
                        newcl()

    def column_constraint(N):
        """
        The function `column_constraint` enforces the constraint that each column in a grid of size N
        must contain different values.
        
        :param N: The parameter N represents the number of columns in the constraint
        """
        for j in range(1, N + 1):
            for i in range(1, N + 1):
                #Must be different values in a column
                for kcolumn in range(1, N + 1):
                    for iColumn in range(1, N + 1):
                        for iColumnAlt in range(iColumn + 1, N + 1):
                            new_not()
                            newlit( iColumn, j, kcolumn)
                            new_not()
                            newlit(iColumnAlt, j, kcolumn)
                            newcl()
        

    def square_constraint(N):
        """
        The function checks for constraints in a square grid where each value must be different within
        the square and across the entire grid.
        
        :param N: The parameter N represents the size of the square. It is used to determine the range
        of the loops and the size of the square
        """
        # Must be different values in a square
        for square_row in range(0, n):
            for square_col in range(0, n):
                for i in range(1, n + 1):
                    #Must be different values in the all square of size nxn
                    for k in range(1, N + 1):
                        for j in range(1, n + 1):
                            for iAlt in range(1, n + 1):
                                for jAlt in range(j + 1, n + 1):
                                    new_not()
                                    newlit(n * square_row + i, n * square_col + j, k)
                                    new_not()
                                    newlit(n * square_row + iAlt, n * square_col + jAlt, k)
                                    newcl()
                        

    if N == 4:
        n = 2
    elif N == 9:
        n = 3
    elif N == 16:
        n = 4
    elif N == 25:
        n = 5
    else:
        exit("Only supports size 4, 9, 16 and 25")
   
    # The `row_constraint(N)`, `column_constraint(N)`, and `square_constraint(N)` functions are
    # responsible for generating the generic constraints for a Sudoku puzzle of size N.
    row_constraint(N)
    column_constraint(N)
    square_constraint(N)    

def sudoku_specific_constraints(myfile, sudoku):
    """
    The function writes specific constraints for a Sudoku puzzle to a file based on the given Sudoku
    grid.
    
    :param myfile: The parameter `myfile` is the file object that you want to write the output to. It
    should be opened in write mode before passing it to the function
    :param sudoku: The parameter "sudoku" is a 2-dimensional list representing the Sudoku puzzle. Each
    element in the list represents a row in the puzzle, and each element within the row represents a
    cell in the puzzle. The value of each cell can be either 0 (empty) or a number from
    """

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    # Notice that the following function only works for N = 4 or N = 9
    def newlit(i,j,k):
        output(str(i)+str(j)+str(k)+ " ")

    def newcl():
        output("0\n")

    for i in range(N):
        for j in range(N):
            if sudoku[i][j] > 0:
                newlit(i + 1, j + 1, sudoku[i][j])
                newcl()

def sudoku_other_solution_constraint(myfile, sudoku):

    N = len(sudoku)

    def output(s):
        myfile.write(s)

    # Notice that the following function only works for N = 4 or N = 9
    def newlit(i,j,k):
        output(str(i)+str(j)+str(k)+ " ")

    def newcl():
        output("0\n")

    # Here should come the constraint generation
    # ...
    newcl()
                
def sudoku_solve(filename):
    """
    The function `sudoku_solve` takes a filename as input, runs a SAT solver on a Sudoku CNF file, and
    returns the solved Sudoku puzzle as a 2D array.
    
    :param filename: The `filename` parameter is the name of the file that contains the Sudoku puzzle in
    CNF format. This file is used as input for the SAT solver to solve the Sudoku puzzle
    :return: The function `sudoku_solve` returns a Sudoku solution as a 2D list if a solution is found.
    If no solution is found or if there is an error, an empty list is returned.
    """
    command = "java -jar org.sat4j.core.jar sudoku.cnf"
    process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    for line in out.split('\n'):
        if line == "" or line[0] == 'c':
            continue
        if line[0] == 's':
            if line != 's SATISFIABLE':
                return []
            continue
        if line[0] == 'v':
            line = line[2:]
            units = line.split()
            if units.pop() != '0':
                exit("strange output from SAT solver:" + line + "\n")
            units = [int(x) for x in units if int(x) >= 0]
            N = len(units)
            if N == 16:
                N = 4
            elif N == 81:
                N = 9
            elif N == 256:
                N = 16
            elif N == 625:
                N = 25
            else:
                exit("strange output from SAT solver:" + line + "\n")
            sudoku = [ [0 for i in range(N)] for j in range(N)]
            # Notice that the following function only works for N = 4 or N = 9
            for number in units:
                sudoku[number // 100 - 1][( number // 10 )% 10 - 1] = number % 10
            return sudoku
        exit("strange output from SAT solver:" + line + "\n")
        return []

def sudoku_generate(size):
    #TODO
    return []
    
from enum import Enum
class Mode(Enum):
    SOLVE = 1
    UNIQUE = 2
    CREATE = 3
    CREATEMIN = 4

OPTIONS = {}
OPTIONS["-s"] = Mode.SOLVE
OPTIONS["-u"] = Mode.UNIQUE
OPTIONS["-c"] = Mode.CREATE
OPTIONS["-cm"] = Mode.CREATEMIN

if len(sys.argv) != 3 or not sys.argv[1] in OPTIONS :
    sys.stdout.write("./sudokub.py <operation> <argument>\n")
    sys.stdout.write("     where <operation> can be -s, -u, -c, -cm\n")
    sys.stdout.write("  ./sudokub.py -s <input>.txt: solves the Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./sudokub.py -u <input>.txt: check the uniqueness of solution for Sudoku in input, whatever its size\n")
    sys.stdout.write("  ./sudokub.py -c <size>: creates a Sudoku of appropriate <size>\n")
    sys.stdout.write("  ./sudokub.py -cm <size>: creates a Sudoku of appropriate <size> using only <size>-1 numbers\n")
    sys.stdout.write("    <size> is either 4, 9, 16, or 25\n")
    exit("Bad arguments\n")

mode = OPTIONS[sys.argv[1]]
if mode == Mode.SOLVE or mode == Mode.UNIQUE:
    filename = str(sys.argv[2])
    sudoku = sudoku_read(filename)
    N = len(sudoku)
    myfile = open("sudoku.cnf", 'w')
    # Notice that this may not be correct for N > 9
    myfile.write("p cnf "+str(N)+str(N)+str(N)+" "+
                 str(sudoku_constraints_number(sudoku))+"\n")
    sudoku_generic_constraints(myfile, N)
    sudoku_specific_constraints(myfile, sudoku)
    myfile.close()
    sys.stdout.write("sudoku\n")
    sudoku_print(sys.stdout, sudoku)
    sudoku = sudoku_solve("sudoku.cnf")    
    sys.stdout.write("\nsolution\n")
    sudoku_print(sys.stdout, sudoku)
    if sudoku != [] and mode == Mode.UNIQUE:
        myfile = open("sudoku.cnf", 'a')
        sudoku_other_solution_constraint(myfile, sudoku)
        myfile.close()
        sudoku = sudoku_solve("sudoku.cnf")
        if sudoku == []:
            sys.stdout.write("\nsolution is unique\n")
        else:
            sys.stdout.write("\nother solution\n")
            sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATE:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
