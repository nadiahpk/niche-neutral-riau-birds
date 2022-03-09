# Equation 17 seems to be an approximation of the expected number of ancestral lineages when mutation is omitted. So see how it looks

import matplotlib.pyplot as plt
from math import exp


# parameters
# ---

dir_results = '../../../results/verify/chen_matches_tavare/'

M = 10000       # size of the population
n = M           # size of the sample = size of population in our case
max_t_pwr = 5   # calculate expected value 10^max_t_pwr generations back

# truncate the calculation when v_i * c_i < vici_cutoff
vici_cutoff = 1e-4 # determines when I truncate terms in the sum

# mutation rates (analogous to immigration in our case)
uV =      [0, 0.001, 0.01, 0.1, 0.5]
colourV = ['red', 'blue', 'orange', 'magenta', 'brown'] # for plotting curve for each mutation rate

# compare the Chen and Tavare equations for each mutation rate
# ---

# add fake lines so I can label Tavare and Chen sold and dashed
plt.plot([], [], ls='solid', color='black', alpha=0.5, label="Exact")
plt.plot([], [], ls='dashed', color='black', label="Chen & Chen approximation")

for colour, u in zip(colourV, uV):

    # up to the max, but we'll delete some later
    tV = [ i*10**j for j in range(max_t_pwr) for i in range(1,10) ] + [ 10**max_t_pwr ]


    # calculate E[D_t] using truncated version of Tavare's exact equation
    # ---

    # split the equation into three terms, called c_i, q_i, and v_i below

    theta = M*u/(1-u)

    # first values
    i = 1
    v_i = (n-i+1) / (n+theta+i-1)
    c_i = 2*i + theta - 1

    # initialise list for storage
    v = [v_i]; c = [c_i];

    i = 2
    while (i <= n) and v_i*c_i > vici_cutoff:

        # recursion for term with falling and rising factorial
        v_i = v[i-2] * (n-i+1) / (n+theta+i-1)
        c_i = 2*i + theta - 1

        # append and increment counter
        v.append( v_i )
        c.append( c_i )
        i += 1

    print('number of terms of v_i used: ' + str(len(v)))

    # q_i term in E[D_t] depends on t, so calculate for each t of interest
    E_DtV = list()
    for t in tV:

        q = [ exp(-i*(i+theta-1)*t / (2*M)) for i in range(1, len(v)+1) ]
        E_Dt = sum( v_i * q_i * c_i for v_i, q_i, c_i in zip(v, q, c) )
        E_DtV.append(E_Dt)

    tV, E_DtV = zip(* [ (t, E_Dt) for t, E_Dt in zip(tV, E_DtV) if E_Dt >= 1  ] )

    # calculate E[D_t] using Chen and Chen's asymptotic approximation
    # ---

    '''
    # experimenting -- no mutations -- works!

    E_Dt_asyV = list()
    for t in tV:

        alpha = t/2
        beta = -t/(2*n)
        eta = alpha*beta / ( alpha*(exp(beta)-1) + beta*exp(beta) )
        E_Dt_asy = 2*eta*n / t 
        E_Dt_asyV.append( E_Dt_asy )

    # experimenting -- mutations -- works!
    E_Dt_asyV = list()
    for t in tV:

        alpha = t/2
        beta = (theta-1)*t/(2*n)
        eta = alpha*beta / ( alpha*(exp(beta)-1) + beta*exp(beta) )
        E_Dt_asy = 2*eta*n / t 
        E_Dt_asyV.append( E_Dt_asy )
    '''

    # simplify the equation a bit
    E_Dt_asyV = list()
    for t in tV:

        alpha = t/2
        beta = (theta-1)*t/(2*n)
        E_Dt_asy = ( t*(theta-1)/2 ) / ( alpha*(exp(beta)-1) + beta*exp(beta) )
        E_Dt_asyV.append( E_Dt_asy )


    # label=r'Chen and Chens Tavare equation (basically exact)');
    plt.plot(tV, E_DtV,     alpha=0.5, color=colour, ls='solid', label=r'$\mu=' + str(u) +'$')
    # label=r'Chen and Chens asymptotic (Eq. 17 + my guesswork)');
    plt.plot(tV, E_Dt_asyV, alpha=1, lw=2, color=colour, ls='dashed')

plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'generations back in time, $t$')
plt.ylabel(r'expected number of old equivalence classes, $E[D_t]$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_results + 'chen_2013.pdf')
plt.close()



