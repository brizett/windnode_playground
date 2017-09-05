# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:15:13 2017

@author: bzimmermann
"""

# Outputlib
from oemof import outputlib

# Default logger of oemof
from oemof.tools import logger

# Import OEMOF base classes
import oemof.solph as solph
import logging
import pandas as pd
import os

# Create time stamp
time_stamp = pd.date_range('1/1/2015', periods=8760, freq='H')

# Set up energy system
esys = solph.EnergySystem(timeindex=time_stamp)

# Read input data
# Frage: Die example_data werden in simple_least_costs für 2012 verwendet, 
# bestehen aber trotz schaltjahr nur aus 8760 zeitschritten...

# filename = os.path.join(os.path.dirname(__file__), 'example_data.csv')
filename_RE = 'K:\Projekte\Aktuell\SINTEG_WindNODE\Arbeitspakete\AP 2\AP 2.1_Verbundkraftwerk Prignitz\Arbeitsordner\OEMOF\example_data.csv'
data_RE = pd.read_csv(filename_RE, sep=",")

# filename_prices = os.path.join(os.path.dirname(__file__), 'spotprices2015.csv')
filename_prices = 'K:\Projekte\Aktuell\SINTEG_WindNODE\Arbeitspakete\AP 2\AP 2.1_Verbundkraftwerk Prignitz\Arbeitsordner\OEMOF\spotprices2015.csv'
data_spotprices = pd.read_csv(filename_prices, sep=",")

# Create el. bus and flow
b_el = solph.Bus(label="electricity")

flow=solph.Flow()
# ! hier ergänzen

# Create fixed source object representing wind power plants
solph.Source(
        label='wind', outputs={b_el: solph.Flow(
                fixed=True, actual_value=data_RE['wind'],nominal_value = 1000000)})

# Create battery
solph.Storage(
        label='storage',nominal_capacity=10000000,
        inputs={b_el: solph.Flow()},
                outputs={b_el: solph.Flow()},
                capacity_loss=0.01, initial_capacity=0.5,
                inflow_conversion_factor=1, outflow_conversion_factor=0.8,
)

# Create Market
solph.Sink(
        label='spotmarket', inputs={b_el: solph.Flow(
                variable_costs=data_spotprices['DA_spotmarket_prices'], fixed=True, nominal_value=1)})

# Optimize energy system
logging.info('Optimize energy system')

# Create problem
om = solph.OperationalModel(esys)

# Set tee to True to get solver output
om.solve(solver='cbc', solve_kwargs={'tee':True})

results = ResultsDataFrame(energy_system=esys)

