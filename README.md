# Quantitative Option Valuation & Scanner Engine

A Python-based quantitative finance tool that scans market data, calculates theoretical option values using multiple mathematical models, and identifies mispriced option contracts across S&P 500 stocks or custom stock lists.

## Features

* **Multi-Model Option Pricing Engine**:

  * **Black-Scholes Model**: Closed-form analytical pricing for European-style options.

  * **Binomial Tree Model (Cox-Ross-Rubinstein)**: Discrete-time lattice model accounting for early exercise features (American options).

  * **Monte Carlo Simulation** *(Planned / In Progress)*: Stochastic path simulation for European and exotic options using Geometric Brownian Motion (GBM).

* **Automated Market Data Ingestion**:

  * Automatically fetches S&P 500 constituents directly from Wikipedia.

  * Retrieves real-time stock quotes, risk-free rates (via `^IRX`), and live option chain data via standard APIs.

* **Custom Input Support**:

  * Load custom ticker lists or localized data files/URLs to run valuation across targeted stock universes.

* **Opportunity Scanner**:

  * Scans contracts expiring daily, weekly, or monthly.

  * Compares model valuations against live asking prices (`ask`) to spot potentially undervalued calls.

  * Exports flagged trading opportunities directly to formatted Excel spreadsheets (`UndervaluedOptions.xlsx`).

## Installation

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Install Dependencies

Clone this repository and install the required Python packages:

```
git clone https://github.com/REEEEZEEEE/Options-Pricing-Algorithm.git
cd Options-Pricing-Algorithm
pip install -r requirements.txt


```

## Usage

### 1. Running the Scanner

To execute the standard scan across all S&P 500 stocks:

```
python sandpPricingAlgorithm.py


```

The script will process each stock, compute annualized volatility from historical prices, evaluate call options across short-term horizons, and save output results into `UndervaluedOptions.xlsx`.

## Pricing Models & Mathematical Overview

### 1. Black-Scholes Model

Evaluates call price $C$ using standard European parameters:

$$
d_1 = \frac{\ln(S / K) + (r + \frac{\sigma^2}{2})T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}
$$

$$
C = S N(d_1) - K e^{-rT} N(d_2)
$$

### 2. Cox-Ross-Rubinstein Binomial Tree

Constructs a discrete lattice over $n$ time steps of size $h = T / n$:

$$
u = e^{\sigma \sqrt{h}}, \quad d = \frac{1}{u}, \quad p = \frac{e^{rh} - d}{u - d}
$$

Backward induction is applied to account for early exercise value at each node $i, j$:

$$
V_{i,j} = \max\left(\text{Payoff}(S_{i,j}), e^{-rh} \left[ p V_{i+1, j+1} + (1-p) V_{i, j+1} \right]\right)
$$

### 3. Monte Carlo Simulation *(Upcoming)*

Simulates asset price paths under Geometric Brownian Motion (GBM):

$$
S_T = S_0 \exp\left( \left(r - \frac{\sigma^2}{2}\right)T + \sigma \sqrt{T} Z \right), \quad Z \sim \mathcal{N}(0, 1)
$$

Discounts the expected terminal payoff back to time zero.

## Roadmap

* $$
  x
  $$

   Integrate Yahoo Finance (`yfinance`) automated retrieval.

* $$
  x
  $$

   Implement Black-Scholes European call pricing.

* $$
  x
  $$

   Fix and calibrate Binomial Tree American option valuation engine.

* $$
  
  $$

   Implement Monte Carlo option valuation engine with configurable sample size.

* $$
  
  $$

   Add CLI arguments for importing custom CSV/Excel file URLs or local file paths for stock ticker inputs.

* $$
  
  $$

   Implement multi-threading (`concurrent.futures`) for accelerated stock universe processing.

* $$
  
  $$

   Support put options evaluation and delta/gamma Greeks calculation.

## License

Distributed under the MIT License. See `LICENSE` for more details.