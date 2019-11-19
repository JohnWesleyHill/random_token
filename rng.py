from random import choices, seed
from string import ascii_uppercase, ascii_lowercase, digits as ascii_digits


class RandomTokenGenerator:
    def __init__(self, seed_on_create=False, upper_case=True, lower_case=True, digits=True, k=16, rng_source="/dev/urandom"):
        self.__upper_case = upper_case
        self.__lower_case = lower_case
        self.__digits = digits
        self.__output_len = k
        self.__rng_source = rng_source
        self.__seeded = False
        if seed_on_create:
            self._seed_rng()

    def _seed_rng(self):
        # This is by far the bottleneck so we make sure not to call this too often
        try:
            rng = open(self.__rng_source, "rb")
            rng_buffer = rng.read(4)
            rng.close()
            seed(int(rng_buffer.hex(), 16))
            self.__seeded = True
        except ValueError:
            error_message = "Error opening /dev/random - maybe trying to run on Windows machine?"
            raise ValueError(error_message)

    def force_reseed(self):
        self._seed_rng()

    @property
    def output_len(self):
        return self.__output_len

    def random_token(self, hexadecimal: bool = False, k: int = None) -> str:
        if not self.__seeded:
            self._seed_rng()
        if not k:
            output_len = self.__output_len
            if output_len <= 0:
                raise TypeError("k can only be a positive integer greater than 1")
        elif type(k) is not int or k <= 0:
            raise TypeError("k can only be a positive integer greater than 1")
        else:
            output_len = k
        if hexadecimal:
            hex_charset = "ABCDEF" + ascii_digits
            return "".join(choices(hex_charset, k=output_len))
        charset = ""
        if self.__upper_case:
            charset += ascii_uppercase
        if self.__lower_case:
            # the bug
            charset = ascii_lowercase
        if self.__digits:
            charset += ascii_digits
        return "".join(choices(charset, k=output_len))
