#!/usr/bin/python

# Universidade Federal da Bahia
# Estrutura de Dados e Algoritmos II
# Author: @marciovicente 
# Email: marciovicente.filho@gmail.com


import sys, struct
sys.path.insert(0, 'libs/')

# TODO - Change another name to Appliocation class
# because this must be a node of list, and not an application

class Node(object):
  """docstring for Node"""

  def __init__(self):
    self.value = None
    self.sequence = None
    self.age = None
    super(Node, self).__init__()


class Application(object):
  """ Application Class """

  def __init__(self):
    self.method = None
    self.file = None
    self.filename = 'binary'
    self.SIZE_OF_FILE = 11
    super(Application, self).__init__()

  def main(self):
    self.open_file()
    operation = raw_input()
    if operation == 'i':
      self.insert_record()
    elif operation == 'c':
      self.query()
    elif operation != 'e':
      return

  def mod(self, n):
    return n % self.SIZE_OF_FILE
  
  def solve_colision(self):
    pass

  def point_to_value(self, value):
    """ This method point to index in file """
    value = int(value)
    index = self.mod(value)
    self.file.seek(index)

  def insert_record(self):
    value = raw_input()
    sequence = raw_input()
    age = raw_input()
    n = Node()
    n.value = value
    n.sequence = sequence
    n.age = age

    if self.file:
      self.point_to_value(n.value)
      if self.file.read(): # ie, if has colision
        print 'chave ja existente: %s' % n.value
        self.solve_colision()
      else:
        self.file.write(str(n.value))

  def query(self):
    value = raw_input()
    self.point_to_value(value)
    if self.file.read():
      print 'chave: %s' % value
      print 'self.sequence'
      print 'self.age'

  def open_file(self):
    self.file = open(self.filename, 'rb+')

  def close_file(self):
    if self.file:
      self.file.close()

app = Application()
app.main()

