import unittest
from rng import RandomTokenGenerator
from string import ascii_lowercase, ascii_uppercase, digits as ascii_digits

DEFAULT_CHARSET = set(ascii_digits + ascii_lowercase + ascii_uppercase)
HEX_CHARSET = set("ABCDEF" + ascii_digits)


class RNGTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = RandomTokenGenerator()

    def test_default(self):
        output_len = self.rng.output_len
        output = self.rng.random_token()
        self.assertEqual(len(output), output_len)

        for x in range(0, output_len):
            self.assertEqual(output[x] in DEFAULT_CHARSET, True)

    def test_invalid_k(self):
        rng = RandomTokenGenerator()
        with self.assertRaises(TypeError):
            rng.random_token(k="a")

    def test_invalid_output_length(self):
        with self.assertRaises(TypeError):
            rng = RandomTokenGenerator(k=-1)
            output = rng.random_token()

    def test_hexadecimal(self):
        output = self.rng.random_token(hexadecimal=True, k=8)
        self.assertEqual(len(output), 8)

        for x in range(0,8):
            self.assertEqual(output[x] in HEX_CHARSET, True)

    def test_caps_only(self):
        rng = RandomTokenGenerator(upper_case=True, lower_case=False, digits=False)
        output = rng.random_token()
        self.assertEqual(len(output), rng.output_len)

        for x in range(0, rng.output_len):
            self.assertEqual(output[x] in ascii_uppercase, True)

    def test_rng_source(self):
        with self.assertRaises(ValueError):
            rng = RandomTokenGenerator(rng_source="/dev/null", seed_on_create=True)

    def test_reseed(self):
        self.rng.force_reseed()
        output = self.rng.random_token(hexadecimal=True)

        for x in range(0, len(output)):
            self.assertEqual(output[x] in HEX_CHARSET, True)


if __name__ == '__main__':
    unittest.main()
