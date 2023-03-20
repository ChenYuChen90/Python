import sys

class Record:
    """Represent a record."""
    def __init__(self, category, description, amount):
        self._category = category
        self._description = description
        self._amount = amount
    def get_category(self):
        return self._category
    def get_description(self):
        return self._description
    def get_amount(self):
        return self._amount
    amount = property(lambda self:self.get_amount())
    category = property(lambda self:self.get_category())
    description = property(lambda self:self.get_description())

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
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
                            records.append(Record(category, name, num))
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
            self._records = records
            self._initial_money = total
    def add(self, record, categories):
        try:                                            #(3)(4)
            description = record.split(' ')            #description format should be like "meal breakfast -50"
            category = description[0]
            name = description[1]
            num = int(description[2])
            if categories.is_category_valid(category):
                self._records.append(Record(category, name, num))
            else:
                print(f'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
        except IndexError:
            print(f'The format of a record should be like this: breakfast -50.\nFail to add a record.')
        except ValueError:
            print(f'Invalid value for money.\nFail to add a record.')
    def view(self):
        """view the records which pass in"""
        total_money = 0
        print(f'Here\'s your expense and income records:')
        print(f'Category\tDescription\t\tAmount Idx')
        print(f'=============== ======================= ======== =====')
        for i, element in enumerate(self._records):
            print(f'{element.category:<15s} {element.description:<23s} {element.amount:<8d} [{i:>3d}]')
            total_money += element.amount
        print(f'=============== ======================= ======== =====')
        print(f'Now you have {total_money} dollars.')
    def delete(self):
        """delete a record in records by index"""
        print(f'Before delete')
        self.view()               #view before delete
        try:                                            #(5)
            del_idx = int(input("Which record do you want to delete?(please enter the list idx to delete the record) "))
        except ValueError:
            print(f'Invalid format. Fail to delete a record.\nYou should enter a number of index to delete the record')
        else:
            try:                                        #(6)
                del self._records[del_idx]
            except IndexError:
                print(f'There\'s no record you choose. Fail to delete a record.')
            else:
                print(f'After delete')
                self.view()       #view after delete for check
        finally:
            return records
    def find(self, target_categories):
        records_list = filter(lambda x : x.category in target_categories, self._records)
        print(f'Here\'s your expense and income records:')
        print(f'Category\tDescription\t\tAmount Idx')
        print(f'=============== ======================= ======== =====')
        total_money = 0
        for i, element in enumerate(records_list):
            print(f'{element.category:<15s} {element.description:<23s} {element.amount:<8d} [{i:>3d}]')
            total_money += element.amount
        print(f'=============== ======================= ======== =====')
        print(f'Now you have {total_money} dollars.')
    def save(self):
        """store the data for reuse"""
        with open('records.txt', 'w') as fh:
            fh.write(f'{str(self._initial_money)}\n')
            list_of_records = []
            for i, element in enumerate(self._records):
                list_of_records.append(f'{str(element.category)} {str(element.description)} {str(element.amount)}\n')
            fh.writelines(list_of_records)

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    def view(self):
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
        view_categorise(self._categories)
    def is_category_valid(self, category):
        def is_valid(categories, category):
            """chack if the category is valid in add function to avoid error"""
            if type(categories) in {list}:
                for i, v in enumerate(categories):
                    p = is_valid(v, category)
                    if p == True:               	#L[i] == val, so we return(i,)
                        return (i,)
                    if p != False:                  #L[i] recursively found val, so we prepend i to its path p
                        return (i,) + p
            return categories == category
        return is_valid(self._categories, category)
    def find_subcategories(self, category):
        def find_subcategories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index+1], True)
            else:
                if categories == category or found == True:
                    yield categories
        return [i for i in find_subcategories_gen(category, self._categories)]

categories = Categories()
records = Records()
while True:
    print("\n")
    command = input("What do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == 'add':
        record = input('Add an expense or income record with category, description, and amount (separate by spaces):')
        records.add(record, categories)
    elif command == 'view':                                         #will calculate total money in view()
        records.view()
    elif command == 'delete':
        records.delete()
    elif command == 'exit':
        records.save()
        break
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input(f'Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    else:                                                           #command didn't exit
        sys.stderr.write('Invalid command. Try again.\n')           #(2)