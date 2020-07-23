#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from dvg_fftw_welchpowerspectrum import FFTW_WelchPowerSpectrum

num_samples = 2 ** 18
Fs = 10000  # [Hz]
freq_1 = 200  # [Hz]
freq_2 = 2100  # [Hz]

t = np.arange(num_samples) / Fs
x = np.sin(2 * np.pi * freq_1 * t) + np.sin(2 * np.pi * freq_2 * t)

ps = FFTW_WelchPowerSpectrum(num_samples, Fs, 2 ** 14)

ans = ps.process_dB(x)

plt.plot(ps.freqs, ans)
plt.show()
