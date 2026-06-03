"""
# P-model and Spatio-Temporal Multifractal Cascade Model (STM-Model 2+1D)

**Autores:** Carlos Eduardo Falanes, Reinaldo Roberto Rosa

**Instituição:** Instituto Nacional de Pesquisas Espaciais - INPE/MCTI

**Contato:** [carlos.falades@inpe.br](mailto:carlos.falades@inpe.br)

---

## Introdução

O **P-model**, proposto por **Meneveau e Sreenivasan (1987)**, é um modelo multifractal em cascata baseado na redistribuição recursiva de energia entre escalas. Esse processo multiplicativo gera estruturas com **auto-similaridade** e **intermitência estatística**, características comuns em sistemas turbulentos.

Neste trabalho, utilizamos a implementação clássica do **P-model 1D** como base para desenvolver uma extensão bidimensional com evolução temporal, denominada **Spatio-Temporal Multifractal Cascade Model (STM-Model 2+1D)**.

---

## P-model 1D

A implementação original do **P-model unidimensional**, desenvolvida por **R.R. Rosa, R. Sautter e N. Joshi**, aplica um processo multiplicativo controlado pelo parâmetro `p`, responsável por introduzir intermitência e comportamento multifractal.

A cada etapa da cascata, a energia é dividida recursivamente em duas partes assimétricas, produzindo uma estrutura hierárquica multifractal.

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1bIjLw2ANqh2v9JG6yM4cOJJZGC1lX7XC" width="400"/>
</div>


![Esquema P-model com serie](https://drive.google.com/uc?export=view&id=10qIIuFnMBd40777LPHqhVAwv8BpCdd5V)

Abaixo está o código base utilizado como referência para a generalização:
"""

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import matplotlib as mpl

plt.rcParams["figure.dpi"] = 150
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["DejaVu Serif"]

plt.rcParams.update(
    {
        "font.size": 13,
        "axes.titlesize": 14,
        "axes.labelsize": 13,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 10,
    }
)

import pandas as pd
import numpy as np
from scipy.stats import norm
import io

# %matplotlib inline

# XP-model adapted from Meneveau & Sreenevasan, 1987 & Malara et al., 2016
# Valid Ranges for p, based on Didier-Sornette's Theory
# Author: R.R.Rosa, R. Sautter and  N. Joshi
# Version: 1.1
# Date: 23/08/2022

import numpy as np

# import statistics as stat
from matplotlib import pyplot


def pmodel(noOrders=5, p=0.5, slope=[]):
    noOrders = int(noOrders)

    dx = np.array([1])
    for n in range(noOrders):
        dx = next_step_1d(dx, p)

    if slope:
        fourierCoeff = fractal_spectrum_1d(2**noOrders, slope / 2)
        meanVal = np.mean(dx)
        stdy = np.std(dx)
        x = np.fft.ifft(dx - meanVal)
        phase = np.angle(x)
        x = fourierCoeff * np.exp(1j * phase)
        x = np.fft.fft(x).real
        x *= stdy / np.std(x)
        x += meanVal
    else:
        x = dx

    return x[0 : 2**noOrders], dx[0 : 2**noOrders]


def next_step_1d(dx, p):
    y2 = np.zeros(dx.size * 2)
    sign = np.random.rand(1, dx.size) - 0.5
    sign /= np.abs(sign)
    y2[0 : 2 * dx.size : 2] = dx + sign * (1 - 2 * p) * dx
    y2[1 : 2 * dx.size + 1 : 2] = dx - sign * (1 - 2 * p) * dx

    return y2


def fractal_spectrum_1d(noValues, slope):
    ori_vector_size = noValues
    ori_half_size = ori_vector_size // 2
    a = np.zeros(ori_vector_size)

    for t2 in range(ori_half_size):
        index = t2
        t4 = 1 + ori_vector_size - t2
        if t4 >= ori_vector_size:
            t4 = t2
        coeff = (index + 1) ** slope
        a[t2] = coeff
        a[t4] = coeff

    a[1] = 0

    return a


# Endogenous (setup: N, p: 0.32-0.42)
# Exogenous (setup: N, p: 0.18-0.28)


N = 10

# Exogenous
p_exo = 0.22
# np.random.seed(126)
np.random.seed(50)
y_exo, dy_exo = pmodel(N, p_exo, 2)

# Endogenous
p_endo = 0.38
# np.random.seed(126)
np.random.seed(50)
y_endo, dy_endo = pmodel(N, p_endo, 2)


def normalize(x):
    x = x + 0.01
    return x / (np.max(x) + 1e-8)


df_exo = normalize(dy_exo)
df_endo = normalize(dy_endo)


fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True)

