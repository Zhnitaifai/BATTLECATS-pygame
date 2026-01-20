nom = [[1, True], [2, False], [3, True]]
def isTrue(a):
    if a[1]:
        print(a)
        return True
newNom = list(filter(isTrue, nom))
print(newNom)