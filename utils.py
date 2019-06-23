import logging
import sys
from random import randint
from typing import AnyStr, Dict, List, Tuple


def fetch_words() -> Dict:
    words = set([
        'panda', 'apple', 'bus', 'car', 'school', 'thanks', 'noodle', 'egg',
        'rooster', 'ostrich', 'elephant', 'zebra', 'rainbow', 'auto', 'mobile',
        'airplane', 'truck'
    ])
    word_lengths = [len(w) for w in words]
    min_word_length, max_word_length = min(word_lengths), max(word_lengths)
    return dict(min_length=min_word_length,
                max_length=max_word_length,
                words=words)


def print_board(board: List[List[AnyStr]]) -> None:
    for row in board:
        for element in row:
            sys.stdout.write(f'{element} ')
        sys.stdout.write('\n')


def is_board_clean(board: List[List[AnyStr]]) -> bool:
    board_rows = len(board)
    for row in range(board_rows):
        for col in board[row]:
            if col != 'C': return False
    return True


def fit_word(board: List[List[AnyStr]], word: AnyStr, row: int, col: int,
             vertical: bool) -> None:
    for letter in word:
        board[row][col] = letter
        if vertical:
            row += 1
        else:
            col += 1


def can_fit_word(board: List[List[AnyStr]], word: AnyStr, row: int, col: int,
                 vertical: bool) -> bool:
    for letter in word:
        if board[row][col] != 'C' and board[row][col] != letter:
            return False
        if vertical:
            row += 1
        else:
            col += 1
    return True


def assign_word_to_board(board: List[List[AnyStr]], word: AnyStr,
                         vertical: bool) -> Tuple[int, int]:
    if vertical:
        row = randint(0, len(board) - 1 - len(word))
        col = randint(0, len(board) - 1)
    else:
        row = randint(0, len(board) - 1)
        col = randint(0, len(board) - 1 - len(word))
    if can_fit_word(board, word, row, col, vertical):
        fit_word(board, word, row, col, vertical)
        return row, col
    return assign_word_to_board(board, word, vertical)


def assign_words(board: List[List[AnyStr]], meta_words: Dict) -> None:
    log = logging.getLogger('assign_words')
    min_word_length = meta_words['min_length']
    max_word_length = meta_words['max_length']
    words = meta_words['words']
    alignment_word = {0: 'horizontal', 1: 'vertical'}
    board_map = {}
    for word in words:
        valign = randint(0, 1)
        log.info(f'assigning {word} in {alignment_word[valign]} order')
        board_map[word] = *assign_word_to_board(board, word, valign), valign
    logging.info('solution: %s', board_map)
