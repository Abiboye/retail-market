""" PYTHON IFE RETAIL MARKET PROJECT
    
    Author: AnonymouX47
    Date Started: Mon Sep 21, 2020
"""

from utils import *  # excludes `_gain`

def read_stock(filepath):
    """ Reads stock data from a csv file
    returns a list of dicts containing the stock data

    Note: Each line of the csv file is expected to be in the form:
    "'item name', 'quantity', 'unit price'\\n"
    """

    stock_file = open(filepath, 'r')
    stock = []  # List to contain stock data

    for line in stock_file:
        line = line.strip('\n').split(', ')
        row = []
        for cell in line:
            row.append(cell.strip("'"))
        row[1:] = map(int, row[1:])
        stock.append({"name": row[0], "quantity": row[1], "price": row[2]})
    stock_file.close()

    # The same can also be achieved with a single statement using list comprehensions.

    # stock = [ {"name": row[0], "quantity": int(row[1]), "price": int(row[2])}
    #         for row in [ [cell.strip("'") for cell in line.strip().split(', ')]
    #         for line in open(filepath, 'r')] ]

    return stock


def display_items(stock, admin=False):
    """ Display available items with their unit prices (and quantity for admin) """

    if admin:
        width = 70
        disp_format = "| {:>2} || {:<30} || {:>14} || {:>8} |"
    else:
        width = 58
        disp_format = "| {:>2} || {:<30} || {:>14} |"
        
    print('=' * width)
    # The number of positional arguments to .format() can exceed
    # the number of replacement fields in the string to be formatted
    # but doing the opposite with automatic field-numbering will cause an error.
    print(disp_format.format("ID", "Item", "Unit Price (#)", "Quantity"))
    print('-' * width)
    for item_id, item in enumerate(stock, 1):
        name, quantity, price = item.values()
        if admin or quantity > 0:
            print(disp_format.format(item_id, name, price, quantity))
    print('=' * width)
    print()


def buy(stock):
    """ Start and Complete a purchase """

    if input("Do you want to see the item list (Y/N)? ").lower() == 'y':
        print()
        display_items(stock)
    else:
        print()
    purchase = {}  # to contain purchase details; {id: qty, ...}
    max_id = len(stock)  # Instead of len() being computed on each iteration.
    progress = 'y'
    while progress == 'y':
        try:
            item_id = int(input("Enter item ID: "))

            # An IndexError can never occour at the last expression here
            # by virtue of the evaluation order of boolean operator `or`.
            if item_id < 1 or item_id > max_id or stock[item_id - 1]["quantity"] == 0:
                print("Invalid Item ID")
                continue

            max_qty = stock[item_id - 1]["quantity"]
            qty_question = "Enter item Quantity (1 - {}): ".format(max_qty)
            quantity = int(input(qty_question))

            if quantity < 1:
                quantity = int(input(qty_question))
                if quantity > max_qty or quantity < 1:
                    print("Invalid Quantity!!")
                    continue
            elif quantity > max_qty:
                print("Sorry, the requested quantity is currently unavailable.\n"
                        "1. Skip item\n"
                        "2. Request all available quantity\n"
                        "3. Enter another quantity\n")

                choice = int(input("Please, Choose an option: "))
                if choice == 1:
                    continue
                elif choice == 2:
                    quantity = max_qty
                elif choice == 3:
                    quantity = int(input(qty_question))
                    if quantity > max_qty or quantity < 1:
                        print("Invalid Quantity!!")
                        continue
                else:
                    print("Wrong Input!!")
                    continue
        except ValueError:
            print("Invalid input!!")
            continue
        else:
            if item_id in purchase:
                print(
                    "This item '{}' has been selected ealier with quantity '{}'".format(
                    stock[item_id]["name"], purchase[item_id]))
                print("1. Change to new quantity\n"
                        "2. Leave with previous quantity\n")

                choice = int(input("Please, Choose an option: "))
                if choice == 1:
                    purchase[item_id] = quantity
                elif choice == 2:
                    pass
                else:
                    print("Wrong input!!\nItem quantity left unchanged")
            else:
                purchase[item_id] = quantity
        finally:
            progress = input("Do you want to buy another item (y/n)? ").lower()
            while progress != 'y' and progress != 'n':
                print("Invalid Input!!")
                progress = input("Do you want to buy another item (y/n)? ").lower()
    print()

    # An empty iterable (len() == 0) has a boolean value `False`, otherwise, `True`.
    if purchase:
        total_amount = make_purchase(stock, purchase)
        update_stock(stock, purchase)
        add_gain(total_amount)
    else:
        print("You didn't select any items")
    print("Thanks for shopping with us!!!\n")


my_stock = read_stock("data.csv")

end_of_day = False
while not end_of_day:
    username = input("Please, Enter Your Name: ")
    print()
    
    if username.lower() == "admin":
        while True:
            print("1. View stock\n"
                "2. Add items\n"
                "3. Change item detail\n"
                "4. View today's gain\n"
                "5. Exit\n"
                "6. End the day\n")

            try:
                choice = int(input("Choose an option: "))
                print()
            except ValueError:
                print("Invalid Input!!\n")
                continue

            if choice == 1:
                display_items(my_stock, admin=True)
            elif choice == 2:
                add_items(my_stock)
            elif choice == 3:
                while True:
                    print("1. Item Name\n"
                        "2. Item Price\n"
                        "3. Item Quantity\n"
                        "4. Back\n")
                    try:
                        choice = int(input("Choose an option: "))
                        print()
                    except ValueError:
                        print("Invalid Input!!\n")
                        continue

                    if choice == 1:
                        change_detail(my_stock, "name")
                    elif choice == 2:
                        change_detail(my_stock, "price")
                    elif choice == 3:
                        change_detail(my_stock, "quantity")
                    elif choice == 4:
                        break
                    else:
                        print("Invalid Option!!\n")
            elif choice == 4:
                view_gain()
            elif choice == 5:
                break
            elif choice == 6:
                end_of_day = True
                break
            else:
                print("Invalid Option!!\n")

    else:  # Any other name is taken as a customer's.
        print(f"Welcome, {username}!\n")

        while True:
            print("1. View item list\n"
                    "2. Purchase Goods\n"
                    "3. Exit\n")

            try:
                choice = int(input("Choose an option: "))
                print()
            except ValueError:
                print("Invalid Input!!\n")
                continue

            if choice == 1:
                display_items(my_stock)
            elif choice == 2:
                buy(my_stock)
            elif choice == 3:
                print(f"Have a good day, {username}!\n"
                        "Thanks for shopping with us.\n")
                break
            else:
                print("Invalid Option!!\n")

