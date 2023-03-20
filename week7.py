import sys
expenses = []
def view_record():
    print(f'Here\'s your expense and income records:')
    print(f'Description             Amount Idx')
    print(f'======================  ====== =====')
    for i, element in enumerate(expenses):
        print(f'{element[0]:<23s} {element[1]:6d} [{i:>3d}]')
    print(f'======================  ====== =====')
    print(f'Now you have {total} dollars.')

try:                                                    #(7)
    with open('records.txt', 'r') as fh:
        try:                                            #(9)
            total = int(fh.readline())
        except ValueError:
            print(f'Invalid format in records.txt for the amount of money. Deleting the contents.')    
            try:                                        #(1)
                total = int(input("How much money do you have? "))
            except ValueError:
                print(f'Invalid value for money. Set to 0 by default.')
                total = 0
        else:
            try:                                        #(10)
                for line in fh.readlines():
                    line = line[:-1]
                    description = line.split(' ')
                    name = description[0]
                    num = int(description[1])
                    expenses.append((name, num))
                    total += num
            except (IndexError, ValueError):
                print(f'Invalid format in records.txt for the record. Deleting the contents.')
                try:                                    #(1)
                    total = int(input("How much money do you have? "))
                except ValueError:
                    print(f'Invalid value for money. Set to 0 by default.')
                    total = 0
            else:
                print(f'Welcome back!')
except FileNotFoundError:
    print(f'Welcome, this is your first time to use this application.')
    try:                                                #(1)
        total = int(input("How much money do you have? "))
    except ValueError:
        print(f'Invalid value for money. Set to 0 by default.')
        total = 0

while True:
    print("\n")
    command = input("What do you want to do (add / view / delete / exit)? ")
    if command == 'add':
        print(f'Add an expense or income record qith description and amount:')
        try:                                            #(3)(4)
            description = input().split(' ')
            name = description[0]
            num = int(description[1])
            expenses.append((name, num))
            total += num
        except IndexError:
            print(f'The format of a record should be like this: breakfast -50.\nFail to add a record.')
        except ValueError:
            print(f'Invalid value for money.\nFail to add a record.')
    elif command == 'view':
        view_record()
    elif command == 'delete':
        print(f'Before delete')
        view_record()
        try:                                            #(5)
            del_idx = int(input("Which record do you want to delete?(please enter the list idx to delete the record) "))
        except ValueError:
            print(f'Invalid format. Fail to delete a record.\nYou should enter a number of index to delete the record')
        else:
            try:                                        #(6)
                total -= expenses[del_idx][1]
                del expenses[del_idx]
            except IndexError:
                print(f'There\'s no record you choose. Fail to delete a record.')
            else:
                print(f'After delete')
                view_record()
    elif command == 'exit':
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')

with open('records.txt', 'w') as fh:
    fh.write(f'{str(total)}\n')
    list_of_records = []
    for i, element in enumerate(expenses):
       list_of_records.append(f'{str(element[0])} {str(element[1])}\n')
    fh.writelines(list_of_records)
    
