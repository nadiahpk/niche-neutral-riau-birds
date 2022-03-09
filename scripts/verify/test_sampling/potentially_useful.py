# bits of code I might need later


'''
data = [['New York Yankees', 'Acevedo Juan', 900000, 'Pitcher'],
        ['New York Yankees', 'Anderson Jason', 300000, 'Pitcher'],
        ['New York Yankees', 'Clemens Roger', 10100000, 'Pitcher'],
        ['New York Yankees', 'Contreras Jose', 5500000, 'Pitcher']]

df = pd.DataFrame.from_records(data, columns = column_names)
'''


# [data[i:i+col] for i in range(0, len(data), col)]

'''
# create a presence-absence matrix of the data
# ---

isle_names = [ 'simulated_' + str(h) for h in range(H) ]
spp_IDs = [ (k, i) for k in range(K) for i in range(len(ancestors[k])) ]
spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]
S = len(spp_IDs)

df = pd.DataFrame(data, index=spp_names)
df.to_csv(dir_results + 'example_1.csv', index=True)


# count the number of species on each island
# ---

if False:
    # use this if you don't make presence-absence matrix above

    no_sppV = [0]*H
    for k in range(K):
        for h in range(H):
            no_sppV[h] += sum( 1 for ni in community[k][h] if ni > 0 )

no_sppV = df.sum(axis=0).values
'''


'''
# plot species area relationship for verifying correctness
# ---

plt.xscale('log')

# do the sample
plt.scatter(JV, no_sppV, alpha=0.7, color='black', label='sample')

# do the theoretical curve
A_pwr_min = np.log10(AV[0]); A_pwr_max = np.log10(AV[-1])
A_pwrV = np.linspace( A_pwr_min, A_pwr_max, 100 )
AV = 10**A_pwrV
JV = [ A*rho for A in AV ]

S_fnc = lambda theta, K, J, m: theta*( digamma( theta/K + ((J-1)*m/(1-m))*( digamma(((J-1)*m/(1-m))+J) - digamma(((J-1)*m/(1-m))) ) ) - digamma( theta/K ) )

SV = [ S_fnc(theta, K, J/K, m) for J in JV ]

plt.plot(AV, SV, color='blue', label='theoretical curve')

# plot critical A
A_crit = theta*(1-m)*(np.exp(K/theta)-1) / ( m*rho*np.log(1/m) )

# decorations
plt.legend(loc='best')
plt.axvline(A_crit, color='black', ls='dashed')
plt.xlabel(r'area (km$^2$)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'example' + suffix + '.pdf')
plt.close()
'''
