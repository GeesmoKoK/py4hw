import math

from .base import Logic


def all_wires(circuit):
    wires = list(circuit._wires.values())
    for child in circuit.children.values():
        wires += all_wires(child)
    return wires


def asciiProgressBar(n, t):
    p = n * 100 / t
    pl = 45
    pok = math.ceil(pl * n / t)
    pko = pl - pok

    sok = '█' * pok
    sko = '░' * pko
    sp = '{:.1f} %'.format(p)
    return '{:8} |{}{}|'.format(sp, sok, sko)


class ToggleCoverage(Logic):
    def __init__(self, parent, name='toggle_cov'):
        wires = all_wires(parent)
        super().__init__(parent, name)
        self.wires = wires
        self.last = {} 
        self.rise = {w: 0 for w in wires}
        self.fall = {w: 0 for w in wires}

    def monitor(self):
        for w in self.wires:
            now = w.get()
            before = self.last.get(w, now)
            changed = before ^ now
            self.rise[w] |= changed & now
            self.fall[w] |= changed & before
            self.last[w] = now

    def covered_bits(self, w):
        return (self.rise[w] & self.fall[w]).bit_count()

    def covered_and_total(self):
        covered = sum(self.covered_bits(w) for w in self.wires)
        total = sum(w.getWidth() for w in self.wires)
        return covered, total

    def percent(self):
        covered, total = self.covered_and_total()
        return 100 * covered / total

    def report(self):
        lines = ['Toggle coverage ' + asciiProgressBar(*self.covered_and_total())]
        for w in self.wires:
            missing = [i for i in range(w.getWidth())
                       if not (self.rise[w] & self.fall[w]) >> i & 1]
            if missing:
                lines.append('  {} bits sin cubrir: {}'.format(w.getFullPath(), missing))
        return '\n'.join(lines)
