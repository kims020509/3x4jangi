test = [1,2,3,4,5]

for idx in range(len(test)):
    temp = test[idx]
    del test[idx]
    print(test)
    test.insert(idx, temp)
print(test)

