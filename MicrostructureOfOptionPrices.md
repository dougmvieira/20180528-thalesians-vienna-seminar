---
title: Microstruture of option prices
author:
- Douglas Vieira
- Imperial College London
date: Vienna, 28 May 2018
---


# Introduction

## Introduction


# Market microstructure review

## Order-driven markets

- Any market participant can submit
  - *Limit orders* to propose buy or sell quotes
  - *Market orders* to trade against existing quotes
  - *Cancellations* to withdraw own unmatched limit orders
- Limit order book is the collection of outstanding limit orders
- Priority of trade among limit orders is usually by price and time

## {data-background-iframe="lob.html"}

## Microstructure noise

- The constraint of prices to the tick grid generates endogenous 'microstructure effects'
- Changing price cause change in priority
- 'Microstructure effects' viewed as 'microstructure noise'
  - High-frequency financial econometrics [@ait2014high]
  - Model of uncertainty zones [@robert2011model]


# Long time dynamics

## Stylised facts in daily prices

- No autocorrelation on log returns
- Heavy tails
- Volatility clustering
- Leverage effect
- [see, e.g. @cont2001empirical]

## S&P 500 futures example

## {data-background-iframe="sp500.html"}

## Heston model example

- The price $S$ follows the SDE

$$\begin{align}
  dS_t      & = \mu S_t dt + \sqrt{V_t} S_t dW_t \\
  dV_t      & = \kappa (\theta - V_t) dt + \nu \sqrt{V_t} dZ_t \\
  d[W, Z]_t & = \rho dt \end{align}$$

- Market state is the pair $(S, V)$

## {data-background-iframe="heston.html"}

## Options dynamics representation

*Theorem.* Assume the market state process $X$ is an Itô diffusion with locally
Lipschitz coefficients, invertible diffusion coefficient matrix and with open
connected support. Then, under no arbitrage, the option $C$ with
square-integrable payoff $f(X_T)$ follows

$$ C_t = \varphi(X_t), \quad dC_t = \nabla_x\varphi(X_t)dX_t, $$

$$ \text{where } \varphi(x) = \mathbb E[f(X_T)\mid X_t=x]. $$

## Some encompassed vanilla models

- Heston model
  - With Feller condition $\nu^2 < 2\kappa\theta$
- SABR model
  - With $\beta = 1$ (lognormal SABR), or
  - Free-boundary [$\beta < 1/2$, see @antonov2015free]
- Bergomi model
  - No restrictions


# Small time dynamics

## Strategy

## Small time asymptotics of global dynamics

*Theorem* Let $X$ be an Itô diffusion, of the form

$$ dX_t = \mu_t dt + \sigma_t dW_t, $$

$$ \text{then } \frac{X_t - \tilde X_t}{\sqrt{t}} \xrightarrow{L^2} 0, $$

$$ \text{where } d\tilde X_t = \sigma_0 dW_t. $$

## S&P 500 futures example revisited

## {data-background-iframe="sp500.html"}

## Stylised microstructure effects

- Discreteness of prices
- Negative autocorrelation on tick price changes (bouncing effects)
- Asynchronous time series
- see, e.g. [@cont2001empirical]

## Round prices to nearest tick

- Features all three stylised facts
- see [@rosenbaum2009integrated]

## Rounded Heston model example

## {data-background-iframe="rounded_heston.html"}


# Conclusion

## Conclusion

## References {.scrollable}
