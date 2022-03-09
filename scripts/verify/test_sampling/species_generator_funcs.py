import numpy as np


# create J[k,h], the number of individuals in niche k on island h
def draw_J(K, JV):

    # secondary parameters
    H = len(JV)     # number of islands

    J = list()
    for k in range(K):

        J.append([])

        for h in range(H):

            Jkh_float = JV[h] / K     # number of individuals that can fit

            # treat the fractional component of Jkh_float probabilistically
            Jkh, prob = (int(Jkh_float // 1), Jkh_float%1)
            if np.random.rand() < prob:
                Jkh += 1

            J[k].append(Jkh)

    return(J)

# create D[k,h], the number of founding individuals in each niche k on island h
def calculate_D(mV, TV, J):

    # secondary parameters
    K = len(J)          # number of niches
    H = len(J[0])       # number of islands

    D = list()
    for k in range(K):

        D.append([])

        for h in range(H):

            T = TV[h]
            m = mV[h]
            if np.isinf(T):

                # then there is only one founding individual
                D[k].append(1)

            else:

                # need to calculate using Chen & Chen's formula
                W = J[k][h] * m / (1-m) # Watterson's theta for the local community
                alpha = T/2
                beta = (W-1)*T/(2*J[k][h])

                if 1 / (1 + np.exp(-beta)) == 1:

                    # avoid overflow warning when beta too large (approx beta > 37, np.exp(beta) > 1e16)
                    Dkh = 1

                else:

                    Dkh = ( T*(W-1)/2 ) / ( alpha*(np.exp(beta)-1) + beta*np.exp(beta) )

                    # round it, and if it's less than 1, set it to 1
                    Dkh = int(round(Dkh))
                    Dkh = 1 if Dkh < 1 else Dkh

                D[k].append(Dkh)

    return(D)


# create a sample using my species generator
def draw_sample_species_generator(theta, mV, J, D):

    # secondary parameters
    K = len(J)          # number of niches
    H = len(J[0])       # number of islands
    thetak = theta/K    # fundamental biodiversity number per niche (assumes equal niches)

    # rows are niches, index is species ID and value is the no. of times that species has immigrated
    ancestors = list() # stores a_k
    community = list() # stores n_{k,h,i}

    # count how many ancestors sampled from each niche
    no_ancestors = [ 0 for k in range(K) ] # l_k

    for k in range(K): # for each niche

        ancestors.append([])
        community.append([])

        for h in range(H): # for each island

            community[k].append([ 0 for a_k in range(len(ancestors[k])) ])
            
            Jkh = J[k][h] # how many individuals in niche k in island h

            # deal with special case, if Jkh = 1, then is a new immigrant
            # necessary bc if Jkh = 1, then I = 0, then I/(I+j) = nan

            if Jkh == 1:

                # has to be a new immigrant
                if np.random.rand() < thetak / ( thetak + no_ancestors[k] ):

                    # the immigrant was a new species
                    ancestors[k].append(1)
                    community[k][h].append(1)

                else:

                    # the immigrant was a species we've seen before
                    prob_i = [ ai / no_ancestors[k] for ai in ancestors[k] ] 
                    i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                    ancestors[k][i_star] += 1
                    community[k][h][i_star] += 1

                # increment the ancestors counter
                no_ancestors[k] += 1

            else: # if Jkh > 1

                # first, sample the individuals who were founders T generations ago, when island separated
                # from mainland (or, if T = inf, then Dkh = 1, therefore just sample the first immigrant)

                Dkh = D[k][h]
                for j in range(Dkh):

                    if np.random.rand() < thetak / ( thetak + no_ancestors[k] ):

                        # the immigrant was a new species
                        ancestors[k].append(1)
                        community[k][h].append(1)

                    else:

                        # the immigrant was a species we've seen before
                        prob_i = [ ai / no_ancestors[k] for ai in ancestors[k] ] 
                        i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                        ancestors[k][i_star] += 1
                        community[k][h][i_star] += 1

                    # increment the ancestors counter
                    no_ancestors[k] += 1


                # now sample the remainder of the individuals, who are a mix of descendants
                # and immigrants

                I = mV[h] * (Jkh-1) / (1-mV[h])     # Etienne's immigration parameter

                for j in range(Dkh, Jkh):

                    if (np.random.rand() < I / (I+j)):

                        # we have drawn an immigrant

                        if np.random.rand() < thetak / ( thetak + no_ancestors[k] ):

                            # the immigrant was a new species
                            ancestors[k].append(1)
                            community[k][h].append(1)

                        else:

                            # the immigrant was a species we've seen before
                            prob_i = [ ai / no_ancestors[k] for ai in ancestors[k] ]
                            i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                            ancestors[k][i_star] += 1
                            community[k][h][i_star] += 1

                        # increment the ancestors counter
                        no_ancestors[k] += 1

                    else:

                        # it's a birth-death
                        prob_i = [ ni / j for ni in community[k][h] ]
                        i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                        community[k][h][i_star] += 1

    return(ancestors, community)
