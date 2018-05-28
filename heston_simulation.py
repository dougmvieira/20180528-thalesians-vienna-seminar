import numpy as np
import pandas as pd
from numba import jit
from parameters import tickdata_start, tickdata_end, dailydata_end


@jit
def simulate_cir(x0, kappa, theta, sigma, d, dW):
    x = np.zeros(len(d) + 1)
    x[0] = x0
    for i in range(1, len(x)):
        x[i] = (x[i-1] + kappa*(theta - x[i-1])*d[i-1]
                + sigma*np.sqrt(x[i-1])*dW[i-1])
    return x

def logspace(start, stop, min_step, max_step):
    num = np.ceil(-np.log(min_step/(stop - start))/np.log(1 + max_step/(stop - start)))
    scales = (1 + max_step/(stop - start))**np.arange(-num, 0)
    return start.to_datetime64() + scales*(stop - start)

np.random.seed(42)

kappa = 5.07
theta = 0.0457
nu = 0.48
rho = -0.767
mu = 3.9*np.sqrt(1 - rho**2)

v0 = theta
s0 = 1640

year = pd.to_timedelta('365.25d')
min_timestep = pd.to_timedelta('1ns')
max_timestep = pd.to_timedelta('6h')

timestamps = logspace(tickdata_start, dailydata_end, min_timestep, max_timestep)
time_steps = pd.Series((timestamps[1:] - timestamps[:-1])/year, timestamps[1:])
innovations = pd.concat(2*[np.sqrt(time_steps)], axis=1, keys=['Price', 'Vol']
                        )*np.random.randn(len(time_steps), 2)

vol = pd.Series(simulate_cir(v0, kappa, theta, nu,
                             time_steps.values, innovations['Vol'].values),
                timestamps, name='Vol')

price = pd.Series(np.log(s0), timestamps, name='Price')
price.iloc[1:] = ((mu - 0.5)*vol.shift().iloc[1:]*time_steps
                  + np.sqrt(vol.shift().iloc[1:])
                    *(rho*innovations['Vol']
                      + np.sqrt(1 - rho**2)*innovations['Price']))
price = np.exp(price.cumsum())

simulation = pd.concat([price, vol], axis=1)
simulation.index.name = 'Time'

simulation.to_pickle('simulation.pickle')
