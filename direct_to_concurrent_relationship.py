def direct_to_concurrent_relationship_function(df,from_activity,to_activity):
    # Change relationship from '→' to '||'
    if from_activity in df.columns and to_activity in df.index:
        if to_activity != from_activity:
            if df.at[from_activity, to_activity] == '→':
                df.at[from_activity, to_activity] = '||'
                #Also change the reverse relationship
                df.at[to_activity, from_activity] = '||'
                print(f"Changed relationship from {from_activity} → {to_activity} to {from_activity} || {to_activity}\n")
            else:
                print(f"No direct relationship from {from_activity} to {to_activity} to change.\n")                        
        else:
                print(f"Same activities detected. No change made.\n")
    else:
        print("Invalid activities provided.\n")

    return df