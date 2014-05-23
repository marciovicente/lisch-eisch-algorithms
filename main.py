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
  """ Object class (Node) """

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
    self.STRUCT_SIZE = 0
    super(Application, self).__init__()

  def init_file(self):
    self.open_file()
    self.file.seek(self.SIZE_OF_FILE * self.STRUCT_SIZE)
    # INIT THE 'R' FLAG
    self.file.seek(0)
    self.file.write(pickle.dumps(self.SIZE_OF_FILE-1))
    self.close_file()

  def create_file(self):
    self.file = file(self.filename, 'w+b')

  def set_struct_size(self):
    n = Node()
    n.value = n.age = n.index = -1
    n.label = 'abcdefghijklmnopqrst'
    dumpped = pickle.dumps(n)
    self.STRUCT_SIZE = sys.getsizeof(dumpped)

  def main(self):
    self.method = raw_input()
    self.filename = 'lisch.dat' if self.method == 'l' else 'eisch.dat'
    if not os.path.exists(self.filename):
      self.create_file()
      self.init_file()

    self.set_struct_size()

    operation = raw_input()
    while operation is not 'e':
      if operation is 'i':
        self.insert_record()
      elif operation is 'c':
        self.query()
      elif operation is 'm':
        print '%.1f' % self.average()
      elif operation is 'r':
        value = raw_input()
        self.remove(value=value)
      elif operation is 'p':
        self.print_file()
      operation = raw_input()
    return

  def mod(self, n):
    return n % self.SIZE_OF_FILE

  def is_position_mod(self, value, pos):
    return True if value % self.SIZE_OF_FILE is pos else False

  def tail(self, obj):
    self.file.seek(obj.index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))
    obj_tmp = pickle.loads(self.file.read())
    if obj_tmp.index:
      self.tail(obj.index)
    return obj.index

  def insert_in_lisch(self, old_obj, new_obj, index=None):
    obj_next = None
    if old_obj.index: # if they has a next
      self.file.seek(old_obj.index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))
      # get the object in position:obj.index
      obj_next = pickle.loads(self.file.read())
      # call solve colision recursive to the obj_next
      self.insert_in_lisch(old_obj=obj_next, new_obj=new_obj, index=old_obj.index)
    else:
      r_flag_index = self.get_flag_index()
      # insert the new record in last position free
      self.point_to_value(r_flag_index)
      self.file.write(pickle.dumps(new_obj))
      # update the old
      index = self.mod(new_obj.value) if not index else index
      self.file.seek(index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))
      old_obj.index = r_flag_index
      # overwrite the old object with the new index
      self.file.write(pickle.dumps(old_obj))
      self.close_file()
      self.update_flag()
      return True

  def insert_in_eisch(self, old_obj, new_obj, obj_tmp=None):
    if old_obj.index:
      self.file.seek(old_obj.index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))
      obj_next = pickle.loads(self.file.read())
      self.insert_in_eisch(old_obj=obj_next, new_obj=new_obj, obj_tmp=old_obj if not obj_tmp else obj_tmp)
      # passing old_obj to not lose the reference
    else:
      r_flag_index = self.get_flag_index()
      if obj_tmp:
        index_aux = obj_tmp.index
        new_obj.index = index_aux
        old_obj = obj_tmp

      self.point_to_value(r_flag_index)
      self.file.write(pickle.dumps(new_obj))
      old_obj.index = r_flag_index
      self.point_to_value(new_obj.value)
      self.file.write(pickle.dumps(old_obj))
    self.update_flag()
    return True


  def solve_colision(self, old_obj, new_obj):
    if new_obj.value is old_obj.value:
      print 'chave ja existente: %s' % new_obj.value
      return False

    if self.file.closed:
      self.open_file()
    if self.method == 'l':
      self.insert_in_lisch(old_obj, new_obj)
    else:
      self.insert_in_eisch(old_obj, new_obj)

  def point_to_value(self, value, rec=None):
    """ This method point to index in a file """

    self.file.seek(0)
    value = int(value)
    index = self.mod(value)
    self.file.seek(index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))

    # if rec:
    #   obj = None
    #   try:
    #     obj = pickle.loads(self.file.read())
    #   except Exception:
    #     pass

    #   if hasattr(obj, 'value') and obj.index and (value is not obj.value):
    #     self.point_to_value(value=obj.index, rec=True)
    #   self.file.seek(index * self.STRUCT_SIZE + len(pickle.dumps(self.SIZE_OF_FILE)))

  def insert_record(self):
    value = raw_input()
    label = raw_input()
    age = raw_input()
    n = Node()
    n.value = int(value)
    n.label = label
    n.age = int(age)
    self.open_file()

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

    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      print u'chave não encontrada: %s' % value
      return False

    # only if it's not called recursive
    if hasattr(obj, 'value') and (obj.value is int(value) and not query_value or int(query_value or -1) is obj.value):
      print 'chave: %s' % obj.value
      print obj.label
      print obj.age
      return True

    if hasattr(obj, 'value') and obj.index: # if has colision
      self.point_to_value(obj.index)
      if self.query(value=obj.index, query_value=value if not query_value else query_value):
        return True

    self.close_file()

  def open_file(self):
    self.file = open(self.filename, 'r+b')

  def close_file(self):
    if self.file:
      self.file.close()

  def update_flag(self):
    if not self.file or self.file.closed:
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
    if not self.file or self.file.closed:
      self.open_file()
    self.file.seek(0)
    index = pickle.loads(self.file.read())
    return index

  def print_file(self):
    self.open_file()
    for i in range(self.SIZE_OF_FILE):
      self.point_to_value(i)
      try:
        obj = pickle.loads(self.file.read())
        print '%s: %s %s %s %s' % (i, obj.value, obj.label, obj.age, obj.index if obj.index else 'nulo')
      except Exception:
        print '%s: vazio' % i
    self.close_file()


  def average(self):
    """ This method calculate the average of a specific value found in file """
    def _count_query(value, next_obj=None):
      self.point_to_value(value if not next_obj else next_obj)
      obj = pickle.loads(self.file.read())
      if obj.value is value:
        return 1
      return 1 + _count_query(value=value, next_obj=obj.index)

    self.open_file()
    count = recorded = 0
    for i in range(self.SIZE_OF_FILE):
      obj = None
      self.point_to_value(i)
      try:
        obj = pickle.loads(self.file.read())
      except Exception:
        pass
      if obj:
        recorded+=1
        count += _count_query(obj.value)
    return float(count)/float(recorded)

  def get_current_position(self, value, position=None):
    self.point_to_value(position or value)
    try:
      obj_tmp = pickle.loads(self.file.read())
    except Exception:
      pass
    if value is obj_tmp.value:
      return position or self.mod(value)
    if obj_tmp.index:
      return self.get_current_position(value=value, position=obj_tmp.index)
    return False

  def remove(self, value, pos=None, next_id=None):
    if not self.file or self.file.closed:
      self.open_file()

    value = int(value)
    obj = None
    self.point_to_value(next_id or value)
    try:
      obj = pickle.loads(self.file.read())
    except Exception:
      print 'chave nao encontrada: %s' % value

    if hasattr(obj, 'value'):
      current_pos = pos or self.get_current_position(value)
      if value is obj.value:
        if obj.index:
          replace_obj = self.search_next(obj=obj, pos=current_pos)
          if replace_obj:
            replaced_pos = self.get_current_position(replace_obj.value)
            self.point_to_value(current_pos)
            self.file.write(pickle.dumps(replace_obj))
            self.point_to_value(replaced_pos)
            self.file.write(pickle.dumps(None))
            self.update_flag()
            return True
        else:
          pass
      if obj.index:
        return self.remove(value=value, pos=current_pos, next_id=obj.index)

  def search_next(self, obj, pos):
    self.point_to_value(obj.index)
    obj = pickle.loads(self.file.read())
    is_mod = self.is_position_mod(value=obj.value, pos=pos)
    if is_mod:
      return obj
    elif obj.index:
      return self.search_next(obj=obj.index, pos=pos)
    return False

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

