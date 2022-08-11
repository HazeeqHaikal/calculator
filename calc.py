import tkinter as tk
import math
from fractions import Fraction as frac

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
WHITE = "#FFFFFF"
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"
global keys
keys = {}
class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        
        self.total_expression = ""
        self.current_expression = "0"
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), ".": (4, 1)
        }
        self.operators = {
            "/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"
        }
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.bind_keys()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
    
    # global key_press
    def key_press(self, event):
        if event.keysym in keys:
            keys[event.keysym].config(bg=LIGHT_GRAY)
                
    # global key_release
    def key_release(self, event):
        operations = ["plus", "minus", "slash", "asterisk"]
        if event.keysym =="Return" :
            keys["Return"].config(bg=LIGHT_BLUE)
        elif event.keysym in operations:
            keys[event.keysym].config(bg=OFF_WHITE)
        elif event.keysym in keys:
            keys[event.keysym].config(bg=WHITE)

    def bind_keys(self):
        self.window.bind_all("<KeyPress>", self.key_press)
        self.window.bind_all("<KeyRelease>", self.key_release)
        self.window.bind("<Return>", lambda event:self.evaluate())
        self.window.bind("<Delete>", lambda event:self.clear())
        self.window.bind("<BackSpace>", lambda event:self.backspace())
        # self.window.bind("<Delete>", lambda event:self.delete())
        
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit = key: self.add_to_expression(digit))

        
        for key in self.operators:
            self.window.bind(key, lambda event, operator=key:self.append_operator(operator))
    
    def delete(self):
        if(len(self.current_expression.strip()) > 1): 
            self.current_expression = self.current_expression.strip()[1:]
        else:
            self.current_expression = str("0")
        self.update_label()
    
    def backspace(self):
        if(len(self.current_expression.strip()) > 1): 
            self.current_expression = self.current_expression.strip()[:-1]
        else:
            self.current_expression = str("0")
        self.update_label()
    
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_square_root_button()
        # self.create_fraction_button()

    
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression,
                               anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        if(self.current_expression.strip().startswith("0") and str(value) == "0"):
            self.current_expression = str(value)
        elif(self.current_expression.count(".") > 0 and str(value) == "."):
            return
        elif(self.current_expression == "Math Error"): 
            self.current_expression = str(value)
        else:
            self.current_expression = self.current_expression.lstrip("0")
            self.current_expression += str(value)
        self.update_label()
        
    def create_digit_buttons(self):      
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            keys.update({str(digit):button})
            button.grid(row=grid_value[0],column=grid_value[1], sticky=tk.NSEW)
            
    def append_operator(self, operator):
        if(str(self.current_expression) == "0"): 
            self.current_expression = "0"
        self.current_expression += " " + operator + " "
        arguments = self.current_expression.split(" ")
        if(arguments[0] == "" and arguments[2] == ""): 
            self.current_expression = ""
            return
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                            font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            # if(i == 0):
            # operations = ["KP_Add", "KP_Divide", "KP_Multiply", "KP_Subtract"]
            symbol = symbol.replace("+", "plus").replace("\u00F7", "slash").replace("\u00D7", "asterisk").replace("-", "minus")
            keys.update({str(symbol):button})
            button.grid(row=i, column=4, columnspan=1, sticky=tk.NSEW)
            # else:
                # button.grid(row=i, column=4, columnspan=2, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = "0"
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda: self.clear())
        button.grid(row=0, column=1, sticky=tk.NSEW)
        keys.update({"Delete":button})
    
    def fraction(self):
        if(self.current_expression == ""): self.total_expression = "0"
        self.current_expression = str(eval(f"frac( {self.current_expression} )"))
        self.update_label()
    
    def create_fraction_button(self):
        button = tk.Button(self.buttons_frame, text="a/b", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=("Arial", 16), borderwidth=0, command=lambda: self.fraction())
        button.grid(row=0, column=5, columnspan=1, sticky=tk.NSEW)
        
    def square(self):
        if(self.current_expression == ""): self.total_expression = "0"
        self.current_expression = str(eval(f"{self.current_expression} ** 2"))
        self.update_label()
        
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda: self.square())
        button.grid(row=0, column=2, sticky=tk.NSEW)
        
    def square_root(self):
        if(str(self.current_expression) == "0"): 
            self.current_expression = "0"
        else:
            self.current_expression = str(eval(f"math.sqrt( {self.current_expression} )"))
        self.update_label()
        
    def create_square_root_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda: self.square_root())
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.key_press
        self.key_release
        
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
        except Exception:
            self.current_expression = "Math Error"
        finally:
            self.total_expression = ""
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE,
                           fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
        keys.update({str("Return"):button})

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        if expression == "Math Error": expression = "" 
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):
        # self.label.config(text=locale.format_string("%d",  int(self.current_expression[:11]), grouping=True))
        self.label.config(text=self.current_expression[:11])
    
    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
