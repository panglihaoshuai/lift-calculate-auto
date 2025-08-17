#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电梯货物装载计算器 - GUI启动器
快速启动美观的图形界面
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行GUI
from elevator_gui import main

if __name__ == "__main__":
    print("🛗 启动电梯货物装载计算器...")
    print("正在加载界面，请稍候...")
    main()
    print("程序已退出")