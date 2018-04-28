# Python-Ply-Interpreter
Variables and Assignments

Variable names begin with an ASCII letter and may be followed by zero or more ASCII letters, digits and underscore. A regular expression that matches variable names is '[A-Za-z][A-Za-z0-9_]*'.

1. Support for assignments to variables (for example, x=1) and to indexed list variables (for example: l[2] = 5 where l was a variable that contained a list, for example, l was previously assigned a list: l=[1,2,3]; after the assignment l[2] = 5, l contains [1,2,5]).

2. Support for variables used in expressions (for example, if x was assigned 1, then print(x) will print 1). Similarly, indexed variables are evaluated if they occur in a place where their value is needed (for example, if l was assigned [1,2,5], then print(l[0]+l[1]+l[1+1]) will print 8). If the variable has had a value assigned to it, the value should be returned. Otherwise, a "Semantic error" should be generated and the program should stop.

When an indexed list variable is used in an expression, then both the list and the index are evaluated to their value and the indexed list expression is evaluated. If the variable is not a list (or a string), or the index is not a integer number, then a "Semantic error" will be produced. If the index is outside the bounds of the array, a "Semantic error" will be produced.

3. Support for statements:

- Block: a block statement consists of zero-or-more statements enclosed in curly braces {...}. When the block executes, each of the statements in the block is executed in sequential order.

- Assignment: an assignment statement consists of an expression, an equals sign, an expression, and a semicolon. When the assignment statement executes, the left expression is assigned the value evaluated of the right-expression.

- Print: a print statement consists of the "print" keyword, a left-parenthesis, an expression, a right-parenthesis, and a semicolon. When the print statement executes, the expression is evaluated for its value.

- Conditional statements:

o If statements: consists of the keyword "if", a left-parenthesis, an expression, a right-parenthesis, and a body block statement. When the if statement executes, if the expression is True, the body block statement is executed.

o If-else statements: consists of the keyword "if", a left-parenthesis, an expression, a right-parenthesis, a body block statement, an “else” keyword and a body block statement . When the if-else statement executes, if the expression is True, the first body block statement is executed, else the second body is executed. The “else” goes with the closest previous “if” in the same block.

- While: a  while statement consists of the keyword "while", a left-parenthesis, an expression, a right-parenthesis, and a body block statement. Executing the while statement begins by evaluating the condition for its value. If that value is False, the while statement terminates. Otherwise, the while statement executes its body block statement, and execution repeats.

An input program consists of a single outermost block statement. Executing the program consists of executing this block.

The program will print "Syntax error" and stop if it encounters a syntax error during parsing. It will print "Semantic error" and stop when it encounters one of the semantic errors as specified above during execution.
