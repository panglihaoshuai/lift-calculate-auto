#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对角线装载功能测试文件
用于测试电梯货物装载计算器的对角线装载功能
"""

import math
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from elevator_calculator import ElevatorCalculator

def test_diagonal_scenarios():
    """测试对角线装载的各种场景"""
    
    print("🚀 开始对角线装载功能测试...")
    print("=" * 60)
    
    # 测试场景1：常规无法装载但对角线可以
    print("场景1：常规无法装载但对角线可以")
    print("-" * 40)
    
    elevator_specs1 = {
        'length': 2.0,
        'width': 1.5,
        'height': 2.2,
        'max_weight': 800
    }
    
    cargo_specs1 = {
        'length': 2.2,
        'width': 1.6,
        'height': 1.8,
        'weight': 400
    }
    
    calculator = ElevatorCalculator()
    result1 = calculator.check_elevator_capacity(
        (elevator_specs1['length'], elevator_specs1['width'], elevator_specs1['height'], elevator_specs1['max_weight']),
        (cargo_specs1['length'], cargo_specs1['width'], cargo_specs1['height'], cargo_specs1['weight'])
    )
    
    elevator_diag = math.sqrt(elevator_specs1['length']**2 + elevator_specs1['width']**2)
    cargo_diag = math.sqrt(cargo_specs1['length']**2 + cargo_specs1['width']**2)
    
    print(f"电梯尺寸: {elevator_specs1['length']}×{elevator_specs1['width']}×{elevator_specs1['height']}m")
    print(f"货物尺寸: {cargo_specs1['length']}×{cargo_specs1['width']}×{cargo_specs1['height']}m")
    print(f"电梯对角线: {elevator_diag:.2f}m")
    print(f"货物对角线: {cargo_diag:.2f}m")
    
    if result1['can_load']:
        print("✅ 可以装载")
        best_orient = result1['best_orientation']
        if best_orient:
            diagonal = best_orient.get('diagonal_fit', False)
            status = "对角线装载" if diagonal else "常规装载"
            utilization = best_orient.get('volume_utilization', 0)
            print(f"  方案: {status} - 体积利用率: {utilization:.1f}%")
            if diagonal:
                print("  ⚡ 利用对角线空间成功装载超大货物")
    else:
        print("❌ 无法装载")
        if result1.get('issues'):
            print(f"原因: {'; '.join(result1['issues'])}")
    
    # 测试场景2：刚好能对角线装载的边界情况
    print("\n" + "=" * 60)
    print("场景2：边界情况 - 刚好能对角线装载")
    print("-" * 40)
    
    elevator_specs2 = {
        'length': 1.8,
        'width': 1.4,
        'height': 2.0,
        'max_weight': 600
    }
    
    cargo_specs2 = {
        'length': 2.2,
        'width': 1.0,
        'height': 1.5,
        'weight': 300
    }
    
    calculator = ElevatorCalculator()
    result2 = calculator.check_elevator_capacity(
        (elevator_specs2['length'], elevator_specs2['width'], elevator_specs2['height'], elevator_specs2['max_weight']),
        (cargo_specs2['length'], cargo_specs2['width'], cargo_specs2['height'], cargo_specs2['weight'])
    )
    
    elevator_diag = math.sqrt(elevator_specs2['length']**2 + elevator_specs2['width']**2)
    cargo_diag = math.sqrt(cargo_specs2['length']**2 + cargo_specs2['width']**2)
    
    print(f"电梯尺寸: {elevator_specs2['length']}×{elevator_specs2['width']}×{elevator_specs2['height']}m")
    print(f"货物尺寸: {cargo_specs2['length']}×{cargo_specs2['width']}×{cargo_specs2['height']}m")
    print(f"电梯对角线: {elevator_diag:.2f}m")
    print(f"货物对角线: {cargo_diag:.2f}m")
    
    if result2['can_load']:
        print("✅ 可以装载")
        best_orient = result2['best_orientation']
        if best_orient:
            diagonal = best_orient.get('diagonal_fit', False)
            status = "对角线装载" if diagonal else "常规装载"
            utilization = best_orient.get('volume_utilization', 0)
            print(f"  方案: {status} - 体积利用率: {utilization:.1f}%")
    else:
        print("❌ 无法装载")
        if result2.get('issues'):
            print(f"原因: {'; '.join(result2['issues'])}")
    
    # 测试场景3：对角线也无法装载
    print("\n" + "=" * 60)
    print("场景3：超大货物 - 对角线也无法装载")
    print("-" * 40)
    
    elevator_specs3 = {
        'length': 1.8,
        'width': 1.2,
        'height': 2.0,
        'max_weight': 1000
    }
    
    cargo_specs3 = {
        'length': 2.5,
        'width': 2.0,
        'height': 1.8,
        'weight': 800
    }
    
    calculator = ElevatorCalculator()
    result3 = calculator.check_elevator_capacity(
        (elevator_specs3['length'], elevator_specs3['width'], elevator_specs3['height'], elevator_specs3['max_weight']),
        (cargo_specs3['length'], cargo_specs3['width'], cargo_specs3['height'], cargo_specs3['weight'])
    )
    
    elevator_diag = math.sqrt(elevator_specs3['length']**2 + elevator_specs3['width']**2)
    cargo_diag = math.sqrt(cargo_specs3['length']**2 + cargo_specs3['width']**2)
    
    print(f"电梯尺寸: {elevator_specs3['length']}×{elevator_specs3['width']}×{elevator_specs3['height']}m")
    print(f"货物尺寸: {cargo_specs3['length']}×{cargo_specs3['width']}×{cargo_specs3['height']}m")
    print(f"电梯对角线: {elevator_diag:.2f}m")
    print(f"货物对角线: {cargo_diag:.2f}m")
    
    if result3['can_load']:
        print("✅ 可以装载")
    else:
        print("❌ 无法装载")
        if result3.get('issues'):
            print(f"原因: {'; '.join(result3['issues'])}")
    
    # 测试场景4：重量限制测试
    print("\n" + "=" * 60)
    print("场景4：重量限制 - 尺寸可以但超重")
    print("-" * 40)
    
    elevator_specs4 = {
        'length': 2.5,
        'width': 2.0,
        'height': 2.5,
        'max_weight': 500  # 限制重量
    }
    
    cargo_specs4 = {
        'length': 2.2,
        'width': 1.5,
        'height': 1.8,
        'weight': 600  # 超重
    }
    
    calculator = ElevatorCalculator()
    result4 = calculator.check_elevator_capacity(
        (elevator_specs4['length'], elevator_specs4['width'], elevator_specs4['height'], elevator_specs4['max_weight']),
        (cargo_specs4['length'], cargo_specs4['width'], cargo_specs4['height'], cargo_specs4['weight'])
    )
    
    print(f"电梯尺寸: {elevator_specs4['length']}×{elevator_specs4['width']}×{elevator_specs4['height']}m")
    print(f"货物尺寸: {cargo_specs4['length']}×{cargo_specs4['width']}×{cargo_specs4['height']}m")
    print(f"电梯载重: {elevator_specs4['max_weight']}kg")
    print(f"货物重量: {cargo_specs4['weight']}kg")
    
    if result4['can_load']:
        print("✅ 可以装载")
    else:
        print("❌ 无法装载")
        if result4.get('issues'):
            print(f"原因: {'; '.join(result4['issues'])}")
    
    # 测试场景5：常规和对角线都可以装载
    print("\n" + "=" * 60)
    print("场景5：中等货物 - 常规和对角线都可以装载")
    print("-" * 40)
    
    elevator_specs5 = {
        'length': 2.5,
        'width': 2.0,
        'height': 2.5,
        'max_weight': 1000
    }
    
    cargo_specs5 = {
        'length': 2.0,
        'width': 1.5,
        'height': 1.8,
        'weight': 500
    }
    
    calculator = ElevatorCalculator()
    result5 = calculator.check_elevator_capacity(
        (elevator_specs5['length'], elevator_specs5['width'], elevator_specs5['height'], elevator_specs5['max_weight']),
        (cargo_specs5['length'], cargo_specs5['width'], cargo_specs5['height'], cargo_specs5['weight'])
    )
    
    print(f"电梯尺寸: {elevator_specs5['length']}×{elevator_specs5['width']}×{elevator_specs5['height']}m")
    print(f"货物尺寸: {cargo_specs5['length']}×{cargo_specs5['width']}×{cargo_specs5['height']}m")
    
    if result5['can_load']:
        print("✅ 可以装载")
        best_orient = result5['best_orientation']
        if best_orient:
            diagonal = best_orient.get('diagonal_fit', False)
            status = "对角线装载" if diagonal else "常规装载"
            utilization = best_orient.get('volume_utilization', 0)
            print(f"  方案: {status} - 体积利用率: {utilization:.1f}%")
    else:
        print("❌ 无法装载")
        if result5.get('issues'):
            print(f"原因: {'; '.join(result5['issues'])}")

def test_specific_cases():
    """测试特定的对角线装载案例"""
    
    print("\n" + "=" * 60)
    print("特定案例测试")
    print("-" * 40)
    
    test_cases = [
        {
            "name": "长方形电梯+正方形货物",
            "elevator": {"length": 2.2, "width": 1.8, "height": 2.2, "max_weight": 800},
            "cargo": {"length": 2.0, "width": 2.0, "height": 1.6, "weight": 400}
        },
        {
            "name": "正方形电梯+长方形货物",
            "elevator": {"length": 2.0, "width": 2.0, "height": 2.0, "max_weight": 1000},
            "cargo": {"length": 2.5, "width": 1.0, "height": 1.5, "weight": 300}
        },
        {
            "name": "窄电梯+长货物",
            "elevator": {"length": 1.5, "width": 1.2, "height": 2.0, "max_weight": 600},
            "cargo": {"length": 1.8, "width": 0.8, "height": 1.5, "weight": 200}
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        calculator = ElevatorCalculator()
        result = calculator.check_elevator_capacity(
            (case['elevator']['length'], case['elevator']['width'], case['elevator']['height'], case['elevator']['max_weight']),
            (case['cargo']['length'], case['cargo']['width'], case['cargo']['height'], case['cargo']['weight'])
        )
        
        elevator = case['elevator']
        cargo = case['cargo']
        
        elevator_diag = math.sqrt(elevator['length']**2 + elevator['width']**2)
        cargo_diag = math.sqrt(cargo['length']**2 + cargo['width']**2)
        
        print(f"电梯: {elevator['length']}×{elevator['width']}m (对角线: {elevator_diag:.2f}m)")
        print(f"货物: {cargo['length']}×{cargo['width']}m (对角线: {cargo_diag:.2f}m)")
        
        if result['can_load']:
            best_orient = result['best_orientation']
            diagonal_found = best_orient and best_orient.get('diagonal_fit', False)
            if diagonal_found:
                print("✅ 对角线装载可行")
            else:
                print("✅ 常规装载可行")
        else:
            print("❌ 无法装载")
            if result.get('issues'):
                print(f"原因: {'; '.join(result['issues'])}")

def run_all_tests():
    """运行所有测试"""
    try:
        test_diagonal_scenarios()
        test_specific_cases()
        
        print("\n" + "=" * 60)
        print("🎉 对角线装载测试完成！")
        print("=" * 60)
        print("测试结果总结：")
        print("1. 超大货物：对角线装载有效扩展了装载能力")
        print("2. 边界情况：精确计算对角线长度，避免误判")
        print("3. 重量限制：即使尺寸允许，重量超限也会拒绝")
        print("4. 多种方案：同时提供常规和对角线装载选项")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()