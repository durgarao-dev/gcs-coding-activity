# function to sort and find median of a list of numbers
import random
def sortAndFindMedian(numbers):
    if len(numbers) == 0:
        return "List is empty"
    else:
        sorted_numbers =sortNumbers(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            return (sorted_numbers[int(n/2) - 1] + sorted_numbers[int(n/2)]) / 2
        else:
            return numbers[int(n/2)]
        
def sortNumbers(numbers):
    length = len(numbers)
    if length <= 1:
        return numbers
    else:
        pivot = numbers.pop(random.randint(0, length-1))
        less = []
        greater = []
        for i in numbers:
            if i <= pivot:
                less.append(i)
            else:
                greater.append(i)
        return sortNumbers(less) + [pivot] + sortNumbers(greater)
    
numbers1 = [] # empty list
numbers2  = [1,14,5,34,23]
print("Input List: {}\n".format(numbers1))
print("Sorted List: {}\n".format(sortNumbers(numbers1)))
print("Median Value of the List:{}\n\n".format(sortAndFindMedian(numbers1)))
print("Input List: {}\n".format(numbers2))
print("Sorted List: {}\n".format(sortNumbers(numbers2)))
print("Median Value of the List:{}\n\n".format(sortAndFindMedian(numbers2)))
