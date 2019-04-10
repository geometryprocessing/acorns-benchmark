from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
import pycparser.c_ast
import c_generator

class Expr(pycparser.c_ast.Node):
    def __init__(self,node):
        if isinstance(node, str):
            self.ast = node
            self.type = 'str'
        else:
            print("Making a new Expression")
            print(type(node))
            self.ast = node
            print(self.ast.show())
            self.type = node.__class__.__name__ 

    def _eval(self):
        if self.type=='BinaryOp':
            return self.eval_match_op()
        elif self.type ==  'FuncCall':
            return self.eval_match_funccall()
        elif self.type == 'str':
            return (self.__variable__(self.ast))._eval()


    def match_op(self):
        if self.ast.op == '+':
            return (self.__add__())._forward_diff(self)
        elif self.ast.op == '-':
            return (self.__sub__())._forward_diff(self)
        elif self.ast.op == '*':
            return (self.__mul__())._forward_diff(self)
        elif self.ast.op == '/':
            return (self.__truediv__())._forward_diff(self)
        else:
            raise NotImplementedError

    def match_funccall(self):
        func = self.ast.name.name
        print(func)
        if func == 'pow':
            return (self.__pow__())._forward_diff(self)
        elif func == 'sin':
            return (self.__sin__())._forward_diff(self)
        elif func == 'cos':
            return (self.__cos__())._forward_diff(self)
        else:
            raise NotImplementedError


    def eval_match_op(self):
        if self.ast.op == '+':
            return (self.__add__())._eval(self)
        elif self.ast.op == '-':
            return (self.__sub__())._eval(self)
        elif self.ast.op == '*':
            return (self.__mul__())._eval(self)
        elif self.ast.op == '/':
            return (self.__truediv__())._eval(self)
        else:
            raise NotImplementedError

    def eval_match_funccall(self):
        func = self.ast.name.name
        if func == 'pow':
            return (self.__pow__())._eval(self)
        if func == 'sin':
            return (self.__sin__())._eval(self)
        if func == 'cos':
            return (self.__cos__())._eval(self)                        
        else:
            raise NotImplementedError

    def _forward_diff(self):
        if self.type=='BinaryOp':
            return self.match_op()
        elif self.type ==  'FuncCall':
            return self.match_funccall()
        elif self.type == 'str':
            return (self.__variable__(self.ast))._forward_diff()            

    def __add__(self):
        return Add()

    def __sub__(self):
        return Subtract()

    def __mul__(self):
        return Multiply()

    def __truediv__(self):
        return Divide()

    def __pow__(self):
        return Pow()

    def __sin__(self):
        return Sine()

    def __cos__(self):
        return Cosine()

    def __variable__(self, name):
        return Variable(name)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def _eval(self):
        # TODO
        return self.name

    def _forward_diff(self):
        return self.name



class Constant(Expr):
    def _eval(self, cache):
        # TODO
        return self.value

    def _forward_diff(self):
        return 0



class Add(Expr):
    def __init__(self):
        pass

    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " + " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        print(type(cur_node.ast))
        print("Forward Diff through add")
        cur_node.ast.show()
        print(type(cur_node.ast.left))
        return Expr(cur_node.ast.left)._forward_diff() + " + " + Expr(cur_node.ast.right)._forward_diff()


class Subtract(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " - " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        return Expr(cur_node.ast.left)._forward_diff() + " - " + Expr(cur_node.ast.right)._forward_diff()


class Multiply(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " * " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left)._eval() # Needs to be a string
        rhs = Expr(cur_node.ast.right)._eval()
        return rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " + " \
                        + lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()


class Divide(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return Expr(cur_node.ast.left).__eval() + " / " + Expr(cur_node.ast.right).__eval()

    def _forward_diff(self,cur_node):
        lhs = Expr(cur_node.ast.left)._eval()
        rhs = Expr(cur_node.ast.right)._eval()
        return "(" +rhs+ " * " +Expr(cur_node.ast.left)._forward_diff() + " - " + \
                         lhs+ " * " +Expr(cur_node.ast.right)._forward_diff()+")" + "/ " + rhs + " * " + rhs

class Pow(Expr):
    def __init__(self):
        pass    
    def _eval(self,cur_node):
        return "pow" # TODO

    def _forward_diff(self,cur_node):
        base = cur_node.ast.args.exprs[0].name
        exp = cur_node.ast.args.exprs[1].value

        der_base = Expr(base)._forward_diff()
        der_exp = Expr(exp)._forward_diff()

        return exp + " * pow("+base+",("+exp+"-1))" 
        # return "(pow("+base+",("+exp+"-1) * "+\
        #         "("+exp+ " * "+ der_base +" + "+base+ " * "+ der_exp+ " * log("+base+")))"


class Sine(Expr):        
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "sin("+Expr(exp)._eval()+")"

    def _forward_diff(self,cur_node):       
        exp = cur_node.ast.args.exprs[0].name
        return "cos("+Expr(exp)._forward_diff() +")"


class Cosine(Expr):
    def __init__(self):
        pass    

    def _eval(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "cos("+Expr(exp)._eval()+")"

    def _forward_diff(self,cur_node):
        exp = cur_node.ast.args.exprs[0].name
        return "-1*sin("+Expr(exp)._forward_diff() +")"

def differentiate(node):
    # print(show_attrs(node.__class__))
    if node.__class__.__name__ == 'BinaryOp':
        op = node.op
        if (op)=='+':
            print("x=a+b")
        elif (op) == '*':
            print("Mult")
        else:
            print(op)

    elif node.__class__.__name__ == 'FuncCall':
        print(node.name.name)
    return

def show_attrs(node):    
    for attr in dir(node):
        print("-----------------")
        print(attr)
        print(getattr(node,attr))

def get_traversal(fun,x):
    nodes = []
    stack = [fun]
    while stack:
        cur_node = stack[0]
        differentiate(cur_node)
        stack = stack[1:]
        nodes.append(cur_node)

        if 'left' in dir(cur_node):
            stack.append(cur_node.left)
        if 'right' in dir(cur_node):
            stack.append(cur_node.right)
    return 0


def grad(ast, x=0):
    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the 
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    assert type(x) in (int, tuple, list), x
    fun = ast.ext[-1].body.block_items[1].init
    fun.show()
    return get_traversal(fun,x)


def grad_without_traversal(ast, x=0):
    """
    Returns a function which computes gradient of `fun` with respect to
    positional argument number `x`. The returned function takes the 
    same arguments as `fun` , but returns the gradient instead. The function
    `fun` is expected to be scalar valued. The gradient has the same type as argument."""
    assert type(x) in (int, tuple, list), x
    fun = ast.ext[-1].body.block_items[1].init
    fun.show()
    derivative = Expr(fun)._forward_diff()       
    print(derivative)
    c_code = c_generator.CGenerator()
    c_code._write(derivative)

def main(filename):
    # if len(sys.argv) > 1:
    #     filename  = sys.argv[1]
    # else:
    #     print("Please provide a filename as argument")

    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    # ast.show()
    grad_without_traversal(ast)

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         filename  = sys.argv[1]
#     else:
#         print("Please provide a filename as argument")

#     ast = parse_file(filename, use_cpp=True,
#             cpp_path='gcc',
#             cpp_args=['-E', r'-Iutils/fake_libc_include'])
#     # ast.show()
#     grad_without_traversal(ast)
