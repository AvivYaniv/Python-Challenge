FILE_NAME = "up.txt"

NONE_VERBOSE, LOW_VERBOSE, HIGH_VERBOSE = 0, 1, 2

VERBOSE_LEVEL = HIGH_VERBOSE
MEMORY_OPTIMISATION = False

DIMENSIONS_HEADER_KEYWORD   = "Dimensions"
HORIZONTAL_HEADER_KEYWORD   = "Horizontal"
VERTICAL_HEADER_KEYWORD     = "Vertical"

BLACK = 'X'
WHITE = ' '
TBD = '?'

INDEX_NOT_FOUND = -1

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def GetRowsNumber(self):
        if not self.rows_number:
            self.rows_number = len(self.matrix)
        return self.rows_number

    def GetColsNumber(self):
        if not self.cols_number:
            self.cols_number = len(self.matrix[0])
        return self.cols_number

    def GetRow(self, row_index):
        return self.matrix[row_index]

    def GetCol(self, col_index):
        return Matrix.Transpose(self).GetRow(col_index)

    def SetCol(self, col, index):
        row_index = 0
        for row in self.matrix:
            row[index] = col[row_index]
            row_index = row_index + 1

    def SetRow(self, row, index):
        self.matrix[index] = row

    @staticmethod
    def GetEmpty(ROWS, COLS, empty):
        empty_matrix = []
        empty_row = (empty, ) * COLS
        for r in xrange(ROWS):
            empty_matrix.append(empty_row)
        return empty_matrix

    @staticmethod
    def CopyMatrix(matrix):        
        copy = list()        
        for ri in xrange(len(matrix)):
            row = list()
            for ci in xrange(len(matrix[ri])):
                row.append(matrix[ri][ci])
            copy.append(row)
        return copy

    @staticmethod
    def Transpose(matrix):  
        return Matrix(map(list, zip(*matrix.matrix)))
    
    def __str__(self):
        view = ""
        row_number = 1
        for row in self.matrix:
            if row_number != 1:
                view = view + "\n"
            view = view + "["
            cell_pos = 1
            for cell in row:            
                view = view + str(cell)
                if cell_pos != len(row):
                    view = view + ","
                cell_pos = cell_pos + 1
            view = view + "]"
            row_number = row_number + 1
        return view
        
    def print_matrix(self):
        print self.__str__()

class NonogramDefinition:
    def __init__(self, ROWS, COLS, rows_segments, cols_segments):        
        self.ROWS = ROWS
        self.COLS = COLS
        self.rows_segments = rows_segments
        self.cols_segments = cols_segments        
    
class Nonogram:
    def __init__(self, board):
        self.board = Matrix(board)

    def GetBoard(self):
        return self.board

    def GetRow(self, row_index):
        return self.GetBoard().GetRow(row_index)

    def GetCol(self, col_index):
        return self.GetBoard().GetCol(col_index)

    def SetCol(self, col, index):
        self.GetBoard().SetCol(col, index)

    def SetRow(self, row, index):
        self.GetBoard().SetRow(row, index)

    @staticmethod
    def GetEmpty(ROWS, COLS):
        return Nonogram(Matrix.GetEmpty(ROWS, COLS, TBD))

    @staticmethod
    def Copy(nonogram):
        return Nonogram(Matrix.CopyMatrix(nonogram.board.matrix))

    def print_nonogram(self):
        self.board.print_matrix()

########## SEGMENT MANIPULATION ##########
class SegmentHandler(object):
    def __init__(self, filled, stop):
        self.filled = filled
        self.stop = stop
        
    def GetSegments(self, array):
        segments = []
        c = 0
        for v in array:
            if v == self.filled:
                c = c + 1
            elif v == self.stop:
                break
            else:
                if c != 0:
                    segments.append(c)
                c = 0
        if c != 0:
            segments.append(c)
        elif len(segments) == 0:
            segments.append(0)
        return segments

    def GetMatrixRowSegments(self, matrix):
        row_segments = []
        for row in matrix.matrix:
            row_segments.append(self.GetSegments(row))
        return row_segments

    def GetMatrixColSegments(self, matrix):
        return self.GetMatrixRowSegments(Matrix.Transpose(matrix))

