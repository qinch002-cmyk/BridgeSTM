import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. 晶格与表面
# =========================================================

def triangular_lattice_points(xmin, xmax, ymin, ymax, a):
    """
    生成二维三角晶格母点阵。
    a: 晶格尺度参数
    """
    points = []

    x_buffer = 2 * a
    y_buffer = 2 * a

    j_step = np.sqrt(3) * a / 2.0
    j_min = int(np.floor((ymin - y_buffer) / j_step)) - 1
    j_max = int(np.ceil((ymax + y_buffer) / j_step)) + 1

    i_min = int(np.floor((xmin - x_buffer) / a)) - 2
    i_max = int(np.ceil((xmax + x_buffer) / a)) + 2

    for j in range(j_min, j_max + 1):
        for i in range(i_min, i_max + 1):
            x = i * a + j * (a / 2.0)
            y = j * (np.sqrt(3) / 2.0 * a)

            if (xmin - x_buffer <= x <= xmax + x_buffer and
                    ymin - y_buffer <= y <= ymax + y_buffer):
                points.append((x, y))

    return points


def make_hopg_sublattices(base_points, a):
    """
    从母点阵生成 HOPG 的两个子晶格 A / B。
    """
    points_A = []
    points_B = []

    dx = a / 2.0
    dy = np.sqrt(3) * a / 6.0

    for x, y in base_points:
        points_A.append((x, y))
        points_B.append((x + dx, y + dy))

    return points_A, points_B


def gaussian_bump(X, Y, x0, y0, sigma, height):
    """
    单个原子的二维高斯凸起。
    X, Y 可以是 meshgrid 数组。
    """
    r2 = (X - x0) ** 2 + (Y - y0) ** 2
    return height * np.exp(-r2 / (2.0 * sigma ** 2))


def build_hopg_surface(X, Y, points_A, points_B, sigma=0.22, hA=1.0, hB=0.18):
    """
    构建 HOPG 表面高度图。
    hA, hB 用来模拟 AB 堆垛导致的两子晶格不等价。
    """
    Z = np.zeros_like(X, dtype=float)

    for x0, y0 in points_A:
        Z += gaussian_bump(X, Y, x0, y0, sigma, hA)

    for x0, y0 in points_B:
        Z += gaussian_bump(X, Y, x0, y0, sigma, hB)

    return Z


def add_large_scale_background(X, Y, amplitude=0.01):
    """
    加一点非常弱的大尺度背景起伏。
    """
    return amplitude * (
        0.7 * np.sin(0.25 * X) * np.cos(0.18 * Y)
        + 0.3 * np.sin(0.12 * X + 0.10 * Y)
    )


# =========================================================
# 2. 虚拟 STM 物理模型
# =========================================================

def tunneling_current_from_gap(gap, I0=1.0, kappa=4.0):
    """
    根据 gap 计算隧穿电流。
    I = I0 * exp(-kappa * gap)

    gap 越小，电流越大。
    若 gap <= 0，视为撞针，返回很大值。
    """
    current = np.zeros_like(gap, dtype=float)

    collision_mask = gap <= 0
    safe_mask = ~collision_mask

    current[collision_mask] = 1e6
    current[safe_mask] = I0 * np.exp(-kappa * gap[safe_mask])

    return current


def simulate_constant_height_scan(surface, z_tip, I0=1.0, kappa=4.0,
                                  noise_std=0.01, seed=42):
    """
    constant-height 扫描：
    - z_tip 固定
    - 每个点只根据 gap = z_tip - surface_height 算电流
    """
    rng = np.random.default_rng(seed)

    gap = z_tip - surface
    current = tunneling_current_from_gap(gap, I0=I0, kappa=kappa)

    # 给电流乘一点相对噪声，更像测量
    noise = rng.normal(0.0, noise_std, size=current.shape)
    current_noisy = current * (1.0 + noise)

    # 防止负值
    current_noisy = np.clip(current_noisy, 0.0, None)

    return current_noisy, gap


# =========================================================
# 3. 图像工具
# =========================================================

def normalize_image(img):
    """
    归一化到 0~1，便于显示。
    """
    img = img - np.min(img)
    max_val = np.max(img)
    if max_val > 0:
        img = img / max_val
    return img


def log_compress(img, eps=1e-12):
    """
    对电流图做对数压缩。
    因为隧穿电流指数变化非常大，不压缩会很难看。
    """
    return np.log(img + eps)


# =========================================================
# 4. 主程序
# =========================================================

def main():
    # -------------------------------
    # 扫描区域与网格
    # -------------------------------
    xmin, xmax = -8, 8
    ymin, ymax = -8, 8

    n = 400
    x = np.linspace(xmin, xmax, n)
    y = np.linspace(ymin, ymax, n)
    X, Y = np.meshgrid(x, y)

    # -------------------------------
    # HOPG 表面参数
    # -------------------------------
    a = 1.6
    sigma = 0.18
    hA = 1.0
    hB = 0.18

    base_points = triangular_lattice_points(xmin, xmax, ymin, ymax, a)
    points_A, points_B = make_hopg_sublattices(base_points, a)

    Z_atoms = build_hopg_surface(
        X, Y,
        points_A, points_B,
        sigma=sigma,
        hA=hA,
        hB=hB
    )

    Z_bg = add_large_scale_background(X, Y, amplitude=0.01)
    Z_surface = Z_atoms + Z_bg

    # -------------------------------
    # 固定探针高度（关键参数）
    # -------------------------------
    # z_tip 必须比表面最大高度略高，否则会撞针
    z_tip = np.max(Z_surface) + 0.35

    # -------------------------------
    # constant-height 扫描
    # -------------------------------
    current_img, gap_img = simulate_constant_height_scan(
        Z_surface,
        z_tip=z_tip,
        I0=1.0,
        kappa=5.0,
        noise_std=0.02,
        seed=7
    )

    # 电流图对数压缩后再显示
    current_log = log_compress(current_img)

    # 显示归一化版本更直观
    surface_show = normalize_image(Z_surface)
    current_show = normalize_image(current_log)

    # -------------------------------
    # 画图
    # -------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    im0 = axes[0].imshow(
        surface_show,
        extent=[xmin, xmax, ymin, ymax],
        origin="lower",
        cmap="gray"
    )
    axes[0].set_title("Ideal HOPG Surface")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    fig.colorbar(im0, ax=axes[0], shrink=0.85)

    im1 = axes[1].imshow(
        current_show,
        extent=[xmin, xmax, ymin, ymax],
        origin="lower",
        cmap="gray"
    )
    axes[1].set_title("Constant-Height STM Current Image")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("y")
    fig.colorbar(im1, ax=axes[1], shrink=0.85)

    im2 = axes[2].imshow(
        gap_img,
        extent=[xmin, xmax, ymin, ymax],
        origin="lower",
        cmap="viridis"
    )
    axes[2].set_title("Gap Map (z_tip - surface)")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("y")
    fig.colorbar(im2, ax=axes[2], shrink=0.85)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()