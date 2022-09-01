# Plotting script for SyLaNN simulations with gammaIdx iteration
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import math
from pylab import cm, contour, colorbar, clabel

gamma_nSteps = 10
gamma_start, gamma_stop = 0, 1+gamma_nSteps
# as a list of integers and list of strings
gamma_list = list(range(gamma_start, gamma_stop))

# folder name and file name (without gammaIdx numbering)
date_str = '2022-08-31'
time_str = '11-04-58'
folder_name = date_str + '_testPlotting'
if os.path == 'nt': # Windows
    folder_path = folder_name + '\\'
else: # Linux 
    folder_path = folder_name + '/'
# Note: leave out idx numbering and file format (.json) as this will change during the results loading loop
simulation_name = '_2Dpoly_whiteNoise_gammaIdx'
time_simulation_name = time_str + simulation_name
path_name = folder_path + time_simulation_name
file_format = '.json'

# create overall dictionary
results_dict = {}

# fill results dictionary with simulation results (nested dictionary of dicionaries)
for gammaIdx in gamma_list:
    current_key = gammaIdx
    current_json_name = path_name + str(current_key) + file_format
    # read current results file and save into dictionary
    json_file_data = open(current_json_name,)
    current_file = json.load(json_file_data)
    json_file_data.close()
    # write into overall dictionary at specific key
    results_dict[current_key] = current_file

######################## Plotting functions ########################
def linePlot_pred_vs_ref(domain, eq_pred, eq_ref, plot_saved_name):
    fig,ax = plt.subplots()
    ref = ax.plot(domain, eq_ref, 'k-', label='reference')
    ax.set_xlabel(r'$\mathbf{x}$')
    ax.set_ylabel(r'$\mathbf{y(x)}$')
    ax2 = ax.twinx()
    pred = ax2.plot(domain, eq_pred, 'r--', label='prediction')
    ax2.set_ylabel(r'$\mathbf{\hat{y}(x)}$', color='r')
    bothPlots = ref+pred
    both_i = [l.get_label() for l in bothPlots]
    ax.legend(bothPlots, both_i, loc='upper left')
    # plt.xlim plt.ylim etc
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

def linePlot_betaAlpha(epochs, beta, alpha, plot_saved_name):
    fig,ax = plt.subplots()
    ref = ax.plot(epochs, beta, 'r-', label=r'$\beta$')
    ax.set_xlabel(r'number of epochs')
    ax.set_ylabel(r'data error factor $\beta$', color='r')
    ax2 = ax.twinx()
    pred = ax2.plot(epochs, alpha, 'b-', label=r'$\alpha$')
    ax2.set_ylabel(r'weights error factor $\alpha$', color='b')
    bothPlots = ref+pred
    both_i = [l.get_label() for l in bothPlots]
    ax.legend(bothPlots, both_i, loc='upper left')
    # plt.xlim plt.ylim etc
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

def linePlot_traintesterror(epochs, train_error, test_error, plot_saved_name):
    fig = plt.figure()
    plt.plot(epochs, train_error, 'b-', label=r'training error $\mathcal{E}_{train}$')
    plt.plot(epochs, test_error, 'r-', label=r'test error $\mathcal{E}_{test}$')
    plt.xlabel(r'number of epochs')
    plt.ylabel(r'sum of squared errors')
    plt.legend(loc='upper right')
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

def linePlot_traintesterror_logscale(epochs, train_error, test_error, plot_saved_name):
    fig = plt.figure()
    plt.semilogy(epochs, train_error, 'b-', label=r'training error $\mathcal{E}_{train}$')
    plt.semilogy(epochs, test_error, 'r-', label=r'test error $\mathcal{E}_{test}$')
    plt.xlabel(r'number of epochs')
    plt.ylabel(r'log(sum of squared errors)')
    plt.legend(loc='upper right')
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

def contourPlot_ref(x_domain, reference, plot_saved_name):
    fig = plt.figure()
    x_min = x_domain[0]
    x_max = x_domain[-1]
    im = plt.imshow(reference, origin='lower', cmap=cm.twilight_shifted, extent=[x_min, x_max, x_min, x_max]) #, 'r-', label=r'test error $\mathcal{E}_{test}$')
    # adding the Contour lines with labels
    cset = contour(reference, np.arange(np.min(reference),np.max(reference),1.5), origin='lower', extent=[x_min, x_max, x_min, x_max], linewidths=1.5, cmap=cm.twilight)
    clabel(cset,inline=True,fmt='%1.1f',fontsize=8)
    colorbar(im) # adding the colobar on the right
    plt.xlabel(r'x')
    plt.ylabel(r'y')
    #plt.colorbar()
    #plt.legend(loc='upper right')
    plot_saved_name = plot_saved_name + '_ref'
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    #plt.grid()
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

def contourPlot_pred(x_domain, prediction, plot_saved_name):
    fig = plt.figure()
    x_min = x_domain[0]
    x_max = x_domain[-1]
    im = plt.imshow(prediction, origin='lower', cmap=cm.twilight_shifted, extent=[x_min, x_max, x_min, x_max]) #, 'r-', label=r'test error $\mathcal{E}_{test}$')
    # adding the Contour lines with labels
    cset = contour(prediction, np.arange(np.min(prediction),np.max(prediction),1.5), origin='lower', extent=[x_min, x_max, x_min, x_max], linewidths=1.5, cmap=cm.twilight)
    clabel(cset,inline=True,fmt='%1.1f',fontsize=8)
    colorbar(im) # adding the colobar on the right
    plt.xlabel(r'x')
    plt.ylabel(r'y')
    #plt.xlim(x_min, x_max)
    #plt.ylim(x_min, x_max)
    #plt.legend(loc='upper right')
    plot_saved_name = plot_saved_name + '_pred'
    fig.savefig(plot_saved_name + '.png', bbox_inches='tight')
    #plt.grid()
    fig.savefig(plot_saved_name + '.pdf', bbox_inches='tight')
    # plt.show()
    plt.close()

