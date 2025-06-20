class Evaluator:
    operations = {
        '+': lambda number_1, number_2: number_1 + number_2,
        '-': lambda number_1, number_2: number_1 - number_2,
        '/': lambda number_1, number_2: number_1 / number_2,
        '*': lambda number_1, number_2: number_1 * number_2
    }


    @staticmethod
    def get_parsed_expression(expression: str) -> int:
        expression_data = []
        
        index = 0
        while index < len(expression):
            if expression[index] == ' ':
                index += 1
                continue
            
            match expression[index]:
                # this adds suppport for + signed expression
                case '+':
                    # if the next character is a string representation of an integer than we assume this is a signed integer
                    if '0' <= expression[index + 1] <= '9':
                        expression_data.append(int(expression[index] + expression[index + 1]))
                        index += 2
                    else:
                        expression_data.append(expression[index])
                        index += 1
                # this adds suppport for - signed expression
                case '-':
                    # if the next character is a string representation of an integer than we assume this is a signed integer
                    if '0' <= expression[index + 1] <= '9':
                        expression_data.append(int(expression[index] + expression[index + 1]))
                        index += 2
                    else:
                        expression_data.append(expression[index])
                        index += 1
                # anything which != ('+', '-', ' ') is added
                # if we have an integer as a string we first convert it to an int and then add it, else we add whatever else we have as it is
                case _:
                    expression_data.append(int(expression[index]) if '0' <= expression[index] <= '9' else expression[index])
                    index += 1
                    
        return expression_data


    @staticmethod
    def is_decimal(value: any):
        value = str(value)
        
        if '.' in value:
            after_decimal_values = value.split('.')[1]
            for value in after_decimal_values:
                if value != '0':
                    return True
        
        return False

    
    @classmethod
    def check_expression_validity(cls, expression: list) -> None:
        # this tests for incorrect operator placement, examples -> (' + 1 1', '(1 2 -) / 2', etc...)
        def check_incorrect_operator_placement():
            for index in range(len(expression)):
                if expression[index] not in cls.operations:
                    continue
                
                if (expression[index - 1] == ')' and
                    (expression[index + 1] == '(' or '0' <= str(expression[index + 1]) <= '9')):
                    continue
                    
                if (expression[index + 1] == '(' and
                    (expression[index - 1] == ')' or '0' <= str(expression[index - 1]) <= '9')):
                    continue
                
                if not ('0' <= str(expression[index - 1]) <= '9' and 
                    '0' <= str(expression[index + 1]) <= '9'):
                    raise Exception
        
        # this checks if each opening bracket has a closing bracket...
        # if we have more opening brackets at the end or if the number of closing brackets are more than opening at any point we raise an error
        def check_for_opening_and_closing_brackets_equality():
            open_brackets = 0
            
            for character in expression:
                match character:
                    case '(':
                        open_brackets += 1
                    case ')':
                        open_brackets -= 1
                
                if open_brackets < 0: 
                    raise Exception
            
            if open_brackets > 0:
                raise Exception
        
        # checks for the consecutive numbers, for example -> '4 + (12 / (1 * 2))' would return 4...though it should return None as 12 > 9 and only 0-9 signed decimals are allowed
        def check_consecutive_number_case():
            for index in range(len(expression)):
                if '0' <= str(expression[index]) <= '9':
                    if index + 1 < len(expression):
                        if '0' <= str(expression[index + 1]) <= '9':
                            raise Exception
        
        # checks for the presence of illegal operators, egamples -> '$', '&', %', etc...
        def check_invalid_characters():
            for character in expression:
                if (character not in ('(', ')') and 
                    not '0' <= str(character) <= '9' and
                    character not in cls.operations):
                    raise Exception
                        
        
        check_incorrect_operator_placement()
        check_for_opening_and_closing_brackets_equality()
        check_consecutive_number_case()
        check_invalid_characters()
        
        
    @classmethod
    def computed_value(cls, characters_stack: list, number: int) -> int:
        # we can have a case such as '1 + (10 + 1)'...
        # according to the code, we will get to point such as '1 + (11)'...
        # in this case after removing the brackets...we will need to check if the value needs to be computed with anything...
        # this function does just that and returns the computed value
        value = number

        if characters_stack and characters_stack[-1] in cls.operations:
            operater, pre_computer_value = characters_stack.pop(), characters_stack.pop()
            value = cls.operations[operater](pre_computer_value, value)

        return value


    @classmethod
    def expression_evaluator(cls, expression: str) -> int:
        """takes a string expression and returns the evaluated result

        Args:
            expression (string): expression to be evaluated
        """
        
        if type(expression) != str:
            return None
        
        # converting the string expression to an array based on if a character != ' ' (we basically ignore all the whitespaces)
        expression = Evaluator.get_parsed_expression(expression)
        
        # we test the expression for validity, and if an error is raied then we return None
        try:
            cls.check_expression_validity(expression)
        except:
            return None
        
        #  if the expression passes the validity tests, then we initiate the computation
        try:
            #  certain edge cases can slip by... such as division by 0 or empty brackets (altough empty brackets will throw an error and None will be returned)
            result = Evaluator.evaluate_expression(expression)
            return result
        except:
            return None


    @classmethod
    def evaluate_expression(cls, expression: list) -> int:
        # we can use a stack based approach
        characters_stack = []
        
        for character in expression:
            # if the character is an operater then add it to the stack and proceed
            if character in cls.operations:
                characters_stack.append(character)
                continue
            
            match character:
                # if it is an opening bracket then append it to the stack and move on
                case '(':
                    characters_stack.append(character)
                # if it is a closing bracket then we can safely assume we have an evaluated value and a opening bracket before this....
                #  so we pop both of these from the stack and append the evaluated number back to the stack
                case ')':
                    pre_evaluated_number, _ = characters_stack.pop(), characters_stack.pop()
                    characters_stack.append(cls.computed_value(characters_stack, pre_evaluated_number))
                # in the case we have an integer...
                # if the list is currently empty  or if the last seen character was an opening bracket then we add the integer and move on
                # else we can safely assume we have an operater and another number before this...
                # so we pop both of these off, carry out the correct computation and append the result onto the stack
                case _:
                    characters_stack.append(cls.computed_value(characters_stack, character))
        
        # the final result would be the last element remaining on the stack
        final_result = characters_stack[0]
        
        # I also had to figure out how to deal with decimals...
        # for example 1 / 1 should give 1 in unit tests but python's division operator would return 1.0...
        # so i also check if the result has a decimal and a non zero value after the deciaml point to return the same...else we return int(final_result)
        return final_result if Evaluator.is_decimal(final_result) else int(final_result)
