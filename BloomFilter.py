import math


class BloomFilter():
    def __init__(self, estimated_elements, false_positive_rate):
        self.M = 2 ** 31 - 1
        self.size_m = round(-estimated_elements * math.log2(false_positive_rate) / math.log(2))
        self.hash_count = round(-math.log2(false_positive_rate))
        self.primes = []
        self.generate_numbers(self.hash_count + 1)
        self.bits = BitArray(self.size_m)


    def generate_numbers(self, count):
        candidate = 2
        while len(self.primes) < count:
            is_prime = True
            for prime in self.primes:
                if prime * prime > candidate:
                    break
                if candidate % prime == 0:
                    is_prime = False
                    break
            if is_prime:
                self.primes.append(candidate)
            candidate += 1 if candidate == 2 else 2

    def hash_function(self, value, index):
        return (((index + 1) * value + self.primes[index]) % self.M) % self.size_m

    def add_element(self, item):
        for i in range(self.hash_count):
            self.bits.set_bit(self.hash_function(item, i))

    def contains(self, item):
        for i in range(self.hash_count):
            if not self.bits.check_bit(self.hash_function(item, i)):
                return False
        return True

    def get_bit_representation(self):
        return self.bits.display_bits()

class BitArray():
    def __init__(self, size):
        self.size = size
        self.data = bytearray(math.ceil(size / 8))

    def set_bit(self, index):
        self.data[index // 8] |= (1 << (7 - (index % 8)))

    def check_bit(self, index):
        return (self.data[index // 8] & (1 << (7 - (index % 8)))) != 0

    def display_bits(self):
        result = ''
        for byte in self.data:
            bits = bin(byte)[2:]
            bits = bits.zfill(8)
            result += bits
        return result[:self.size]

if __name__ == "__main__":
    initialized = False
    while True:
        try:
            user_input = input()
            if user_input:
                parts = user_input.split(" ")
                cmd = parts[0]
                try:
                    if cmd == "set" and len(parts) == 3 and not initialized:
                        if int(parts[1]) <= 0:
                            raise Exception('error')
                        num_of_elements = int(parts[1])
                        if float(parts[2]) <= 0 or float(parts[2]) >= 1:
                            raise Exception('error')
                        false_positive = float(parts[2])
                        bloom_filter = BloomFilter(num_of_elements, false_positive)
                        if bloom_filter.size_m == 0 or bloom_filter.hash_count == 0:
                            del bloom_filter
                            raise Exception('error')
                        print(f"{bloom_filter.size_m} {bloom_filter.hash_count}")
                        initialized = True

                    elif cmd == "add" and len(parts) == 2:
                        try:
                            bloom_filter.add_element(int(parts[1]))
                        except:
                            raise Exception('error')

                    elif cmd == "search" and len(parts) == 2:
                        try:
                            if bloom_filter.contains(int(parts[1])):
                                print('1')
                            else:
                                print('0')
                        except:

                            raise Exception('error')

                    elif cmd == "print" and len(parts) == 1:
                        try:
                            print(bloom_filter.get_bit_representation())
                        except:
                            raise Exception('error')
                    else:
                        raise Exception('error')
                except Exception as error:
                    print(error)

        except EOFError:
            break
