def bubble_sort_right_to_left(arr):
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        # Traverse from right to left
        for j in range(n - 1, i, -1):
            if arr[j] < arr[j - 1]:
                # Swap elements
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                swapped = True
        
        # If no swaps happened, the list is already sorted
        if not swapped:
            break
    
    return arr

numbers = [5, 3, 8, 4, 2]

sorted_numbers = bubble_sort_right_to_left(numbers)

print(sorted_numbers)