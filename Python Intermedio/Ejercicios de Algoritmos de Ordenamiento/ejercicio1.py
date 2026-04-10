def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        swapped = False  # Track if a swap happens
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps happened, the list is already sorted
        if not swapped:
            break
    
    return arr

numbers = [5, 3, 8, 7, 2]

sorted_numbers = bubble_sort(numbers)

print(sorted_numbers)