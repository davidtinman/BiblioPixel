import copy, unittest
from bibliopixel.project import fix
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix


def fix_before(desc):
    return fix.fix_before_recursion(desc)


def fix_after(desc):
    return fix.fix_after_recursion(desc)


class FixTest(unittest.TestCase):
    def test_both(self):
        actual = fix_before({'layout': 'matrix', 'drivers': []})
        expected = {
            'layout': 'matrix',
            'drivers': fix.DEFAULT_DRIVERS}
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(
            fix_before({}),
            {'drivers': fix.DEFAULT_DRIVERS})

    def test_drivers_one(self):
        self.assertEqual(
            fix_before({'driver': 'lpd8806'}),
            {'drivers': [{'typename': 'lpd8806'}]})

    def test_layout(self):
        source = {
            'drivers': [{}],
            'run_animation': {
                'animation': {
                    'datatype': BaseMatrixAnim,
                    'width': 23,
                    'height': 32,
                    'wombat': 7,
                },
                'run': {},
            }
        }
        actual = fix_after(copy.deepcopy(source))
        expected = dict(
            source, layout={'datatype': Matrix, 'width': 23, 'height': 32})
        self.assertEqual(actual, expected)
