
import tm
import exceptions
from configuration import TMConfiguration
from tape import TMTape

class NTM():
    """A nondeterministic Turing machine."""
    def __init__(
            self, *, states, input_symbols, tape_symbols, transitions,
            initial_state, blank_symbol, final_states):
        """Initialize a complete Turing machine."""
        self.states = states
        self.input_symbols = input_symbols
        self.tape_symbols = tape_symbols
        self.transitions = transitions
        self.initial_state = initial_state
        self.blank_symbol = blank_symbol
        self.final_states = final_states
        self.validate()

    def _validate_transition_state(self, transition_state):
        if transition_state not in self.states:
            raise exceptions.InvalidStateError(
                'transition state is not valid ({})'.format(transition_state)
            )

    def _validate_transition_symbols(self, state, paths):
        for tape_symbol in paths.keys():
            if tape_symbol not in self.tape_symbols:
                raise exceptions.InvalidSymbolError(
                    'transition symbol {} for state {} is not valid'.format(
                        tape_symbol, state
                    )
                )

    def _validate_transition_result_direction(self, result_direction):
        if result_direction not in ("L", "N", "R"):
            raise exceptions.InvalidDirectionError(
                'result direction is not valid ({})'.format(result_direction)
            )

    def _validate_transition_result(self, result):
        result_state, result_symbol, result_direction = result
        if result_state not in self.states:
            raise exceptions.InvalidStateError(
                'result state is not valid ({})'.format(result_state)
            )
        if result_symbol not in self.tape_symbols:
            raise exceptions.InvalidSymbolError(
                'result symbol is not valid ({})'.format(result_symbol)
            )
        self._validate_transition_result_direction(result_direction)

    def _validate_transition_results(self, paths):
        for results in paths.values():
            for result in results:
                self._validate_transition_result(result)

    def _validate_transitions(self):
        for state, paths in self.transitions.items():
            self._validate_transition_state(state)
            self._validate_transition_symbols(state, paths)
            self._validate_transition_results(paths)

    def _validate_final_state_transitions(self):
        for final_state in self.final_states:
            if final_state in self.transitions:
                raise exceptions.FinalStateError(
                    'final state {} has transitions defined'.format(
                        final_state))

    def validate(self):
        # """Return True if this NTM is internally consistent."""
        # self._read_input_symbol_subset()
        # self._validate_blank_symbol()
        # self._validate_transitions()
        # self._validate_initial_state()
        # self._validate_initial_state_transitions()
        # self._validate_nonfinal_initial_state()
        # self._validate_final_states()
        self._validate_final_state_transitions()
        return True

    def _get_transitions(self, state, tape_symbol):
        """Get the transition tuples for the given state and tape symbol."""
        if state in self.transitions and tape_symbol in self.transitions[
            state]:            
            #print(self.transitions[state][tape_symbol],state,tape_symbol)
            return self.transitions[state][tape_symbol]

        else:
            return set()

    def _has_accepted(self, configuration):
        """Check whether the given config indicates accepted input."""
        # print(configuration)
        return configuration.state in self.final_states

    def _get_next_configurations(self, old_config):
        """Advance to the next configurations."""
        transitions = self._get_transitions(
            old_config.state, old_config.tape.read_symbol()
        )
        new_configs = set()
        for new_state, new_tape_symbol, direction in transitions:
            tape = old_config.tape
            tape = tape.write_symbol(new_tape_symbol)
            tape = tape.move(direction)
            new_configs.add(TMConfiguration(new_state, tape))
        #print(new_configs)
        return new_configs

    def read_input(self, input_str):
        """
        Check if the given string is accepted by this automaton.
        Return the automaton's final configuration if this string is valid.
        """
        # "Fast-forward" generator to get its final value
        for config in self.read_input_stepwise(input_str):
            pass
        return config

    def read_input_stepwise(self, input_str, count=99999):
        """
        Check if the given string is accepted by this Turing machine.
        Yield the current configurations of the machine at each step.
        """
        current_configurations = {
            TMConfiguration(
                self.initial_state,
                TMTape(input_str, blank_symbol=self.blank_symbol))}
        yield current_configurations
        c = 1
        #print(self.initial_state)
        # The initial state cannot be a final state for a NTM, so the first
        # iteration is always guaranteed to run (as it should)
        while current_configurations:
            new_configurations = set()
            for config in current_configurations:
                # print(config.state, config.tape.tape, config.tape.blank_symbol, config.tape.current_position)
                # config.print()
                if self._has_accepted(config):
                    # One accepting configuration is enough.
                    return
                new_configurations.update(
                    self._get_next_configurations(config))
            current_configurations = new_configurations
            yield current_configurations
            c = c + 1
            if( c == count):
                break

    def printConfig(self, input_str, count):
        """
        Check if the given string is accepted by this Turing machine.
        Yield the current configurations of the machine at each step.
        """
        current_configurations = {
            TMConfiguration(
                self.initial_state,
                TMTape(
                    input_str,
                    blank_symbol=self.blank_symbol))}
        c = 0
        while current_configurations:
            new_configurations = set()
            for config in current_configurations:
                if self._has_accepted(config):
                    return
                new_configurations.update(
                    self._get_next_configurations(config))
            c = c + 1
            current_configurations = new_configurations
            if(c == count):
                yield current_configurations
                break

