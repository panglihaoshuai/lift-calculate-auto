#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电梯货物装载计算器 - 现代化GUI界面
美观简约的界面设计，与主程序分离
"""

import tkinter as tk
from tkinter import ttk, messagebox
import elevator_calculator

class ElevatorCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛗 电梯货物装载计算器")
        self.root.geometry("800x700")
        self.root.configure(bg="#f8f9fa")
        
        # 设置主题样式
        self.setup_styles()
        
        # 创建主界面
        self.create_widgets()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 定义颜色主题
        self.colors = {
            'primary': '#007bff',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
        # 配置样式
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                       foreground=self.colors['primary'])
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Result.TLabel', font=('Segoe UI', 11))
        style.configure('Success.TLabel', foreground=self.colors['success'], 
                       font=('Segoe UI', 11, 'bold'))
        style.configure('Error.TLabel', foreground=self.colors['danger'], 
                       font=('Segoe UI', 11, 'bold'))
        
        # 按钮样式
        style.configure('Primary.TButton', font=('Segoe UI', 11), 
                       background=self.colors['primary'], foreground='white')
        style.configure('Success.TButton', font=('Segoe UI', 11), 
                       background=self.colors['success'], foreground='white')
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = ttk.Frame(self.root, style='Title.TFrame')
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = ttk.Label(title_frame, text="🛗 电梯货物装载计算器", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # 创建笔记本式布局
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 输入页面
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="📊 参数输入")
        self.create_input_page(input_frame)
        
        # 结果页面
        result_frame = ttk.Frame(self.notebook)
        self.notebook.add(result_frame, text="📋 分析结果")
        self.create_result_page(result_frame)
        
        # 关于页面
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ 关于")
        self.create_about_page(about_frame)
        
    def create_input_page(self, parent):
        """创建输入页面"""
        # 电梯参数组
        elevator_group = ttk.LabelFrame(parent, text="电梯规格", padding=15)
        elevator_group.pack(fill=tk.X, padx=20, pady=10)
        
        # 电梯尺寸输入
        ttk.Label(elevator_group, text="长度 (米):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.elevator_length = ttk.Entry(elevator_group, width=10, font=('Segoe UI', 11))
        self.elevator_length.grid(row=0, column=1, padx=5, pady=5)
        self.elevator_length.insert(0, "1.6")
        
        ttk.Label(elevator_group, text="宽度 (米):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.elevator_width = ttk.Entry(elevator_group, width=10, font=('Segoe UI', 11))
        self.elevator_width.grid(row=1, column=1, padx=5, pady=5)
        self.elevator_width.insert(0, "1.4")
        
        ttk.Label(elevator_group, text="高度 (米):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.elevator_height = ttk.Entry(elevator_group, width=10, font=('Segoe UI', 11))
        self.elevator_height.grid(row=2, column=1, padx=5, pady=5)
        self.elevator_height.insert(0, "2.3")
        
        ttk.Label(elevator_group, text="限重 (公斤):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.elevator_limit = ttk.Entry(elevator_group, width=10, font=('Segoe UI', 11))
        self.elevator_limit.grid(row=3, column=1, padx=5, pady=5)
        self.elevator_limit.insert(0, "1000")
        
        # 货物参数组
        cargo_group = ttk.LabelFrame(parent, text="货物规格", padding=15)
        cargo_group.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(cargo_group, text="长度 (米):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cargo_length = ttk.Entry(cargo_group, width=10, font=('Segoe UI', 11))
        self.cargo_length.grid(row=0, column=1, padx=5, pady=5)
        self.cargo_length.insert(0, "1.2")
        
        ttk.Label(cargo_group, text="宽度 (米):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cargo_width = ttk.Entry(cargo_group, width=10, font=('Segoe UI', 11))
        self.cargo_width.grid(row=1, column=1, padx=5, pady=5)
        self.cargo_width.insert(0, "0.8")
        
        ttk.Label(cargo_group, text="高度 (米):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.cargo_height = ttk.Entry(cargo_group, width=10, font=('Segoe UI', 11))
        self.cargo_height.grid(row=2, column=1, padx=5, pady=5)
        self.cargo_height.insert(0, "1.0")
        
        ttk.Label(cargo_group, text="重量 (公斤):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.cargo_weight = ttk.Entry(cargo_group, width=10, font=('Segoe UI', 11))
        self.cargo_weight.grid(row=3, column=1, padx=5, pady=5)
        self.cargo_weight.insert(0, "200")
        
        # 人员参数组
        people_group = ttk.LabelFrame(parent, text="人员配置", padding=15)
        people_group.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(people_group, text="运送人员数量:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_people = ttk.Spinbox(people_group, from_=1, to=10, width=8, font=('Segoe UI', 11))
        self.num_people.grid(row=0, column=1, padx=5, pady=5)
        self.num_people.set("1")
        
        # 计算按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        calculate_btn = ttk.Button(button_frame, text="🔍 开始分析", 
                                  command=self.calculate_capacity, style='Primary.TButton')
        calculate_btn.pack(side=tk.LEFT, padx=5)
        
        # 新增“开始计算”按钮
        calculate_btn2 = ttk.Button(button_frame, text="🚀 开始计算", 
                                   command=self.calculate_capacity, style='Primary.TButton')
        calculate_btn2.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="🔄 清空", 
                              command=self.clear_inputs)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 快速结果区域
        quick_result_frame = ttk.LabelFrame(parent, text="快速结果预览", padding=15)
        quick_result_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.quick_result_label = ttk.Label(quick_result_frame, 
                                          text="💡 点击'开始分析'按钮查看结果", 
                                          font=('Segoe UI', 12), 
                                          foreground='#6c757d')
        self.quick_result_label.pack(pady=10)
        
    def create_result_page(self, parent):
        """创建结果页面"""
        # 创建滚动文本框
        result_frame = ttk.Frame(parent)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 结果文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=25, 
                                  font=('Segoe UI', 11), bg='white')
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, 
                                command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 添加标签
        self.result_text.tag_configure('title', font=('Segoe UI', 16, 'bold'), 
                                     foreground=self.colors['primary'])
        self.result_text.tag_configure('success', font=('Segoe UI', 11, 'bold'), 
                                     foreground=self.colors['success'])
        self.result_text.tag_configure('error', font=('Segoe UI', 11, 'bold'), 
                                     foreground=self.colors['danger'])
        self.result_text.tag_configure('header', font=('Segoe UI', 12, 'bold'))
        
    def create_about_page(self, parent):
        """创建关于页面"""
        about_text = """