class NonogramSegmentHandler(SegmentHandler):
    def __init__(self, nonogram_definition):
        SegmentHandler.__init__(self, BLACK, TBD)
        self.definition = nonogram_definition
        
    def GetSegments(self, array):
        return super(NonogramSegmentHandler, self).GetSegments(array)

    def GetRowSegments(self, nonogram):
        return super(NonogramSegmentHandler, self).GetMatrixRowSegments(nonogram.GetBoard())

    def GetColSegments(self, nonogram):
        return super(NonogramSegmentHandler, self).GetMatrixColSegments(nonogram.GetBoard())

    def IsSegmentContradiction(self, desired_segments, actual_segments, last_cell):
        if actual_segments[0] != 0:    
            for i in xrange(min(len(desired_segments), len(actual_segments))):
                # If actual last segment if bounded by TBD
                if (last_cell == BLACK) and (i == len(actual_segments) - 1):
                    # Estimate actual last segment length
                    # If it's lenght exceeds desired segment legth
                    # than its a contradiction
                    if actual_segments[i] > desired_segments[i]:
                            return True
                    # No contradiction, because it's the last velue to check - ending loop
                    else:
                            break
                else:
                    if actual_segments[i] != desired_segments[i]:
                        return True
        return False

    def IsColSegmentContradiction(self, nonogram, row_index, board_invalids, bpk, next_illegals):
        desired_segments = self.definition.cols_segments
        actual_segments = self.GetColSegments(nonogram)
		
	# Going over last row placment cells
        for ci in xrange(self.definition.COLS):
	    # Value of current col of current last row placement
            value_in_row = nonogram.GetCol(ci)[row_index]

            # If contradiction has been dectected by placing current row in current board
            if self.IsSegmentContradiction( \
                desired_segments[ci], \
                actual_segments[ci], \
                value_in_row):
                # Adding the value that caused the contradiction to current board-row invalids
                board_invalids.GetBoardInvalids(row_index, bpk).append( \
                                (ci, value_in_row))               
                return True
	    # No contradiction found
            else:
                last_actual_segment_index = len(actual_segments[ci]) - 1
                
		# If we are in the beginning of segment created by current row placed on current board
                if value_in_row == BLACK and actual_segments[ci][last_actual_segment_index] == 1:
		    # If there are more actual segments than desired; current board with current row combination is invalid
                    if len(desired_segments[ci]) < len(actual_segments[ci]):
                        return True                    
                    
                    last_actual_segment = actual_segments[ci][last_actual_segment_index]
                    last_desired_segment = desired_segments[ci][last_actual_segment_index]

                    # If current detected last segment lasts beyoned the board; current board with current row combination is invalid 
                    if self.definition.ROWS <= row_index + (last_desired_segment - last_actual_segment):
                        return True
                    
                    # Setting for current board, next rows invalid cells - to match current detected last segment
                    r = 0
                    if (last_desired_segment - last_actual_segment) > 0:                        
                        for d in xrange(last_actual_segment, last_desired_segment):
                            r = r + 1
                            next_illegals[row_index + r] = (ci, WHITE)        
        return False

    def IsRowSegmentsSatisfied(self, nonogram, index):
        row = nonogram.GetRow(index)
        actual_segments = self.GetSegments(row)
        desired_segments = self.definition.rows_segments[index]
        return actual_segments == desired_segments

    def IsColSegmentsSatisfied(self, nonogram, index):
        col = nonogram.GetCol(index)
        actual_segments = self.GetSegments(col)
        desired_segments = self.definition.cols_segments[index]
        return actual_segments == desired_segments

    def IsAllRowSegmentsSatisfied(self, nonogram):
        for i in xrange(self.definition.ROWS):
            if not self.IsRowSegmentsSatisfied(nonogram, i):
                return False
        return True

    def IsAllColSegmentsSatisfied(self, nonogram):
        for i in xrange(self.definition.COLS):
            if not self.IsColSegmentsSatisfied(nonogram, i):
                return False
        return True

