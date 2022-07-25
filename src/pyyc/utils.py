###########################################################
# File: src/pyyc/utils.py                                 #
# Description: Utility functions, constants, and classes  #
###########################################################

from datetime import datetime
import re
from os import path
import sys
import pprint


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def get(self, i):
        return self.items[i]

    def peek(self):
        return self.items[len(self.items)-1]

    def top(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


class WasmModule():
    '''
    Class for generating instructions during IR and x86 gen
    Add checks for src and dst types. Dst cannot be immediate
    '''

    def __init__(self):
        self.expressions = []
        self.fstack = Stack()
        self.indent = 0

    def add_exp(self, exp):
        if exp:
            if isinstance(exp, list):
                for s in exp:
                    s = " " * self.indent + str(s)
                    self.instructions.append(s)
            else:
                s = " " * self.indent + str(exp)
                self.expressions.append(s)


    def add(self, obj):
        # dispatch based on type
        pprint.pprint(obj)
        if isinstance(obj, list):
            self.body(obj)
        else:
            for attr in obj.keys():
                if attr == 'module':
                    self.module(obj[attr])
                elif attr == 'body':
                    self.body(obj[attr])
                elif attr == 'import':
                    self.imprt(obj[attr])
                elif attr == 'func':
                    self.func(obj[attr])
                elif attr == 'assignment':
                    self.assignment(obj[attr])
                elif attr == 'rval':
                    self.rval(obj[attr])
                elif attr == 'call':
                    self.call(obj[attr])
                elif attr == 'const':
                    self.const(obj[attr])
                elif attr == 'name':
                    self.name(obj[attr])
                elif attr == 'print':
                    self.print_(obj[attr])
                elif attr == 'bin_op':
                    self.bin_op(obj[attr])
                elif attr == 'unary_op':
                    self.unary_op(obj[attr])
                elif attr == 'if':
                    self.if_(obj[attr])
                
            

    def module(self, obj):
        self.add_exp("(module")
        self.indent += 4
        for attr in obj.keys():
            self.add(obj)
        self.indent -= 4
        self.add_exp(")")

    def body(self, obj):
        for items in obj:
            self.add(items)

    def func(self, obj):
        if 'fname' in obj.keys():
            self.add_exp("(func $%s" % obj['fname'])
        else:
            self.add_exp("(func")
        self.indent += 4
        if 'params' in obj.keys():
            for param in obj['params']:
                self.decl_param(param)
        if 'ret' in obj.keys():
            self.decl_ret(obj['ret'])
        if 'locals' in obj.keys():
            for local in obj['locals']:
                self.decl_local(local)
        if 'body' in obj.keys():
            self.body(obj['body'])
        # export is pending
        self.indent -= 4
        self.add_exp(")")
        self.add_exp('(export "%s" (func $%s))' % (obj['fname'], obj['fname']))
    
    def bin_op(self, obj):
        if obj['op'] == 'add':
            self.add_exp("(i32.add")
        elif obj['op'] == '&':
            self.add_exp("(i32.and")
        elif obj['op'] == '|':
            self.add_exp("(i32.or")
        elif obj['op'] == 'eq':
            self.add_exp("(i32.eq")
        elif obj['op'] == 'ne':
            self.add_exp("(i32.ne")
        elif obj['op'] == '>>':
            self.add_exp("(i32.shr_u")


        left = obj['left']
        right = obj['right']
        self.indent += 4
        self.add(left)
        self.add(right)
        self.indent -= 4
        self.add_exp(")")


    def unary_op(self, obj):
        pprint.pprint(obj)
        if obj['op'] == 'sub':
            self.add_exp("(i32.sub")
            self.indent += 4
            self.add_exp('(i32.const 0)')
            self.add(obj['operand'])
            self.indent -= 4
            self.add_exp(")")
        elif obj['op'] == '~':
            self.add_exp("(i32.xor")
            self.indent += 4
            self.add_exp('(i32.const -1)')
            self.add(obj['operand'])
            self.indent -= 4
            self.add_exp(")")
        


    def if_(self, obj):
        self.add_exp("(if")
        
        self.indent += 4
        self.add(obj['cond'])
        self.indent += 4

        self.add_exp("(then")
        self.indent += 4
        self.add(obj['then'])
        self.indent -= 4
        self.add_exp(")")
        
        self.add_exp("(else")
        self.indent += 4
        self.add(obj['else'])
        self.indent -= 4
        self.add_exp(")")
        
        self.indent -= 4
        self.indent -= 4
        
        self.add_exp(")")


    def print_(self, obj):
        self.add_exp("(call $print_any")
        self.indent += 4
        self.add(obj['args'])
        self.indent -= 4
        self.add_exp(")")

    def assignment(self, obj):
        self.add_exp("(set_local $%s" % obj['lval'])
        self.add(obj)

    def rval(self, obj):
        self.indent += 4
        self.add(obj)
        self.indent -= 4
        self.add_exp(")")


    def const(self, obj):
        self.add_exp("(%s.const %s)" % (obj['type'], obj['value']))

    def name(self, name):
        self.add_exp("(get_local $%s)" % name)

    def call(self, obj):
        self.add_exp("(call $%s" % (obj['fname']))
        self.indent += 4
        self.add(obj['args'])
        self.indent -= 4
        self.add_exp(')')


    def imprt(self, obj):
        '''
        WASM imports work on two level namespace
        '''
        for pobj in obj.keys():
            for cobj in obj[pobj].keys():
                import_object = obj[pobj][cobj]
                for attr in import_object.keys():
                    if attr == 'func':
                        self.import_func(
                            pobj, cobj, import_object[attr])
                    

    def import_func(self, pobj, obj, func):
        fname = func['fname']
        params = func['params']
        ret = func['ret']

        self.add_exp("(import \"%s\" \"%s\" (func $%s" % (pobj, obj, fname))
        self.indent += 4
        for param in params:
           self.decl_param(param)

        self.decl_ret(ret)
        self.indent -= 4
        self.add_exp("))")
        return self

    def decl_local(self, local):
        local_type = ''
        local_name = ''
        for attr in local.keys():
            if attr == 'type':
                local_type = ' ' + local[attr]
            elif attr == 'name':
                local_name = " $%s" % local[attr]
        if local_type is not None and local_name is not None:
            local_str = '(local' + local_name + local_type + ')'
        self.add_exp(local_str)

    def decl_param(self, param):
        param_type = ''
        param_name = ''
        for attr in param.keys():
            if attr == 'type':
                param_type += ' ' + param[attr]
            elif attr == 'name':
                param_name += " $%s" % param[attr]
        if param_type is not None and param_name is not None:
            param_str = '(param ' + param_name + param_type + ')'
        self.add_exp(param_str)

    def decl_ret(self, ret):
        ret_str = ''
        for attr in ret.keys():
            if attr == 'type':
                ret_str += ' ' + ret[attr]
            elif attr == 'name':
                ret_str += " $%s" % ret[attr]
        if ret and ret_str is not None:
            ret_str = '(result ' + ret_str + ')'
        self.add_exp(ret_str)

    def raw_append(self, stmt):
        self.add_exp(str(stmt))
        return self

    def clear(self):
        self.expressions = []

class Type:
    i32 = 'i32'
    i64 = 'i64'
    f32 = 'f32'
    f64 = 'f64'


#####################
# Helper Functions
#####################
def tmpvar(prefix="tmp"):
    '''
    Generate unique temporary variable name.
    '''
    if not hasattr(tmpvar, "counter"):
        tmpvar.counter = 0
    tmpvar.counter += 1
    return prefix + "_" + datetime.now().strftime("%d") + "_" + str(tmpvar.counter)


def is_int(s):
    if (isinstance(s, int)):
        return True
    else:
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
    return s.isdigit()


def flatten_list(seq):
    '''
    Flatten 2D list into 2D list
    '''
    l = []
    for elem in seq:
        t = type(elem)
        if t is list:
            for elem2 in flatten_list(elem):
                l.append(elem2)
        else:
            l.append(elem)
    return l


def write_to_file(file, data, suffix=None):
    '''
    Write to a file with or without separate suffix
    Usage: 1. write_to_file("file_name", data, ".py")
           2. write_to_file("file_name.py", data) 
    '''
    if isinstance(suffix, str):
        head, filename = path.split(file)
        filename = path.splitext(filename)[0] + suffix
        file = path.join(head, filename)
    with open(file, "w") as f:
        for expr in data:
            f.write(str(expr) + "\n")


def read_file(filename):
    '''
    Read each line and put it in a list
    '''
    with open(filename) as f:
        return f.read().splitlines()


# CONSTANTS

#######################################
# To reduce string replication errors #
#######################################

INT = "int"
BOOL = "bool"
BIG = "big"
EAX = "%eax"
EBX = "%ebx"
ECX = "%ecx"
EDX = "%edx"
ESI = "%esi"
EDI = "%edi"
ESP = "%esp"
EBP = "%ebp"
SHIFT = 2 # Projection/Injection SHIFT for tag management
MASK = 3
FRAMEBASE = "(%ebp)"
REGISTER = "register"
STACK = "stack"
CONST = "const"
VARIABLE = "variable"
SPILLFILE = "spill.ir"
LAMBDA = "lambda"
CONDITIONAL = "conditional"
UNCONDITIONAL = "unconditional"

registers = [EAX, EBX, ECX, EDX, ESI, EDI]
num_registers = len(registers)
caller_saved_registers = [EAX, ECX, EDX]


def from_ebp(offset):
    return str(offset) + FRAMEBASE


# Register allocation Graph

class Graph(object):
    class Vertex():
        def __init__(self, name):
            self.name = name
            self.possible_colors = set()
            self.neighbors = set()
            self.color = None
            self.type = REGISTER if name in [
                EAX, EBX, ECX, EDX, ESP, EBP, ESI, EDI] else STACK if FRAMEBASE in name else CONST if re.match(r'^\d+$', name) else VARIABLE
            self.unspillable = False

        def __str__(self):
            return "\nVertex(Name(%s), \n\t Neighbors(%s), \n\t PossibleColors(%s), \n\t Color(%s), \n\t Type(%s), \n\t Unspillable(%s))\n" % (
                str(self.name), str(self.neighbors), str(self.possible_colors), str(self.color), str(self.type), str(self.unspillable))

        def __repr__(self):
            return self.__str__()

        def __eq__(self, other):
            return self.name == other.name

        def __ne__(self, other):
            return not self.__eq__(other)

        def __hash__(self):
            return hash(self.name)

    def __init__(self, directed=False):
        self.__vertices = {}
        self.__directed = directed

    def add_vertex(self, name):
        if self.__vertices.get(name) is None:
            self.__vertices[name] = self.Vertex(name)

    def add_edge(self, v1, v2):
        self.__vertices[v1].neighbors.add(v2)
        if not self.__directed:
            self.__vertices[v2].neighbors.add(v1)

    # Gives a vertex given a name.
    def get_vertex(self, name):
        return self.__vertices.get(name)

    def get_most_constrained_vertex(self):
        '''
        Most constrained vertex is the one that is not yet colored and has the fewest possible colors.
        If there are more than one, the one with the most neighbors is chosen.
        '''
        least_possible_colors = sys.maxint
        most_constrained_vertex = []
        for v in filter(lambda v: v.color == None, self.__vertices.values()):
            if len(v.possible_colors) < least_possible_colors:
                least_possible_colors = len(v.possible_colors)
                most_constrained_vertex = [v.name]
            elif len(v.possible_colors) == least_possible_colors or v.unspillable:
                most_constrained_vertex.append(v.name)
        if len(most_constrained_vertex) == 0:
            return None

        # If there are more than one, the one with the most neighbors is chosen.
        most_constrained_vertex = sorted(most_constrained_vertex, key=lambda v: len(
            self.__vertices[v].neighbors), reverse=True)
        # If there are unspillable vertices, bring them to the front of the list.
        most_constrained_vertex = sorted(
            most_constrained_vertex, key=lambda v: self.__vertices[v].unspillable, reverse=True)
        return most_constrained_vertex[0]

    def get_vertices(self):
        return self.__vertices.keys()

    def get_edges(self):
        edges = []
        for v in self.__vertices:
            for neighbor in self.__vertices[v].neighbors:
                edges.append((v, neighbor))
        return edges

    def get_neighbors(self, v):
        return self.__vertices[v].neighbors

    def get_possible_colors(self, v):
        return self.__vertices[v].possible_colors

    def get_color(self, v):
        return self.__vertices[v].color

    def get_type(self, v):
        return self.__vertices[v].type

    def is_unspillable(self, v):
        return self.__vertices[v].unspillable

    def set_possible_colors(self, v, possible_colors):
        self.__vertices[v].possible_colors = set(possible_colors)

    def set_color(self, v, color):
        self.__vertices[v].color = color

    def set_type(self, v, type):
        self.__vertices[v].type = type

    def set_unspillable(self, v, unspillable):
        self.__vertices[v].unspillable = unspillable

    def __str__(self):
        out = "Undirected Graph(" if not self.__directed else "Directed Graph("
        out += str(self.__vertices) + ")"
        return out

    def __len__(self):
        return len(self.__vertices)

    def __repr__(self):
        return self.__str__()

    def __contains__(self, v):
        return v in self.__vertices


class InstGen():
    '''
    Class for generating instructions during IR and x86 gen
    Add checks for src and dst types. Dst cannot be immediate
    '''

    def __init__(self):
        self.instructions = []

    def movl(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("movl %s, %s" % (str(src), str(dst)))
        return self

    def addl(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("addl %s, %s" % (str(src), str(dst)))
        return self

    def negl(self, dst):
        self.instructions.append("negl %s" % str(dst))
        return self

    def subl(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("subl %s, %s" % (str(src), str(dst)))
        return self

    def pushl(self, dst):
        if is_int(dst):
            dst = "$%s" % dst
        self.instructions.append("pushl %s" % str(dst))
        return self

    def popl(self, dst):
        if is_int(dst):
            dst = "$%s" % dst
        self.instructions.append("popl %s" % str(dst))
        return self

    def cmpl(self, lhs, rhs):
        if is_int(lhs):
            src = "$%s" % lhs
        self.instructions.append("cmpl %s, %s" % (str(lhs), str(rhs)))
        return self

    def jmp(self, label):
        self.instructions.append("jmp %s" % str(label))
        return self

    def jne(self, label):
        self.instructions.append("jne %s" % str(label))
        return self

    def ifeq(self, lhs, rhs, label=None):
        if is_int(lhs):
            lhs = "$%s" % lhs
        self.cmpl(lhs, rhs)
        self.jne("else_" + str(label))
        self.then_(label)
        return self

    def whileeq(self, lhs, rhs, label=None):
        if is_int(lhs):
            lhs = "$%s" % lhs
        self.cmpl(lhs, rhs)
        self.jne("endwhile_" + str(label))
        self.do_(label)

    def else_(self, label=None, jmp=True):
        if jmp:
            self.jmp("endif_" + str(label))
        self.instructions.append("else_%s:" % str(label))
        return self

    def then_(self, label=None):
        self.instructions.append("then_%s:" % str(label))
        return self

    def do_(self, label=None):
        self.instructions.append("do_%s:" % str(label))
        return self

    def endif_(self, label=None):
        self.jmp("endif_%s" % str(label))
        self.instructions.append("endif_%s:" % str(label))
        return self

    def while_(self, label=None):
        self.instructions.append("while_%s:" % str(label))
        return self

    def endwhile_(self, label=None):
        self.instructions.append("endwhile_%s:" % str(label))
        return self

    def call(self, label):
        self.instructions.append("call %s" % str(label))
        return self

    def orl(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("orl %s, %s" % (str(src), str(dst)))
        return self

    def andl(self, src, dst):
        if (is_int(src)):
            src = "$" + str(src)
        self.instructions.append("andl %s, %s" % (str(src), str(dst)))
        return self

    def notl(self, dst):
        self.instructions.append("notl %s" % str(dst))
        return self

    def shl(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("shl %s, %s" % (str(src), str(dst)))
        return self

    def shr(self, src, dst):
        if is_int(src):
            src = "$%s" % src
        self.instructions.append("shr %s, %s" % (str(src), str(dst)))
        return self

    def label(self, label):
        self.instructions.append("%s:" % str(label))
        return self

    def globl(self, symbol):
        self.instructions.append(".globl %s" % str(symbol))
        return self

    def ret(self):
        self.instructions.append("ret")
        return self

    def leave(self):
        self.instructions.append("leave")
        return self

    def raw_append(self, stmt):
        self.instructions.append(str(stmt))
        return self

    def clear(self):
        self.instructions = []
