import functools, time, unittest
from bibliopixel.threads import sub

WAIT_FOR_SUB = 0.1


def pause(delay=0.01):
    time.sleep(delay)


def run(input, output, *arg, **kwds):
    pause()

    output.put('first')

    if arg != (1, 2, 3):
        raise ValueError('1 2 3')

    if kwds != dict(a=1):
        raise ValueError('a=1')

    pause()
    output.put('second')


class SubTest(unittest.TestCase):
    def do_test(self, use_subprocess):
        s, input, output = sub.run(
            run, 1, 2, 3, a=1, use_subprocess=use_subprocess)
        self.assertTrue(s.is_alive())
        self.assertEqual(output.get(), 'first')
        self.assertTrue(s.is_alive())
        self.assertEqual(output.get(), 'second')
        pause()
        self.assertFalse(s.is_alive())

    def test_subprocess(self):
        self.do_test(True)

    def test_threading(self):
        self.do_test(False)
