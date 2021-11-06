# def announce(f):
#     def wrapper():
#         print("About to run the function")
#         f()
#         print("Done with the function")
#     return wrapper

# @announce
# def hello():
#     print("Hello, world!")
#     i = 3
#     return i

# hello = hello()
# print(hello)

# def our_decorator(func):
#     def function_wrapper(x):
#         print("Before calling " + func.__name__)
#         func(x)
#         print("After calling " + func.__name__)
#     return function_wrapper

# @our_decorator
# def foo(x):
#     print("Hi, foo has been called with " + str(x))

# foo('Mighty')

# our_decorator("hello")


def my_decorator(func): # takes function below decorator
    def function_wrapper(x): # takes function's values that was called
        i = x + x
        func(i)
        print(i)
    return function_wrapper

@my_decorator
def hello(y):
    print("Hello, World!")

hello(21)