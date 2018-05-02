# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:01:17 2018

@author: s_zhangyw
"""

def solver(w_1, w_bench, expect_rtn, trade_cost, X_style, X_industry, tol_style, tol_industry):

    N = len(w)

    def func(w, w_1, expect_rtn, trade_cost, sign=-1.0):
        res = w.dot(expect_rtn) - trade_cost * (w - w_1).abs().sum() / 2.0
        return res * sign

    cons = ({'type': 'eq',
             'fun': lambda x: np.array(x.sum() - 1.0),
             'jac': lambda x: np.ones(N)},
             {'type': 'ineq',
             'fun': lambda x: np.ones(N) * tol_style - (x - w_bench).dot(X_style).abs()},
            {'type': 'ineq',
             'fun': lambda x: np.ones(N) * tol_industry - (x - w_bench).dot(X_industry).abs()}
             )

    res = minimize(func, [1/N]*N, args=(w_1, w_bench, expect_rtn, trade_cost, X_style, X_industry, tol_style, tol_industry),
                   constraints=cons, bounds=[(0, 1)]*N, method='SLSQP', tol=1e-18, options={'disp': False, 'maxiter': 1000})

    return res.x

def main():
    arr_w_bench = 
    arr_expect_rtn = 
    trade_cost = 
    X_style =
    X_industry =
    tol_style =
    tol_industry =
    
    arr_w = arr_w_bench.copy()

    for i in range(1000):
        if i = 0:
            arr_w[i] = arr_w_bench[i]
        else:
            arr_w[i] = solver(arr_w[i-1], arr_w_bench[i], arr_expect_rtn[i], trade_cost, X_style, X_industry, tol_style, tol_industry)

    return arr_w

if __name__ == '__main__':
    main()

