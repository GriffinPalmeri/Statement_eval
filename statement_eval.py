# File: statement_eval.py
# Author(s): Gabe Krishnadasan and Griffin Palmeri
# Date: 02/06/21
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements.

import re  # For regular expressions

class BadStatement(Exception):
    pass

def interpret_statements(filename):
    """
    Function that reads statements from the file whose
    name is filename, and prints the result of each statement,
    formatted exactly as described in the psa1 problem statement.  
    interpret_statements must use the evaluate_expression function,
    which appears next in this file.
    """
    variables = {}
    line_num = 0
    value = 0
    opened_file = open(filename, "r")
    # Loop through each line in the file, counting each line
    for line in opened_file:
        line_num += 1
        
        # Gets rid of all comments on the line we are working with
        if line.find("#") >= 0:
            line = line[:line.find("#")]

          
        tokens = line.split()
        # if the line is empty/only had comments we don't compute/print anything for it
        if len(tokens) != 0:
             # check if the line is going to be an assignment statement and then deal with it appropiately 
            try:
                if len(tokens) >= 3 and tokens[1] == "=":
                    if is_valid(tokens[0]): 
                        value = evaluate_expression(tokens[2:], variables)
                        variables[tokens[0]] = value
                        answer = f"{value:0.2f}"
                        print("Line " + str(line_num) + ": " + str( tokens[0] ) + " = " + str(answer))
                
                # last else takes care of a line that only has operations, taking a different approach than an assign statement
                else:
                    value = evaluate_expression(tokens, variables)
                    answer = f"{value:0.2f}"
                    print("Line " + str(line_num) + ":", end =" " )
                    for item in tokens:
                        print(str(item), end =" ")
                    print("= " + str(answer) )   
            except BadStatement:
                print("Line " + str(line_num) + ": Invalid statement")
                


def evaluate_expression(tokens, variables):
    """
    Function that evaluates an expression represented by tokens.
    tokens is a list of strings that are the tokens of the expression.  
    For example, if the expression is "salary + time - 150", then tokens would be
    ["salary", "+", "time", "-", "150"].  variables is a dictionary that maps 
    previously assigned variables to their floating point values.

    Returns the value that is assigned.

    If the expression is invalid, the BadStatement exception is raised.
    """
    final_value = 0.0
    plus = True
    minus = False
    
    # Check if statement starts with, or ends with an operator
    if len(tokens) >= 1:
        if tokens[0] == "+" or tokens[0] == "-" or tokens[0] == "=" or tokens[-1] == "=" or tokens[-1] == "+" or tokens[-1] == "-":
            raise BadStatement
    
    # Iterates through items in tokens, adding or subtracting to the final value, based on the operator
   
    for item in tokens:
        try:
            if item in variables:
                if plus == True:
                    final_value += float(variables[item])
                    plus = False
                elif minus == True:
                    final_value -= float(variables[item])
                    minus = False
                else:
                    # raise Badstatement error if both plus/minus are False, which means two numbers were lined in a row.
                    raise BadStatement
            
            elif item == "+":
                plus = True
            elif item == "-":
                minus = True
            else: 
                if plus == True:
                    final_value += float(item)
                    plus = False
                elif minus == True:
                    final_value -= float(item)
                    minus = False 
                else:
                    # raise Badstatement error if both plus/minus are False, which means two numbers were lined in a row.
                    raise BadStatement    
    
        # The two exceptions we suspect will happen are value errors, and type errors when we convert items to float    
        except ValueError:
            raise BadStatement
        except TypeError:
            raise BadStatement
       
    return final_value

# Checks if the string given is a valid variable name
def is_valid(s):
    if re.fullmatch("[A-Za-z][A-Za-z0-9]*", s):
        return True
    else:
        raise BadStatement

    

# You can add additional helper method(s) if you want.

if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)
