a=input("Enter a string: ")

print("No. of characters in the string is: ",len(a))

print("Reverse of string: ",a[::-1])

if a==a[::-1]:
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")

c,v=0,0
for i in a:
    if i in "aeiouAEIOU":
        v += 1
    else:
        c += 1
print("No. of vowels in the string is: ",v)
print("No. of consonants in the string is: ",c)

print("String in uppercase: ",a.upper())
print("String in lowercase: ",a.lower())

print("String after spaces removed: ",a.replace(" ",""))

r=input("Enter a word to replace: ")
new=input("Enter the new word: ")
print("String after replacing: ",a.replace(r,new))

characount={}
for i in a:
    if i in characount:
        characount[i] = characount[i] + 1
    else:
        characount[i] = 1
print("Character count in the string: ")
for i in characount:
    print(i," : ",characount[i])

start=int(input("Enter the starting index: "))
end=int(input("Enter the ending index: "))
print("Substring: ",a[start:end])

word1=input("Enter first word: ")
word2=input("Enter second word: ")
if sorted(word1) == sorted(word2):
    print("The words are anagrams.")
else:
    print("The words are not anagrams.")