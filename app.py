#!/usr/bin/env python3
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

@st.cache_data
def integrate(sigma, rho, beta, dt, tmax, initial_state):
    def lorenz(s):
        x, y, z = s
        return np.array([
            sigma * (y - x),
            rho   * x - y - x*z,
            -beta * z + x*y
        ])
    def rk4_step(s, dt):
        k1 = lorenz(s)
        k2 = lorenz(s + dt*k1/2)
        k3 = lorenz(s + dt*k2/2)
        k4 = lorenz(s + dt*k3)
        return s + dt*(k1+2*k2+2*k3+k4)/6

    n = int(tmax/dt)
    t = 0.0
    s = np.array(initial_state, dtype=float)
    traj = np.zeros((n+1, 4))
    traj[0] = [t, *s]
    for i in range(1, n+1):
        s = rk4_step(s, dt)
        t += dt
        traj[i] = [t, *s]
    return traj

st.title("Lorenz 方程式 可視化アプリ")

# サイドバーでパラメータを受け取る
#sigma = st.sidebar.slider("σ", 0.0, 50.0, 10.0, step=0.1)
sigma = st.sidebar.number_input("σ", min_value=0.0, max_value=50.0, value=10.0, step=0.01)
#rho   = st.sidebar.slider("ρ", 0.0, 200.0, 100.0, step=0.1)
rho = st.sidebar.number_input("ρ", min_value=0.00, max_value=200.00, value=110.0, step=0.01)
#beta  = st.sidebar.slider("β", 0.0, 10.0, 8.0/3.0, step=0.01)
beta = st.sidebar.number_input("β", min_value=0.0, max_value=10.0, value=8.0/3.0, step=0.01)

dt    = st.sidebar.number_input("dt", min_value=0.001, max_value=1.0, value=0.003, step=0.001, format="%.3f")
tmax  = st.sidebar.number_input("t_max", min_value=1.0, max_value=1000.0, value=100.0, step=1.0)
initial = st.sidebar.text_input("初期状態 ( x, y, z )", "1.0, 1.0, 1.0")
initial_state = [float(v) for v in initial.split(", ")]

# ページ上に現在のパラメータを表示
st.markdown(
    f"- パラメータ: $ \\sigma = {sigma} $, $ \\rho  = {rho} $, $ \\beta = {beta} $ \n"
    f"- 初期状態: $ (x, y, z) = {initial_state}$ "
    )

# integrate を直接呼び出して毎回新しいデータを作成
data = integrate(sigma, rho, beta, dt, tmax, initial_state)
t, x, y, z = data[:,0], data[:,1], data[:,2], data[:,3]

st.subheader("3D Lorenz attractor")
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.plot(x, y, z, linewidth=0.5, alpha=0.8)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
st.pyplot(fig)
