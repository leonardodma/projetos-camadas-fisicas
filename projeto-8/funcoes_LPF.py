import scipy.signal as sg
from scipy.signal import butter, lfilter, freqz
from scipy import signal


def LPF(signal, cutoff_hz, fs):
	#####################
	# Filtro
	#####################
	# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
	nyq_rate = fs/2
	width = 5.0/nyq_rate
	ripple_db = 60.0 #dB
	N , beta = sg.kaiserord(ripple_db, width)
	taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	return( sg.lfilter(taps, 1.0, signal))
