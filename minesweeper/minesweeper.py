import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        print("New Sentence ", self.cells, count)
        self.mines = set()
        self.safe = set()
        self.reduce()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def is_subset(self, other):
        return self.cells < other.cells

    def subtract(self, other):
        return Sentence(self.cells - other.cells, self.count - other.count)
    
    def is_fully_evaluated(self):
        return len(self.cells) == 0

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return set(self.mines)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return set(self.safe)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mines.add(cell)
            self.cells.remove(cell)
            self.count -= 1
            self.reduce()

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safe.add(cell)
            self.cells.remove(cell)
            self.reduce()

    def reduce(self):
        if len(self.cells) == 0:
            return

        if len(self.cells) == self.count:
            self.mines.update(self.cells)
            print("fines found here ====", self.mines)
            self.cells = set()
            self.count = 0

        if self.count == 0:
            self.safe.update(self.cells)
            self.cells = set()

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        self.remaining_moves = set()
        for i in range(self.width):
            for j in range(self.height):
                self.remaining_moves.add((i, j))

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #self.remaining_moves.remove(cell)
        self.moves_made.add(cell)
        self.mark_safe(cell)
        new_sentence = self.get_new_sentence(cell, count)
        if new_sentence is None:
            return None
        self.knowledge.append(new_sentence)
        
        self.learn_from_knowledge()


    def learn_from_knowledge(self):
        while True:
            known_mines = set()
            known_safes = set()
            unfinished_sentences = []

            fully_evaluated_count = 0
            for sentence in self.knowledge:
                known_mines.update(sentence.known_mines())
                known_safes.update(sentence.known_safes())
                if not sentence.is_fully_evaluated():
                    unfinished_sentences.append(sentence)
                else:
                    fully_evaluated_count += 1 

            self.knowledge = unfinished_sentences
            for cell in known_mines:
                if cell not in self.mines:
                    self.mark_mine(cell)
            for cell in known_safes:
                if cell not in self.safes:
                    self.mark_safe(cell)
            print("Number of sentences removed:", fully_evaluated_count)

            # perform inference
            new_sentences = []

            indexes_of_sentences_to_remove = set()
            knowledge_size = len(self.knowledge)

            for i in range(knowledge_size):
                for j in range(i + 1, knowledge_size):
                    if self.knowledge[i].is_subset(self.knowledge[j]):
                        new_sentences.append(self.knowledge[j].subtract(self.knowledge[i]))
                    elif self.knowledge[j].is_subset(self.knowledge[i]):
                        new_sentences.append(self.knowledge[i].subtract(self.knowledge[j]))
                    elif self.knowledge[i] == self.knowledge[j]:
                        indexes_of_sentences_to_remove.add(i)
            
            print("Number of Duplicate knowledge found:", len(indexes_of_sentences_to_remove))
            print("Number of new knowledge found:", len(new_sentences))

            unique_knowledge = []
            for i in range(knowledge_size):
                if i not in indexes_of_sentences_to_remove:
                    unique_knowledge.append(self.knowledge[i])

            print("Number of Unique Knowledge:", len(unique_knowledge))


            new_known_mines = set()
            new_known_safes = set()
            for sentence in new_sentences:
                if sentence.is_fully_evaluated():
                    print(sentence)
                    new_known_mines.update(sentence.known_mines())
                    new_known_safes.update(sentence.known_safes())
                else:
                    unique_knowledge.append(sentence)
            
            index_of_new_sentences_to_remove = set()
            new_sentences_size = len(unique_knowledge)
            for i in range(new_sentences_size):
                for j in range(i + 1, new_sentences_size):
                    if unique_knowledge[i] == unique_knowledge[j]:
                        index_of_new_sentences_to_remove.add(i)
                        break
            
            temp_sentences = []
            for i in range(new_sentences_size):
                if i not in index_of_new_sentences_to_remove:
                    temp_sentences.append(unique_knowledge[i])

            self.knowledge = temp_sentences

            new_marks = 0
            for cell in new_known_mines:
                if cell not in self.mines:
                    self.mark_mine(cell)
                    new_marks += 1
            for cell in new_known_safes:
                if cell not in self.safes:
                    self.mark_safe(cell)
                    new_marks += 1
            
            print("Size of new Knowldge base:", len(self.knowledge))

            if fully_evaluated_count == 0 and new_marks == 0:
                break
        print("Number of known mines:", len(self.mines))
        print(self.mines)
        print("Number of known safe cells:", len(self.safes))


    def get_new_sentence(self, cell, count):
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        neighbours = []
        effective_count = count

        for deltaX, deltaY in directions:
            new_cell = (cell[0] + deltaX, cell[1] + deltaY)
            if 0 <= new_cell[0] < self.width and 0 <= new_cell[1] < self.height:
                if new_cell in self.safes:
                    continue
                if new_cell in self.mines:
                    effective_count -= 1
                    continue
                neighbours.append(new_cell)


        if len(neighbours) == 0:
            return None
        
        new_sentence = Sentence(neighbours, effective_count)
        print(new_sentence)
        return new_sentence

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = self.safes - self.moves_made
        if len(possible_moves) != 0:
            return possible_moves.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.width):
            for j in range(self.height):
                all_moves.add((i, j))
        all_moves = all_moves - self.mines
        all_moves = all_moves - self.moves_made
        if len(all_moves) != 0:
            return random.choice(list(all_moves))
        return None
