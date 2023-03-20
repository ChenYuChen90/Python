expenses = []
def view_record():
    print(f'Here\'s your expense and income records:')
    print(f'Description             Amount Idx')
    print(f'======================  ====== =====')
    for i, element in enumerate(expenses):
        print(f'{element[0]:<23s} {element[1]:6d} [{i:>3d}]')
    print(f'======================  ====== =====')
    print(f'Now you have {total} dollars.')

total = int(input("How much money do you have? "))
while True:
    print("\n")
    command = input("What do you want to do (add / view / delete / exit)? ")
    if command == 'add':
        print(f'Add an expense or income record qith description and amount:')
        description = input().split(' ')
        name = description[0]
        num = int(description[1])
        expenses.append((name, num))
        total += num
    elif command == 'view':
        view_record()
    elif command == 'delete':
        print(f'Before delete')
        view_record()
        del_idx = int(input("Which record do you want to delete?(please enter the list idx to delete the record) "))
        total -= expenses[del_idx][1]
        del expenses[del_idx]
        print(f'After delete')
        view_record()
    else :
        break

