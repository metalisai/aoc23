vals = {"1": 1,
"2": 2,
"3": 3,
"4": 4,
"5": 5,
"6": 6,
"7": 7,
"8": 8,
"9": 9,
"one": 1,
"two": 2,
"three": 3,
"four": 4,
"five": 5,
"six": 6,
"seven": 7,
"eight": 8,
"nine": 9
}

def findAny(arr, haystack, offset):
    for el in arr:
        match = True
        matchStr = "?"
        for idx in range(len(el)):
            if haystack[offset+idx] != el[idx]:
                match = False
                break
        if match:
            matchStr = el
            return matchStr
    return None

stage1 = True

with open("/home/ttammear/Downloads/input", "r") as f:
    sum = 0
    for line in f:
        arr = []
        for idx in range(len(line)):
            if stage1:
                nums = list(vals.keys())[:9]
            else:
                nums = vals.keys()
            result = findAny(nums, line, idx)
            if result is not None:
                arr.append(result)
        arr = [vals[x] for x in arr]
        sum += arr[0]*10 + arr[-1]
    print(f"sum is {sum}")
