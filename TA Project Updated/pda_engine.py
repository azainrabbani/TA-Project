"""PDA Engine - Pure computation logic (no GUI)"""

class PDA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.stack = ["$"]
        self.steps = []
        self.step_index = 0

    def next_step(self):
        if self.step_index < len(self.steps):
            step = self.steps[self.step_index]
            self.step_index += 1
            return step
        return None

    def load_even_a(self, input_str):
        self.reset()
        for i, ch in enumerate(input_str):
            if ch != "a": return False
            if self.stack[-1] == "A":
                self.stack.pop()
                action = "a,A/ε"
            else:
                self.stack.append("A")
                action = "a,$/A"
            self.steps.append({"step": i+1, "input": ch, "action": action, "stack_top": self.stack[-1], "stack": self.stack[:]})
        return self.stack == ["$"]

    def load_odd_a(self, input_str):
        self.reset()
        for i, ch in enumerate(input_str):
            if ch != "a": return False
            if self.stack[-1] == "A":
                self.stack.pop()
                action = "a,A/ε"
            else:
                self.stack.append("A")
                action = "a,$/A"
            self.steps.append({"step": i+1, "input": ch, "action": action, "stack_top": self.stack[-1], "stack": self.stack[:]})
        return self.stack == ["$", "A"]

    def load_parentheses(self, input_str):
        self.reset()
        for i, ch in enumerate(input_str):
            if ch == "(": 
                self.stack.append("(")
                action = "(,ε/("
            elif ch == ")":
                if self.stack[-1] == "(": 
                    self.stack.pop()
                    action = "),(/ε"
                else: return False
            else: return False
            self.steps.append({"step": i+1, "input": ch, "action": action, "stack_top": self.stack[-1], "stack": self.stack[:]})
        return self.stack == ["$"]

    def load_palindrome_even(self, input_str):
        self.reset()
        n = len(input_str)
        if n % 2 != 0: return False
        for i, ch in enumerate(input_str):
            if i < n//2:
                self.stack.append(ch)
                action = f"{ch},ε/{ch}"
            else:
                if self.stack and self.stack[-1] == input_str[n-1-i]:
                    self.stack.pop()
                    action = f"{ch},{ch}/ε"
                else: return False
            self.steps.append({"step": i+1, "input": ch, "action": action, "stack_top": self.stack[-1] if self.stack else "$", "stack": self.stack[:]})
        return self.stack == ["$"]

    def load_anbn(self, input_str):
        self.reset()
        for i, ch in enumerate(input_str):
            if ch == "a":
                self.stack.append("A")
                action = "a,ε/A"
            elif ch == "b":
                if self.stack and self.stack[-1] == "A":
                    self.stack.pop()
                    action = "b,A/ε"
                else: return False
            else: return False
            self.steps.append({"step": i+1, "input": ch, "action": action, "stack_top": self.stack[-1] if self.stack else "$", "stack": self.stack[:]})
        return self.stack == ["$"]

    def run_simulation(self, language, input_str):
        """Run complete simulation for given language"""
        methods = {
            "Even number of a": self.load_even_a,
            "Odd number of a": self.load_odd_a,
            "Balanced Parentheses": self.load_parentheses,
            "Even Palindrome": self.load_palindrome_even,
            "a^n b^n": self.load_anbn
        }
        return methods.get(language, lambda x: False)(input_str)