class MatrixSegmentManipulator:
    def __init__(self, unknown, filled, length):
        self.unknown = unknown
        self.filled = filled
        self.length = length
        
    def GenerateRightmost(self, segments):
        result = []
        i = 0
        for s in segments:
            result.extend([self.filled, ] * int(s))
            i = i + s
            if i < self.length:
                result.extend(self.unknown)
                i = i + 1
        if i < self.length:
            result.extend([self.unknown, ] * (self.length - i))
        return result

    def GenerateLeftmost(self, segments):
        return self.GenerateRightmost(segments[::-1])[::-1]

    def GetOverlapping(self, segments):
        result = [self.unknown, ] * self.length
        rightmost = self.GenerateRightmost(segments)    
        leftmost = self.GenerateLeftmost(segments)    
        is_rightmost_segment = False    
        is_leftmost_segment = False    
        rightmost_segment_number = 0
        leftmost_segment_number = 0
        for i in xrange(self.length):
            if rightmost[i] == self.unknown:
                is_rightmost_segment = False
            elif not is_rightmost_segment:
                is_rightmost_segment = True
                rightmost_segment_number = rightmost_segment_number + 1
            if leftmost[i] == self.unknown:
                is_leftmost_segment = False
            elif not is_leftmost_segment:
                is_leftmost_segment = True
                leftmost_segment_number = leftmost_segment_number + 1
            if rightmost_segment_number == leftmost_segment_number:
                if rightmost[i] == leftmost[i] == self.filled:
                    result[i] = self.filled
        return result

class NonogramSegmentManipulator:
    def __init__(self, nonogram_definition):
        self.definition = nonogram_definition
        self.segment_handler = NonogramSegmentHandler(nonogram_definition)
        self.rows_segment_manipulator = \
            MatrixSegmentManipulator(TBD, BLACK, nonogram_definition.ROWS)
        self.cols_segment_manipulator = \
            MatrixSegmentManipulator(TBD, BLACK, nonogram_definition.COLS)
        
    def GetKnownRowOverlapping(self):
        known = []
        for segments in self.definition.rows_segments:
            known.append(self.rows_segment_manipulator.GetOverlapping(segments))
        return known

    def GetKnownColOverlapping(self):
        known = []
        for segments in self.definition.cols_segments:
            known.append(self.cols_segment_manipulator.GetOverlapping(segments))
        return Matrix.Transpose(Matrix(known))

    def IsColSegmentContradiction(self, nonogram, row_index, board_invalids, bpk, next_illegals):
        return self.segment_handler.IsColSegmentContradiction(nonogram, row_index, board_invalids, bpk, next_illegals)

    def IsAllSegmentsSatisfied(self, nonogram):
        return self.segment_handler.IsAllRowSegmentsSatisfied(nonogram) and \
               self.segment_handler.IsAllColSegmentsSatisfied(nonogram)

    @staticmethod
    def ApplyKnownNonogram(board, known):
        row_index = 0
        for row in board:
            known_row = known.matrix[row_index]
            cell_index = 0
            for cell in row:            
                if known_row[cell_index] == BLACK:
                    board[row_index][cell_index] = BLACK
                cell_index = cell_index + 1
            row_index = row_index + 1
        return Nonogram(board)

    def WhitenKnownRowSegments(self, nonogram):
        for index in xrange(self.definition.ROWS):
            if self.segment_handler.IsRowSegmentsSatisfied(nonogram, index):
                nonogram.SetRow([WHITE if v == TBD else v for v in nonogram.GetRow(index)], index)
                
    def WhitenKnownColSegments(self, nonogram):        
        for index in xrange(self.definition.COLS):
            if self.segment_handler.IsColSegmentsSatisfied(nonogram, index):
                nonogram.SetCol([WHITE if v == TBD else v for v in nonogram.GetCol(index)], index)

    def WhitenKnownSegments(self, nonogram):
        self.WhitenKnownRowSegments(nonogram)
        self.WhitenKnownColSegments(nonogram)

import itertools

class StarsAndBars:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.i = 0
        self.binomial_coefficient = self._GetBinomialCoefficient()

    def _GetBinomialCoefficient(self):
        return list(itertools.combinations(xrange(self.n+self.k-1), self.k-1))

    def HasNextStructure(self):        
        return self.i < len(self.binomial_coefficient)

    def GetNextStarsAndBars(self):
        c = self.binomial_coefficient[self.i]
        self.i = self.i + 1
        return [b-a-1 for a, b in zip((-1,)+c, c+(self.n+self.k-1,))]

import gc

