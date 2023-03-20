t = input("How much money do you have ?")
total = int(t)
expression = input("Add some expense or income records with description ans amount:\n")
description = expression.split(', ')
expenses = []
for i in range(len(description)):
    ll = description[i].split(' ')
    name = ll[0]
    num = int(ll[1])
    expenses.append((name, num))
#print(expenses)
print(f'Here\'s your expense and income records:')
for i in range(len(expenses)):
    print(f'{expenses[i][0]} {expenses[i][1]}')
    total += expenses[i][1]
print(f'Now you have {total} dollars.')
