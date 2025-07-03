def path_exists(df, from_activity, to_activity):
    """
<<<<<<< HEAD
    Check if there is a path from from_activity to to_activity following '→' in the Matrix.
=======
    Check if there is a path from from_activity to to_activity following '→' or '~>' in the Matrix.
>>>>>>> f0fbb74 (Added more options for relaxation)
    """
    visited = set()
    stack = [from_activity]
    while stack:
        current = stack.pop()
        if current == to_activity:
            return True
        visited.add(current)
        for col in df.columns:
<<<<<<< HEAD
            if df.at[current, col] == '→' and col not in visited:
=======
            if (df.at[current, col] == '→' or df.at[current, col] == '~>' or df.at[current,col]=='||') and col not in visited:
>>>>>>> f0fbb74 (Added more options for relaxation)
                stack.append(col)
    return False
        
def remove_all_relationships_function(df, from_activity,to_activity):
    """
    Remove all relationships from a specific activity to another in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
        if from_activity != to_activity:
            # Check if a path exists from from_activity to to_activity
            if not path_exists(df, from_activity, to_activity):
<<<<<<< HEAD
                print(f"No path exists from {from_activity} to {to_activity}.")
                return df
            # If a path exists, remove all relationships along the path
            # and add a new relationship from from_activity to to_activity
            print(f"Removing relationship from {from_activity} to {to_activity}.")
=======
                print(f"No path exists from {from_activity} to {to_activity}.\n")
                return df
            # If a path exists, remove all relationships along the path
            # and add a new relationship from from_activity to to_activity
            print(f"Removing relationship between {from_activity} and {to_activity}.")
>>>>>>> f0fbb74 (Added more options for relaxation)
            # Find all successors of from_activity until to_activity
            successorsOfFromActivity = []
            temp_from_activity = from_activity
            visited = set()
            while temp_from_activity != to_activity:
                found = False
                visited.add(temp_from_activity)
                for col in df.columns:
<<<<<<< HEAD
                    if df.at[temp_from_activity, col] == '→' and col != to_activity and col not in visited:
=======
                    if (df.at[temp_from_activity, col] == '→' or df.at[temp_from_activity,col]=='~>' or df.at[temp_from_activity,col]=='||') and col != to_activity and col not in visited:
>>>>>>> f0fbb74 (Added more options for relaxation)
                        successorsOfFromActivity.append((temp_from_activity,col))
                        temp_from_activity = col
                        found = True
                        break
                if not found:
                    # No further successor found, break to avoid infinite loop
                    break
           
            predecessorsOfToActivity = []
            temp_to_activity = to_activity
            visited = set()
            while temp_to_activity != from_activity:
                found = False
                visited.add(temp_to_activity)
                for col in df.columns:
<<<<<<< HEAD
                    if df.at[col, temp_to_activity] == '→' and col != from_activity and col not in visited:
=======
                    if (df.at[col, temp_to_activity] == '→' or df.at[col,temp_to_activity]=='~>' or df.at[col,temp_to_activity]=='||') and col != from_activity and col not in visited:
>>>>>>> f0fbb74 (Added more options for relaxation)
                        predecessorsOfToActivity.append((col,temp_to_activity))
                        temp_to_activity = col
                        found = True
                        break
                if not found:
                    # No further predecessor found, break to avoid infinite loop
                    break
<<<<<<< HEAD
            print(f"Successors of '{from_activity}': {successorsOfFromActivity}")    
            print(f"Predecessors of '{to_activity}': {predecessorsOfToActivity}")
            # Remove the relationships along the found path
            for src, tgt in successorsOfFromActivity:
                df.at[src, tgt] = '-'
                #print(f"Removed relationship: {src} -> {tgt}")
            for src, tgt in predecessorsOfToActivity:
                df.at[src, tgt] = '-'
                #print(f"Removed relationship: {src} -> {tgt}")
            # Add a new relationship from from_activity to to_activity
            df.at[from_activity, to_activity] = '~>'
            print(f"Added relationship: {from_activity} ~> {to_activity}")
            
=======
            print(f"Successors of '{from_activity}' until '{to_activity}': {successorsOfFromActivity}")    
            print(f"Predecessors of '{to_activity}' until '{from_activity}': {predecessorsOfToActivity}")
            # Remove the relationships along the found path
            for src, tgt in successorsOfFromActivity:
                df.at[src, tgt] = '-'
                print(f"Removed relationship: {src} -> {tgt}")
                # Also remove the reverse relationships
                df.at[tgt, src] = '-'   
            for src, tgt in predecessorsOfToActivity:
                df.at[src, tgt] = '-'
                print(f"Removed relationship: {src} -> {tgt}")
                # Also remove the reverse relationships
                df.at[tgt, src] = '-'
            # Add a new relationship from from_activity to to_activity
            df.at[from_activity, to_activity] = '~>'
            # Also add the reverse relationship
            df.at[to_activity, from_activity] = '<~'
            print(f"Added relationship: {from_activity} ~> {to_activity}")
            # Also chcek for the self-loop case
            unique_successors_predecessors = set()
            for src, tgt in successorsOfFromActivity:
                unique_successors_predecessors.add(src)
                unique_successors_predecessors.add(tgt)
            for src, tgt in predecessorsOfToActivity:
                unique_successors_predecessors.add(src)
                unique_successors_predecessors.add(tgt)
            for activity in unique_successors_predecessors:
                if df.at[activity, activity] == '||':
                    df.at[activity, activity] = '-'
                    print(f"Remove self-loop for {activity}.")

>>>>>>> f0fbb74 (Added more options for relaxation)
        else:
            print(f"Cannot remove relationship from {from_activity} to itself.")
            
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.")
    
    return df