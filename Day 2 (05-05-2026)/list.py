l=[]
n=int(input("Enter the number of elements: "))
for i in range(n):
    e=int(input("Enter element: "))
    l.append(e)
print("List: ",l)

print("\nFirst element: ",l[0])
print("Last element: ",l[-1])

a=int(input("\nEnter an element to add: "))
l.append(a)
print("List after adding element: ",l)

b=int(input("\nEnter an element to remove: "))
if b in l:  
    l.remove(b)
    print("List after removing element: ",l)
else:
    print("Element not found in the list.") 

print("\nMaximum element: ",max(l))
print("Minimum element: ",min(l))

print("\nReversed list: ",l[::-1])

print("\nAscending order: ",sorted(l))
print("Descending order: ",sorted(l, reverse=True))

elecount={}
for i in l:
    if i in elecount:
        elecount[i] = elecount[i] + 1
    else:
        elecount[i] = 1
print("\nElement count in the list: ")
for i in elecount: 
    print(i," : ",elecount[i])  

l1=[]
l2=[]
m=int(input("\nEnter the number of elements for first list: "))
for i in range(m):  
    e=int(input("Enter element for first list: "))
    l1.append(e)
o=int(input("\nEnter the number of elements for second list: "))
for i in range(o):  
    e=int(input("Enter element for second list: "))
    l2.append(e)
print("First list: ",l1)    
print("Second list: ",l2)    
print("Merged list: ",l1+l2)

l = list(elecount.keys())
n = len(l)
print("\nList after removing duplicates: ",l)

lr=0
slr=0
for i in l:
    if i > lr:
        slr = lr
        lr = i
    elif i > slr and i != lr:
        slr = i
print("\nSecond largest element: ",slr)

even=[]
odd=[]
c=0
while c < n:
    if l[c] % 2 == 0:
        even.append(l[c])
    else:
        odd.append(l[c])
    c += 1
print("\nEven list: ",even)
print("Odd list: ",odd) 