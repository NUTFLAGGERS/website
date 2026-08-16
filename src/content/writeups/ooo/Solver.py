targets = [205, 196, 215, 218, 225, 226, 1189, 2045, 2372, 9300, 8304, 660, 8243, 16057, 16113, 16057, 16004, 16007, 16006, 8561, 805, 346, 195, 201, 154, 146, 223]

flag = ["l"]  # or list("lactf{") and then loop from 5

for i in range(len(targets) - 1):
    next_code = targets[i] - ord(flag[i])
    flag.append(chr(next_code))

print("".join(flag))