import csv

def generate_declarative_constraints_function(relationSet,selfRelationSet):
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
        #print(" ",value[0], " ", formatted_elements)
        if value[0] in selfRelationSet:
            constraint=f"Response({value[0]}, {{{formatted_elements}}})"
        else:
            # If the first element is not a self-loop, use AlternateResponse
            # This assumes that self-loops are handled separately
            constraint=f"AlternateResponse({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
    #print("secondElementMatching: ",len(secondElementMatching))
    for value in secondElementMatching:
        formatted_elements = ", ".join(value[0])  # Convert frozenset to a comma-separated string
        if value[1] in selfRelationSet:
            constraint=f"Response({{{formatted_elements}}}, {value[1]})"
        else:
            # If the second element is not a self-loop, use AlternateResponse
            # This assumes that self-loops are handled separately
            constraint=f"AlternateResponse({{{formatted_elements}}},{value[1]})"
        declarativeConstraints.append(constraint)
    #print("soloTuple: ",len(soloTuple))
    for value in soloTuple:
        if (value[0] or value[1]) in selfRelationSet:
            constraint=f"Response({value[0]},{value[1]})"
        else:
            # If the tuple is not a self-loop, use AlternateResponse
            # This assumes that self-loops are handled separately
            constraint=f"AlternateResponse({value[0]},{value[1]})"
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

    