# Fig. 1a: Endogenous
axes[0].plot(df_endo, lw=0.9)
# axes[0].set_ylim(0, 0.4)
axes[0].set_ylabel("Normalized amplitude")
axes[0].set_title("(a) Endogenous time series (p = {:.2f})".format(p_endo))
axes[0].grid(alpha=0.3)

# Fig. 1b: Exogenous
axes[1].plot(df_exo, lw=0.9)
# axes[1].set_ylim(0, 0.01)
axes[1].set_xlabel("Time steps")
axes[1].set_ylabel("Normalized amplitude")
axes[1].set_title("(b) Exogenous time series (p = {:.2f})".format(p_exo))
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()


def prepare_series(series, peak_percentile=99):
    normalized_series = (series - np.min(series)) / (
        np.max(series) - np.min(series) + 1e-6
    )

    df = pd.DataFrame({"raw": series, "normalized": normalized_series})

    threshold = np.percentile(df["normalized"], peak_percentile)
    df["peak"] = (df["normalized"] > threshold).astype(int)
    df["peak_threshold"] = threshold

    return df


df_endo_peaks = prepare_series(df_endo, peak_percentile=99)
df_exo_peaks = prepare_series(df_exo, peak_percentile=99)

fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True)

#  Endogenous
t_endo = np.arange(len(df_endo_peaks))
theta_endo = df_endo_peaks["peak_threshold"].iloc[0]

axes[0].plot(t_endo, df_endo_peaks["normalized"], lw=0.9, label="P-model time series")

# Threshold line
axes[0].axhline(
    theta_endo,
    linestyle="--",
    linewidth=1.4,
    label="XE threshold (99th percentile)",
    color="orange",
)

# Peaks
axes[0].plot(
    t_endo[df_endo_peaks["peak"] == 1],
    df_endo_peaks.loc[df_endo_peaks["peak"] == 1, "normalized"],
    "x",
    markersize=6,
    label="Extreme events (XE)",
    color="red",
)

axes[0].set_ylabel("Normalized amplitude")
axes[0].set_title(
    "(a) Endogenous time series and extreme event identification (p = {:.2f})".format(
        p_endo
    )
)
axes[0].grid(alpha=0.3)
axes[0].legend(frameon=True)

#  Exogenous
t_exo = np.arange(len(df_exo_peaks))
theta_exo = df_exo_peaks["peak_threshold"].iloc[0]

axes[1].plot(t_exo, df_exo_peaks["normalized"], lw=0.9, label="P-model time series")

# Threshold line
axes[1].axhline(
    theta_exo,
    linestyle="--",
    linewidth=1.4,
    label="XE threshold (99th percentile)",
    color="orange",
)

# Peaks
axes[1].plot(
    t_exo[df_exo_peaks["peak"] == 1],
    df_exo_peaks.loc[df_exo_peaks["peak"] == 1, "normalized"],
    "x",
    markersize=6,
    label="Extreme events (XE)",
    color="red",
)

axes[1].set_xlabel("Time steps")
axes[1].set_ylabel("Normalized amplitude")
axes[1].set_title(
    "(b) Exogenous time series and extreme event identification (p = {:.2f})".format(
        p_exo
    )
)
axes[1].grid(alpha=0.3)
axes[1].legend(frameon=True)

plt.tight_layout()
plt.show()

