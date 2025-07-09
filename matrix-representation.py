
# File: matrix-representation.py
# This script demonstrates how to manipulate a matrix representation of activities
# Import necessary libraries
import pandas as pd
from allow_self_loop import allow_self_loop_function
from remove_activity import remove_activity_function
from remove_direct_relationship import remove_direct_relationship_function
from remove_all_relationships import remove_all_relationships_function
from direct_to_concurrent_relationship import direct_to_concurrent_relationship_function
from exclusive_to_direct_relationship import exclusive_to_direct_relationship_function
from exclusive_to_concurrent_relationship import exclusive_to_concurrent_relationship_function
from generate_declarative_constraints import generate_declarative_constraints_function

if __name__ == "__main__":
    
    # simple matrix representation of activities
    """matrix=[['','S','A','B','C','D','E'],
    ['S', '-', '→', '-', '-', '-', '-'],
    ['A', '←', '-', '→', '-', '-', '-'],
    ['B', '-', '←', '-', '→', '-', '-'],
    ['C', '-', '-', '←', '-', '→', '-'],
    ['D', '-', '-', '-', '←', '-', '→'],
    ['E', '-', '-', '-', '-', '←', '-']]"""

    # An exemplary BPMN process model of a procurement process: matrix representation of activities  
    matrix=[['', 'CPR','KPR','CPO','RG','PQC','RI','SP','CO','RR'],
            ['CPR', '-', '→', '-', '-', '-', '-', '-', '-', '-'],
            ['KPR', '←', '-', '→', '-', '-', '-', '-', '-', '→'],
            ['CPO', '-', '←', '-', '→', '-', '-', '-', '-', '-'],
            ['RG', '-', '-', '←', '-', '→', '-', '-', '-', '-'],
            ['PQC', '-', '-', '-', '←', '-', '→', '-', '-', '-'],
            ['RI', '-', '-', '-', '-','←', '-', '→', '-', '-'],
            ['SP','-','-','-','-','-', '←', '-', '→', '-'],
            ['CO','-','-','-','-','-', '-', '←', '-', '-'],
            ['RR','-','←','-','-','-', '-', '-', '-', '-']]
    # BPIC 2019 based process model: -3-way Match, Invoice before Goods Receipt - Standard and Framework Orders". Figure 5 for the visualization of the model [1].
    # 1. Diba, K., Remy, S., & Pufahl, L. (2019, June). Compliance and performance analysis of procurement processes using process mining. In International conference on process mining. 
    # Create Purchase Requisition Item (CPRI)
    # Create Purchase Order Item (CPOI)
    # Receive Order Confirmation (ROC)
    # Change Price (CP)
    # Change Quantity (CQ)
    # Record Goods Receipt (RGR)
    # Record Invoice Receipt (RIR)
    # Vendor creates invoice (VCI)
    # Remove Payment Block (RPB)
    # Clear Invoice (CI)
    
    """matrix=[['','CPRI','CPOI','ROC','CP','CQ','RGR','RIR','VCI','RPB','CI'],
            ['CPRI', '-', '→', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['CPOI', '←', '-', '→', '→', '→', '→', '→', '→', '-', '-'],
            ['ROC', '-', '←', '-', '-', '→', '→', '→', '→', '-', '-'],
            ['CP', '-', '←', '-', '-', '→', '→', '→', '→', '-', '-'],
            ['CQ', '-', '←', '←', '←', '-', '→', '→', '||', '-', '-'],
            ['RGR', '-', '←', '←', '←', '←', '-', '||', '||', '→', '→'],
            ['RIR', '-', '←', '←', '←', '←', '-', '-', '||', '→', '→'],
            ['VCI', '-', '←', '←', '←', '||', '||', '||', '-', '→', '→'],
            ['RPB', '-', '-', '-', '-', '-', '←', '←', '←', '-', '→'],
            ['CI', '-', '-', '-', '-', '-','←', '←', '←', '←','-']]"""
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
        print("3. Remove direct relationship")
        print("4. Remove all relationships/activties between two activities")
        print("5. From direct(→) to concurrent(||) relationship")
        print("6. From exclusive(-) to direct(→) relationship")
        print("7. From exclusive(-) to concurrent(||) relationship")
        print("8. Show Matrix")
        print("9. Reset to Original Matrix")
        print("10. Generate Declarative Constraints")
        print("0. Exit")
        choice = input("Enter your choice (0-10): ")

        if choice == "1": #Allow self-loop
            activity = input("Enter activity for self-loop: ")
            df = allow_self_loop_function(df, activity)
            print(df)
        elif choice == "2": #Remove activity
            activity = input("Enter activity to remove: ")
            df = remove_activity_function(df, activity)
            print(df)
        elif choice == "3": #Remove specific relationship
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_direct_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "4": #Remove all relationships/activities between two activities
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = remove_all_relationships_function(df, from_activity, to_activity)
            print(df)
        elif choice == "5": #From direct(→) to concurrent(||) relationship
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df=direct_to_concurrent_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "6": #From exclusive(-) to direct(→) relationship
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df=exclusive_to_direct_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "7": #From exclusive(-) to concurrent(||) relationship
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df = exclusive_to_concurrent_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "8": # Show Matrix
            print(df)
        elif choice == "9": # Reset to Original Matrix
            print("Reset to Original Matrix:")
            df= df_original.copy()
            df.index.name = None  # Reset index name
            print(df)
        elif choice == "10": # Generate Declarative Constraints
            relationSet = set()
            selfRelationSet = set()
            # Iterate through the DataFrame to find relations
            for i in df.index:
                for j in df.columns:
                    if df.at[i, j] == '→' or df.at[i, j] == '~>':
                        relationSet.add((i, j))
                    elif df.at[i, j] == '||':
                        relationSet.add((i, j))
                        if i == j:
                            print(f"Self loop found: {i} || {j}")
                            selfRelationSet.add(i)
                        #else:
                            
            print("Relation Set generated from the Matrix:")              
            print(relationSet)
            print("Generating Declarative Constraints...")
            generate_declarative_constraints_function(relationSet,selfRelationSet)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")






