import csv

def generate_declarative_constraints_function(df):
    relationSet = set()
    # Iterate through the DataFrame to find relations
    for i in df.index:
        for j in df.columns:
            if df.at[i, j] == '→' or df.at[i, j] == '~>' or df.at[i, j] == '||':
                relationSet.add((i, j))
    print("Relation Set generated from the Matrix:")              
    print(relationSet)
    firstElementMatching=set()
    for tuple in relationSet:
        findSimilarFirstElement = {t[1] for t in relationSet if t[0] == tuple[0]}
        firstElementMatching.add((tuple[0], frozenset(findSimilarFirstElement)))
       
    declarativeConstraints=[]
    for value in firstElementMatching:
        formatted_elements = ", ".join(value[1])  # Convert frozenset to a comma-separated string
        constraint=f"Response({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
   
    print("Declarative Constraints generated:")
    for constraint in declarativeConstraints:
        print(constraint)
    # Save declarativeConstraints to a CSV file
    with open("output\\declarative-constraints.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Declarative Constraints"])  # Header row

        # Write rows for each constraint 
        for constraint in declarativeConstraints:
            writer.writerow([constraint])

    print("Declarative Constraints saved to 'output\\declarative-constraints.csv'")

    