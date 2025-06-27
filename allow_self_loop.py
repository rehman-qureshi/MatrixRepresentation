def allow_self_loop_function(df,index=None):
    """
    Allow self-loops in the DataFrame by adding '||' to the diagonal.
    """
    if index is not None:
        if index in df.index:
            df.at[index, index] = '||'
        else:
            print(f"Activtiy '{index}' not found in Matrix.")
    return df