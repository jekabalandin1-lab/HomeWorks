#try:
#    a = int(input("a:"))
#    print(1/a)
#except ZeroDivisionError as zde:
#    print("На 0 ділити не можна")


#########2
#list = {"u1":"10-11",
   #     "u2":"11-12",
    #    "u3":"12-13"}

#try:
 #  print(list[input("user: ")])
#except KeyError as ke:
 #   print("User not found")


#########3

from colorama import init, Fore, Back, Style
init()

a = input(Fore.YELLOW +"a:")

try:
    print(Fore.BLUE + f'{int(a)}')
except ValueError as ve:
    print(Fore.RED + "Неможливо конвертувати в число")