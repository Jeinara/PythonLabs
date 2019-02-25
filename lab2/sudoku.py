import copy
import multiprocessing
import random
import time


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    current_val = 0
    new_list = []
    inner_list = []
    for i in range(0, len(values)):
        inner_list.append(values.pop(0))
        current_val = current_val + 1
        if (current_val == n):
            current_val = 0
            new_list.append(inner_list)
            inner_list = []

    return new_list


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    new_list = []
    i = 9
    for current_val in range(0, i):
        new_list.append(values[current_val][pos[1]])
    return new_list


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    a = int(pos[0] / 3) * 3
    b = int(pos[1] / 3) * 3
    new_list = []
    for i in range(a, a + 3):
        row_list = values[i]
        for j in range(b, b + 3):
            new_list.append(row_list[j])
    return new_list


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    stop = False
    i = 0
    j = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == '.':
                stop = True
                break
        if stop:
            break

    if stop:
        return (i , j)
    else:
        return None


def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    actual_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    new_set = set()
    new_set.update(row)
    new_set.update(col)
    new_set.update(block)
    new_set.remove('.')
    actual_elements = actual_set.difference(new_set)
    return actual_elements


def solve(grid):
    """ Решение пазла, заданного в grid
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    """

    solution = copy.deepcopy(grid)
    if found_grid(solution):
        return solution
    return None


def found_grid(grid):
    min_possible_value_count_cell = None
    while True:
        min_possible_value_count_cell = None
        for rowIndex in range(9):
            for columnIndex in range(9):
                if grid[rowIndex][columnIndex] != '.':
                    continue
                possible_values = find_possible_values(grid, (rowIndex, columnIndex))
                possible_value_count = len(possible_values)
                if possible_value_count == 0:
                    return False
                if possible_value_count == 1:
                    grid[rowIndex][columnIndex] = possible_values.pop()
                if not min_possible_value_count_cell or \
                        possible_value_count < len(min_possible_value_count_cell[1]):
                    min_possible_value_count_cell = ((rowIndex, columnIndex), possible_values)
        if not min_possible_value_count_cell:
            return True
        elif 1 < len(min_possible_value_count_cell[1]):
            break
    r, c = min_possible_value_count_cell[0]
    for v in min_possible_value_count_cell[1]:
        solution_copy = copy.deepcopy(grid)
        solution_copy[r][c] = v
        if found_grid(solution_copy):
            for r in range(9):
                for c in range(9):
                    grid[r][c] = solution_copy[r][c]
            return True
    return False


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    if (solution is not None):
        print("Проверка на правильность решения судоку...")
        right_decision = True
        for rowIndex in range(9):
            for columnIndex in range(9):
                current_set = get_row(solution, (rowIndex, columnIndex))
                if (len(current_set) != 9):
                    right_decision = False
                current_set = get_col(solution, (rowIndex, columnIndex))
                if (len(current_set) != 9):
                    right_decision = False
                current_set = get_block(solution, (rowIndex, columnIndex))
                if (len(current_set) != 9):
                    right_decision = False

        return right_decision
    else:
        return False


def generate_sudoku(N):
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    new_grid = read_sudoku('defpuzzle.txt')
    random.shuffle(new_grid)
    for k in range(9):
        j = random.randint(0, 8)
        if (j == 8):
            for i in range(9):
                new_grid[i][j], new_grid[i][j - 1] = new_grid[i][j - 1], new_grid[i][j]
        else:
            for i in range(9):
                new_grid[i][j], new_grid[i][j + 1] = new_grid[i][j + 1], new_grid[i][j]
    start_num = 81
    while True:
        if (start_num == N):
            resolved_grid = solve(new_grid)
            if (resolved_grid is None):
                return generate_sudoku(N)
            else:
                display(new_grid)
                print("Его решение: ")
                display(solve(new_grid))
                return new_grid
        random_i = random.randint(0, 8)
        random_j = random.randint(0, 8)
        if (new_grid[random_i][random_j] != '.'):
            new_grid[random_i][random_j] = '.'
            start_num = start_num - 1


def run_solve(fname):
    grid = read_sudoku(fname)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f'{fname}: {end-start}')


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        print(check_solution(solution))
        display(solution)

    for fname in ('puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt'):
        p = multiprocessing.Process(target=run_solve, args=(fname,))
        p.start()
