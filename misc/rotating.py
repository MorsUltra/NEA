def rotate_right(arr, l, r):
    temp = arr[r]
    for i in range(r, l, -1):
        arr[i] = arr[i - 1]
    arr[l] = temp

    return arr

def rotate_left(arr, l, r):
    temp = arr[l]
    for i in range(l, r):
        arr[i] = arr[i+1]
    arr[r] = temp
