import compiler
from compiler.ast import Name, Const, Subscript
import utils
from utils import MASK, SHIFT, Type

class WatVisitor(compiler.visitor.ASTVisitor):
    '''
    A visitor that walks the flattened AST and prints out Web Assembly Text Format code
    '''

    def __init__(self):
        self.wat = utils.WasmModule()
        self.fenv = utils.Stack()

    def visitModule(self, node):
        import_obj = {
            'import': {
                'cruntime': {
                    'get_fun_ptr': {
                        'func': {
                            'fname': 'get_fun_ptr',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'get_free_vars': {
                        'func': {
                            'fname': 'get_free_vars',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'print_any': {
                        'func': {
                            'fname': 'print_any',
                            'params': [{'type': Type.i32}],
                            'ret': {}
                        }
                    },
                    'input': {
                        'func': {
                            'fname': 'input',
                            'params': [],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'create_closure': {
                        'func': {
                            'fname': 'create_closure',
                            'params': [{'type': Type.i32}, {'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'is_int': {
                        'func': {
                            'fname': 'is_int',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'is_true': {
                        'func': {
                            'fname': 'is_true',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'add': {
                        'func': {
                            'fname': 'add',
                            'params': [{'type': Type.i32}, {'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'error_pyobj': {
                        'func': {
                            'fname': 'error_pyobj',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'is_bool': {
                        'func': {
                            'fname': 'is_bool',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'is_big': {
                        'func': {
                            'fname': 'is_big',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'project_int': {
                        'func': {
                            'fname': 'project_int',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'project_bool': {
                        'func': {
                            'fname': 'project_bool',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'project_big': {
                        'func': {
                            'fname': 'project_big',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'inject_int': {
                        'func': {
                            'fname': 'inject_int',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'inject_bool': {
                        'func': {
                            'fname': 'inject_bool',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'inject_big': {
                        'func': {
                            'fname': 'inject_big',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'set_subscript': {
                        'func': {
                            'fname': 'set_subscript',
                            'params': [{'type': Type.i32}, {'type': Type.i32}, {'type': Type.i32}],
                            'ret': {}
                        }
                    },
                    'equal': {
                        'func': {
                            'fname': 'equal',
                            'params': [{'type': Type.i32}, {'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'not_equal': {
                        'func': {
                            'fname': 'not_equal',
                            'params': [{'type': Type.i32}, {'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'get_subscript': {
                        'func': {
                            'fname': 'get_subscript',
                            'params': [{'type': Type.i32}, {'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'create_list': {
                        'func': {
                            'fname': 'create_list',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    },
                    'create_dict': {
                        'func': {
                            'fname': 'create_dict',
                            'params': [{'type': Type.i32}],
                            'ret': {'type': Type.i32}
                        }
                    }
                }
            }
        }

        module = { 'module': {
            'body': [import_obj, self.visit(node.node)]
            }
        }

        self.wat.add(module)

    def visitStmt(self, node):
        stmts = []
        for child in node.nodes:
            stmts.append(self.visit(child))
        return stmts

    def visitConst(self, node):
        const = {
            'const': {
                'value': node.value,
                'type': Type.i32
            }
        }
        return const

    def visitName(self, node):
        name = {
            'name': node.name
        }
        return name

    def visitPrintnl(self, node):
        printnl = {
            'print': {
                'args': self.visit(node.nodes[0]),
            }
        }
        return printnl


    def visitAssign(self, node):
        '''
        We are right now only handling i32 and i64 assignments
        '''
       
        if isinstance(node.nodes[0], Subscript):
            subscript = node.nodes[0]
            listname = self.visit(subscript.expr)
            index = self.visit(subscript.subs[0])
            value = self.visit(node.expr)
            assign = {
                'call': {
                    'fname': 'set_subscript',
                    'args': [listname, index, value]
                }
            }
            return assign

        # This will be have to adeed to the top of the function
        lval = self.visit(node.nodes[0])
        rval = self.visit(node.expr)
        print lval
        self.fenv.top().add(lval)

        # Use SExpression
        assignment = {
            'assignment': {
                'lval': lval,
                'rval': rval
            }
        }
        return assignment

    def visitAssName(self, node):
        return node.name

    def visitAdd(self, node):
        add = {
            'bin_op': {
                'op': 'add',
                'left': {
                    'call': {
                        'fname': 'project_int',
                        'args': [self.visit(node.left)]
                    }
                },
                'right': {
                    'call': {
                        'fname': 'project_int',
                        'args': [self.visit(node.right)]
                    }
                }
            }
        }
        return add

    def visitUnarySub(self, node):
        # FIXME
        # Right now this is a bit hacky
        # WASM doesn't have a unary minus operator
        # 
        unary_sub = {
            'unary_op': {
                'op': 'sub',
                'operand': {
                    'call': {
                        'fname': 'project_int',
                        'args': [self.visit(node.expr)]
                    }
                }

            }
        }
        return unary_sub

    def visitCompare(self, node):
        # check mask
        left = self.visit(node.expr)
        right = self.visit(node.ops[0][1])
        op = node.ops[0][0]

        get_tag = {
            'bin_op': {
                'op': '&',
                'left': {
                    'const': {
                        'value': MASK,
                        'type': Type.i32
                    }
                },
                'right': left
            }
        }

        # Check if it is big by checking if the and of 
        # one of the operand and mask is equal to the mask
        # Note: we are only checking the left side of the comparison
        check_tag = {
            'bin_op': {
                'op': 'eq',
                'left': get_tag,
                'right': {
                    'const': {
                        'value': MASK,
                        'type': Type.i32
                    }
                }
            }
        }

        # Invert the mask so that we 
        # can get the pointer if the operand is big
        invert_mask = {
            'unary_op': {
                'op': '~',
                'operand': {
                    'const': {
                        'value': MASK,
                        'type': Type.i32
                    }
                }
            }
        }

        # Get the pointer from the left operand
        # using the inverted mask
        invert_tag_left = {
            'bin_op': {
                'op': '&',
                'left': invert_mask,
                'right': left
            }
        }

        # Get the pointer from the right operand
        # using the inverted mask
        invert_tag_right = {
            'bin_op': {
                'op': '&',
                'left': invert_mask,
                'right': right
            }
        }

        # Compare the pointers
        cmp_big = {
            'call': {
                'fname': 'equal' if op == '==' else 'not_equal',
                'args': [invert_tag_left, invert_tag_right]
            }
        } 

        # Compare the values in left and right
        # by right shifting the left operand
        # and then comparing it to the (right shifted) 
        # right operand
        cmp_int_bool = {
            'bin_op': {
                'op': 'eq' if op == '==' else 'ne',
                'left': {
                    'bin_op': {
                        'op': '>>',
                        'left': left,
                        'right': {
                            'const': {
                                'value': SHIFT,
                                'type': Type.i32
                            }   
                        }
                    }
                },
                'right': {
                    'bin_op': {
                        'op': '>>',
                        'left': right,
                        'right': {
                            'const': {
                                'value': SHIFT,
                                'type': Type.i32
                            }
                        }
                    }
                }
            }
        }

        # Mistakes: 
        # lval needs to be declared at the top of the function
        # Remember: AssName returns a strin, 
        # Name returns a dict, and lval in assignment is always 
        # a string. 
        # Make sure to Convert it to name when 
        # you assign it to the real assignment (return)
        # we need a get_local
        lval = utils.tmpvar()
        self.fenv.top().add(lval)
        
        assign_cmp_big = {
            'assignment': {
                'lval': lval,
                'rval': cmp_big
            }
        }

        assign_cmp_int_bool = {
            'assignment': {
                'lval': lval,
                'rval': cmp_int_bool
            }
        }
        
        # If the operand is big, then
        # compare the pointers
        # else compare the values
        compare = {
            'if': {
                'cond': check_tag,
                'then': assign_cmp_big,
                'else': assign_cmp_int_bool
            }
        }

        assign_result = {
            'assignment': {
                'lval': lval,
                'rval': {
                    'call': {
                        'fname': 'inject_bool',
                        'args': [self.visit(Name(lval))]
                    }
                }
            }
        }
        
        return [compare, assign_result, self.visit(Name(lval))]
    
    def visitIf(self, node):
        if_ = {
            'if': {
                'cond': self.visit(node.tests[0][0]),
                'then': self.visit(node.tests[0][1]),
                'else': self.visit(node.else_)
            }
        }
        return if_
    
    # def visitWhile(self, node):
    #     while_ = {
    #         'block': {
    #             'label': {
    #                 'name': 'while_' + str(utils.tmpvar())
    #                 }
    #             },
    #             'body': [
    #                 {
    #                     'loop': {
    #                         'label': {
    #                             'name': 'loop_' + str(utils.tmpvar())
    #                         },
    #                         'cond': self.visit(node.test),
    #                         'body': self.visit(node.body),
    #                         'br_if': {
    #                             'name': 'while_' + str(utils.tmpvar())
    #                         }
    #                     },
    #                 }
    #             ]
    #         }
    #     return while_

    def visitCallFunc(self, node):
        # We will not be handling lambdas in 
        # function calls
        call_func = {
            'call': {
                'fname': node.node.name,
                'args': [self.visit(arg) for arg in node.args]
            }
        }
        return call_func

    def visitList(self, node):
        length = len(node.nodes)

        create_list = {
            'call': {
                'fname': 'create_list',
                'args': [{
                    'call': {
                        'fname': 'inject_int',
                        'args': [{
                            'const': {
                                'value': length,
                                'type': Type.i32
                            }
                        }]
                    }
                }]
            }
        }

        list_ptr = {
            'call': {
                'fname': 'inject_big',
                'args': [create_list]
            }
        }


        lval = utils.tmpvar()
        self.fenv.top().add(lval)
        list_ptr_name = {
            'assignment': {
                'lval': lval,
                'rval': list_ptr
            }            
        }

        assign_list = []
        for idx, v in enumerate(node.nodes):
            set_subscript = {
                'call': {
                    'fname': 'set_subscript',
                    'args': [self.visit(Name(lval)),
                    {
                        'call': {
                            'fname': 'inject_int',
                            'args': [{
                                'const': {
                                    'value': idx,
                                    'type': Type.i32
                                }
                            }]
                        }
                    },
                    self.visit(v)]
                }
            }
            assign_list.append(set_subscript)
        
        return [list_ptr_name, assign_list, self.visit(Name(lval))]

    def visitSubscript(self, node):
        subscript = {
            'call': {
                'fname': 'get_subscript',
                'args': [self.visit(node.expr), self.visit(node.subs[0])]
            }
        }
        return subscript


    def visitFunction(self, node):

        # WASM requires that we declare all the local variables upfront
        self.fenv.push(set([])) # So create a new environment

        function = {
            'func': {
                'fname': node.name,
                'params': [{'name': argname, 'type': Type.i32} for argname in node.argnames],
                # 'ret': {'type': Type.i32},
                'body': [self.visit(node.code)]
            }
        }

        # ADD THE LOCALS TO THE TOP OF THE FUNC, WASM DOES NOT ALLOW LOCALS IN THE MIDDLe OF A FUNCTION
        function['func']['locals'] = [{'name': lval, 'type': Type.i32} for lval in self.fenv.top()]
        self.fenv.pop() # destroy the environment

        return function

    def visitReturn(self, node):
        return {'return': self.visit(node.value)}



def get_wat(node):
    wat = compiler.visitor.walk(node, WatVisitor())
    return wat.wat.expressions
