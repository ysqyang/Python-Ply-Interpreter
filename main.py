import ply.lex as lex
import ply.yacc as yacc
import sys
import re

class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name not in names:
            raise Semantic_Error()
        else:
            return names[self.name]

class NumberNode(Node):
    def __init__(self, v):
        if '.' in v:
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value

class BooleanNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value

class StringNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value

class ListNode(Node):
    def __init__(self):
        self.value = []

    def evaluate(self):
        return [x.evaluate() for x in self.value]

class IndexNode(Node):
    def __init__(self, l, idx):
        self.l = l
        self.index = idx

    def evaluate(self):
        l = self.l.evaluate()
        idx = self.index.evaluate()
        if type(l) in {str, list} and type(idx) == int and (-len(l) <= idx < len(l)):
            return l[idx]
        else:
            raise Semantic_Error()

class GroupNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        return self.value.evaluate()

class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        num_types = {int, float}
        v1 = self.v1.evaluate()
        v2 = self.v2.evaluate()
        if self.op == '+':           
            if (type(v1) in num_types and type(v2) in num_types) or ((type(v1) in {str, list}) and type(v1) == type(v2)):
                return v1 + v2
            else:
                raise Semantic_Error()
        elif self.op == '-':  
            if type(v1) in num_types and type(v2) in num_types:
                return v1 - v2
            else:
                raise Semantic_Error()
        elif self.op == '*':  
            if type(v1) in num_types and type(v2) in num_types:
                return v1 * v2
            else:
                raise Semantic_Error()
        elif self.op == '/': 
            if type(v1) in num_types and type(v2) in num_types and v2 != 0:
                return v1 / v2
            else:
                raise Semantic_Error()
        elif self.op == '//': 
            if type(v1) in num_types and type(v2) in num_types and v2 != 0:
                return v1 // v2
            else:
                raise Semantic_Error()
        elif self.op == '%':
            if type(v1) in num_types and type(v2) in num_types and v2 != 0:
                return v1 % v2
            else:
                raise Semantic_Error()
        elif self.op == '**': 
            if type(v1) in num_types and type(v2) in num_types:
                return v1**v2
            else:
                raise Semantic_Error()
        elif self.op == 'and':
            if type(v1) != bool or type(v2) != bool:
                raise Semantic_Error()
            else:
                return v1 and v2
        elif self.op == 'or':
            if type(v1) != bool or type(v2) != bool:
                raise Semantic_Error()
            else:
                return v1 or v2
        elif self.op == '<':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 < v2
            else:
                raise Semantic_Error()
        elif self.op == '<=':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 <= v2
            else:
                raise Semantic_Error()
        elif self.op == '>':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 > v2
            else:
                raise Semantic_Error()
        elif self.op == '>=':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 >= v2
            else:
                raise Semantic_Error()
        elif self.op == '==':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 == v2
            else:
                raise Semantic_Error()
        elif self.op == '<>':
            if (type(v1) in num_types and type(v2) in num_types) or (type(v1) == type(v2) == str):
                return v1 != v2
            else:
                raise Semantic_Error()
        elif self.op == 'in':
            if (type(v1) == type(v2) == str) or type(v2) == list:
                return v1 in v2
            else:
                raise Semantic_Error()

class UopNode(Node):
    def __init__(self, op, v):
        self.op = op
        self.value = v

    def evaluate(self):
        v = self.value.evaluate()
        if self.op == '-':
            if type(v) in {int, float}:
                return -v
            else:
                raise Semantic_Error()
        elif self.op == 'not':
            if type(p[2]) == bool:
                return not v
            else:
                raise Semantic_Error()

class PrintNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):
        print(self.value.evaluate())

class AssignNode(Node):
    def __init__(self, t, val):
        self.target = t
        self.value = val

    def execute(self):
        idxs = []
        x = self.target
        while (type(x)) != VariableNode:
            if (type(x)) != IndexNode:
                #print('not index node!!!')
                raise Semantic_Error() 
            idx = x.index.evaluate()
            x = x.l
            if type(idx) == int: 
                idxs.insert(0, idx)
            else:
                raise Semantic_Error()
        
        if len(idxs) == 0:
            names[x.name] = self.value.evaluate()
        else:
            try:
                l = names[x.name]
                for idx in idxs[:-1]:
                    l = l[idx]
                l[idxs[-1]] = self.value.evaluate()
            except:
                raise Semantic_Error()

class BlockNode(Node):
    def __init__(self, s):
        self.sl = [s]

    def execute(self):
        for statement in self.sl:
            if statement is not None:
                statement.execute()

class IfNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self):
        if self.condition.evaluate() == True:
            self.block.execute()

class IfElNode(Node):
    def __init__(self, condition, if_block, el_block):
        self.condition = condition
        self.if_block = if_block
        self.el_block = el_block

    def execute(self):
        if self.condition.evaluate() == True:
            self.if_block.execute()
        else:
            self.el_block.execute()

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self):
        while self.condition.evaluate() == True:
            self.block.execute()

class Semantic_Error(Exception):
    pass

class Syntax_Error(Exception):
    pass

reserved = {
   'if': 'IF',
   'else': 'ELSE',
   'while': 'WHILE',
   'print': 'PRINT',
   'in': 'IN',
   'not': 'NOT',
   'and': 'AND',
   'or': 'OR',
}

