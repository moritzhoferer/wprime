#! /usr/bin/python3

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

l_time = 'secs'
l_pwr = '42 days'

Y_MIN, Y_MAX = 50, 1400
X_MIN, X_MAX = .9, 3600

time_markers = {'1 sec': 1, '5 sec': 5, '10 sec': 10, '1 min': 60, '5 min': 300,
    '10 min': 600, '20 min': 1200}


def fit_func(t, wp, cp):
    return wp/t + cp

def estimator(s: pd.Series):
    popt, _ = curve_fit(
        fit_func, s.index, s.iloc[:,0],  
        )
    return popt

# Power curve exported from your profile at https://www.intervals.icu/power
if len(sys.argv) > 1:
    input_file_path = sys.argv[1]
else:
    print('No input file given! Therefore, the example data is used')
    input_file_path = os.path.dirname(os.path.abspath(__file__)) + '/example.csv'

graphic_name = input_file_path.split('/')[-1].split('.')[0]
graphic_path = f'./{graphic_name}.png' 

# Lower time limit
t_min = 180
# Upper time limit
t_max = 1800

all_data = pd.read_csv(input_file_path, index_col='secs')
_columns = [c for c in all_data.columns if "FFT" not in c]

counter = 0
for l_pwr, data in all_data[_columns].items():
    data = data.dropna()

    interfunc = interp1d(data.index, data.values, kind='cubic', bounds_error=False) 
    range_ = np.logspace(
        np.log10(min(data.index)),
        np.log10(max(data.index)),
        50
    )
    dict_ = {l_time: range_, l_pwr: interfunc(range_)}
    interpolated_data = pd.DataFrame(dict_).set_index(l_time)

    # Get values for W' and CP and print them
    _filter = (interpolated_data.index>=t_min) & (interpolated_data.index<=t_max)
    wp, cp = estimator(interpolated_data[_filter])
    print(f'{l_pwr:s}\nW\': {wp:7.0f} Joule\nCP: {cp:7.0f} Watt\n')

    # Visualization
    plt.vlines(time_markers.values(), Y_MIN, Y_MAX, colors='grey', linestyles='dashed')
    for k, v in time_markers.items():
        plt.text(v, .98*Y_MAX, k, rotation=-90, va='top', ha='left')
    plt.plot(
        data.index, data.values, 
        label=f'{l_pwr:s} [W\': {wp/1e3:.1f}kJ, CP: {cp:.0f}W]',
        color=f'C{counter:d}',
        )
    times = data[(data.index>=t_min) & (data.index<=t_max)].index
    plt.plot(
        times, fit_func(times, wp, cp), 
        '--',
        color=f'C{counter:d}',
        )
    counter+=1

plt.title('W\' estimator')
plt.xlabel('Time [s]')
plt.ylabel('Power [W]')
plt.xscale('log')
plt.legend(loc='lower left')
plt.ylim(Y_MIN, Y_MAX)
plt.xlim(X_MIN, X_MAX)
plt.tight_layout(pad=.2)
plt.savefig(graphic_path)
