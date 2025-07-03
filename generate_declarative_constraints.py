import csv

def generate_declarative_constraints_function(relationSet):
    #print(f"generate_declarative_constraints_function length of relationSet: ",len(relationSet))
    
    firstElementMatching=set()
    secondElementMatching=set()
    soloTuple=set()
    for tuple in relationSet:
        findSimilarFirstElement = {t[1] for t in relationSet if t[0] == tuple[0]}
        if len(findSimilarFirstElement) >1:
            firstElementMatching.add((tuple[0], frozenset(findSimilarFirstElement)))
        else:
            findSimilarSecondElement = {t[0] for t in relationSet if t[1] == tuple[1]}
            if len(findSimilarSecondElement)>1:
                secondElementMatching.add((frozenset(findSimilarSecondElement),tuple[1]))
            else:
                soloTuple.add(tuple)
    declarativeConstraints=[]
    for value in firstElementMatching:
        formatted_elements = ", ".join(value[1])  # Convert frozenset to a comma-separated string
        constraint=f"Response({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
    #print("secondElementMatching: ",len(secondElementMatching))
    for value in secondElementMatching:
        formatted_elements = ", ".join(value[0])  # Convert frozenset to a comma-separated string
        constraint=f"Response({{{formatted_elements}}},{value[1]})"
        declarativeConstraints.append(constraint)
    #print("soloTuple: ",len(soloTuple))
    for value in soloTuple:
        constraint=f"Response({value})"
        declarativeConstraints.append(constraint)
    
    # Save declarativeConstraints to a CSV file
    with open("output\\declarative-constraints.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Declarative Constraints"])  # Header row

        # Write rows for each constraint 
        for constraint in declarativeConstraints:
            writer.writerow([constraint])

    print("Declarative Constraints saved to 'output\\declarative-constraints.csv'")

    