🛗 电梯货物装载计算器 v2.0

📋 功能特点：
• 支持3D对角线计算
• 考虑安全间隙和人员因素
• 提供6种摆放方向分析
• 检查电梯门通行能力
• 评估重量分布和重心
• 生成详细分析报告

🔧 技术参数：
• 单人重量：75kg
• 单人占用空间：0.4㎡
• 人员高度：1.8m
• 安全间隙：0.1m
• 门安全间隙：0.05m

💡 使用说明：
1. 输入电梯规格参数
2. 输入货物尺寸和重量
3. 设置运送人员数量
4. 点击分析获取结果

⚠️ 注意事项：
• 所有参数必须为正数
• 建议预留安全空间
• 重量接近上限时需谨慎
• 实际使用时请参考电梯说明书

© 2024 电梯货物装载计算器
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, font=('Segoe UI', 11), 
                            bg='white', padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, about_text)
        text_widget.configure(state='disabled')
        
    def calculate_capacity(self):
        """计算装载能力"""
        try:
            # 获取输入参数
            elevator_length = float(self.elevator_length.get())
            elevator_width = float(self.elevator_width.get())
            elevator_height = float(self.elevator_height.get())
            elevator_limit = float(self.elevator_limit.get())
            
            cargo_length = float(self.cargo_length.get())
            cargo_width = float(self.cargo_width.get())
            cargo_height = float(self.cargo_height.get())
            cargo_weight = float(self.cargo_weight.get())
            
            num_people = int(self.num_people.get())
            
            # 验证输入
            if any(val <= 0 for val in [elevator_length, elevator_width, elevator_height, 
                                      elevator_limit, cargo_length, cargo_width, 
                                      cargo_height, cargo_weight]):
                messagebox.showerror("输入错误", "所有参数必须为正数！")
                return
            
            # 创建计算器实例
            calculator = elevator_calculator.ElevatorCalculator()
            
            # 计算结果
            result = calculator.check_elevator_capacity(
                (elevator_length, elevator_width, elevator_height, elevator_limit),
                (cargo_length, cargo_width, cargo_height, cargo_weight),
                num_people
            )
            
            # 显示结果
            self.display_result(result, elevator_length, elevator_width, elevator_height, 
                              elevator_limit, cargo_length, cargo_width, cargo_height, 
                              cargo_weight, num_people)
            
            # 自动切换到结果页面
            self.notebook.select(1)
            
            # 显示成功提示
            if result['can_load']:
                messagebox.showinfo("分析完成", "✅ 货物可以安全装载！\n\n请查看'分析结果'标签页获取详细信息")
            else:
                messagebox.showwarning("分析完成", "❌ 货物无法安全装载！\n\n请查看'分析结果'标签页了解原因")
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字！")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误：{str(e)}")
    
    def display_result(self, result, el, ew, eh, elevator_limit, cl, cw, ch, cargo_weight, num_people):
        """显示计算结果"""
        # 更新快速结果预览
        if result['can_load']:
            self.quick_result_label.config(
                text=f"✅ 可以装载！\n总重量利用率：{result['utilizations']['weight']:.1f}% | "
                     f"体积利用率：{result['utilizations']['volume']:.1f}%",
                foreground=self.colors['success'],
                font=('Segoe UI', 12, 'bold')
            )
        else:
            issues = len(result['issues'])
            self.quick_result_label.config(
                text=f"❌ 无法装载！\n发现{issues}个问题，请查看详细分析",
                foreground=self.colors['danger'],
                font=('Segoe UI', 12, 'bold')
            )
        
        # 详细结果显示
        self.result_text.delete(1.0, tk.END)
        
        # 结果标题
        if result['can_load']:
            title = "✅ 分析结果：可以安全装载\n"
            self.result_text.insert(tk.END, title, 'success')
        else:
            title = "❌ 分析结果：无法安全装载\n"
            self.result_text.insert(tk.END, title, 'error')
        
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # 参数信息
        self.result_text.insert(tk.END, "📐 电梯规格：", 'header')
        self.result_text.insert(tk.END, f"{el}×{ew}×{eh}m, 限重{elevator_limit}kg\n")
        
        self.result_text.insert(tk.END, "📦 货物规格：", 'header')
        self.result_text.insert(tk.END, f"{cl}×{cw}×{ch}m, 重量{cargo_weight}kg\n")
        
        self.result_text.insert(tk.END, "👥 人员配置：", 'header')
        self.result_text.insert(tk.END, f"{num_people}人, 总重量{num_people*75}kg\n\n")
        
        # 利用率统计
        self.result_text.insert(tk.END, "📊 利用率统计：\n", 'header')
        self.result_text.insert(tk.END, f"   货物重量占比：{result['utilizations']['cargo_weight']:.1f}%\n")
        self.result_text.insert(tk.END, f"   人员重量占比：{result['utilizations']['person_weight']:.1f}%\n")
        self.result_text.insert(tk.END, f"   总重量利用率：{result['utilizations']['weight']:.1f}%\n")
        self.result_text.insert(tk.END, f"   体积利用率：{result['utilizations']['volume']:.1f}%\n\n")
        
        # 人员分析
        person_analysis = result['person_analysis']
        self.result_text.insert(tk.END, "👥 人员空间分析：\n", 'header')
        self.result_text.insert(tk.END, f"   电梯内剩余面积：{person_analysis['remaining_area']:.2f}㎡\n")
        self.result_text.insert(tk.END, f"   人员所需面积：{person_analysis['person_area_needed']:.2f}㎡\n")
        self.result_text.insert(tk.END, f"   重量限制下最大人数：{person_analysis['max_people_by_weight']}人\n")
        self.result_text.insert(tk.END, f"   空间限制下最大人数：{person_analysis['max_people_by_space']}人\n\n")
        
        # 3D可视化摆放指导
        self.result_text.insert(tk.END, "📐 3D空间摆放指导\n", 'header')
        self.result_text.insert(tk.END, "=" * 30 + "\n\n")
        
        # 所有摆放方向可视化
        orientations = result.get('orientations', [])
        if orientations:
            self.result_text.insert(tk.END, "🎯 6种摆放方向对比：\n\n", 'header')
            
            for i, ori in enumerate(orientations, 1):
                dims = ori['orientation']
                util = ori['volume_utilization']
                
                # 判断是否为对角线方案
                status = "✅"
                diag_flag = ori.get('diagonal_fit', False)
                if diag_flag:
                    status = "🟦 斜放"
                self.result_text.insert(tk.END, f"{status} 方向{i}: {dims[0]}×{dims[1]}×{dims[2]}m "
                                           f"(利用率: {util:.1f}%)\n")
                # ASCII可视化
                ascii_diagram = self.generate_ascii_diagram(el, ew, dims[0], dims[1], diag_flag)
                self.result_text.insert(tk.END, ascii_diagram + "\n\n")
        
        # 最佳摆放详细指导
        if result['best_orientation']:
            best = result['best_orientation']
            self.result_text.insert(tk.END, "\n🎯 推荐摆放方案：\n", 'header')
            self.result_text.insert(tk.END, f"   货物尺寸：{best['orientation'][0]}×{best['orientation'][1]}×{best['orientation'][2]}m\n")
            self.result_text.insert(tk.END, f"   空间利用率：{best['volume_utilization']:.1f}%\n")
            
            # 对角线装载特殊指导
            is_diagonal = best.get('diagonal_fit', False)
            if is_diagonal:
                import math
                self.result_text.insert(tk.END, "\n📋 对角线装载指导\n", 'header')
                guide = f"""\🎯 对角线装载方案（超大货物专用）

电梯尺寸：{el}×{ew}×{eh}米
货物尺寸：{best['orientation'][0]}×{best['orientation'][1]}×{best['orientation'][2]}米

📐 装载要点：
• 货物需沿电梯对角线方向放置
• 利用对角线长度：{math.sqrt(el**2 + ew**2):.1f}米
• 货物对角线：{math.sqrt(best['orientation'][0]**2 + best['orientation'][1]**2):.1f}米

⚠️ 注意事项：
• 需要{num_people}人配合操作
• 先调整货物角度，再缓慢推入
• 确保货物重心稳定，避免倾斜
• 装载后检查四个角落的间隙

🎨 装载步骤：
1. 将货物旋转45度角
2. 对准电梯对角线方向
3. 缓慢推入，注意边缘对齐
4. 确认装载完成，关闭电梯门
                """
                self.result_text.insert(tk.END, guide)
            else:
                # 3D坐标指导
                self.result_text.insert(tk.END, "\n📍 3D坐标定位：\n", 'header')
                self.result_text.insert(tk.END, f"   • 货物中心点：({el/2:.1f}, {ew/2:.1f}, {best['orientation'][2]/2:.1f})\n")
                self.result_text.insert(tk.END, f"   • 货物边缘：距离电梯壁各0.1m安全间隙\n")
                self.result_text.insert(tk.END, f"   • 货物方向：长边{'沿电梯长度' if best['orientation'][0] <= el else '沿电梯宽度'}摆放\n")
                
                # 可视化装载图
                loading_guide = self.generate_loading_guide(el, ew, eh, 
                                                          best['orientation'][0], 
                                                          best['orientation'][1], 
                                                          best['orientation'][2],
                                                          num_people)
                self.result_text.insert(tk.END, loading_guide)
        
        # 问题列表
        if result['issues']:
            self.result_text.insert(tk.END, "⚠️ 发现的问题：\n", 'header')
            for issue in result['issues']:
                self.result_text.insert(tk.END, f"   • {issue}\n")
            self.result_text.insert(tk.END, "\n")
        
        # 建议列表
        if result['recommendations']:
            self.result_text.insert(tk.END, "💡 建议：\n", 'header')
            for rec in result['recommendations']:
                self.result_text.insert(tk.END, f"   • {rec}\n")
    
    def generate_ascii_diagram(self, elevator_l, elevator_w, cargo_l, cargo_w, is_diagonal=False):
        """生成ASCII可视化图，支持对角线显示"""
        scale = min(20 / elevator_l, 10 / elevator_w)
        el_scaled = max(1, int(elevator_l * scale))
        ew_scaled = max(1, int(elevator_w * scale))
        cl_scaled = max(1, int(cargo_l * scale))
        cw_scaled = max(1, int(cargo_w * scale))
        
        diagram = []
        
        if is_diagonal:
            diagram.append("电梯对角线装载示意图")
            diagram.append("┌" + "─" * el_scaled + "┐")
            
            # 对角线放置：用斜线表示
            for w in range(ew_scaled):
                line = "│"
                for l in range(el_scaled):
                    # 计算对角线位置
                    if abs(l - w * el_scaled/ew_scaled) < max(cl_scaled, cw_scaled)/2:
                        line += "◢"
                    elif abs(l - (ew_scaled-w) * el_scaled/ew_scaled) < max(cl_scaled, cw_scaled)/2:
                        line += "◣"
                    else:
                        line += " "
                line += "│"
                diagram.append(line)
            
            diagram.append("└" + "─" * el_scaled + "┘")
            diagram.append(f"电梯: {elevator_l}×{elevator_w}m | 货物: {cargo_l}×{cargo_w}m (斜放)")
            diagram.append("⚡ 利用对角线空间，可装载超大货物")
        else:
            diagram.append("电梯俯视图 (单位: 格)")
            diagram.append("┌" + "─" * el_scaled + "┐")
            
            # 计算货物居中位置
            start_l = max(0, (el_scaled - cl_scaled) // 2)
            start_w = max(0, (ew_scaled - cw_scaled) // 2)
            
            for w in range(ew_scaled):
                line = "│"
                for l in range(el_scaled):
                    if (start_l <= l < start_l + cl_scaled and 
                        start_w <= w < start_w + cw_scaled):
                        line += "█"
                    else:
                        line += " "
                line += "│"
                diagram.append(line)
            
            diagram.append("└" + "─" * el_scaled + "┘")
            diagram.append(f"电梯: {elevator_l}×{elevator_w}m | 货物: {cargo_l}×{cargo_w}m")
        
        return "\n".join(diagram)
    
    def generate_loading_guide(self, el, ew, eh, cl, cw, ch, num_people):
        """生成简化的3D装载指导图"""
        guide = []
        
        # 简化版电梯布局图
        guide.append("\n📊 电梯装载示意图：")
        guide.append("┌──────────────────────────────────────────┐")
        guide.append("│  🚪 电梯门 (正面)                        │")
        guide.append("│  ┌──────────────────────────────────┐  │")
        guide.append("│  │                                  │  │")
        guide.append("│  │  📦 货物摆放区域                  │  │")
        guide.append("│  │  长: {:.1f}m 宽: {:.1f}m 高: {:.1f}m  │  │".format(cl, cw, ch))
        guide.append("│  │                                  │  │")
        guide.append("│  └──────────────────────────────────┘  │")
        guide.append("│  👥 人员站立区域                        │")
        guide.append("└──────────────────────────────────────────┘")
        
        # 简单方位说明
        guide.append("\n📍 具体摆放指导：")
        guide.append("   📐 货物位置：电梯正中央")
        guide.append("   📏 前后间隙：前 {:.1f}m，后 {:.1f}m".format(el-cl, el-cl))
        guide.append("   📏 左右间隙：左 {:.1f}m，右 {:.1f}m".format(ew-cw, ew-cw))
        guide.append("   📏 上下间隙：上方 {:.1f}m".format(eh-ch))
        
        # 人员位置建议
        person_area = 0.4 * num_people
        remaining_area = (el * ew) - (cl * cw)
        
        guide.append("\n👥 人员安排：")
        guide.append("   🚶 人员数量：{}人".format(num_people))
        guide.append("   📏 需要空间：{:.1f}㎡".format(person_area))
        guide.append("   📍 站立位置：货物两侧或后方".format())
        
        if remaining_area < person_area * 1.5:
            guide.append("   ⚠️  提示：空间较紧张，建议减少人员")
        
        # 操作步骤
        guide.append("\n✅ 装载步骤：")
        guide.append("   1️⃣ 将货物推入电梯中央")
        guide.append("   2️⃣ 确认四周间隙足够")
        guide.append("   3️⃣ 人员站在安全区域")
        guide.append("   4️⃣ 关闭电梯门开始运行")
        
        return "\n".join(guide)

    def clear_inputs(self):
        """清空输入"""
        self.elevator_length.delete(0, tk.END)
        self.elevator_length.insert(0, "1.6")
        
        self.elevator_width.delete(0, tk.END)
        self.elevator_width.insert(0, "1.4")
        
        self.elevator_height.delete(0, tk.END)
        self.elevator_height.insert(0, "2.3")
        
        self.elevator_limit.delete(0, tk.END)
        self.elevator_limit.insert(0, "1000")
        
        self.cargo_length.delete(0, tk.END)
        self.cargo_length.insert(0, "1.2")
        
        self.cargo_width.delete(0, tk.END)
        self.cargo_width.insert(0, "0.8")
        
        self.cargo_height.delete(0, tk.END)
        self.cargo_height.insert(0, "1.0")
        
        self.cargo_weight.delete(0, tk.END)
        self.cargo_weight.insert(0, "200")
        
        self.num_people.set("1")
        
        # 清空结果
        self.result_text.delete(1.0, tk.END)
        self.quick_result_label.config(
            text="💡 点击'开始分析'按钮查看结果",
            foreground='#6c757d',
            font=('Segoe UI', 12)
        )

def main():
    """主函数"""
    root = tk.Tk()
    app = ElevatorCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()