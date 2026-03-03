## Plan: FMCW毫米波雷达信号处理可视化仿真系统

### TL;DR
构建一个基于 Python 的 FMCW 雷达全栈仿真教学系统。使用 NumPy/SciPy 实现信号处理算法，Matplotlib/Plotly 做可视化，Jupyter Notebook 作为教学载体，可选 Streamlit 构建交互式 Web 界面。系统涵盖从 Chirp 信号生成到目标跟踪的完整处理链。

**核心算法：**
- 距离维处理：Range FFT
- 速度维处理：Doppler FFT → Range-Doppler Map
- 目标检测：CA-CFAR / OS-CFAR
- 角度估计：DBF、MUSIC、ESPRIT
- 目标跟踪：卡尔曼滤波

---

### Steps

**Phase 1 - 基础架构 (Week 1)**
1. 创建项目结构 `fmcw_radar_sim/`，包含 `src/core/`、`src/processing/`、`src/visualization/` 模块
2. 实现 `radar_params.py`：使用 `dataclass` 定义雷达参数（载频 77GHz、带宽 4GHz、Chirp 周期 40μs 等）
3. 实现 `signal_generator.py`：生成 FMCW Chirp 信号 $s(t) = \cos(2\pi f_c t + \pi \mu t^2)$
4. 实现 `channel_model.py`：单目标/多目标回波仿真，含时延和衰减

**Phase 2 - 距离-速度处理 (Week 2)**
5. 实现 `range_fft.py`：差拍信号 Range FFT，支持窗函数（Hanning/Hamming/Blackman）
6. 实现 `doppler_fft.py`：跨 Chirp 相位变化提取，生成 Range-Doppler Map
7. 实现 `noise_models.py`：AWGN 热噪声、地杂波模型
8. 可视化：时域波形、频谱图、RD Map 热力图

**Phase 3 - 目标检测 (Week 3)**
9. 实现 `cfar.py`：
   - CA-CFAR（单元平均）
   - OS-CFAR（有序统计）
   - 2D-CFAR（Range-Doppler 二维）
10. 可视化：CFAR 阈值曲面、检测点叠加显示

**Phase 4 - 角度估计 (Week 4)**
11. 实现 `angle_estimation.py`：
    - 数字波束形成（DBF）：$P(\theta) = |a(\theta)^H X|^2$
    - MUSIC 算法：协方差矩阵特征分解 + 伪谱搜索
    - ESPRIT 算法（可选进阶）
12. 可视化：空间谱、DOA 标注

**Phase 5 - 目标跟踪 (Week 5)**
13. 实现 `tracking.py`：
    - 卡尔曼滤波器（匀速模型）
    - 数据关联（匈牙利算法）
14. 可视化：目标轨迹、预测与观测对比

**Phase 6 - 教学界面 (Week 6)**
15. 创建 Jupyter Notebooks：
    - `01_fmcw_basics.ipynb`：Chirp 信号原理
    - `02_range_processing.ipynb`：距离检测
    - `03_doppler_processing.ipynb`：速度检测
    - `04_cfar_detection.ipynb`：CFAR 算法
    - `05_angle_estimation.ipynb`：角度估计
    - `06_full_pipeline.ipynb`：完整处理链
16. （可选）创建 `streamlit_app.py`：交互式 Web 演示界面，支持参数滑块实时调节

---

### 项目结构

```
fmcw_radar_sim/
├── requirements.txt              # numpy, scipy, matplotlib, plotly, streamlit
├── config/
│   └── radar_params.yaml         # 默认雷达参数
├── src/
│   ├── core/
│   │   ├── radar_params.py       # 参数配置类
│   │   ├── signal_generator.py   # Chirp信号生成
│   │   └── channel_model.py      # 目标/信道模型
│   ├── processing/
│   │   ├── range_fft.py          # 距离FFT
│   │   ├── doppler_fft.py        # 多普勒FFT
│   │   ├── cfar.py               # CFAR检测
│   │   ├── angle_estimation.py   # 角度估计
│   │   └── tracking.py           # 卡尔曼跟踪
│   ├── visualization/
│   │   ├── signal_plots.py       # 波形绘制
│   │   ├── spectrum_plots.py     # 频谱/RD Map
│   │   └── interactive.py        # 交互控件
│   └── utils/
│       ├── window_functions.py   # 窗函数
│       └── noise_models.py       # 噪声模型
├── notebooks/
│   └── 01_fmcw_basics.ipynb ...  # 教学笔记本
└── app/
    └── streamlit_app.py          # Web界面
```

---

### 关键公式速查

| 参数 | 公式 |
|------|------|
| 距离分辨率 | $\Delta R = c / 2B$ |
| 速度分辨率 | $\Delta v = \lambda / 2NT_c$ |
| 最大不模糊距离 | $R_{max} = f_s c T_c / 2B$ |
| 最大不模糊速度 | $v_{max} = \lambda / 4T_c$ |

---

### 技术栈

| 库 | 用途 |
|----|------|
| `numpy` | 数值计算、FFT |
| `scipy` | 信号处理、窗函数 |
| `matplotlib` | 静态图表 |
| `plotly` | 交互式图表 |
| `streamlit` | Web 界面 |
| `ipywidgets` | Jupyter 交互控件 |

---

### Verification
- 单目标场景：验证 Range FFT 峰值位置与设定距离一致
- 运动目标：验证 Doppler FFT 速度估计正确
- CFAR：设置 Pfa=1e-4，统计虚警率是否匹配
- 角度：设置 30° 目标，验证 MUSIC 谱峰位置
- 运行单元测试：`pytest tests/`

### Bug Fix Log
- **已修复：Range FFT 单测边界混叠问题**
    - 现象：`test_range_fft_peak_near_truth` 在目标距离设为 30m 时失败，峰值落在 0m 附近。
    - 根因：当前参数下最大不模糊距离约 30m，测试点位于边界，差拍频率发生混叠。
    - 修复：将测试目标距离从 30m 调整为 10m（安全工作区间内）。
    - 结果：`pytest` 全部通过（2 passed）。
    - 约束：后续验证场景默认使用 $R < 0.8 \cdot R_{max}$，避免边界混叠误判。

---

### Decisions
- **教学载体选择 Jupyter Notebook**：代码与可视化一体，便于理解
- **可选 Streamlit Web 界面**：可部署分享，适合演示
- **先实现 DBF 再 MUSIC**：DBF 简单直观，MUSIC 作为进阶
- **卡尔曼滤波使用匀速模型**：满足大多数场景，后续可扩展

---

这是一个完整的 FMCW 雷达仿真教学系统方案，预计 6 周可完成核心功能。你觉得这个方案如何？是否需要调整范围或优先级？
