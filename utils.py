import logging
import sys
from random import randint
from typing import AnyStr, Dict, List, Tuple

alignment_word = {0: 'horizontal', 1: 'vertical'}


def fetch_words() -> Dict:
    words = set([
        'panda', 'apple', 'bus', 'car', 'school', 'thanks', 'noodle', 'egg',
        'rooster', 'ostrich', 'elephant', 'zebra', 'mobile', 'doodle', 'dog',
        'air', 'truck', 'cat', 'radio', 'ear', 'led', 'hat', 'bill'
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
                 is_vertical: bool) -> bool:
    log = logging.getLogger('can_fit_word')

    for letter in word:
        if board[row][col] != 'C' and board[row][col] != letter:
            log.debug(f'Cannot {alignment_word[is_vertical]} fit {word} at {row}/{col}')
            return False
        if is_vertical:
            row += 1
        else:
            col += 1
    log.debug(f'{alignment_word[is_vertical]} fit successful at {row}/{col}')
    return True


def assign_word_to_board(board: List[List[AnyStr]], word: AnyStr,
                         is_vertical: bool) -> Tuple[int, int]:
    log = logging.getLogger('assign_word_to_board')
    # try a random cell to fit word
    if is_vertical:
        row = randint(0, len(board) - 1 - len(word))
        col = randint(0, len(board) - 1)
    else:
        row = randint(0, len(board) - 1)
        col = randint(0, len(board) - 1 - len(word))
    if can_fit_word(board, word, row, col, is_vertical):
        fit_word(board, word, row, col, is_vertical)
        log.info(f'first {alignment_word[is_vertical]} fit succeeded for {word} on {row}/{col}')
        return row, col
    max_tries = len(board) ** 2
    tries = max_tries
    # retry with first cell in current row or column
    if is_vertical:
        col = 0
    else:
        row = 0
    log.info(
        f'first {alignment_word[is_vertical]} fit failed for {word} on {row}/{col}. Attempting iterative approach'
    )
    while tries:
        if is_vertical:
            if row + len(word) > len(board):
                col += 1
                col %= len(board)
                row = 0
        else:
            if col + len(word) > len(board):
                row += 1
                row %= len(board)
                col = 0
        log.info(
            f'fitting {word} {alignment_word[is_vertical]} on {row}/{col} [{len(board)}]'
        )
        if can_fit_word(board, word, row, col, is_vertical):
            fit_word(board, word, row, col, is_vertical)
            log.info(f'{alignment_word[is_vertical]} fit succeeded for {word} in {max_tries - tries} tries')
            return row, col
        if is_vertical:
            row += 1
        else:
            col += 1
        tries -= 1
    log.fatal(f'Exhausted tries: Cannot assign {word}')
    # return assign_word_to_board(board, word, is_vertical)


def assign_words(board: List[List[AnyStr]],
                 meta_words: Dict) -> Tuple[bool, Dict]:
    log = logging.getLogger('assign_words')
    min_word_length = meta_words['min_length']
    max_word_length = meta_words['max_length']
    words = meta_words['words']
    board_map = {}
    for word in words:
        valign = randint(0, 1)
        log.info(f'assigning {word} in {alignment_word[valign]} order')
        word_pos = assign_word_to_board(board, word, valign)
        if word_pos is None:
            log.error('Cannot fit word: [%s]', word)
            return False, {}
        board_map[word] = *word_pos, valign
    return True, board_map
