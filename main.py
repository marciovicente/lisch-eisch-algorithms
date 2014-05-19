# -*- coding: utf-8 -*-

# Universidade Federal da Bahia
# Estrutura de Dados e Algoritmos II
# Author: @marciovicente
# Email: marciovicente.filho@gmail.com


import sys, struct, os, pickle
sys.path.insert(0, 'libs/')

# TODO - Change another name to Appliocation class
# because this must be a node of list, and not an application

class Node(object):
  """docstring for Node"""

  def __init__(self):
    self.value = None
    self.label = None
    self.age = None
    self.index = None
    super(Node, self).__init__()


class Application(object):
  """ Application Class """

  def __init__(self):
    self.method = None
    self.file = None
    self.filename = 'lisch.dat'
    self.SIZE_OF_FILE = 11
    super(Application, self).__init__()

  def init_file(self):
    n = Node()
    n.value = n.label = n.age = n.index = ''
    dumpped = pickle.dumps(n)
    obj_size = sys.getsizeof(dumpped)
    self.open_file()
    self.file.seek(self.SIZE_OF_FILE * obj_size)
    self.close_file()

  def create_file(self):
    self.file = file(self.filename, 'w+b')
    # self.open_file()
    # self.file.seek(0)
    # THE FLAG WILL POIN TO LAST REGISTER POSSIBLE IN FILE
    # self.file.write('%s' % self.SIZE_OF_FILE)
    # self.close_file()

  def main(self):
    self.method = raw_input()
    self.filename = 'lisch.dat' if self.method == 'l' else 'eisch.dat'
    if not os.path.exists(self.filename):
      self.create_file()
      self.init_file()

    operation = raw_input()
    while operation != 'e':
      if operation == 'i':
        self.insert_record()
      elif operation == 'c':
        self.query()
      elif operation == 'r':
        self.remove()
      operation = raw_input()
    return

  def mod(self, n):
    return n % self.SIZE_OF_FILE

  def solve_colision(self):
    pass

  def point_to_value(self, value):
    """ This method point to index in a file """
    self.file.seek(0)
    value = int(value)
    index = self.mod(value)
    length = 211 if index > 1 else 1 # TODO - Change 211 to global dynamic variable
    self.file.seek(index * length) # + len(str(self.SIZE_OF_FILE))

  def insert_record(self):
    # if os.path.getsize(self.filename) >= self.SIZE_OF_FILE:
    #   print 'Arquivo cheio'

    value = raw_input()
    label = raw_input()
    age = raw_input()
    n = Node()
    n.value = value
    n.label = label
    n.age = age
    self.open_file()
    if self.file:
      self.point_to_value(n.value)
      obj = None
      try:
        obj = pickle.loads(self.file.read())
      except Exception:
        pass
      if obj: # ie, if has colision
        print 'chave ja existente: %s' % n.value
        self.solve_colision()
      else:
        self.point_to_value(n.value)
        self.file.write(pickle.dumps(n))
      self.close_file()

  def query(self):
    self.open_file()
    obj = None
    value = raw_input()
    self.point_to_value(value)

    # TODO, Implements when the position doesn't exist
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      print u'chave não encontrada: %s' % value

    if obj:
      print 'chave: %s' % obj.value
      print obj.label
      print obj.age
    self.close_file()

  def remove(self):
    value = raw_input()
    pass

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def close_file(self):
    if self.file:
      self.file.close()

app = Application()
app.main()

