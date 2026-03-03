# radar-signal-processing-sim

📡 FMCW 雷达信号处理可视化仿真平台（Python + Streamlit）

## 项目简介

这个项目用于演示 FMCW 雷达信号处理的核心流程，包含：

- 回波与信道建模
- 距离维 FFT（Range FFT）
- 多普勒维 FFT（Doppler FFT）
- CFAR 检测
- 角度估计
- 全流程可视化与交互展示

项目同时提供模块化源码、分阶段 Jupyter Notebook，以及 Streamlit 交互页面。

## 环境要求

- Python 3.10+
- Linux / macOS / Windows（WSL）

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行方式

### 1) 启动可视化应用

```bash
streamlit run app/streamlit_app.py
```

### 2) 运行测试

```bash
pytest -q
```

### 3) 学习与实验 Notebook

按顺序建议：

1. `notebooks/01_fmcw_basics.ipynb`
2. `notebooks/02_range_processing.ipynb`
3. `notebooks/03_doppler_processing.ipynb`
4. `notebooks/04_cfar_detection.ipynb`
5. `notebooks/05_angle_estimation.ipynb`
6. `notebooks/06_full_pipeline.ipynb`

## 项目结构

```text
fmcw_radar_sim/
├── app/                    # Streamlit 应用
├── config/                 # 雷达参数配置
├── notebooks/              # 分步骤教学 Notebook
├── src/
│   ├── core/               # 信号生成与参数定义
│   ├── processing/         # 距离/多普勒/CFAR/角度处理
│   ├── utils/              # 工具函数（噪声、窗函数等）
│   └── visualization/      # 绘图与交互
└── tests/                  # 测试用例
```

## 许可

当前仓库未声明开源许可证；如需开源发布，建议补充 `LICENSE` 文件。

---

## English

📡 FMCW Radar Signal Processing Visualization Simulator (Python + Streamlit)

### Overview

This project demonstrates a complete FMCW radar signal processing workflow, including:

- Echo and channel modeling
- Range FFT
- Doppler FFT
- CFAR detection
- Angle estimation
- End-to-end visualization and interactive exploration

It provides modular source code, step-by-step Jupyter notebooks, and a Streamlit app.

### Requirements

- Python 3.10+
- Linux / macOS / Windows (WSL)

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

#### 1) Run the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

#### 2) Run tests

```bash
pytest -q
```

#### 3) Notebook learning path

Recommended order:

1. `notebooks/01_fmcw_basics.ipynb`
2. `notebooks/02_range_processing.ipynb`
3. `notebooks/03_doppler_processing.ipynb`
4. `notebooks/04_cfar_detection.ipynb`
5. `notebooks/05_angle_estimation.ipynb`
6. `notebooks/06_full_pipeline.ipynb`

### Project structure

```text
fmcw_radar_sim/
├── app/                    # Streamlit app
├── config/                 # Radar parameter configuration
├── notebooks/              # Step-by-step notebooks
├── src/
│   ├── core/               # Signal generation and parameter definitions
│   ├── processing/         # Range/Doppler/CFAR/angle processing
│   ├── utils/              # Utilities (noise, windows, etc.)
│   └── visualization/      # Plotting and interactive visualization
└── tests/                  # Test cases
```

### License

No open-source license is declared yet. Add a `LICENSE` file if you plan to publish this project as open source.
