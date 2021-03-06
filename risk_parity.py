# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 13:54:42 2018

@author: Jeremy
"""

import numpy as np
from matplotlib import pyplot as plt
from numpy.linalg import inv,pinv
from scipy.optimize import minimize


# risk budgeting optimization
def calculate_portfolio_var(w,V):
    # function that calculates portfolio risk
    # w: vector of assets weight
    # V: covariance of assets return
    w = np.matrix(w)
    return (w*V*w.T)[0,0]

def calculate_risk_contribution(w,V):
    # function that calculates asset contribution to total risk
    w = np.matrix(w)
    sigma = np.sqrt(calculate_portfolio_var(w,V))
    # Marginal Risk Contribution
    MRC = V*w.T
    # Risk Contribution
    RC = np.multiply(MRC,w.T)/sigma
    return RC

def risk_budget_objective(x,pars):
    # calculate portfolio risk
    V = pars[0]# covariance table
    x_t = pars[1] # risk target in percent of portfolio risk
    sig_p =  np.sqrt(calculate_portfolio_var(x,V)) # portfolio sigma
    risk_target = np.asmatrix(np.multiply(sig_p,x_t))
    asset_RC = calculate_risk_contribution(x,V)
    J = sum(np.square(asset_RC-risk_target.T))[0,0] # sum of squared error
    return J

def total_weight_constraint(x):
    return np.sum(x)-1.0

def long_only_constraint(x):
    return x

########################## for an instance ##################################

if __name__ = '_main_':
    # your risk budget percent of total portfolio risk (equal risk)
    x_t = [0.25, 0.25, 0.25, 0.25] 
    V = np.matrix('123 37.5 70 30; 37.5 122 72 13.5; 70 72 321 -32; 30 13.5 -32 52')/100 # covariance
    w0 = [0.25, 0.25, 0.25, 0.25]
    cons = ({'type': 'eq', 'fun': total_weight_constraint},
    {'type': 'ineq', 'fun': long_only_constraint})
    res= minimize(risk_budget_objective, w0, args=[V,x_t], method='SLSQP',constraints=cons, 
                  options={'disp': True})
    w_rb = np.asmatrix(res.x)
    print(w_rb)