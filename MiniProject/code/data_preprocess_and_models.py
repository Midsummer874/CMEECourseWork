import pandas as pd
import scipy as sc
import numpy as np
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns # You might need to install this (e.g., pip install seaborn)
from scipy.optimize import leastsq
from sklearn.metrics import r2_score
from lmfit import Minimizer, Parameters, report_fit

import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("../data/LogisticGrowthData.csv")
df.insert(0, "ID", df.Species + "_" + df.Temp.map(str) + "_" + df.Medium + "_" + df.Citation)

def residuals_logistic(params , Time, PopBio):
    N_0, N_max, r = params
    predict = N_0 * N_max * np.exp(r * Time) / (N_max + N_0 * (np.exp(r*Time) - 1))
    return PopBio - predict

def logistic_fit(Time, PopBio):
    init_params = [PopBio[0], PopBio[-1], 0.5]
    param_lsq = leastsq(residuals_logistic, init_params, args=(Time, PopBio))[0]
    N_0, N_max, r = param_lsq
    PopBio_pred = N_0 * N_max * np.exp(r * Time) / (N_max + N_0 * (np.exp(r*Time) - 1))
    return param_lsq, PopBio_pred

def residuals_gompertz(params, t, data):
    '''Model a logistic growth and subtract data'''
    #Get an ordered dictionary of parameter values
    v = params.valuesdict()
    #Logistic model
    model = v['N_0'] + (v['N_max'] - v['N_0']) * \
    np.exp(-np.exp(v['r_max'] * np.exp(1) * (v['t_lag'] - t) / \
                   ((v['N_max'] - v['N_0']) * np.log(10)) + 1))
    #Return residuals
    return model - data

def Gompertz_fit(Time, PopBio):
    #Create object for parameter storing
    params_gompertz = Parameters()
    # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
    params_gompertz.add_many(('N_0', np.log(PopBio)[0] , True, 0, None, None, None),
                             ('N_max', np.log(PopBio)[-1], True, 0, None, None, None),
                             ('r_max', 0.62, True, None, None, None, None),
                             ('t_lag', 5, True, 0, None, None, None))#I see it in the graph

    #Create a Minimizer object
    minner = Minimizer(residuals_gompertz, params_gompertz, fcn_args=(Time, np.log(PopBio)))
    #Perform the minimization
    fit_gompertz = minner.minimize()
    return fit_gompertz
    

def cal_AIC(y_true, y_pred , p):
    residual = y_true - y_pred 
    RSS = sum(residual**2)
    n = len(y_true)
    AIC = n * np.log(RSS/n) + 2*p
    return AIC
    
    
def cal_AICC(y_true, y_pred , p):
    aic = cal_AIC(y_true, y_pred , p)
    n = len(y_true)
    AICC = aic + 2*p*(p + 1)/(n - p - 1)
    return AICC
    
# def save_figure_fitting(Time, PopBio, PopBio_pred, fit_name , unit, fileName ):
#     plt.scatter( Time, PopBio, label = 'Observation')
#     plt.plot(Time, PopBio_pred, label = 'Logistic fit', c = 'r')
#     plt.xlabel("Time(Hours)")
#     plt.ylabel("Population({})".format(unit))
#     plt.legend()
#     plt.title(fit_name)
#     plt.savefig(fileName, dpi = 500)
#     plt.show()

ID_set = sorted(set(df['ID']))
DFs = []

R2_list = []
AIC_list = []
AICC_list = []

logistic_params = []
Gompertz_params = []
OLS_params = []
Quadratic_params = []


ID_list = []
unit_list = []

