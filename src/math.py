class Math():
    def addition(value1, value2):
        if not isinstance(value1, int) and not isinstance(value2, int):
            return 'Invalid input'
        else:
            return value1 + value2

    __fib_cache = {}
    def generate_fibonacci(self, length):
        if length in Math.__fib_cache:
            return Math.__fib_cache[length]
        else:
            if length == 0:
                return 0
            if length == 1 or length == 2:
                return 1
            Math.__fib_cache[length] = Math().generate_fibonacci(length-1) + Math().generate_fibonacci(length-2)
            return Math.__fib_cache[length]


def main():
    print(Math.generate_fibonacci(10))


if __name__ == "__main__":
    main()
