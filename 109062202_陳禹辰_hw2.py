import sys

def add(records = []):
    print(f'Add an expense or income record with description and amount:')
    try:                                            #(3)(4)
        description = input().split(' ')            #description format should be like "breakfast -50"
        name = description[0]
        num = int(description[1])
        records.append((name, num))
    except IndexError:
        print(f'The format of a record should be like this: breakfast -50.\nFail to add a record.')
    except ValueError:
        print(f'Invalid value for money.\nFail to add a record.')
    finally:
        return records

def view_record(total_money, records = []):
    print(f'Here\'s your expense and income records:')
    print(f'Description             Amount Idx')
    print(f'======================  ====== =====')
    for i, element in enumerate(records):
        print(f'{element[0]:<23s} {element[1]:6d} [{i:>3d}]')
        total_money += element[1]
    print(f'======================  ====== =====')
    print(f'Now you have {total_money} dollars.')

def delete(total_money, records = []):
    print(f'Before delete')
    view_record(total_money, records)               #view before delete
    try:                                            #(5)
        del_idx = int(input("Which record do you want to delete?(please enter the list idx to delete the record) "))
    except ValueError:
        print(f'Invalid format. Fail to delete a record.\nYou should enter a number of index to delete the record')
    else:
        try:                                        #(6)
            del records[del_idx]
        except IndexError:
            print(f'There\'s no record you choose. Fail to delete a record.')
        else:
            print(f'After delete')
            view_record(total_money, records)       #view after delete for check
    finally:
        return records

def save(total_money, records = []):                #store the data for reuse
    with open('records.txt', 'w') as fh:
        fh.write(f'{str(total_money)}\n')
        list_of_records = []
        for i, element in enumerate(records):
            list_of_records.append(f'{str(element[0])} {str(element[1])}\n')
        fh.writelines(list_of_records)    

def initialize():
    records = []
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
                        records.append((name, num))
                except (IndexError, ValueError):
                    print(f'Invalid format in records.txt for the record. Deleting the contents.')
                    try:                                    #(1)
                        total = int(input("How much money do you have? "))
                    except ValueError:
                        print(f'Invalid value for money. Set to 0 by default.')
                        total = 0
                else:
                    print(f'Welcome back!')
    except FileNotFoundError:                               #first time open this program
        print(f'Welcome, this is your first time to use this application.')
        try:                                                #(1)
            total = int(input("How much money do you have? "))
        except ValueError:
            print(f'Invalid value for money. Set to 0 by default.')
            total = 0
    finally:
        return total, records

initial_money, expenses = initialize()
while True:
    print("\n")
    command = input("What do you want to do (add / view / delete / exit)? ")
    if command == 'add':
        expenses = add(expenses)
    elif command == 'view':                                         #will calculate total money in view()
        view_record(initial_money, expenses)
    elif command == 'delete':
        expenses = delete(initial_money, expenses)
    elif command == 'exit':
        save(initial_money, expenses)
        break
    else:                                                           #command didn't exit
        sys.stderr.write('Invalid command. Try again.\n')           #(2)

