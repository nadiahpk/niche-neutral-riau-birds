
def standardise_name(string):
    # colleagues keep on changing the data
    # this avoids issues with arbitrary upper and lower cases etc.

    return( string.lower().replace(' ', '_').replace('-','_').replace('\'','').replace('(','').replace(')','') )
