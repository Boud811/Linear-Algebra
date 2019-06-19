class Matrix():
    def __init__(self, rows):
        self.rows = rows
        
        if isinstance(self[0], list):
            self.col = len(self[0])
            self.row = len(self)
        else:
            self.row = len(self)
            self.col = 1 
        self.size = (self.row, self.col)

    def sp_col(self, j):

        if j < self.col:
            col = []
            for rownum in range(self.row):
                col.append(self[rownum][j])
            return col
        else:
            raise IndexError
    def get_leading_ones(self):
        self.leading_ones = []
        #creating a list of the column location of the leading ones
        for i in range(self.row):
            for j in range(self.col):
                if self[i][j]== 1:
                    self.leading_ones.append(j)
                    break
        return self.leading_ones 
    def print_matrix(self):
        for row in self:
            print(row)
    def is_ref(self):
        row = 0
        leadingOnes = self.get_leading_ones()
        #1st condition (stairs shape)
        for leading in range(len(leadingOnes)-1):
            if leadingOnes[leading] >= leadingOnes[leading+1]:
                return False
        #2nd condition (the entries under each leading one = 0)
        for leading in range(len(leadingOnes)):
            column = self.sp_col(leadingOnes[leading])
            row += 1
            for i in range(self.row):
                if row + i < len(column):
                    if column[row+i] != 0:
                        return False
        for row in range(self.row):
            if not iszerovec(self[row]):
                if firstNonZeroElement(self[row])!= 1:
                    return False
        return True
    def row_refrence(self, j, n):
        """

        :param j: column
        :param n: starting row position
        :return: first non zero element after n
        """
        for i in range(self.row-n):
            if self[i+n][j] != 0:
                return (i+n)
    def non_zero_columns(self):
    
        cols =[]
        for col in range(self.col):
            if not iszerovec(self.sp_col(col)):
                cols.append(col)
        return cols
    def swap(self, i, j):
        """
        the first Elementary row operation
        :param i: first row
        :param j: second row
        :return: Matrix, with the rows swapped
        """
        temprow = self[i]
        self.rows[i] =self[j]
        self.rows[j]=temprow
        del temprow
        return self

    def multiplying_row_by(self, i, k):
        """
        the second Elementary row operation
        :param i: row number
        :param k: a constant
        :return: A matrix, with the row i multiplied by the constant k
        """
        if k != 0:
            for num in range(self.col):
                self[i][num] = self[i][num] * k
            return self 
        else: 
            print('you can not preforme this operation if k = 0')
            return self


    def multiplying_row_adding(self, i, j, k):
        """
        the third Elementary row operation
        :param i: first row number
        :param j: second row number
        :param k: a constant
        :return: A Matrix, with the row i multiplied by the constant k and added to the row j
        """
        for num in range(self.col):
            self[j][num] = self[j][num] + self[i][num] * k
        return self 

    def ref(self, steps =False, countR = 0):
        """

        :param steps: if True, then the program shows the steps
        :param countR: the number of iterations
        :return: the equivalence of A in Row Echelon Form
        """
        
        if countR == 0 and steps == True:
            print("----------------- \n Before")
            self.print_matrix()
            print("-----------------")

        if self.is_ref():
            if steps == True:
                print("----------------- \n After")
                self.print_matrix()
            return self
        if countR > len(self.non_zero_columns()):
            if steps == True:
                self.print_matrix()
            return self
        elif countR <= len(self.non_zero_columns()):
            if steps == True:
                print("Step: ", countR + 1)
            counter = countR
            firstNonZeroEntryCol = self.non_zero_columns()[countR]

            firstNonZeroEntryRow = self.row_refrence(firstNonZeroEntryCol, countR)
            #swapping
            if firstNonZeroEntryRow == countR: #you don't swap something with itself! 
                pass
            else:
                if steps == True:
                    print("Swapping row: ", firstNonZeroEntryRow, "with: ", countR)
                self = Matrix(self.swap(firstNonZeroEntryRow, countR))
            #multiplying
            if 1 / self[countR][firstNonZeroEntryCol] == 1: #multiplyig by one is like adding zero 
                pass
            else:
                if steps == True:                
                    print('multiplying row: ', countR, 'by: ', 1 / self[countR][firstNonZeroEntryCol])
                self = Matrix(self.multiplying_row_by(countR, 1/self[countR][firstNonZeroEntryCol]))

            #making the numbers under 1 equal to zero
            for element in range(self.col):
                if counter > countR and counter <self.row:
                    if  self[element + countR][firstNonZeroEntryCol] == 0: #adding zero is like multiplyig by one
                        pass
                    else:
                        if steps == True:                        
                            print('multiplying row: ', countR, "By: ", (-1 * self[element + countR][firstNonZeroEntryCol]), "adding it to: ", counter)
                        self = Matrix(self.multiplying_row_adding( countR, counter, (-1 * self[element+countR][firstNonZeroEntryCol])))
                counter = counter + 1


            if steps == True:
                self.print_matrix()
                print("-----------------")

            return self.ref( steps, countR+1)

    def rref(self, steps=False):
        self = Matrix(self.ref(steps))
        counter = self.rank-1  #the indexes of non zero rows 
        column_list = self.non_zero_columns()
        column_list.reverse()
        for column in column_list:
             
            last_non_zero_col = self.sp_col(column)[counter]
            for i in range(1, counter+1):
                if steps == True:
                    print("multiplying row: ", counter, "by", -1 * self[counter-i][column], "Adding that to: ", counter-i )
                self = Matrix(self.multiplying_row_adding(counter, counter-i,-1 * self[counter-i][column]))
            counter -= 1
            if steps == True:

                print("-----------------")
                self.print_matrix()
                print("-----------------")
        return self

    @property
    def rank(self):
        counter = self.row
        for row in self.ref():
            if iszerovec(row):
                counter -=1
        return counter

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        self.line = 0
        return self
    def __setattr__(self, rows, somerow):
        self.__dict__[rows] = somerow
    def __next__(self):
        if self.line >=self.row: 
            raise StopIteration
        current = self.rows[self.line]
        self.line += 1 
        return current

    def __getitem__(self, key):
        
        return self.rows[key]

    
def get_matrix():
    m = int(input("How many rows? "))
    n = int(input("How many columns? "))
    A = []
    for i in range(m):
        entry_row = []
        for j in range(n):
            entry = int(input("the entry in the row {} and the column {}: ".format(i+1, j+1)))
            entry_row.append(entry)
        A.append(entry_row)
    return Matrix(A)

def iszerovec(v):
 
    for e in v:
        if e != 0:
            return False
    return True

def firstNonZeroElement(v):

    for element in v:
        if element != 0:
            return element

