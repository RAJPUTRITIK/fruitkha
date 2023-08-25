def fun1():
    global a
    a='wow'

def fun2():
    print(a)

fun1()
fun2()



n=5
if all(n%i !=0 for i in range(2,n)):
    print('prime num')
else:
    print('not prime')

# a=14
# b=4
# print(True & False)
# print(a and b)

# a=True
# b=True
# print( a & b)

# i.product.price|mul:i.quantity
							

# print('ritik'-'rajput')
# a=5
# b='5'
# print(a==b)

# num=2100
# if num%4==0 or num%100!=0 and  num%400==0:
#     print('leap year')
# else:
#     print('not a leap year')
    
print(int(4 & 1))