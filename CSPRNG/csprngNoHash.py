import os
import hashlib

# https://docs.python.org/3/library/hashlib.html
# Notes: For experiments, could use hashlib's different sha methods like sha256() or sha3_384() (dunno what it would do)
#                         could use different byte lengths

class CSPRNG_no_hash:
    def __init__(self, byte_length) -> None:
        self.byte_length = byte_length
        self.seed = self.generate_seed()

    # Returns 32 random bytes from the operating system random number generator. Useful when we want to compare os
    def generate_seed(self):
        """
        Generates an initial seed with os prng
        Returns: initial seed composed of 32 bytes
        """
        test = os.urandom(self.byte_length)
        # print(len(test))
        return test

    def rand_bytes(self, n):
        """
        Generates random bytes
        Args:
            n: number of bytes
        Returns: n random bytes
        """
        hmac = hashlib.sha256()
        hmac.update(self.seed)
        self.seed = hmac.digest()  # update the self.seed so that next number is different
        return self.seed[:n]
        # we truncate the seed here because sha256 makes hmac.digest() return 32 bytes and we might not always want that

    def rand_int(self, lower, upper):
        """
        Generates random integer
        Args:
            lower: lower bound of the random integer
            upper: upper bound of the random integer
        Returns: random integer x where lower <= x <= upper
        """
        range = upper - lower
        if range <= 0:
            raise ValueError("Upper Bound must be greater than Lower Bound")
        rand_int = int.from_bytes(self.seed, byteorder = 'big')
        return lower + (rand_int % range)


csprng = CSPRNG(32)
print(csprng.rand_int(0, 100))
