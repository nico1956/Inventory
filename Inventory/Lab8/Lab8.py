# Libby Bakalar, Nico Busatto, Mitchel Melvin
# April 30, 2019
# This program will give the user the option to add, delete, 
# or display inventory from a warehouse 
# This program uses pickling to serialize and deserialize 
# items from inventory from a file 

import pickle
import os
import time

def main():
    
    inventoryDictionary = {'ice cream':'5.99', 'banana':'2.99', 'pasta':'4.99', 'apples':'1.99', 'potato chips':'3.99'}
    addedSet = set()
    deletedSet = set()

    try:
        pickle_in = open("inventory.pickle","rb")
        itemsAdded_in = open("addedItems.pickle", "rb")
        itemsDeleted_in = open("deletedItems.pickle", "rb")
        inventoryDictionary = pickle.load(pickle_in)
        addedSet = pickle.load(itemsAdded_in)
        deletedSet = pickle.load(itemsDeleted_in)

    except pickle.UnpicklingError as e:
        # normal, somewhat expected
        menu(inventoryDictionary, addedSet, deletedSet)
    except (AttributeError, EOFError, ImportError, IndexError) as e:
        # secondary errors
        menu(inventoryDictionary, addedSet, deletedSet)
    except Exception as e:
        #everything else, fatal errors
        print("File fatal error occurred, new data won't be saved")
        print("")
        menu(inventoryDictionary, addedSet, deletedSet)

    menu(inventoryDictionary, addedSet, deletedSet)

def menu(invDict, addSet, delSet):
    again = "Y"
    print("Enter 1 to add to inventory ")
    print("Enter 2 to delete from inventory ")
    print("Enter 3 to show deleted/added items")
    print("Enter 4 to display inventory ")
    print("Enter anything else to exit ")
    print("")
    choice = str(input("Your selection: "))

    if choice == "1" or choice == "2": 
        if choice == "1":  # adding to inventory
            while again == "Y": 
                addTo(invDict, addSet)
                again = str.upper(input("Add another? (Y or N): \n"))
            menu(invDict, addSet, delSet)

        else: # if choice = 2(delete from)
            while again == "Y":
                deleteFrom(invDict, delSet)
                again = str.upper(input("Delete another? (Y or N): \n"))
            menu(invDict, addSet, delSet)

    elif choice == "3": # displaying added/deleted items 
        del_addDisplay(addSet, delSet)
        print("")
        menu(invDict, addSet, delSet)

    elif choice == "4":# displaying 
        output(invDict)
        menu(invDict, addSet, delSet)

    else: # Exiting
        # opens files 
        itemsAdded_out = open("addedItems.pickle", "wb")
        itemsDeleted_out = open("deletedItems.pickle", "wb")
        pickle_out = open("inventory.pickle","wb")

        # dumps items to pickle files 
        pickle.dump(addSet, itemsAdded_out)
        pickle.dump(delSet, itemsDeleted_out)
        pickle.dump(invDict, pickle_out)

        # closes files 
        pickle_out.close()
        itemsAdded_out.close()
        itemsDeleted_out.close()

        # ends program 
        print("Program ending! Have a good one!")
        time.sleep(4) # sleeps for 4 seconds
        os._exit(1) # then closes program 
            
def addTo(invDict, addSet): 
    ok = False
    item = str(input("What item would you like to add to the inventory? "))
    invDict.update({item : "0"})    # adds item to inventory dictionary
    addSet.update([item]) # adds item to added set 

    while ok == False:
        try:
            price = float(input("What is the item price? ")) 
            invDict.update({item : price})  # adds price to inventory dictionary 
            ok = True
            print("Thank you! " + item + " has now been added! Its price is " + '${:,.2f}'.format(float(price)) + ".")
        except: 
            print("Error, " + item + " not added")
            ok = False

def deleteFrom(invDict, delSet):
    ok = False
    while ok == False:
        try:
            item = str(input("What item would you like to delete from inventory? "))
            delSet.update([item])  # adds item to deleted set 
            del invDict[item] # deletes item from inventory

            print("Thank you! " + item + " has now been deleted!")
            ok = True
        except:
            print("Error, " + item + " not found")
            ok = False

def del_addDisplay(addSet, delSet): # displaying added/deleted items 
    print("")
    print("Added Items: " + str(addSet).strip('{}'))
    print("Deleted Items: " + str(delSet).strip('{}'))

def output(invDict): # diplaying inventory and prices 
    print("")
    print("Your inventory is: ")
    print("")
    print("Item\t\tPrice")
    print("-----------------------")
    for k , v in invDict.items():
        print(str('{:<8}'.format(k)) + "\t" + '${:,.2f}'.format(float(v)))
    print("")

# calls main
main()