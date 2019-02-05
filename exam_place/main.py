#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This tool reads the Excel files of HSHN's "HIS Online-Portal" to create
a placement of the students for the examination. THis placement is either
a text file or an Excel file (option "-o"). The name of the examination is
retrieved from the first input Excel file.

:copyright: (c) 2015 by Detlef Stern
:license: Apache 2.0, see LICENSE
"""

import argparse
import collections
import os.path
import random

import xlrd
import xlwt


Student = collections.namedtuple('Student', 'last,first')


class Application(object):
    """Application class. Mostly used as a namespace."""

    def __init__(self):
        self._topic = None
        self._students = {}

    def read_input_file(self, xls_name):
        """
        Read an Excel file with the given name and add the students to the list
        of all students.
        """
        workbook = xlrd.open_workbook(xls_name, ragged_rows=True)
        sheet = workbook.sheet_by_index(0)
        if self._topic is None:
            self._topic = sheet.cell(0, 0).value[8:].strip()
        for row_num in range(4, sheet.nrows):
            row = sheet.row(row_num)
            if len(row) < 3:
                continue
            self._students[row[0].value] = Student(row[1].value, row[2].value)

    def _shuffle_students(self):
        """Return a randomized list of student identifikation keys."""
        key_list = list(self._students.keys())
        random.shuffle(key_list)
        return key_list

    def print_placement(self):
        """Print the placement on Stdout."""
        key_list = self._shuffle_students()
        max_place = len(str(len(self._students)))
        max_key = max(len(key) for key in self._students.keys())
        max_first = max(len(s.first) for s in self._students.values())
        max_last = max(len(s.last) for s in self._students.values())

        print(self._topic)
        print("=" * len(self._topic))
        print()
        for place, key in enumerate(key_list, start=1):
            student = self._students[key]
            print(
                str(place).rjust(max_place),
                key.rjust(max_key),
                student.last.ljust(max_last),
                student.first.ljust(max_first))

    def write_placement(self, out_name):
        """Write the placement into an Excel file."""
        key_list = self._shuffle_students()
        style0 = xlwt.easyxf('font: bold on; align: horiz center')
        style_header_center = xlwt.easyxf('font: bold on; align: horiz center')
        style_header_left = xlwt.easyxf('font: bold on; align: horiz left')
        style_list_center = xlwt.easyxf('align: horiz center')
        style_list_cross = xlwt.easyxf('border: bottom 1; border: right 1; align: horiz left')
        style_list_sign = xlwt.easyxf('border: bottom 1; align: horiz left')
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Placement')
        sheet.write_merge(0, 0, 0, 5, self._topic, style0)
        sheet.write(2, 0, "Platz", style_header_center)
        sheet.write(2, 1, "MatNr", style_header_center)
        sheet.write(2, 2, "Nachname", style_header_left)
        sheet.write(2, 3, "Vorname", style_header_left)
        sheet.write(2, 4, "Spickzettel", style_header_left)
        sheet.write(2, 5, "Unterschrift", style_header_left)
        for row, key in enumerate(key_list, start=3):
            student = self._students[key]
            sheet.write(row, 0, row - 2, style_list_center)
            sheet.write(row, 1, key, style_list_center)
            sheet.write(row, 2, student.last)
            sheet.write(row, 3, student.first)
            sheet.write(row, 4, ' ', style_list_cross)
            sheet.write(row, 5, ' ', style_list_sign)
        sheet.col(0).width = 0x600
        sheet.col(1).width = 0xA00
        sheet.col(2).width = 0x1400
        sheet.col(3).width = 0x1400
        sheet.col(4).width = 0xC00
        sheet.col(5).width = 0x1400
        workbook.save(out_name)


def filename(value):
    """Check for a valid file name."""
    _, ext = os.path.splitext(value)
    if ext.lower() not in ('.xls', '.xlsx'):
        raise ValueError("Invalid file name '{}'".format(value))
    return value


def filename_readable(value):
    """Check for a valid file name and whether the file is readable."""
    value = filename(value)
    with open(value, 'rb'):
        pass
    return value


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Place students for examination.')
    parser.add_argument(
        '-o', '--out', metavar='PLACE', type=filename,
        help="Placement XLS file")
    parser.add_argument(
        'xlsfile', nargs='+', type=filename_readable, help='XLS input file')
    args = parser.parse_args()
    app = Application()
    for xls_name in args.xlsfile:
        app.read_input_file(xls_name)
    if args.out is None:
        app.print_placement()
    else:
        app.write_placement(args.out)


if __name__ == '__main__':
    main()
