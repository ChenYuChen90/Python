import sys

def initialize_categories():
    """initialize the categories"""
    list = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    return list

def initialize():
    """initialize the money and expense from records which is used last time"""
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
                        category = description[0]
                        name = description[1]
                        num = int(description[2])
                        records.append((category, name, num))
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

def is_category_valid(categories, category):
    """chack if the category is valid in add function to avoid error"""
    if type(categories) in {list}:
        for i, v in enumerate(categories):
            p = is_category_valid(v, category)
            if p == True:               	#L[i] == val, so we return(i,)
                return (i,)
            if p != False:                  #L[i] recursively found val, so we prepend i to its path p
                return (i,) + p
    return categories == category

def add(records = [], categories = []):
    """add a record in records the format is (category, name, number)"""
    print(f'Add an expense or income record with category, description, and amount (separate by spaces):')
    try:                                            #(3)(4)
        description = input().split(' ')            #description format should be like "meal breakfast -50"
        category = description[0]
        name = description[1]
        num = int(description[2])
        if is_category_valid(categories, category):
            records.append((category, name, num))
        else:
            print(f'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
    except IndexError:
        print(f'The format of a record should be like this: breakfast -50.\nFail to add a record.')
    except ValueError:
        print(f'Invalid value for money.\nFail to add a record.')
    finally:
        return records

def view_record(total_money, records = []):
    """view the records which pass in"""
    print(f'Here\'s your expense and income records:')
    print(f'Category\tDescription\t\tAmount Idx')
    print(f'=============== ======================= ======== =====')
    for i, element in enumerate(records):
        print(f'{element[0]:<15s} {element[1]:<23s} {element[2]:<8d} [{i:>3d}]')
        total_money += element[2]
    print(f'=============== ======================= ======== =====')
    print(f'Now you have {total_money} dollars.')

def delete(total_money, records = []):
    """delete a record in records by index"""
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

def save(total_money, records = []):
    """store the data for reuse"""
    with open('records.txt', 'w') as fh:
        fh.write(f'{str(total_money)}\n')
        list_of_records = []
        for i, element in enumerate(records):
            list_of_records.append(f'{str(element[0])} {str(element[1])} {str(element[2])}\n')
        fh.writelines(list_of_records)    

def view_categorise(categories = [], prefix = ()):
    """view the categories"""
    if type(categories) in {list}:
        i = 0
        for v in categories:
            if type(v) not in {list}:
                i += 1
            view_categorise(v, prefix + (i,))
    else:
        s = ' ' * 4 * (len(prefix) - 1)
        s += '.'.join(map(str, prefix))
        s += '. ' + categories
        print(s)

def find(categories = [], records = []):
    """find the records in category which user wants to find"""
    category = input(f'Which category do you want to find? ')
    category_list = find_subcategories(category, categories)
    records_list = filter(lambda x : x[0] in category_list, records)
    print(f'Here\'s your expense and income records under category "{category}":')
    view_record(0, records_list)

def find_subcategories(category, categories):
    """find the subcategories in the category which user wants to find"""
    if type(categories) == list:
        for v in categories:
            p = find_subcategories(category, v)
            if p == True:
                # if found, return the flatten list including itself and its subcategories
                index = categories.index(v)
                if index + 1 < len(categories) and type(categories[index + 1]) == list:
                    return flatten(categories[index:index + 2])
                else:
                    # return only itself if no subcategories
                    return [v]
            if p != []:
                return p
    return True if categories == category else []       # return [] instead of False if not found

def flatten(L):
    """return a flat list that contains all element in the nested list L"""
    if type(L) == list:
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    else:
        return [L]

categories = initialize_categories()
initial_money, expenses = initialize()
while True:
    print("\n")
    command = input("What do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == 'add':
        expenses = add(expenses, categories)
    elif command == 'view':                                         #will calculate total money in view()
        view_record(initial_money, expenses)
    elif command == 'delete':
        expenses = delete(initial_money, expenses)
    elif command == 'exit':
        save(initial_money, expenses)
        break
    elif command == 'view categories':
        view_categorise(categories)
    elif command == 'find':
        find(categories, expenses)
    else:                                                           #command didn't exit
        sys.stderr.write('Invalid command. Try again.\n')           #(2)

