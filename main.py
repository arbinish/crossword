from utils import fetch_words, print_board, assign_words
from pprint import pformat
import logging
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)


def main():
    meta_words = fetch_words()
    num_words = len(meta_words['words'])
    logging.info(meta_words)
    if num_words < meta_words['max_length']:
        num_words = meta_words['max_length'] + 1

    for size in range(meta_words['max_length'] + 1,
                      meta_words['max_length'] + 10):
        # create a num_words x num_words board
        logging.info('Attempting new board with size %d', size)
        maze = ['R' for _ in range(size)]
        for row in range(size):
            maze[row] = ['C' for _ in range(size)]

        is_fit, board_map = assign_words(maze, meta_words)
        if is_fit:
            print_board(maze)
            logging.info(
                'optimal solution: board size: %d, number of words: %d, max word length: %d',
                size, num_words, meta_words['max_length'])
            logging.info('board_map: %s', pformat(board_map))
            return
    logging.fatal('Cannot find a solution')


if __name__ == "__main__":
    main()