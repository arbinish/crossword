from utils import fetch_words, print_board, assign_words
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
    num_words = 10
    # create a num_words x num_words board
    maze = ['R' for _ in range(num_words)]
    for row in range(num_words):
        maze[row] = ['C' for _ in range(num_words)]
    assign_words(maze, meta_words)
    print_board(maze)


if __name__ == "__main__":
    main()