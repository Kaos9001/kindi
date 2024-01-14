class Node: # frankenstein baseado na resposta https://stackoverflow.com/questions/43689114/recursively-print-all-attributes-lists-dicts-etc-of-an-object-in-python
    def to_dict(self):
        return {str(self.__class__.__name__): {item: (self.__dict__[item].to_dict() if isinstance(self.__dict__[item],  Node)
                                      else ([obj.to_dict() if isinstance(obj, Node) else obj for obj in self.__dict__[item]] if (isinstance(self.__dict__[item], list) or isinstance(self.__dict__[item], tuple))
                                            else self.__dict__[item]))
                                      for item in sorted(self.__dict__)}}

class BinOp(Node):
    def __init__(self, optype=None, left=None, right=None):
        self.left = left
        self.right = right
        self.optype = optype


class Literal(Node):
    def __init__(self, value=None, ltype=None):
        self.value = value
        self.type = ltype


class FunctionCall(Node):
    def __init__(self, id=None, args=None):
        self.id = id
        self.args = args


class Block(Node):
    def __init__(self, command=None, next_block=None):
        self.command = command
        self.next_block = next_block

class Array(Node):
    def __init__(self, items=None):
        self.items = items

class AssignArray(Node):
    def __init__(self, id=None, length=None, content=None, vtype=None):
        self.id = id
        self.type = vtype
        self.content = content
        self.length = length

class Assign(Node):
    def __init__(self, id=None, vtype=None, value=None):
        self.id = id
        self.type = vtype
        self.value = value


class Reassign(Node):
    def __init__(self, id=None, value=None):
        self.id = id
        self.value = value


class ReassignArray(Node):
    def __init__(self, id=None, value=None, index=None):
        self.id = id
        self.value = value
        self.index = index

class Return(Node):
    def __init__(self, value=None):
        self.value = value


class Print(Node):
    def __init__(self, content=None):
        self.content = content


class Read(Node):
    def __init__(self, file=None):
        self.file = file


class Write(Node):
    def __init__(self, file=None, content=None):
        self.content = content
        self.file = file


class Crypt(Node):
    def __init__(self, ctype=None, style=None, args=None):
        self.type = ctype
        self.style = style
        self.args = args


class UnaryOp(Node):
    def __init__(self, optype=None, arg=None):
        self.type = optype
        self.arg = arg


class Conditional(Node):
    def __init__(self, condition=None, on_true=None, on_else=None):
        self.condition = condition
        self.on_true = on_true
        self.on_else = on_else


class Concat(Node):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right


class ID(Node):
    def __init__(self, id=None):
        self.id = id


class While(Node):
    def __init__(self, condition=None, block=None):
        self.condition = condition
        self.block = block

class FunctionDef(Node):
    def __init__(self, on_call=None, args=None, id=None):
        self.args = args
        self.on_call = on_call
        self.id = id

class Argument(Node):
    def __init__(self, id=None, atype=None):
        self.id = id
        self.type = atype

class GetFromArray(Node):
    def __init__(self, id=None, index=None):
        self.id = id
        self.index = index
