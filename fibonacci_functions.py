import math

def functions_description():
    return """
1. strings_to_chars_to_int(string) It takes a word as input, and returns the ASCII INT values of characters in the word as a list
2. int_list_to_exponential_sum(list) It takes a list of integers and returns the sum of exponentials of those integers
3. fibonacci_numbers(int) It takes an integer, like 6, and returns first 6 integers in a fibonacci series as a list.
"""

def functions_map():
    return {
        "strings_to_chars_to_int": strings_to_chars_to_int,
        "int_list_to_exponential_sum": int_list_to_exponential_sum,
        "fibonacci_numbers": fibonacci_numbers
    }

def strings_to_chars_to_int(string):
    return [ord(char) for char in string]

def int_list_to_exponential_sum(int_list):
    int_list = eval(int_list)
    return sum(math.exp(i) for i in int_list)

def fibonacci_numbers(n):
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]