class BoardPossibilities:
    def __init__(self):
        self.delimeter = "-"
        self.boards = {}

    def DeleteBoards(self):
        self.boards.clear()

    def AddEmpty(self):
        self.AddBoard(None, None, [])

    def _GetNextBoardId(self, bpk, crp):
        if bpk is None:
            return "0" + self.delimeter
        return bpk + self.delimeter + str(crp) + self.delimeter

    def AddBoard(self, board_id, row_id, board):
        new_board_id = self._GetNextBoardId(board_id, row_id)        
        self.boards[new_board_id] = board
        return new_board_id

class BoardInvalidCells:
    def __init__(self, ROWS):
        self.invalid_cells = [{} for i in xrange(ROWS)]

    def AddInvalidCells(self, row_id, board_id, cells):
        self.self.invalid_cells[row_id][board_id] = cells

    def DeleteRow(self, row_id):
        self.invalid_cells[row_id].clear()

    def GetBoardInvalids(self, row_id, bpk):
        invalids = self.invalid_cells[row_id].get(bpk)

	# If invalid cells list hasn't been created yet - creating it
        if invalids is None:
            self.invalid_cells[row_id][bpk] = []

        return self.invalid_cells[row_id].get(bpk)

    def UpdateInvalidCellsBoardIds(self, row_id, new_board_ids):
        row_invalids = self.invalid_cells[row_id]
        for old_board_id in row_invalids.keys():
            for new_board_id in new_board_ids:                
                if new_board_id.startswith(old_board_id):
                    row_invalids[new_board_id] = row_invalids[old_board_id][::]
            del row_invalids[old_board_id]