# a = NTM(
#     states={'q0', 'q1', 'q2'},
#     input_symbols={'0'},
#     tape_symbols={'0'},
#     transitions={
#         'q0': {'0': {('q1', '0', 'R')}},
#         'q1': {'0': {('q2', '0', 'L')}}
#     },
#     initial_state='q0',
#     blank_symbol='.',
#     final_states={'q2'}
# )

ntm1 = NTM(
    states={'q0', 'q1', 'q2', 'q3'},
    input_symbols={'0', '1', '2'},
    tape_symbols={'0', '1', '2', '.'},
    transitions={
        'q0': {
            '0': {('q0', '0', 'R')},
            '1': {('q1', '1', 'R'), ('q2', '1', 'R')},
        },
        'q1': {
            '1': {('q1', '1', 'R')},
            '.': {('q3', '.', 'N')},
        },
        'q2': {
            '2': {('q0', '2', 'R')},
        },
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q3'}
)

# ntm1.read_input('0')
# ntm1.read_input('02')
# print(ntm1.read_input('00120001111'))


ntm2 = NTM(
    states={'q1', 'q2', 'q3', 'q4', 'q5', 'q6'},
    input_symbols={'a', 'b', 'c'},
    tape_symbols={'a', 'b', 'c', '.', '0','1','2'},
    transitions={
        'q1': {
            'a': {('q2', '0', 'R')},
            '1': {('q5', '1', 'R')},
        },
        'q2': {
            'b': {('q3', '1', 'R')},
            '1': {('q2', '1', 'R')},
            'a': {('q2', 'a', 'R')},
        },
        'q3': {
            'b': {('q3', 'b', 'R')},
            '2': {('q3', '2', 'R')},
            'c': {('q4', '2', 'L')},
        },
        'q4': {
            '0': {('q1', '0', 'R')},
            '1': {('q4', '1', 'L')},
            '2': {('q4', '2', 'L')},
            'a': {('q4', 'a', 'L')},
            'b': {('q4', 'b', 'L')},
        },
        'q5': {
            '1': {('q5', '1', 'R')},
            '2': {('q5', '2', 'R')},
            '.': {('q6', '.', 'L')},
        },
    },
    initial_state='q1',
    blank_symbol='.',
    final_states={'q6'}
)
#print(ntm2.read_input('abc'))
#print(ntm2.read_input('aabbcc'))
#print(ntm2.read_input('aaabbbccc'))


ntm3 = NTM(
    states={'q1', 'q2', 'q3', 'q4', 'q5'},
    input_symbols={'a', 'b'},
    tape_symbols={'a', 'b', ' ', 'x'},
    transitions={
        'q1': {
            'x': {('q1', 'x', 'R')},
            'a': {('q2', 'x', 'R')},
            'b': {('q3', 'x', 'R')},
            ' ': {('q5', ' ', 'N')},
        },
        'q2': {
            'b': {('q4', 'x', 'L')},
            'x': {('q2', 'x', 'R')},
            'a': {('q2', 'a', 'R')},
        },
        'q3': {
            'b': {('q3', 'b', 'R')},
            'x': {('q3', 'x', 'R')},
            'a': {('q4', 'x', 'L')},
        },
        'q4': {
            ' ': {('q1', ' ', 'R')},
            'x': {('q4', 'x', 'L')},
            'a': {('q4', 'a', 'L')},
            'b': {('q4', 'b', 'L')},
        },

    },
    initial_state='q1',
    blank_symbol=' ',
    final_states={'q5'}
)

#print(ntm3.read_input('ab'))
#print(ntm3.read_input('aabb'))
print(ntm3.read_input('aaabb'))

#print config
for configs in ntm2.printConfig("aabbcc",7):
    print(configs)
print('*****')
#print history
for configs in ntm2.read_input_stepwise("aabbcc",7):
    print(configs)
