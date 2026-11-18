import pytest

from py4hw.cover import asciiProgressBar

def pytest_addoption(parser):
    parser.addoption(
        "--deep_random",
        action="store_true",
        default=False,
        help="Run full / extended iteration tests"
    )


@pytest.fixture
def is_deep_random(request):
    if request.config.getoption("--deep_random"):
        return True  # High iterations for individual runs
    return False   #


test_classes = []


def pytest_collection_modifyitems(items):
    for item in items:
        if item.cls is not None and item.cls not in test_classes:
            test_classes.append(item.cls)


def pytest_terminal_summary(terminalreporter):
    coverages = {}
    for cls in test_classes:
        if hasattr(cls, 'cov'):
            coverages[cls.__module__ + '.py::' + cls.__name__] = cls.cov
    table = ['| Test | Cobertura toggle | Bits cubiertos | Bits totales |',
             '|---|---|---|---|']
    details = []
    for name, cov in sorted(coverages.items()):
        covered, total = cov.covered_and_total()
        table.append('| {} | {:.1f}% | {} | {} |'.format(name, 100 * covered / total, covered, total))
        details.append('### {}\n```\n{}\n```'.format(name, cov.report()))
    text = '# Cobertura de toggle\n\n' + '\n'.join(table) + '\n\n' + '\n\n'.join(details) + '\n'

    # Cobertura de linea: solo las clases que la usan (de momento Test_LineCoverage)
    line_details = []
    for cls in test_classes:
        if hasattr(cls, 'line'):
            name = cls.__module__ + '.py::' + cls.__name__
            line_details.append('### {}\n```\n{}\n```'.format(name, cls.line.report()))
    text += '\n# Cobertura de linea\n\n' + '\n\n'.join(line_details) + '\n'

    terminalreporter.write_sep('=', 'Toggle coverage por clase')
    for name, cov in sorted(coverages.items()):
        terminalreporter.write_line('{:<50} {}'.format(name, asciiProgressBar(*cov.covered_and_total())))
    terminalreporter.write_sep('=', 'Line coverage')
    for cls in test_classes:
        if hasattr(cls, 'line'):
            terminalreporter.write_line(cls.__module__ + '.py::' + cls.__name__)
            terminalreporter.write_line(cls.line.report())
    with open(terminalreporter.config.rootpath / 'coverage_report.md', 'w') as f:
        f.write(text)
    terminalreporter.write_line('Informe completo en coverage_report.md')
