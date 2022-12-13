import collections


class TMConfiguration():
    """A Turing machine configuration."""
    def __init__(self, state, tape):
        self.state = state
        self.tape = tape

    def __repr__(self):
        """Return a string representation of the configuration."""
        return '\'{}\', {}'.format(
            self.state, self.tape
        )

    def print(self):
        """Print the machine's current configuration in a readable form."""
        print('{current_state}: {tape}\n{current_position}'.format(
            current_state=self.state,
            tape=''.join(self.tape).rjust(
                len(self.tape),
                self.tape.blank_symbol),
            # tape = self.tape.get_symbols_as_str(),
            current_position='^'.rjust(
                self.tape.current_position + len(self.state) + 3
            ),
        ))