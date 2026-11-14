"""Figure: the seven-colouring, its cyclic locus V (honeycomb lattice), and the gadget."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle, Rectangle
from fasthex import colour_arr

plt.rcParams.update({'font.size': 8})
fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.9))

# panel 1: the colouring + L
ax = axes[0]
ax.set_aspect('equal')
R = 2 / 5
cmap = plt.get_cmap('tab10')
n = 10
xs = np.linspace(-1.4, 1.4, 440)
ys = np.linspace(-1.4, 1.4, 440)
X, Y = np.meshgrid(xs, ys)
C = colour_arr(X, Y)
ax.imshow(C, extent=[xs[0], xs[-1], ys[0], ys[-1]], origin='lower', cmap=cmap, vmin=-0.5, vmax=9.5,
          interpolation='nearest')
for m in range(-3, 4):
    for nn in range(-3, 4):
        cx, cy = np.sqrt(3) * (2 * m - nn) / 5, 3 * nn / 5
        if abs(cx) > 1.7 or abs(cy) > 1.7:
            continue
        for k in range(6):
            a = np.pi / 6 + k * np.pi / 3
            ax.plot([cx + R * np.cos(a)], [cy + R * np.sin(a)], '.', ms=2.2, color='k')
ax.set_title(r"$c_0$: colours and $L=$ honeycomb vertices", fontsize=8)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)

# panel 2: the shadow certificate around p_0
ax = axes[1]
ax.set_aspect('equal')
p0 = (1 / 55, 18 / 55)
xs = np.linspace(p0[0] - 1.25, p0[0] + 1.25, 620)
ys = np.linspace(p0[1] - 1.25, p0[1] + 1.25, 620)
X, Y = np.meshgrid(xs, ys)
ax.imshow(colour_arr(X, Y), extent=[xs[0], xs[-1], ys[0], ys[-1]], origin='lower',
          cmap=cmap, vmin=-0.5, vmax=9.5, interpolation='nearest', alpha=0.75)
for eps, col in [(0.0071, 'k'), (1 / 70, 'r')]:
    for rr in (1 - eps, 1 + eps):
        ax.add_patch(Circle(p0, rr, fill=False, lw=0.9, color=col,
                            ls='-' if abs(rr - 1) > 1e-9 else '--'))
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(p0[0] + np.cos(t), p0[1] + np.sin(t), 'k--', lw=0.8)
ax.set_title(r"annuli $1\pm0.0071$ (black) and $1\pm1/70$ (red):" + "\nno colour 0, 2, 3", fontsize=8)
ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1])

# panel 3: the gadget inside W
ax = axes[2]
ax.set_aspect('equal')
ax.add_patch(Rectangle((p0[0] - 0.01, p0[1] - 0.01), 0.02, 0.02, fill=False, lw=1.0, color='k'))
for i, (q, rho) in enumerate([(p0[0] + 0.01 * 2 ** (-n - 3), 0.01 * 2 ** (-n - 14)) for n in (0, 1, 2, 3)]):
    ax.add_patch(Circle((q, p0[1]), max(rho, 6e-4), fill=False, lw=0.8, color='C3'))
    ax.plot([q, q + max(rho, 6e-4)], [p0[1], p0[1]], lw=0.6, color='C3')
ax.plot([p0[0]], [p0[1]], 'k+', ms=8)
ax.annotate(r"$p_0$", (p0[0], p0[1]), textcoords="offset points", xytext=(4, -9))
ax.annotate("Mercedes disks $D_n$\n(radii scaled for visibility)", (p0[0] + 0.006, p0[1] + 0.006),
            fontsize=7)
ax.set_title(r"$W$ (side $1/50$) and the accumulating disks", fontsize=8)
ax.set_xlim(p0[0] - 0.012, p0[0] + 0.013); ax.set_ylim(p0[1] - 0.012, p0[1] + 0.013)

plt.tight_layout()
plt.savefig('figure.png', dpi=190)
print("wrote figure.png")
