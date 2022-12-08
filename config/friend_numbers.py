n: int = 1000

for i in range(2, n, 1):
    s1 = 0
    for j in range(1, i, 1):
        if i % j == 0:
            s1 += j
    s2 = 0
    for k in range(1, s1, 1):
        if s1 % k == 0:
            s2 += k

    if s1 == s2:
        print(s1, s2)

