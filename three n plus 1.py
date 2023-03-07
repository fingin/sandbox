12#is even or odd
def EvenOdd(n):
    if n%2==0:
        return True
    else:
        return False



def loop1(N,X):
    while True:
        if EvenOdd(N):
            #print("Even")
            N = N/2
        else:
            #print("Odd")
            N = (3*N)+1
        if N == 1: 
            #3print("Entered 4321 loop")
            print("loop:",X)
            return False
        #print(N)
        X = X+1
    #TODO: diplay a tree graph of evry number N using PyGame
def loop2(N,X):
    while True:
        if EvenOdd(N):
            print("Even")
            N = N*2
        else:
            print("Odd")
            N = (N/3)-1
        if N == 1: 
            print("Entered 4321 loop")
            print("loop:",X)
            x = 0
            N = int(input("Enter a number: "))
        if N == 0:
            print("Entered 0 loop")
            print("loop:",X)
            x = 0
            N = int(input("Enter a number: "))
        print(N)
        X = X+1
    #TODO: diplay a tree graph of evry number N using PyGame

N = int(input("Enter a number: "))
X = 0
H = ((2**999999999999999999999999999999999999999999999999999999999999999999999999999)**999999999999999999999999999999999999999999999999999)+1
while True:
    if loop1(H,X):
        print("counter example: ",X)
        break
    H+=1



