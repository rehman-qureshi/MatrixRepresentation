def relationship_exists(df, from_activity, to_activity):
    """
    Check if a specific relationship exists between two activities in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
        return df.at[from_activity, to_activity] == '→'
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.")
        return False

def remove_specific_relationship_function(df, from_activity, to_activity):
    """
    Remove a specific relationship between two activities in the Matrix.
    """
    if from_activity in df.columns and to_activity in df.index:
        if from_activity != to_activity:
            # Check if a path exists from from_activity to to_activity
            if not relationship_exists(df, from_activity, to_activity):
                print(f"No relationship from {from_activity} to {to_activity}.")
                return df
            # If a path exists, remove the relationship
            print(f"Removing relationship from {from_activity} to {to_activity}.")
            predecessorsOfFromActivtiy = [col for col in df.columns if df.at[col, from_activity] == '→']
            print(f"Predecessors of '{from_activity}': {predecessorsOfFromActivtiy}")
            # Remove the relationship from from_activity to to_activity
            df.at[from_activity, to_activity] = '-'
            print(f"Removed relationship: {from_activity} -> {to_activity}")
            for predecessor in predecessorsOfFromActivtiy:
                if predecessor != to_activity:
                    #df.at[predecessor, from_activity] = '-'
                    #print(f"Removed relationship: {predecessor} -> {from_activity}")
                    df.at[predecessor, to_activity] = '~>'
                    print(f"Added relationship: {predecessor} ~> {to_activity}")
        else:
            print(f"Cannot remove relationship from {from_activity} to itself.")
    else:
        print(f"Activities '{from_activity}' or '{to_activity}' not found in Matrix.")
    return df