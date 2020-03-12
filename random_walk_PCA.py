# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 05:29:56 2020

@author: Rene
"""
    from sklearn.decomposition import PCA
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy
    
    # SETUP simulation parameters
    N_intervals =  5000 # can restrict range to see how interval sample range affects behaviour
    N_samples = 1000 
    N_PCs = 5
    fig_num = 0
    mu = 1
    sd = 1
    np.random.seed(8736)
    
    sim_data = np.empty((N_samples,N_intervals))
    # starts the samples at zero, to start at random positions 
    sim_data[:,0] = np.zeros((N_samples)) 
    
    # simulate time dependent random walk - you can replace the step change with 
    # any distribution or stochastic process you want. The -0.5 gives a mean change of 0
    for i in range(1,N_intervals):
        sim_data[:,i] = sim_data[:,i-1] + np.random.normal( mu , sd , (N_samples) )
    
    # plot how the data varies against time for each run
    fig_num =+ 1
    plt.figure(fig_num)
    plt.plot(sim_data.T)
    plt.xlabel('Time Increment')
    plt.ylabel('Value')
    title = str( N_samples ) + ' simulated random time walks' 
    plt.title(title)
    plt.figure(fig_num).savefig( title + '.png')
                                  
    # plot dispersion against interval 
    sim_data_sd = np.std(sim_data,axis=0)
    fig_num += 1
    plt.figure(fig_num)
    plt.plot(sim_data_sd)
    plt.xlabel('Time Increment')
    plt.ylabel('SD')
    title = ( 'Standard Devation between ' + str( N_samples ) + 
             ' simulated random time walks vs time interval' )
    plt.title(title)
    plt.figure(fig_num).savefig( title + '.png')
    
    # plot R2 against interval 
    ranges = (10**np.arange(np.log10(50),np.log10(5001),0.25)).astype('int')
    r = np.empty((N_samples,np.shape(ranges)[0]))
    for iSam in range(N_samples):
        for iInt in range(ranges.shape[0]):
            a , b , r[iSam,iInt], p , se = ( 
                scipy.stats.linregress(np.arange(ranges[iInt]), sim_data[iSam,:ranges[iInt]]) )
            #currently not storing slope a or intercept b as only looking at R
    fig_num += 1
    plt.figure(fig_num)
    plt.plot(ranges, r.T**2,'.') # this is one version of R2
    plt.xlabel('Time Increment')
    plt.ylabel('$R^2$')
    title = ( 'Individal R2 for ' + str( N_samples ) + 
             ' simulated random time walks vs interval' )
    plt.title(title)
    plt.figure(fig_num).savefig( title + '.png')
    
    fig_num += 1
    plt.figure(fig_num)
    plt.plot(ranges, np.mean(r.T**2,axis=1),'.') # this is one version of R2
    plt.xlabel('Time Increment')
    plt.ylabel('$R^2$')
    title = ( 'mean R2 for ' + str( N_samples ) + 
             ' simulated random time walks vs interval' )
    plt.title(title)
    plt.figure(fig_num).savefig( title + '.png')
    
    
    # Here's the PCA eigenvectors
    random_walk_PCA = PCA( n_components=N_PCs )  # fit a PCA to the simulated data
    random_walk_PCA.fit(sim_data)
    fig_num = fig_num+1
    plt.figure(fig_num)
    plt.plot(random_walk_PCA.components_.T + np.arange(0,-0.05*N_PCs,-0.05))
    plt.xlabel('Time Increment')
    plt.ylabel('Weighting')
    title = 'PCA eigenvectors  from ' + str( N_samples ) + ' random walks' 
    plt.title(title)
    plt.figure(fig_num).savefig( title + '.png' )
    
                       