######################## PLOTS #########################
# E(lastic)N(et), Lhalf, BR on/off, Div on/off
plot_folder_name = date_str + '_plots' + simulation_name + '_EN_BR-on-Div-on'
try:
    os.mkdir(plot_folder_name)
except OSError:
    print ("Creation of the directory %s failed (already exists)" % plot_folder_name)
else:
    print ("Successfully created the directory %s " % plot_folder_name)

if os.path == 'nt': # Windows
    plots_path = plot_folder_name + '\\'
else: # Linux 
    plots_path = plot_folder_name + '/'

#file_type = '.png'
is2D = True

if is2D is False:
    # Loop over gamma values (L1 ratio of elastic net penalty) and create/save plots
    for plotIdx in gamma_list:
        current_results = results_dict[plotIdx]
        x_domain = current_results['domain_test']
        x_domain_steps = 100
        x_domain = np.linspace(x_domain[0], x_domain[1], num=x_domain_steps)
        # plot ref vs prediction
        plot_name = 'gammaIdx' + str(plotIdx) + '_ref-vs-pred'# + file_type
        path_saveTo = plots_path + plot_name
        ref_eq = eval(current_results['ref_fct_str'])
        ref_eq_list = [ref_eq(i) for i in x_domain]
        prediction = eval(current_results['found_eq'])
        # TODO find way to cut predicted results vars!
        # TODO why exp etc with Python's math module?
        # prediction_list = [prediction(i,1,1) for i in x_domain]
        prediction_list = [prediction(i) for i in x_domain]
        linePlot_pred_vs_ref(x_domain, prediction_list, ref_eq_list, path_saveTo)

        # plot training and testing errors
        plot_name = 'gammaIdx' + str(plotIdx) + '_errors'# + file_type
        path_saveTo = plots_path + plot_name
        n_epochs = current_results['trainEpochs3']
        epochs = np.linspace(1, n_epochs, num=n_epochs+1)
        train_error_onlySSE = current_results['training_onlySSE_loss']
        # train_error = data_dict['training_loss']
        test_error = current_results['testing_loss']
        linePlot_traintesterror(epochs, train_error_onlySSE, test_error, path_saveTo)

        # plot training and testing errors (log scale)
        plot_name = 'gammaIdx' + str(plotIdx) + '_errorsLog'# + file_type
        path_saveTo = plots_path + plot_name
        linePlot_traintesterror_logscale(epochs, train_error_onlySSE, test_error, path_saveTo)

        # plot factor development of BR
        if current_results['chooseBR'] is True:
            plot_name = 'gammaIdx' + str(plotIdx) + '_BRfactors'# + file_type
            path_saveTo = plots_path + plot_name
            beta = current_results['beta_SSE']
            alpha = current_results['alpha_reg']
            nUpdates_BR = len(beta)
            epochs_BR = np.linspace(1, n_epochs, num=nUpdates_BR)
            linePlot_betaAlpha(epochs_BR, beta, alpha, path_saveTo)

if is2D is True:
    # Loop over gamma values (L1 ratio of elastic net penalty) and create/save plots
    for plotIdx in gamma_list:
        current_results = results_dict[plotIdx]
        x_domain = current_results['domain_test']
        x_domain_steps = 100
        domain_discr = np.linspace(x_domain[0], x_domain[1], num=x_domain_steps)
        X, Y = np.meshgrid(domain_discr, domain_discr)
        # plot ref vs prediction
        plot_name = 'gammaIdx' + str(plotIdx)
        path_saveTo = plots_path + plot_name
        ref_eq = eval(current_results['ref_fct_str'])
        ref_eq_list = ref_eq(X, Y) # [ref_eq(i) for i in x_domain]
        contourPlot_ref(x_domain, ref_eq_list, path_saveTo)

        plot_name = 'gammaIdx' + str(plotIdx)
        path_saveTo = plots_path + plot_name
        prediction = eval(current_results['found_eq'])
        prediction_list = prediction(X, Y) # [prediction(i,j) for i in domain_discr for j in domain_discr]
        contourPlot_pred(x_domain, prediction_list, path_saveTo)

        # plot training and testing errors
        plot_name = 'gammaIdx' + str(plotIdx) + '_errors'# + file_type
        path_saveTo = plots_path + plot_name
        n_epochs = current_results['trainEpochs3']
        epochs = np.linspace(1, n_epochs, num=n_epochs+1)
        train_error_onlySSE = current_results['training_onlySSE_loss']
        # train_error = data_dict['training_loss']
        test_error = current_results['testing_loss']
        linePlot_traintesterror(epochs, train_error_onlySSE, test_error, path_saveTo)

        # plot training and testing errors (log scale)
        plot_name = 'gammaIdx' + str(plotIdx) + '_errorsLog'# + file_type
        path_saveTo = plots_path + plot_name
        linePlot_traintesterror_logscale(epochs, train_error_onlySSE, test_error, path_saveTo)

        # plot factor development of BR
        if current_results['chooseBR'] is True:
            plot_name = 'gammaIdx' + str(plotIdx) + '_BRfactors'# + file_type
            path_saveTo = plots_path + plot_name
            beta = current_results['beta_SSE']
            alpha = current_results['alpha_reg']
            nUpdates_BR = len(beta)
            epochs_BR = np.linspace(1, n_epochs, num=nUpdates_BR)
            linePlot_betaAlpha(epochs_BR, beta, alpha, path_saveTo)

print('Done plotting.')
