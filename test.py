import math

def zero_one(arr, i, j):
    if len(arr) == 0:
        return 0
    q = math.floor((i+j)/2)
    if arr[q] == 1:
        if arr[q+1] == 0:
            return j-q
        else:
            return zero_one(arr, q+1, j)
    else:
        if arr[q-1] == 1:
            return j-q+1
        else:
            return zero_one(arr, i, q-1) + j-q+1
        
print(zero_one([1,1,1,0,0,0,0,0], 0, 7))