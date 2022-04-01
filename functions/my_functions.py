from scipy.special import lambertw, digamma
from scipy.optimize import minimize
import numpy as np

# functions for species generator
# ---

def draw_J_from_float(J_f):

    J = list() # for storing the integer results
    for k, Jk in enumerate(J_f):

        J.append([])

        for Jkh_float in Jk:

            if Jkh_float == 0:

                Jkh = 0

            else:

                Jkh, prob = (int(Jkh_float // 1), Jkh_float%1)
                if np.random.rand() < prob:
                    Jkh += 1

            J[k].append(Jkh)

    return(J)


def draw_J_general(island2niches, JV, H, K):
    '''
    Draw J[k][h], the number of individuals in each niche k on each island h.
    Assumes niches have equal sizes.
    The fractional components of JV are treated probabilistically.

    
    Inputs:
    ---

    island2niches, dict { island: [ niches ] }
        A dictionary saying which islands h contain which niches k

    JV, list of floats
        The "simple" J, the carrying capacity of each island h as number of individuals

    H, integer
        Number of islands in the archipelago

    K, integer
        The total number of niches in the *archipelago*


    Outputs:
    ---

    J, list of lists of integers
        The number of individuals in each niche k on each island h
    '''

    island_num_niches = [ len(island2niches[h]) for h in range(H) ]

    J = list()
    for k in range(K):

        J.append([])

        for h in range(H):

            if k in island2niches[h]:

                num_niches = island_num_niches[h]
                Jkh_float = JV[h] / num_niches

                # treat the fractional component of Jkh_float probabilistically
                Jkh, prob = (int(Jkh_float // 1), Jkh_float%1)
                if np.random.rand() < prob:
                    Jkh += 1

            else:

                Jkh = 0

            J[k].append(Jkh)

    return(J)

def draw_sample_species_generator_general(thetakV, mV, J, D=None):
    '''
    Draw a sample using my species generator.

    Inputs
    ---

    thetakV, list of floats
        The fundamental biodiversity parameter for each niche k

    mV, list of floats
        The immigration parameter for each island h

    J, list of list of floats
        J[k][h] the number of individuals in niche k on island h

    D, list of lists of integers (optional)
        D[k][h] The number of founding individuals in each niche k (rows) on each island h (cols).
        e.g., created by calculate_D()


    Outputs:
    ---

    ancestors, list of lists of integers 
        ancestors[k][species_ID] The number of times in each niche k each ancestor species (idx) was drawn from the mainland

    community, list of lists of lists of integers
        community[k][h][species_ID] The abundace in each niche k on each island h of each species (idx).
        A zero or the absence of the index indicates that the species with that index was not present in this niche on this island.

    '''

    if D is None:
        D = [ [ 1 for jj in j ] for j in J ]

    # secondary parameters
    K = len(J)          # number of niches
    H = len(J[0])       # number of islands

    # rows are niches, index is species ID and value is the no. of times that species has immigrated
    ancestors = list() # stores a_k
    community = list() # stores n_{k,h,i}

    # count how many ancestors sampled from each niche
    no_ancestors = [ 0 for k in range(K) ] # l_k

    for k in range(K): # for each niche

        thetak = thetakV[k]
        ancestors.append([])
        community.append([])

        for h in range(H): # for each island

            community[k].append([ 0 for a_k in range(len(ancestors[k])) ])
            
            Jkh = J[k][h] # how many individuals in niche k in island h

            # deal with special case, if Jkh = 1, then is a new immigrant
            # necessary bc if Jkh = 1, then I = 0, then I/(I+j) = nan

            if Jkh == 0:

                pass # no individuals for this island and this niche

            elif Jkh == 1:

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

def draw_J(K, JV):
    '''
    Draw J[k][h], the number of individuals in each niche k on each island h.
    Simpler version that assumes all islands have the same number of niches of equal proportions.
    The fractional components of JV are treated probabilistically.

    
    Inputs:
    ---

    K, integer
        The total number of niches on each island

    JV, list of floats
        The "simple" J, the carrying capacity of each island h as number of individuals


    Outputs:
    ---

    J, list of lists of integers
        J[k][h] The number of individuals in each niche k on each island h
    '''

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

def calculate_D(mV, TV, J):
    '''
    Create D[k][h], the number of founding individuals in each niche k on island h.


    Inputs:
    ---

    mV, list of floats
        The immigration parameter for each island h
    TV, list of floats
        Time since separation for each island h. Use np.inf for always separate.
    J, list of list of integers
        J[k][h] the number of individuals in niche k on island h


    Outputs:
    ---

    D, list of list of integers
        D[k][h], the number of founding individuals in each niche k on island h.

    '''

    # secondary parameters
    K = len(J)          # number of niches
    H = len(J[0])       # number of islands

    D = list()
    for k in range(K):

        D.append([])

        for h in range(H):

            if J[k][h] == 0:

                Dkh = 0 # no individuals means no ancestor

            else:

                T = TV[h]
                m = mV[h]
                if np.isinf(T):

                    # then there is only one founding individual
                    Dkh = 1

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
# this function is a simple one that assumes the number of niches on each island is constant
def draw_sample_species_generator(theta, mV, J, D=None):
    '''
    Draw a sample using my species generator.
    Simpler version that assumes all islands have the same number of niches.

    Inputs
    ---

    theta, float
        The total fundamental biodiversity number. Function will divide
        by the number of niches to get a per-niche value.

    mV, list of floats
        m[h] The immigration parameter for each island h

    J, list of list of floats
        J[k][h] the number of individuals in each niche k on each island h

    D, list of lists of integers (optional)
        D[k][h] The number of founding individuals in each niche k (rows) on each island h (cols).
        e.g., created by calculate_D()


    Outputs:
    ---

    ancestors, list of lists of integers 
        ancestors[k][species_ID] The number of times in each niche k each ancestor species (idx) was drawn from the mainland

    community, list of list of lists of integers
        community[k][h][species_ID] The abundace in each niche k on each island h of each species (idx).
        A zero or the absence of the index indicates that the species with that index was not present in this niche on this island.
    '''

    if D is None:
        D = [ [ 1 for jj in j ] for j in J ]


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

            if Jkh == 0:

                pass # no individuals for this island and this niche

            elif Jkh == 1:

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


# functions for Chisholm model
# ---

# function for turning a species abundance distribution into a count in Preston-style Octaves
def sad2octaves(sad, octave_barriers):
    '''

    Inputs:
    ---

    sad, list of ints:
        Indices are species and values are abundances of each species

    octave_barriers, list of ints:
        Defines the barriers of the octaves
        example: octave_barriers = [ 2**(i) for i in range(max_pwr+1) ]
        
    Outputs:
    ---

    v, list of ints:
        The number of species whose abundance falls in each octave

    labs, list of strings:
        Labels for plotting giving the range of each octave
    '''

    max_pwr = len(octave_barriers) - 1
    v = list()
    labs = list()
    for idx in range(1, max_pwr+1):

        # octave bounds
        oct_hi = octave_barriers[idx];      i_hi = oct_hi-1
        oct_lo = octave_barriers[idx-1];    i_lo = oct_lo-1

        # string for the octave label
        labs.append(str(oct_lo) + '-' + str(oct_hi))

        # Preston style Octave counting -- abundances on the octave are split between the two octaves

        i_max = len(sad)

        if i_max < i_hi:

            # it's possible that the upper octave exceeds the upper abundance class in the sad
            # e.g. if very low event_rate, then all individuals are one species

            sum_indiv = sum( sad[ i_lo + 1 : i_max ] ) + 0.5*sad[i_lo]

        else:

            sum_indiv = sum( sad[ i_lo + 1 : i_hi ] ) + 0.5*sad[i_lo] + 0.5*sad[i_hi]

        v.append(sum_indiv)

    return(v, labs)


# Eq. 2.5 in Chisholm et al. (2016)
def S_fnc(theta, K, J, m):
    '''
    Inputs
    ---

    theta, float
        The total fundamental biodiversity number across all niches
    K, integer
        The number of niches
    J, float
        The carrying capacity of the island *per niche*
    m, float
        Migration parameter, immigrants per birth

    Outputs
    ---

    S, float
        Species richness
    '''
    
    S = theta*( digamma( theta/K + ((J-1)*m/(1-m))*( digamma(((J-1)*m/(1-m))+J) - digamma(((J-1)*m/(1-m))) ) ) - digamma( theta/K ) )

    return(S)


# function for fitting the species richness v island area relationship from Chisholm et al. (2016)
# and finding the (K, theta, m) set that minimises the residual
def fit_area_richness(A, S_true, rho = 1259, Ks = [1, 2, 3]):
    '''
    Inputs:
    ---

    A 
        np array of floats. Island areas.
    S_true
        np array of integers. Island species richnesses corresponding to A.
    rho
        Float. Density in individuals per unit area with units corresponding to A.
    Ks
        List of integers. List of number of niches K for which the (theta, m) that minimises the residual should be calculated

    Outputs:
    ---

    fits
        List of lists. Each element is a list corresponding to a K-value in the input Ks.
        Each element of the list is: K, residual, theta estimate, m estimate, critical area estimate.

        
    '''

    # Eq. 2.5 in Chisholm et al. (2016)
    S_fnc = lambda theta, K, J, m: theta*( digamma( theta/K + ((J-1)*m/(1-m))*( digamma(((J-1)*m/(1-m))+J) - digamma(((J-1)*m/(1-m))) ) ) - digamma( theta/K ) )


    # fit (theta, m) pair for each value of K
    # ---

    fits = list()
    for K in Ks:

        if K == Ks[0]: # on the first go, use first-estimate method from Chisholm et al. (2016)

            # initial guess for migration rate
            A_med = np.median(A)
            J = rho*A_med
            m0 = -J / ( rho * A_med * np.real(lambertw(-K/(rho*A_med),-1)) )

            # initial guess for theta
            A_max_idx = np.argmax(A)
            A_max = A[A_max_idx]
            S_A_max = S_true[A_max_idx]
            gamma = m0*(rho*A_max-1) / (1-m0)
            theta0 = S_A_max*gamma*np.log(m0) / \
                    ( S_A_max - gamma*np.log(m0) * np.real(lambertw( S_A_max*np.exp(S_A_max/(gamma*np.log(m0))) / (gamma*np.log(m0)), -1 )) )

        # else: uses the initial guess for the previous K value

        # find the (theta, m) pair that minimises the residual
        residual_fnc = lambda theta_m: np.sum(( S_true - np.array([ S_fnc(theta_m[0], K, rho*Ai/K, theta_m[1]) for Ai in A ]) )**2)
        result = minimize(residual_fnc, [theta0, m0], method='BFGS')
        theta_est, m_est = result.x
        residual_est = result.fun

        # also calculate A_critical
        A_crit = theta_est*(1-m_est)*(np.exp(K/theta_est)-1) / ( m_est*rho*np.log(1/m_est) )

        # store
        fits.append([ K, residual_est, theta_est, m_est, A_crit ])

    return(fits)