DFs = []
for i, ID in enumerate(ID_set):
    mask = df.ID == ID
    ID_df = df[mask].reset_index(drop = True)
    unit = df['PopBio_units'][0]
    ID_df = ID_df[ID_df['Time'] > 0]
    ID_df = ID_df[ID_df['PopBio'] > 0]
    ID_df = ID_df.sort_values("Time")
    Time = ID_df['Time'].values
    PopBio = ID_df['PopBio'].values
    
    predict_df = pd.DataFrame({'Time': Time, 'PopBio':PopBio })
    predict_df['PopBio_units'] = unit
    predict_df.insert(0, "ID",  ID)
    
    try:
    
        # Gompertz model
        fit_gompertz = Gompertz_fit(Time, PopBio)
        N_0 = fit_gompertz.params['N_0'].value
        N_max = fit_gompertz.params['N_max'].value
        r_max = fit_gompertz.params['r_max'].value
        t_lag = fit_gompertz.params['t_lag'].value

        log_PopBio_pred = N_0 + (N_max - N_0) * \
            np.exp(-np.exp(r_max * np.exp(1) * (t_lag - Time) / \
                           ((N_max - N_0) * np.log(10)) + 1))

        Gompertz_pred = np.exp(log_PopBio_pred)
        Gompertz_r2 = r2_score(PopBio, Gompertz_pred)  
        Gompertz_AIC = cal_AIC(PopBio, Gompertz_pred, p = 4)
        Gompertz_AICC = cal_AICC(PopBio, Gompertz_pred, p = 4)

        # Logistic model
        param_lsq, Logistic_pred = logistic_fit(Time, PopBio)
        Logistic_r2 = r2_score(PopBio, Logistic_pred)   
        Logistic_AIC = cal_AIC(PopBio, Logistic_pred, p = 3)
        Logistic_AICC = cal_AICC(PopBio, Logistic_pred, p = 3)

        # OLS fit
        fit_linear_OLS = np.polyfit(Time, np.log(PopBio), 3) # degree = 3 as this is a cubic 
        OLS_func = np.poly1d(fit_linear_OLS)
        log_PopBio_pred = OLS_func(Time)
        OLS_pred = np.exp(log_PopBio_pred)
        OLS_r2 = r2_score(PopBio, OLS_pred)
        OLS_AIC = cal_AIC(PopBio, OLS_pred, p = 4)
        OLS_AICC = cal_AICC(PopBio, OLS_pred, p = 4)
        
        # Quadratic fit
        fit_Quadratic_OLS = np.polyfit(Time, np.log(PopBio), 2) # degree = 2 as this is a Quadratic 
        OLS_func = np.poly1d(fit_Quadratic_OLS)
        log_PopBio_pred = OLS_func(Time)
        OLS_pred = np.exp(log_PopBio_pred)
        Quadratic_r2 = r2_score(PopBio, OLS_pred)
        Quadratic_AIC = cal_AIC(PopBio, OLS_pred, p = 3)
        Quadratic_AICC = cal_AICC(PopBio, OLS_pred, p = 3)
        
        # summary 
        predict_df['Gompertz_fit'] = Gompertz_pred
        predict_df['Logistic_fit'] = Logistic_pred
        predict_df['OLS_fit'] = OLS_pred
        DFs.append(predict_df)
        unit_list.append(unit)
        ID_list.append(ID)
        
        R2_list.append([Gompertz_r2,Logistic_r2, OLS_r2, Quadratic_r2 ])
        AIC_list.append([Gompertz_AIC, Logistic_AIC, OLS_AIC, Quadratic_AIC])
        AICC_list.append([Gompertz_AICC, Logistic_AICC, OLS_AICC, Quadratic_AICC])
        
        Gompertz_params.append([N_0, N_max, r_max, t_lag])
        logistic_params.append(param_lsq)
        OLS_params.append(fit_linear_OLS)
        Quadratic_params.append(fit_Quadratic_OLS)

        # fitting figure
        length_ID = len(ID)
        n_split = 6
        row_length = length_ID // n_split
        title = []
        for i in range(n_split - 1):
            title.append(ID[i*row_length :i*row_length+row_length])
        title.append(ID[i*row_length+row_length:])
        title = '\n'.join(title)

        fileName = "../sandbox/"+ ID[:50] + '.png'

#        plt.figure(figsize = (7,4))
#        plt.scatter( Time, PopBio, label = 'Observation')
#        plt.plot(Time, Logistic_pred, label = 'Logistic fit')
#        plt.plot(Time, Gompertz_pred, label = 'Gompertz fit')
#        plt.plot(Time, OLS_pred, label = 'OLS fit')
#        plt.legend()
#        plt.xlabel("Time(Hours)")
#        plt.ylabel("Population({})".format(unit))
#       plt.title(title)
#        plt.savefig(fileName, dpi = 500)
#        plt.show()
    except:
        pass


concat_pred_df = pd.concat(DFs)
concat_pred_df.to_csv('../results/prediction_result.csv', index = None)


logistic_param_df = pd.DataFrame(logistic_params, columns = ['N_0', 'N_max', 'r'])
logistic_param_df.insert(0,'PopBio_units', unit_list)
logistic_param_df.insert(0,'ID', ID_list)
logistic_param_df['R-square'] = np.array(R2_list)[:,1]
logistic_param_df['AIC'] = np.array(AIC_list)[:,1]
logistic_param_df.to_csv("../results/Logistic_fit_params_result.csv", index = None)