class NonogramSolver:
    def __init__(self, definition):
        self.definition = definition
        self.segment_manipulator = NonogramSegmentManipulator(definition)

    def _Heuristic(self):
        # Finding black cells, known by overlapping between min-max position of segments        
        row_overlapping = self.segment_manipulator.GetKnownRowOverlapping()
        col_overlapping = self.segment_manipulator.GetKnownColOverlapping()
        # Applying both row & col known black cells
        nonogram = NonogramSegmentManipulator.ApplyKnownNonogram(row_overlapping, col_overlapping)
        # Whiten space between segments that match to given restrictions
        self.segment_manipulator.WhitenKnownSegments(nonogram)
        return nonogram

    @staticmethod
    def _GenerateRowStructuresManagersArray(rows_segments, row_length):
        row_structures = []
        for rs in rows_segments:
            row_structures.append(NonogramRowStructureManager(rs, \
                                  row_length))
        return row_structures

    def _ResetRowStructureManager(self, row_structures_managers, ri):
        row_structures_managers[ri] = \
            NonogramRowStructureManager(self.definition.rows_segments[ri], \
                                        self.definition.COLS)
    
    @staticmethod
    def _IsValidRowStructure(desired, actual, row_index):
        desired_row = desired.GetRow(row_index)
        actual_row = actual
        for i in xrange(len(desired_row)):
            desired_value = desired_row[i]
            actual_value = actual_row[i]
            if (desired_value == BLACK and actual_value == WHITE) or \
               (actual_value == BLACK and desired_value == WHITE):
                   return False
        return True

    def _GetAllRowsPossibilities(self, nonogram):
        row_structures_managers = \
            NonogramSolver._GenerateRowStructuresManagersArray( \
                self.definition.rows_segments,
                self.definition.COLS)
        all_rows_possibilities = [[] for i in xrange(self.definition.ROWS)]
        
        # Going over the rows, placing them at possible positions
        for ri in xrange(self.definition.ROWS):
            current_row_possibilities = []
            # If row has been solved
            if not TBD in nonogram.GetRow(ri):
                current_row_possibilities.append(nonogram.GetRow(ri))
            # Row hasn't been solved
            else:
                # Going over row structure possibilities, adding valid
                while row_structures_managers[ri].HasNextStructure():
                    row_structure = row_structures_managers[ri].GetNextStructure()                    
                    if NonogramSolver._IsValidRowStructure(nonogram, row_structure, ri):
                        current_row_possibilities.append(row_structure)
            all_rows_possibilities[ri] = current_row_possibilities
        return all_rows_possibilities

    def _IsInvalidRow(self, possible_row, invalid_rows_cells):
        for (index, value) in invalid_rows_cells:
            if possible_row[index] == value:
                return True
        return False

    def _BuildBoard(self, all_rows_possibilities, board_posibilities_indexes):
        board = Nonogram.GetEmpty(self.definition.ROWS, self.definition.COLS)
        for (row_index, possible_row_stucture) in board_posibilities_indexes:
            board.SetRow(all_rows_possibilities[row_index][possible_row_stucture], row_index)
        return board

    def _BuildPossibleBoards(self, all_rows_possibilities):
        board_possibilities = BoardPossibilities()
        board_possibilities.AddEmpty()

        boards_invalids = BoardInvalidCells(self.definition.ROWS)

        # Going over all rows possibilities
        for row_index in xrange(len(all_rows_possibilities)):
            current_row_possibilities = all_rows_possibilities[row_index]

            if VERBOSE_LEVEL >= 1:
                    print "Working on row [", row_index, "]"
            if VERBOSE_LEVEL > 1:
                    print "Boards possibilities	: ", len(board_possibilities.boards)
                    print "Row possibilities 	: ", len(current_row_possibilities)
                    print "Actual to process	: ", "{:,}".format(len(board_possibilities.boards) * len(current_row_possibilities))

            # No boards to proccess - no need to continue
            if 0 == len(board_possibilities.boards):
                return None

            # Updating the previous illegal cells' board Ids
            if row_index > 0:
                boards_invalids.UpdateInvalidCellsBoardIds(row_index, board_possibilities.boards.keys())

            board_with_current_row_possibilities = BoardPossibilities()
            # Going over all current row possibilities
            for crp in xrange(len(current_row_possibilities)):
                possible_row = current_row_possibilities[crp]

                # Going over board possibilities and setting current row
                for bpk in board_possibilities.boards.keys():                   
                    # If row dosen't contain cells that contradict col segments restrictions
                    if not self._IsInvalidRow(possible_row, boards_invalids.GetBoardInvalids(row_index, bpk)):
                        current_board = self._BuildBoard(all_rows_possibilities, board_possibilities.boards[bpk])
                        current_board.SetRow(possible_row, row_index)
                        
                        next_illegals = {}
			# If board with current row possibility has no contradiction
                        if not self.segment_manipulator.IsColSegmentContradiction(current_board, row_index, boards_invalids, bpk, next_illegals):                       
                            current_board_possibilities = board_possibilities.boards[bpk][::]
                            current_board_possibilities.append((row_index, crp))
                            nbpk = board_with_current_row_possibilities.AddBoard(bpk, str(crp), current_board_possibilities)

                            if 0 != len(next_illegals.items()):
                                for (ri, illegal_cell) in next_illegals.items():
                                    boards_invalids.GetBoardInvalids(ri, nbpk).append(illegal_cell)
                                    
			# Deleting current board, after using it			
                        del current_board
 
            # Deleting unused objects
            board_possibilities.DeleteBoards()
            boards_invalids.DeleteRow(row_index)
			
            if MEMORY_OPTIMISATION:
                gc.clean()
            
            # Setting board possibilities, after adding for each of them all current row possibilities
            board_possibilities = board_with_current_row_possibilities

        return [self._BuildBoard(all_rows_possibilities, b) for b in board_possibilities.boards.values()]

    def _GetSolution(self, board_possibilities):
        # Going over board possibilities
        for possible_board in board_possibilities:
            if self.segment_manipulator.IsAllSegmentsSatisfied(possible_board):
                return possible_board
        return None

    def Solve(self):
        # Heuristic determing which cells are white or black
        print "Start Heuristic"        
        base_nonogram = self._Heuristic()
        print "End Heuristic"

        print "Start _GetAllRowsPossibilities" 
        # Getting all rows possibilities
        all_rows_possibilities = self._GetAllRowsPossibilities(base_nonogram)
        print "End _GetAllRowsPossibilities"

        print "Start _BuildPossibleBoards" 
        # Building all possible boards
        board_possibilities = self._BuildPossibleBoards(all_rows_possibilities)
        print "End _BuildPossibleBoards"

        # If no possible boards found
        if board_possibilities is None:
            return None 
        
        # Finding the board that matches the segment restrictions
        return self._GetSolution(board_possibilities)

class NonogramWhiteDistributer:
    def __init__(self, whites_to_distribute, white_segments):
        self.whites_distributer = StarsAndBars(whites_to_distribute, white_segments)

    def HasNextStructure(self):        
        return self.whites_distributer.HasNextStructure()
        
    def GetNextWhiteDistribution(self):
        return self.whites_distributer.GetNextStarsAndBars()
      
