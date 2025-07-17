
# File: driver.py
# This script demonstrates how to manipulate a matrix representation of activities
# Import necessary libraries
import pandas as pd
from allow_self_loop import allow_self_loop_function
from remove_activity import remove_activity_function
from remove_direct_relationship import remove_direct_relationship_function
from remove_all_relationships import remove_all_relationships_function
from direct_to_concurrent_relationship import direct_to_concurrent_relationship_function
from exclusive_to_direct_relationship import exclusive_to_direct_relationship_function
from generate_declarative_constraints import generate_declarative_constraints_function
from add_true_exclusion_relationships import add_true_exclusion_relationships_function
import sys
from create_alpha_relations_matrix import matrix_function
from visualize_pnml_model import visualize_function

if __name__ == "__main__":
    

    if len(sys.argv) != 2:
        print("Usage: python driver.py <pnml_file_path>")
        sys.exit(1)
    
    pnml_path = sys.argv[1]
    # Call the visualization function
    #output_file=visualize_function(pnml_path)
   

    # Call the matrix function
    matrix=matrix_function(pnml_path)
    if matrix is None:
        print("Failed to create the alpha relations matrix.")
        sys.exit(1)
    
        
    # simple matrix representation of activities
    """matrix=[['','S','A','B','C','D','E'],
    ['S', '-', '→', '-', '-', '-', '-'],
    ['A', '←', '-', '→', '-', '-', '-'],
    ['B', '-', '←', '-', '→', '-', '-'],
    ['C', '-', '-', '←', '-', '→', '-'],
    ['D', '-', '-', '-', '←', '-', '→'],
    ['E', '-', '-', '-', '-', '←', '-']]"""

    # An exemplary BPMN process model of a procurement process: matrix representation of activities  
    """matrix=[['', 'CPR','KPR','CPO','RG','PQC','RI','SP','CO','RR'],
            ['CPR', '-', '→', '-', '-', '-', '-', '-', '-', '-'],
            ['KPR', '←', '-', '→', '-', '-', '-', '-', '-', '→'],
            ['CPO', '-', '←', '-', '→', '-', '-', '-', '-', '-'],
            ['RG', '-', '-', '←', '-', '→', '-', '-', '-', '-'],
            ['PQC', '-', '-', '-', '←', '-', '→', '-', '-', '-'],
            ['RI', '-', '-', '-', '-','←', '-', '→', '-', '-'],
            ['SP','-','-','-','-','-', '←', '-', '→', '-'],
            ['CO','-','-','-','-','-', '-', '←', '-', '-'],
            ['RR','-','←','-','-','-', '-', '-', '-', '-']]"""
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
            ['RIR', '-', '←', '←', '←', '←', '||', '-', '||', '→', '→'],
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
    # Add true exclusion relationships to the Matrix
    df=add_true_exclusion_relationships_function(df)
    print(df)
    # Store the original DataFrame for reference
    df_original = df.copy()
    while True:
        print("\nChoose a relaxation operation:")
        print("1. Allow Self-loop")
        print("2. Remove Activity")
        print("3. Remove Direct relationship")
        print("4. Remove All Relationships Between Two Activities")
        print("5. From Direct (→) to Concurrent (||)")
        print("6. From Exclusive (#) to Direct (→)")
        print("7. Show Matrix")
        print("8. Reset to Original Matrix")
        print("9. Generate Declarative Constraints")
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
        elif choice == "6": #From exclusive(#) to direct(→) relationship
            from_activity = input("Enter from_activity: ")
            to_activity = input("Enter to_activity: ")
            df=exclusive_to_direct_relationship_function(df, from_activity, to_activity)
            print(df)
        elif choice == "7": # Show Matrix
            print(df)
        elif choice == "8": # Reset to Original Matrix
            print("Reset to Original Matrix:")
            df= df_original.copy()
            df.index.name = None  # Reset index name
            print(df)
        elif choice == "9": # Generate Declarative Constraints
            print("Generating Declarative Constraints...")
            generate_declarative_constraints_function(df)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.") 