Gompertz_param_df = pd.DataFrame(Gompertz_params, columns = ['N_0', 'N_max', 'r_max', 't_lag'])
Gompertz_param_df.insert(0,'PopBio_units', unit_list)
Gompertz_param_df.insert(0,'ID', ID_list)
Gompertz_param_df['R-square'] = np.array(R2_list)[:,0]
Gompertz_param_df['AIC'] = np.array(AIC_list)[:,0]
Gompertz_param_df.to_csv("../results/Gompertz_fit_params_result.csv", index = None)

OLS_param_df = pd.DataFrame(OLS_params, columns = [ 'Time^3', 'Time^2', 'Time', 'constant'])
OLS_param_df.insert(0,'PopBio_units', unit_list)
OLS_param_df.insert(0,'ID', ID_list)
OLS_param_df['R-square'] = np.array(R2_list)[:,-2]
OLS_param_df['AIC'] = np.array(AIC_list)[:,-2]
OLS_param_df.to_csv("../results/Cubic_Polynomial_fit_params_result.csv", index = None)

Quadratic_param_df = pd.DataFrame(Quadratic_params, columns = [ 'Time^2', 'Time', 'constant'])
Quadratic_param_df.insert(0,'PopBio_units', unit_list)
Quadratic_param_df.insert(0,'ID', ID_list)
Quadratic_param_df['R-square'] = np.array(R2_list)[:,-1]
Quadratic_param_df['AIC'] = np.array(AIC_list)[:,-1]
Quadratic_param_df.to_csv("../results/Quadratic_Polynomial_fit_params_result.csv", index = None)



model_names = ['Logistic', 'Gompertz', 'Cubic Polynomial', 'Quadratic Polynomial']

R2_df = pd.DataFrame(R2_list, index = ID_list, columns = model_names)
print("R-square descriptive statistics:")
print(R2_df.describe())


AIC_df = pd.DataFrame(AIC_list, index = ID_list, columns = model_names)
print("AIC descriptive statistics:")
print(AIC_df.describe())

AICC_df = pd.DataFrame(AICC_list, index = ID_list, columns = model_names)
print("AICC descriptive statistics:")
print(AICC_df.describe())

fitted_count = (R2_df > 0 ).sum()
plt.figure(figsize = (9,5))
plt.bar(model_names, fitted_count , alpha = 0.5)
plt.grid()
plt.ylabel("Count")
plt.title("Convergence Count for Different Model Method")
plt.savefig('../results/Model_Convergence_Count.png', dpi = 500)
#plt.show()

n = len(R2_df)
R2_arr = R2_df.values.ravel()
labels = model_names * n
temp_df = pd.DataFrame({'R-square': R2_arr , "Model": labels})
temp_df = temp_df[temp_df['R-square'] > 0 ]
plt.figure(figsize = (9,6))
sns.boxplot(x = 'Model', y = 'R-square', data = temp_df)
plt.title("Model R-square distribution comparison", fontsize = 14)
plt.savefig('../results/Model_R2_distribution.png', dpi = 500)
#plt.show()


AIC_arr = AIC_df.values.ravel()
AICC_arr = AICC_df.values.ravel()
temp_df = pd.DataFrame({'AIC': AIC_arr , 'AICC': AICC_arr,  "Model": labels})
plt.figure(figsize = (9,6))
sns.boxplot(x = 'Model', y = 'AIC', data = temp_df)
plt.title("Model AIC distribution comparison", fontsize = 14)
plt.savefig('../results/Model_AIC_distribution.png', dpi = 500)
#plt.show()

AIC_arr = AIC_df.values.ravel()
AICC_arr = AICC_df.values.ravel()
temp_df = pd.DataFrame({'AIC': AIC_arr , 'AICC': AICC_arr,  "Model": labels})
plt.figure(figsize = (9,6))
sns.boxplot(x = 'Model', y = 'AICC', data = temp_df)
plt.title("Model AICC distribution comparison", fontsize = 14)
plt.savefig('../results/Model_AICC_distribution.png', dpi = 500)
#plt.show()

plt.figure(figsize = (12,5))
for col in AIC_df.columns:
    plt.plot(range(n), AIC_df[col], label = col, alpha = 0.6)
plt.xlabel("ID Index")
plt.legend()
plt.ylabel("AIC")
plt.savefig('../results/ID_AIC_distribution.png', dpi = 500)
#plt.show()

plt.figure(figsize = (12,5))
for col in AICC_df.columns:
    plt.plot(range(n), AICC_df[col], label = col, alpha = 0.6)
plt.xlabel("ID Index")
plt.legend()
plt.ylabel("AICC")
plt.savefig('../results/ID_AICC_distribution.png', dpi = 500)
#plt.show()