tokens = [
    'NAME','NUMBER','STRING','BOOLEAN',
    'ASSIGN','PLUS','MINUS','TIMES','DIVIDE','QUOTIENT','MODULUS','POW',
    'LT','LEQ','GT','GEQ','EQ','NEQ',
    'LPAREN','RPAREN','LBRACK','RBRACK','LBRACE','RBRACE','COMMA','SEMICOLON'
    ] + list(reserved.values())

# Tokens
t_ASSIGN   = r'='
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_QUOTIENT = r'//'
t_MODULUS  = r'%'
t_POW      = r'\*\*'

t_LT  = r'<'
t_LEQ = r'<='
t_GT  = r'>'
t_GEQ = r'>='
t_EQ  = r'=='
t_NEQ = r'<>'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA  = r','
t_SEMICOLON = r';'

t_ignore = " \t\n"

def t_BOOLEAN(t):
    r'True|False'
    if t.value == 'True':
        t.value = BooleanNode(True) 
    else:
        t.value = BooleanNode(False) 
    return t

def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'-?\d*(\d\.|\.\d)\d* | \d+'
    try:
        t.value = NumberNode(t.value)
    except ValueError:
        print("Value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.value = StringNode(t.value[1:-1])
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

####################################################################

# Parsing rules
precedence = (
    ('nonassoc', 'LBRACE', 'RBRACE'),
    ('nonassoc', 'ASSIGN'),
    ('left','OR'),
    ('left','AND'),
    ('nonassoc','NOT'),
    ('nonassoc','LT','LEQ','GT','GEQ','NEQ','EQ','IN'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','QUOTIENT','MODULUS'),
    ('nonassoc','UMINUS'),
    ('right','POW'),
    ('nonassoc','LBRACK','RBRACK')
    )

# dictionary of names
names = {}

def p_block(p):
    'block : LBRACE inblock RBRACE'
    #print('reducing inblock to block')
    p[0] = p[2]

def p_inblock(p):
    'inblock : inblock statement'
    #print('reducing to inblock')
    p[0] = p[1]
    p[0].sl.append(p[2])

def p_inblock_base(p):
    'inblock : statement'
    #print('reducing statement to inblock')
    p[0] = BlockNode(p[1])

def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    #print('reducing to print stmt')
    p[0] = PrintNode(p[3])

def p_statement_assign(p):
    'statement : expression ASSIGN expression SEMICOLON'
    #print('reducing to assign stmt')
    p[0] = AssignNode(p[1], p[3])

def p_statement_else(p):
    'statement : IF LPAREN expression RPAREN block ELSE block'
    #print('reducing to ifelse stmt')
    p[0] = IfElNode(p[3], p[5], p[7])

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN block'
    #print('reducing to if stmt')
    p[0] = IfNode(p[3],p[5])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN block'
    #print('reducing to while stmt')
    p[0] = WhileNode(p[3], p[5])

def p_statement_group(p):
    'statement : LBRACE statement RBRACE'
    #print('reducing statement to statement')
    p[0] = p[2]

def p_statement_empty(p):
    'statement : empty'
    #print('reducing empty to statement')
    pass

def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression QUOTIENT expression
               | expression MODULUS expression
               | expression POW expression
               | expression AND expression
               | expression OR expression
               | expression LT expression
               | expression LEQ expression
               | expression GT expression
               | expression GEQ expression
               | expression EQ expression
               | expression NEQ expression
               | expression IN expression
    '''
    p[0] = BopNode(p[2], p[1], p[3])

def p_expression_uop(p):
    '''
    expression : MINUS expression %prec UMINUS
               | NOT expression
    '''
    p[0] = UopNode(p[1], p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_list(p):
    'list : LBRACK inlist RBRACK'
    p[0] = p[2]

def p_inlist(p):
    'inlist : inlist COMMA expression'
    p[0] = p[1]
    p[0].value.append(p[3])

def p_inlist_expression(p):
    'inlist : expression'
    p[0] = ListNode()
    p[0].value.append(p[1])

def p_inlist_empty(p):
    "inlist : empty"
    p[0] = ListNode()

def p_expression_index(p):
    'expression : expression LBRACK expression RBRACK'
    p[0] = IndexNode(p[1], p[3])

def p_expression_base(p):
    '''
    expression : NUMBER 
               | STRING
               | BOOLEAN
    '''
    p[0] = p[1]

def p_expression_list(p):
    "expression : list"
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    p[0] = VariableNode(p[1])

def p_empty(p):
    'empty :'
    pass 

def p_error(p):
    'Syntax error :'
    parser.token()
    raise Syntax_Error()
    
lexer = lex.lex()
parser = yacc.yacc()

def main():
    try:
        f = open(sys.argv[1])
    except OSError:
        print('Cannot open file "{}"'.format(sys.argv[1])) 
        return
    
    instream = f.read()
    '''
    lexer.input(instream)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    '''     
    try:
        ast = parser.parse(instream)
        ast.execute()
    except Semantic_Error:
        print('Semantic error')
    except Syntax_Error:
        print('Syntax error')

    f.close()

if __name__ == '__main__':
    main()



