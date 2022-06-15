def reverse_digits(num: int) -> int:
    count = 0
    number = num
    reverse_num: int = 0

    while num > 0:
        count += 1
        num = num // 10

    for i in range(count):
        digit = number % 10
        reverse_num += digit * 10 ** (count - i - 1)
        number = number // 10

    return reverse_num


print(reverse_digits(3))






def convert_to_binary(num: int) -> str:
    s: str = ''
    binary: str = ''
    while num > 0:
        q = num % 2
        num = num // 2
        s += str(q)
    for i in range(1, len(s) + 1):
        binary += s[-i]
    return binary


print(convert_to_binary(13))