"""
## STM-Model (2+1)D

A generalização proposta estende o modelo para um campo espaço-temporal definido por:

[
A(t,x,y)
]

onde `x` e `y` representam as dimensões espaciais e `t` representa o tempo.

Cada instante `t` corresponde a um campo bidimensional multifractal, e a sequência desses campos descreve a evolução temporal do sistema. Dessa forma, o modelo representa uma cascata multifractal **2D no espaço + 1D no tempo**.

Essa abordagem permite simular estruturas mais próximas de sistemas físicos reais, como turbulência e campos geofísicos.

![Esquema STM 2+1D](https://drive.google.com/uc?export=view&id=1jN-euZhssp-Vz9-H3Y42PxObmOmvQ6ju)

---

## Implementação do STM-Model

O modelo foi construído preservando a lógica multiplicativa do **P-model**, adicionando evolução temporal e interação espacial entre os pontos da malha.
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def stm_model(n, p=0.5, sigma=10):
    field = np.ones((1, 1, 1))

    for _ in range(n):
        field = next_step_2d(field, p, sigma)

    field = gaussian_filter(field, sigma=sigma)

    return field


def next_step_2d(field, p, sigma):
    nx, ny, nz = field.shape
    new_field = np.zeros((2 * nx, 2 * ny, 2 * nz))

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                base = field[i, j, k]

                # escolhas independentes em cada direção
                px = p if np.random.rand() < 0.5 else (1 - p)
                py = p if np.random.rand() < 0.5 else (1 - p)
                pz = p if np.random.rand() < 0.5 else (1 - p)

                weights = 2 * np.array(
                    [
                        px * py * pz,
                        px * py * (1 - pz),
                        px * (1 - py) * pz,
                        px * (1 - py) * (1 - pz),
                        (1 - px) * py * pz,
                        (1 - px) * py * (1 - pz),
                        (1 - px) * (1 - py) * pz,
                        (1 - px) * (1 - py) * (1 - pz),
                    ]
                )

                idx = 0
                for di in range(2):
                    for dj in range(2):
                        for dk in range(2):
                            new_field[2 * i + di, 2 * j + dj, 2 * k + dk] = (
                                base * weights[idx]
                            )
                            idx += 1

    # aplica filtro gaussiano após cada step
    # new_field = gaussian_filter(new_field, sigma=sigma)

    return new_field


import matplotlib.pyplot as plt
import numpy as np

p_exo = 0.18
np.random.seed(351)
df_exo = stm_model(8, p_exo)

p_endo = 0.48
np.random.seed(351)
df_endo = stm_model(8, p_endo)

# normalização entre 0 e 1
df_exo_norm = (df_exo - df_exo.min()) / (df_exo.max() - df_exo.min())
df_endo_norm = (df_endo - df_endo.min()) / (df_endo.max() - df_endo.min())

# slice central de cada campo
# best_exo = df_exo_norm.shape[2] // 2
# best_endo = df_endo_norm.shape[2] // 2

# encontrar o slice z com maior valor máximo
max_por_slice_exo = df_exo_norm.max(axis=(0, 1))
max_por_slice_endo = df_endo_norm.max(axis=(0, 1))

best_exo = np.argmax(max_por_slice_exo)
best_endo = np.argmax(max_por_slice_endo)

slice_exo = df_exo_norm[:, :, best_exo]
slice_endo = df_endo_norm[:, :, best_endo]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

im1 = axes[0].imshow(slice_exo, cmap="inferno", origin="lower", vmin=0, vmax=1)
axes[0].set_title(f"Exo (p = {p_exo}), Frame = {best_exo}")
plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

im2 = axes[1].imshow(slice_endo, cmap="inferno", origin="lower", vmin=0, vmax=1)
axes[1].set_title(f"Endo (p = {p_endo}), Frame = {best_endo}")
plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()

print("Slice Exo:\n", slice_exo)

print("Slice Endo:\n", slice_endo)

from matplotlib import animation

plt.rcParams["animation.embed_limit"] = 150

# usar os dados normalizados diretamente
data_exo = df_exo_norm
data_endo = df_endo_norm

# dimensões
frame_height, frame_width = data_exo[:, :, 0].shape
x_coords = np.arange(frame_width)
y_coords = np.arange(frame_height)
X, Y = np.meshgrid(x_coords, y_coords)

# escala fixa de 0 a 1
zmin_exo, zmax_exo = 0, 1
zmin_endo, zmax_endo = 0, 1

# figura com 2 gráficos 3D
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(121, projection="3d")
ax2 = fig.add_subplot(122, projection="3d")


def init():
    ax1.clear()
    ax2.clear()

    surf1 = ax1.plot_surface(X, Y, data_exo[:, :, 0], cmap="inferno", vmin=0, vmax=1)
    surf2 = ax2.plot_surface(X, Y, data_endo[:, :, 0], cmap="inferno", vmin=0, vmax=1)

    ax1.set_zlim(0, 1)
    ax2.set_zlim(0, 1)

    ax1.set_title("Exo - Frame 0")
    ax2.set_title("Endo - Frame 0")

    return surf1, surf2


def update(frame_index):
    ax1.clear()
    ax2.clear()

    surf1 = ax1.plot_surface(
        X, Y, data_exo[:, :, frame_index], cmap="inferno", vmin=0, vmax=1
    )
    surf2 = ax2.plot_surface(
        X, Y, data_endo[:, :, frame_index], cmap="inferno", vmin=0, vmax=1
    )

    ax1.set_zlim(0, 1)
    ax2.set_zlim(0, 1)

    ax1.set_title(f"Exo - Frame {frame_index}")
    ax2.set_title(f"Endo - Frame {frame_index}")

    return surf1, surf2


ani = animation.FuncAnimation(
    fig, update, frames=data_exo.shape[2], init_func=init, interval=200, blit=False
)

ani.save("animacao_exo_endo.mp4", writer="ffmpeg", fps=20)

plt.close()
# HTML(ani.to_jshtml())


"""


## Considerações finais

O **STM-Model 2+1D** é uma extensão natural das cascatas multifractais clássicas para domínios espaço-temporais. O modelo mantém as propriedades multifractais do **P-model**, incorporando dependência espacial e evolução temporal, tornando-se adequado para a simulação de sistemas complexos.

"""
