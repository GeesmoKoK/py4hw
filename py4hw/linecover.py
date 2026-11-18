import os
import sys

from .cover import asciiProgressBar


def all_components(circuit):
    components = [circuit]
    for child in circuit.children.values():
        components += all_components(child)
    return components


class LineCoverage:
    def __init__(self, circuit):
        # executed: por cada funcion medida, el conjunto de lineas que se han ejecutado
        self.executed = {}
        # total: por cada funcion medida, todas sus lineas de codigo
        self.total = {}
        for component in all_components(circuit):
            for name in ['propagate', 'clock', 'run']:
                function = getattr(type(component), name, None)
                if function is not None:
                    code = function.__code__
                    self.executed[code] = set()
                    self.total[code] = self.code_lines(code)

    def code_lines(self, code):
        lines = set()
        for start, end, line in code.co_lines():
            if line is not None:
                lines.add(line)
        lines.discard(code.co_firstlineno)    # la linea del 'def' no cuenta
        return lines

    def start(self):
        sys.settrace(self.trace_calls)

    def stop(self):
        sys.settrace(None)

    def trace_calls(self, frame, event, arg):
        if frame.f_code in self.executed:
            return self.trace_lines
        return None

    def trace_lines(self, frame, event, arg):
        if event == 'line':
            self.executed[frame.f_code].add(frame.f_lineno)
        return self.trace_lines

    def covered_and_total(self):
        covered = 0
        total = 0
        for code in self.total:
            covered += len(self.executed[code] & self.total[code])
            total += len(self.total[code])
        return covered, total

    def percent(self):
        covered, total = self.covered_and_total()
        return 100 * covered / total

    def report(self):
        covered, total = self.covered_and_total()
        if total == 0:
            return 'Line coverage: sin lineas que medir'
        lines = ['Line coverage ' + asciiProgressBar(covered, total)]
        for code in self.total:
            missing = sorted(self.total[code] - self.executed[code])
            if missing:
                lines.append('  {} ({}) lineas sin cubrir: {}'.format(
                    code.co_qualname, os.path.basename(code.co_filename), missing))
        return '\n'.join(lines)
