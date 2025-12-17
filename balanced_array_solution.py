"""
Solution for the Balanced Array Problem

Problem: Given an array of integers, find the minimum number of elements that must be removed
so that the array becomes balanced. An array is balanced if the largest number is at most
twice the smallest number.

You can:
- Remove any number of elements from the array
- Change at most one element to any positive integer you choose

Constraints:
- 2 ≤ size of arr ≤ 2 * 10^5
- 1 ≤ arr[i] ≤ 10^9
"""


def min_removal(arr):
    """
    Find the minimum number of elements to remove to make the array balanced.

    Args:
        arr: List of integers

    Returns:
        Minimum number of elements to remove

    Algorithm:
    1. Sort the array
    2. For each possible contiguous range [i, j] in the sorted array:
       - Case 1: Keep all elements without changing (check if arr[j] <= 2 * arr[i])
       - Case 2: Change the first element (check if arr[j] <= 2 * arr[i+1])
       - Case 3: Change the last element (check if arr[j-1] <= 2 * arr[i])
    3. Return n - max_keep (where max_keep is the maximum elements we can keep)

    Time Complexity: O(n^2) where n is the length of the array
    Space Complexity: O(1) excluding the space for sorting
    """
    n = len(arr)

    # Edge case: if array has only 1 element, we can't make it balanced
    # (need at least 2 elements)
    if n == 1:
        return 0

    # Sort the array to easily find min and max in any range
    sorted_arr = sorted(arr)

    max_keep = 0

    # Try all possible contiguous ranges [i, j]
    for i in range(n):
        for j in range(i, n):
            length = j - i + 1

            # Case 1: Don't change any element
            # Check if arr[j] <= 2 * arr[i]
            if sorted_arr[j] <= 2 * sorted_arr[i]:
                max_keep = max(max_keep, length)

            # Case 2: Change the first element (need at least 2 elements)
            # After changing first element, min becomes arr[i+1], max is arr[j]
            # Check if arr[j] <= 2 * arr[i+1]
            if j > i and sorted_arr[j] <= 2 * sorted_arr[i + 1]:
                max_keep = max(max_keep, length)

            # Case 3: Change the last element (need at least 2 elements)
            # After changing last element, min is arr[i], max becomes arr[j-1]
            # Check if arr[j-1] <= 2 * arr[i]
            if j > i and sorted_arr[j - 1] <= 2 * sorted_arr[i]:
                max_keep = max(max_keep, length)

    # Return the minimum number of elements to remove
    return n - max_keep


def main():
    """Test the solution with the provided examples."""

    # Example 1
    arr1 = [7, 4, 2, 3, 12, 9]
    result1 = min_removal(arr1)
    print(f"Example 1:")
    print(f"Input: arr = {arr1}")
    print(f"Output: {result1}")
    print(f"Expected: 2")
    print(f"Correct: {result1 == 2}")
    print()

    # Example 2
    arr2 = [4, 6, 2, 9, 8, 7, 3]
    result2 = min_removal(arr2)
    print(f"Example 2:")
    print(f"Input: arr = {arr2}")
    print(f"Output: {result2}")
    print(f"Expected: 2")
    print(f"Correct: {result2 == 2}")
    print()

    # Additional test cases
    print("Additional Test Cases:")

    # Test case 3: Already balanced
    arr3 = [1, 2]
    result3 = min_removal(arr3)
    print(f"Test 3 (already balanced): arr = {arr3}, result = {result3}, expected = 0")

    # Test case 4: Need to remove all but 2
    arr4 = [1, 100, 50]
    result4 = min_removal(arr4)
    print(f"Test 4: arr = {arr4}, result = {result4}")

    # Test case 5: All elements the same
    arr5 = [5, 5, 5, 5]
    result5 = min_removal(arr5)
    print(f"Test 5 (all same): arr = {arr5}, result = {result5}, expected = 0")


if __name__ == "__main__":
    main()
