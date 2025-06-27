
# File: matrix-representation.py
# This script demonstrates how to manipulate a matrix representation of activities
# Import necessary libraries
import pandas as pd
from allow_self_loop import allow_self_loop_function
from remove_activity import remove_activity_function
from remove_specific_relationship import remove_specific_relationship_function
from remove_all_relationships import remove_all_relationships_function

if __name__ == "__main__":
    
    matrix=[['','S','A','B','C','D','E'],
    ['S', '-', '→', '-', '-', '-', '-'],
    ['A', '←', '-', '→', '-', '-', '-'],
    ['B', '-', '←', '-', '→', '-', '-'],
    ['C', '-', '-', '←', '-', '→', '-'],
    ['D', '-', '-', '-', '←', '-', '→'],
    ['E', '-', '-', '-', '-', '←', '-']]

    print("\nMatrix Representation:")
    df = pd.DataFrame(matrix[1:], columns=matrix[0])
    # Set first column as index
    df = df.set_index('')
    # Remove the name of the index
    df.index.name = None
    # Now you have a clean DataFrame
    print(df)
    # Store the original DataFrame for reference
    df_original = df.copy()
    while True:
        print("\nChoose a relaxation operation:")
        print("1. Allow self-loop")
        print("2. Remove activity")
        print("3. Remove specific relationship")
        print("4. Remove all relationships/activties between two activities")
        print("5. Show Matrix")
        print("6. Reset to Original Matrix")
        print("0. Exit")
        choice = input("Enter your choice (0-6): ")

        if choice == "1":
            activity = input("Enter activity for self-loop: ")
            df = allow_self_loop_function(df, activity)
            print(df)
        elif choice == "2":
            activity = input("Enter activity to remove: ")
            df = remove_activity_function(df, activity)
            print(df)
        elif choice == "3":
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_specific_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "4":
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_all_relationships_function(df, from_activity, to_activity)
            print(df)
        elif choice == "5":
            print(df)
        elif choice == "6":
            print("Reset to Original Matrix:")
            df= df_original.copy()
            df.index.name = None  # Reset index name
            print(df)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")






