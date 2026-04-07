import tkinter as tk


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.expression = ""
        self._create_widgets()
        self._bind_keys()

    def _create_widgets(self):
        self.display = tk.Entry(self, font=("Segoe UI", 24), justify="right", bd=4, relief="ridge")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.display.insert(0, "0")
        self.display.config(state="readonly")

        buttons = [
            ("C", 1, 0, self.clear),
            ("⌫", 1, 1, self.backspace),
            ("(", 1, 2, lambda: self._append("(")),
            (")", 1, 3, lambda: self._append(")")),
            ("7", 2, 0, lambda: self._append("7")),
            ("8", 2, 1, lambda: self._append("8")),
            ("9", 2, 2, lambda: self._append("9")),
            ("÷", 2, 3, lambda: self._append("/")),
            ("4", 3, 0, lambda: self._append("4")),
            ("5", 3, 1, lambda: self._append("5")),
            ("6", 3, 2, lambda: self._append("6")),
            ("×", 3, 3, lambda: self._append("*")),
            ("1", 4, 0, lambda: self._append("1")),
            ("2", 4, 1, lambda: self._append("2")),
            ("3", 4, 2, lambda: self._append("3")),
            ("-", 4, 3, lambda: self._append("-")),
            ("0", 5, 0, lambda: self._append("0")),
            (".", 5, 1, lambda: self._append(".")),
            ("=", 5, 2, self.calculate),
            ("+", 5, 3, lambda: self._append("+")),
        ]

        for (text, row, col, command) in buttons:
            button = tk.Button(self, text=text, command=command, font=("Segoe UI", 18), width=4, height=2)
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def _bind_keys(self):
        allowed_keys = "0123456789+-*/()."
        self.bind("<Key>", lambda event: self._on_key(event, allowed_keys))
        self.bind("<Return>", lambda event: self.calculate())
        self.bind("<BackSpace>", lambda event: self.backspace())
        self.bind("<Escape>", lambda event: self.clear())

    def _on_key(self, event, allowed_keys):
        key = event.char
        if key in allowed_keys:
            self._append(key)
        elif key == "\r":
            self.calculate()

    def _append(self, value):
        if self.expression == "0" and value not in ".+-*/()":
            self.expression = value
        else:
            self.expression += value
        self._update_display(self.expression)

    def _update_display(self, text):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, text)
        self.display.config(state="readonly")

    def clear(self):
        self.expression = ""
        self._update_display("0")

    def backspace(self):
        self.expression = self.expression[:-1]
        self._update_display(self.expression if self.expression else "0")

    def calculate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression, {"__builtins__": None}, {})
            self.expression = str(result)
            self._update_display(self.expression)
        except Exception:
            self.expression = ""
            self._update_display("Error")


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
