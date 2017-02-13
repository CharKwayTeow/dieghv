from os import listdir
from os.path import join
from enum import Enum


class SectionType(Enum):
  """The type of the section in a dictionary"""
  HEADER = 0
  CHAR = 1      # 字典字音
  EXT_CHAR = 2  # 增補字音
  WORD = 3      # 增補詞語
  UNDEFINED = 4


_SECTION_TITLES = {
  SectionType.CHAR: '# 字典字音',
  SectionType.EXT_CHAR: '# 增補字音',
  SectionType.WORD: '# 增補詞語',
  SectionType.UNDEFINED: '# UNDEFINED'}

_FILENAME_SUFFIX = 'dict.yaml'
_OUTPUT_FILE = 'diff.out'


def get_all_dict_files():
  return [file for file in listdir('..') if file.endswith(_FILENAME_SUFFIX)]


def parse_line(line, file, summary_table):
  item, _, pronunciation = line.partition('\t')
  pronunciation = pronunciation[:-1]  # Omits the '\n' at the end of the line.
  if item in summary_table:
    data = summary_table[item]
    if file in data:
      data[file].append(pronunciation)
    else:
      data[file] = [pronunciation]
  else:
    summary_table[item] = {file: [pronunciation]}


def aggregate_by_file(file, summary_table):
  with open(join('..', file), 'r') as f:
    parsing_type = SectionType.HEADER
    for line in f:
      next_parsing_mode = SectionType(parsing_type.value + 1)
      if line.startswith(_SECTION_TITLES[next_parsing_mode]):
        parsing_type = next_parsing_mode
      if parsing_type == SectionType.HEADER or line.startswith('#'):
        continue
      parse_line(line, file, summary_table)
    f.close()


def get_diff(files, summary_table):
  num_of_files = len(files)
  for item, data in summary_table.items():
    if len(data) != num_of_files:
      print('{}:{}'.format(item, data))


def main():
  files = get_all_dict_files()
  summary_table = {}
  for file in files:
    aggregate_by_file(file, summary_table)
  get_diff(files, summary_table)


if __name__ == '__main__':
  main()
