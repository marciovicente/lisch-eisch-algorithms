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
    # INIT THE 'R' FLAG
    self.file.seek(0)
    self.file.write(pickle.dumps(self.SIZE_OF_FILE))
    self.close_file()

  def create_file(self):
    self.file = file(self.filename, 'w+b')

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
        # self.remove()
        self.print_flag()
      operation = raw_input()
    return

  def mod(self, n):
    return n % self.SIZE_OF_FILE

  def solve_colision(self, old_obj, new_obj):
    if self.file.closed:
      self.open_file()
    if self.method == 'l':
      r_flag_index = self.get_flag_index()
      old_obj.index = r_flag_index
      # pointer to old object value
      # import pdb; pdb.set_trace()
      self.point_to_value(old_obj.value)
      # overwrite the old object with the new index
      self.file.write(pickle.dumps(old_obj))
      # save the new instance in r flag
      self.point_to_value(r_flag_index)
      self.file.write(pickle.dumps(new_obj))
      self.update_flag()
      self.close_file()
    else:
      pass

  def point_to_value(self, value):
    """ This method point to index in a file """
    self.file.seek(0)
    value = int(value)
    index = self.mod(value)
    length = 211 if index > 1 else 1 # TODO - Change 211 to global dynamic variable
    self.file.seek(index * length + len(pickle.dumps(self.SIZE_OF_FILE)))

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
        if n.value == obj.value:
          print 'chave ja existente: %s' % n.value
        else:
          self.solve_colision(old_obj=obj, new_obj=n)
      else:
        self.point_to_value(n.value)
        self.file.write(pickle.dumps(n))
        self.update_flag()
      self.close_file()

  def query(self, value=None, query_value=None):
    self.open_file()
    obj = None
    if not value:
      value = raw_input()
    self.point_to_value(value)

    # TODO, Implements when the position doesn't exist
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      print u'chave não encontrada: %s' % value
      return False

    # only if it's not called recursive
    # import pdb; pdb.set_trace()
    if obj and (int(obj.value) is int(value) and not query_value or int(query_value or -1) is int(obj.value)):
      print 'chave: %s' % obj.value
      print obj.label
      print obj.age
      return True

    if obj and obj.index: # if was colision
      self.point_to_value(obj.index)
      if self.query(value=obj.index, query_value=value if not query_value else query_value):
        return True

    self.close_file()
    print u'chave não encontrada: %s' % value

  def remove(self):
    value = raw_input()
    pass

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def close_file(self):
    if self.file:
      self.file.close()

  def update_flag(self):
    if self.file.closed:
      self.open_file()

    self.file.seek(0)
    for i in reversed(range(self.SIZE_OF_FILE)):
      self.point_to_value(i)
      try:
        # if exists a record, bypass
        obj = pickle.loads(self.file.read())
      except Exception:
        # if pickle generate a error == doesn't have record
        # then I'll save in flag the new free position in file
        self.file.seek(0)
        self.file.write(pickle.dumps(i))
        return

  def get_flag_index(self):
    if self.file.closed:
      self.open_file()
    self.file.seek(0)
    index = pickle.loads(self.file.read())
    return index

  # ###############################
  # ########## TEMPORARY ##########
  # ###############################
  def print_flag(self):
    self.open_file()
    self.file.seek(0)
    print pickle.loads(self.file.read())
    self.close_file()

app = Application()
app.main()