class NonogramRowStructureManager:
    def __init__(self, row_segments, row_length):
        self.row_length = row_length
        self.row_segments = row_segments
        self.minimal_whites = self._GetMinimalWhitesBetweenSegments()
        self._CreateRowWhiteDistributer()

    def _CreateRowWhiteDistributer(self):        
        number_of_blacks = sum(self.row_segments)
        white_segments = len(self.minimal_whites)
        known_whites_number = sum(self.minimal_whites)
        whites_to_distribute = self.row_length - number_of_blacks - known_whites_number
        self.whites_distributer = NonogramWhiteDistributer(whites_to_distribute, white_segments)

    @staticmethod
    def _GenerateRow(black_segments, white_segments):
        row = []
        bsi = 0
        wsi = 0
        current = WHITE
        while wsi < len(white_segments):
            n = 0
            if current == WHITE:
                n = white_segments[wsi]
                wsi = wsi + 1
                row.extend([current, ] * n)
                current = BLACK
            else:
                n = black_segments[bsi]
                bsi = bsi + 1
                row.extend([current, ] * n)
                current = WHITE
        return row

    def HasNextStructure(self):
        return self.whites_distributer.HasNextStructure()

    def GetNextStructure(self):
        white_distribution = self.whites_distributer.GetNextWhiteDistribution()
        white_segments = \
            [x + y for x, y in zip(self.minimal_whites, white_distribution)]
        return NonogramRowStructureManager._GenerateRow(self.row_segments, white_segments)
    
    # Getting list denoting the minimal whites between segments
    # e.g.
    #   Row black segments: [5, 3, 7] ->
    #   Minimal whites between segments: [0, 1, 1, 0]
    def _GetMinimalWhitesBetweenSegments(self):
        minimal_whites = []
        minimal_whites.extend([0])
        minimal_whites.extend([1,] * (len(self.row_segments) - 1))
        minimal_whites.extend([0])
        return minimal_whites
                
class NonogramFileLoader:
    @staticmethod
    def _ParseNonogramFile(lines):   
        parse_state = ""
        rows_segments = []
        cols_segments = []
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            elif DIMENSIONS_HEADER_KEYWORD in line:
                parse_state = DIMENSIONS_HEADER_KEYWORD
            elif HORIZONTAL_HEADER_KEYWORD in line:
                parse_state = HORIZONTAL_HEADER_KEYWORD
            elif VERTICAL_HEADER_KEYWORD in line:
                parse_state = VERTICAL_HEADER_KEYWORD
            else:
                if parse_state == DIMENSIONS_HEADER_KEYWORD:
                    tokens = line.split(" ")
                    ROWS, COLS = map(int, line.split(" "))
                elif parse_state == HORIZONTAL_HEADER_KEYWORD:
                    rows_segments.append(map(int, line.split(" ")))
                elif parse_state == VERTICAL_HEADER_KEYWORD:
                    cols_segments.append(map(int, line.split(" ")))
        return NonogramDefinition(ROWS, COLS, rows_segments, cols_segments)

    @staticmethod                                      
    def LoadNonogramFile(name):
        nonogram_file = open(name, "r")
        lines = nonogram_file.readlines()
        return NonogramFileLoader._ParseNonogramFile(lines)

# Main
def main():
    nonogram_definition = NonogramFileLoader.LoadNonogramFile(FILE_NAME)

    ##print "Solving nonogram: "
    ##print "Rows:", nonogram_definition.ROWS
    ##print "Cols: ", nonogram_definition.COLS
    ##print "Rows Segments: ", nonogram_definition.rows_segments
    ##print "Cols Segments: ", nonogram_definition.cols_segments

    import time
    start_time = time.clock()

    ##print "B: "
    ##PrintNonogram(nonogram)
    ##
    ##print "A: "
    ##PrintNonogram(current_board)

    solution = NonogramSolver(nonogram_definition).Solve()
    
    if solution:
        total_time = time.clock() - start_time
        solution.print_nonogram()
        print "Solved: ", int(total_time / 60), " minutes and ", int(total_time % 60), " seconds"
    else:
        print "No solution found :("


if __name__ == "__main__":
    main()
