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


np.random.seed(42)

kappa = 5.07
theta = 0.0457
nu = 0.48
rho = -0.767
mu = 3.9*np.sqrt(1 - rho**2)

v0 = theta
s0 = 1640

fine_step = pd.to_timedelta('0.1s')
coarse_step = pd.to_timedelta('10s')
year = pd.to_timedelta('365.25d')

fine_timestamps = np.arange(tickdata_start, tickdata_end, fine_step) + fine_step
coarse_timestamps = np.arange(tickdata_end, dailydata_end, coarse_step
                              ) + coarse_step

time_steps = pd.concat([pd.Series(fine_step/year, fine_timestamps),
                        pd.Series(coarse_step/year, coarse_timestamps)])
innovations = pd.concat(2*[np.sqrt(time_steps)], axis=1, keys=['Price', 'Vol']
                        )*np.random.randn(len(time_steps), 2)
simulation_index = np.insert(time_steps.index, 0, tickdata_start)

vol = pd.Series(simulate_cir(v0, kappa, theta, nu,
                             time_steps.values, innovations['Vol'].values),
                simulation_index, name='Vol')

price = pd.Series(np.log(s0), simulation_index, name='Price')
price.iloc[1:] = ((mu - 0.5)*vol.shift().iloc[1:]*time_steps
                  + np.sqrt(vol.shift().iloc[1:])
                    *(rho*innovations['Vol']
                      + np.sqrt(1 - rho**2)*innovations['Price']))
price = np.exp(price.cumsum())

simulation = pd.concat([price, vol], axis=1)
simulation.to_pickle('simulation.pickle')
