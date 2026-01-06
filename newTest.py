def beep(a):
    if a > 2:
        b = beep(a-2)
    elif a > -2:
        b = beep(a-1)
    else:
        b = int(a/2)
    return b
c = beep(51)
print(c)