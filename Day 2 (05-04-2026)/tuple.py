print(""" Stage 0:
 ----------
    |   |
        |
        |
        |
        |
        |
==========""")


n=int(input("Enter number of elements: "))
for i in range(n):
    e=int(input("Enter element: "))
    l.append(e)
t=tuple(l)
print("Tuple: ",t)

a=int(input("\nEnter number to add: "))
r=int(input("\nEnter number to remove: "))
l=list(t)
l.append(a)
l.remove(r)
t=tuple(l)
print("Tuple after adding and removing elements: ",t)

elecount={}
for i in t:
    if i in elecount:
        elecount[i] = elecount[i] + 1
    else:
        elecount[i] = 1
print("\nElement count in the tuple: ")
for i in elecount: 
    print(i," : ",elecount[i])

s=int(input("\nEnter number to get its index: "))
if s in t:
    print("Index of", s, "is:", t.index(s))
else:
    print("Number not found in the tuple.")

o=int(input("\nEnter number of elements for first tuple: "))
t1=()
for i in range(o):
    e=int(input("Enter element for first tuple: "))
    t1 = t1 + (e,)
p=int(input("\nEnter number of elements for second tuple: "))
t2=()
for i in range(p):
    e=int(input("Enter element for second tuple:"))
    t2 = t2 + (e,)
print("\nFirst tuple: ",t1)
print("Second tuple: ",t2)
print("Concatenated tuple: ",t1+t2)

start=int(input("\nEnter starting index: "))
end=int(input("Enter ending index: "))
print("Sliced tuple: ",t[start:end])

s=int(input("\nEnter number to search: "))
if s in t:
    print(s, "is present in the tuple.")
else:
    print(s, "is not present in the tuple.")

print("\nLength of the tuple: ",len(t))

b=int(input("\nEnter number of element for list: "))
for i in range(b):
    e=int(input("Enter element for list: "))
    l.append(e) 
print("List: ",l)
print("Tuple: ",tuple(l))

print("Iterating through the tuple: ")
for i in t:
    print(i, end=" ")