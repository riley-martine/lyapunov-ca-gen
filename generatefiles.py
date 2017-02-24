#!/usr/bin/env python3
"""Generates files with defect cones for cellular automata."""
import random
from typing import List
from cellautocommon import get_rows


def make_rand_files(rules: List, number_of_files: int=1, len_first_row: int=500, number_of_rows: int=1000) -> None:
    """Generates automata files and defect cones.

    Keyword arguments:
    rules -- A list (or tuple) of rules (0-255) to generate files for
    number_of_files -- How many files to make for each automata
    len_first_row -- Length of randomly generated first row
    number_of_rows -- Number of rows to generate in each file

    Effects:
    Creates files in current directory. This can be big.
    """
    def write_file(rows: List, rule: int, iteration: int, extension: str):
        """Write the files, given rule, iteration, and extension."""
        file_name = '.'.join([str(rule), str(iteration), extension])
        with open(file_name, 'w') as file:
            for row in rows:
                file.write(row + '\n')

    def invert_middle_item(row: List) -> List:
        """Returns the original list, with the middle item inverted."""
        middle_index = len(row) // 2
        middle_item = first_row[middle_index]
        middle_item_inverted = (int(middle_item) + 1) % 2

        return row[:middle_index] + str(middle_item_inverted) + row[middle_index + 1:]

    for rule in rules:
        for iteration in range(number_of_files):
            first_row = ''.join([str(random.randint(0, 1))
                                 for k in range(len_first_row)])
            rows = get_rows(first_row=first_row, rule=rule,
                            number_of_rows=number_of_rows)
            write_file(rows=rows, rule=rule,
                       iteration=iteration, extension='rows')

            first_row2 = invert_middle_item(first_row)
            rows2 = get_rows(first_row=first_row2, rule=rule,
                             number_of_rows=number_of_rows)
            write_file(rows=rows2, rule=rule,
                       iteration=iteration, extension='rows2')

            errors = [
                ''.join(
                    [str((int(rows[row][k] != rows2[row][k]))) for k, _ in enumerate(rows[row])])
                for row, _ in enumerate(rows)
            ]
            write_file(rows=errors, rule=rule,
                       iteration=iteration, extension='errors')


if __name__ == '__main__':
    make_rand_files(rules=(30, 90, 110), number_of_files=1,
                    len_first_row=500, number_of_rows=500)
