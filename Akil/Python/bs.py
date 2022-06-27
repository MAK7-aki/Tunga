def binary_search(arr,low,high,x):
    mid=0

    while low <= high:

        mid= int((low+high)/2)

        if arr[mid] == x:
            return mid

        elif arr[mid]<x:
            low = mid+1

        elif arr[mid]>x:
            high = mid-1

        
    return -1


arr = [1,5,9,12,23,45]
x=23

k=binary_search(arr,0,len(arr)-1,x)
print(k)