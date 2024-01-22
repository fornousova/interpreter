class Interpreter:
    def __init__(self):
        self.variables = {}
        self.current_indentation = 0
        self.current_line = 0
        self.lines = []


    def run(self, code):
        self.lines = code.split('\n')
        self.execute_block()

    def execute_line(self):
        tokens = self.lines[self.current_line].split()
        if len(tokens) == 0:
            return

        if tokens[0] == 'cele':
            self.declare_variable(tokens)
        elif tokens[0] == 'kdyz':
            self.execute_if(tokens)
        elif tokens[0] == 'pro':
            self.execute_for(tokens)
        elif tokens[0] == 'vypis':
            self.execute_print(tokens)
        else:
            self.execute_assignment(tokens)

    def declare_variable(self, tokens):
        # Příklad: int i
        var_name = tokens[1]
        self.variables[var_name] = None

    def execute_assignment(self, tokens):
        # Příklad: X = Y + 3
        var_name = tokens[0]
        value = self.evaluate_expression(tokens[2:])
        self.variables[var_name] = value

    def evaluate_expression(self, tokens):
        if tokens[0].startswith('"') and tokens[-1].endswith('"'):
            # It's a string literal, remove quotes and return
            return ' '.join(tokens)

        # Evaluace jednoduchého výrazu (pouze sčítání, odčítání, násobení, dělení)
        result = None
        current_operator = None

        for token in tokens:
            if token in ['+', '-', '*', '/', '==','<','>']:
                current_operator = token
            else:
                if result is None:
                    result = self.get_variable_value(token)
                else:
                    value = self.get_variable_value(token)
                    result = self.apply_operator(result, current_operator, value)

        return result

    def get_variable_value(self, var_name):
        if var_name.isnumeric():
            return int(var_name)
        elif var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"Variable {var_name} not declared")

    def apply_operator(self, left, operator, right):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '==':
            return left == right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right

    def execute_if(self, tokens):
        # Příklad: if X == Y: ...
        condition = self.evaluate_expression(tokens[1:])
        self.current_indentation += 1
        self.current_line += 1
        if condition:
            self.execute_block()
        else:
            # If the condition is not met, skip the block
            self.skip_block()
        self.current_indentation -= 1

    def execute_for(self, tokens):
        # Příklad: for i in range(3): ...
        var_name = tokens[1]
        range_end = int(tokens[3])
        current_line = self.current_line + 1
        for i in range(range_end):
            self.variables[var_name] = i
            self.current_indentation += 1
            self.current_line = current_line
            self.execute_block()
            self.current_indentation -= 1

    def execute_block(self):
        # Metoda pro vykonání bloku kódu
        while self.current_line < len(self.lines):

            line = self.lines[self.current_line]

            # Ignorovat prázdné řádky
            if line.strip() == '':
                self.current_line += 1
                continue

            # Zjistit úroveň odsazení aktuálního řádku
            current_indentation = len(line) - len(line.lstrip())

            # Porovnat s aktuální úrovní odsazení
            if current_indentation == self.current_indentation:
                # Řádek patří do aktuálního bloku
                self.execute_line()
                self.current_line += 1
            elif current_indentation < self.current_indentation:
                # Snížení úrovně odsazení, ukončení bloku
                self.current_line -= 1
                return
            else:
                # Neplatné odsazení
                raise Exception("Invalid indentation in the code")

    def skip_block(self):
        while self.current_line < len(self.lines):

            line = self.lines[self.current_line]

            # Ignorovat prázdné řádky
            if line.strip() == '':
                self.current_line += 1
                continue
            
            # Zjistit úroveň odsazení aktuálního řádku
            current_indentation = len(line) - len(line.lstrip())

            # Porovnat s aktuální úrovní odsazení
            if current_indentation == self.current_indentation:
                # Řádek patří do aktuálního bloku
                self.current_line += 1
            elif current_indentation < self.current_indentation:
                # Snížení úrovně odsazení, ukončení bloku
                self.current_line -= 1
                return
            else:
                # Neplatné odsazení
                raise Exception("Invalid indentation in the code")

    def execute_print(self, tokens):
        value = self.evaluate_expression(tokens[1:])
        print(value)

# Příklad použití
interpreter = Interpreter()
code = """
cele i
X = 4
Y = 5
kdyz X == Y
 vypis "X je rovno Y"
kdyz X > Y
 vypis "X je vetsi nez Y"
kdyz X < Y
 vypis "X je mensi nez Y"
pro i do 1000
 vypis i + 1
"""
interpreter.run(code)
