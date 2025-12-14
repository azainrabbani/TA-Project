from collections import deque, namedtuple

Configuration = namedtuple("Configuration", ["state", "position", "stack", "trace"])

class NPDA:
    def __init__(self, pda):
        self.states = pda["states"]
        self.start_state = pda["start_state"]
        self.accept_states = pda["accept_states"]
        self.start_stack_symbol = pda["start_stack_symbol"]
        self.transitions = pda["transitions"]

    def simulate(self, input_string):
        queue = deque()
        queue.append(
            Configuration(
                self.start_state,
                0,
                [self.start_stack_symbol],
                []
            )
        )

        visited = set()

        while queue:
            current = queue.popleft()
            state, pos, stack, trace = current

            key = (state, pos, tuple(stack))
            if key in visited:
                continue
            visited.add(key)

            # ACCEPT condition
            if pos == len(input_string) and state in self.accept_states:
                return True, trace

            next_input = input_string[pos] if pos < len(input_string) else ""
            stack_top = stack[-1] if stack else None

            for t in self.transitions:
                if t["from"] == state and t["pop"] == stack_top:
                    if t["input"] == next_input or t["input"] == "":
                        new_stack = stack[:-1] + t["push"]
                        new_pos = pos + (1 if t["input"] != "" else 0)

                        description = (
                            f"State: {state} → {t['to']} | "
                            f"Read: {t['input'] or 'ε'} | "
                            f"Stack: {stack} → {new_stack}"
                        )

                        queue.append(
                            Configuration(
                                t["to"],
                                new_pos,
                                new_stack,
                                trace + [description]
                            )
                        )

        return False, trace
