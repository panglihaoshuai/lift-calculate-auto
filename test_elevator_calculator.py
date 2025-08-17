#!/usr/bin/env python3
"""
电梯货物装载计算器测试文件
测试各种实际场景，验证程序的实用性和准确性
"""

import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

# 导入被测试的程序
from elevator_calculator import ElevatorCalculator

class TestElevatorCalculatorRealScenarios(unittest.TestCase):
    """测试真实场景下的电梯装载计算"""
    
    def setUp(self):
        """设置测试环境"""
        self.calculator = ElevatorCalculator()
    
    def test_standard_office_elevator_furniture(self):
        """测试标准办公电梯运送办公家具"""
        # 标准客梯参数（常见办公楼）
        elevator = (1.4, 1.1, 2.2, 1000)
        
        # 办公桌（中等尺寸）
        cargo = (1.2, 0.6, 0.75, 80)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        self.assertTrue(result['can_load'])
        self.assertLess(result['utilizations']['weight'], 20)  # 重量利用率应该很低
        self.assertGreater(result['utilizations']['volume'], 10)  # 空间利用率较高
    
    def test_large_freight_elevator_equipment(self):
        """测试大型货梯运送重型设备"""
        # 大型货梯参数（工厂/仓库）
        elevator = (2.5, 2.0, 2.5, 3000)
        
        # 工业设备
        cargo = (2.0, 1.5, 1.8, 2000)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        self.assertTrue(result['can_load'])
        self.assertGreater(result['utilizations']['weight'], 40)
        self.assertLess(result['utilizations']['weight'], 80)  # 重量利用率适中
    
    def test_small_residential_elevator_sofa(self):
        """测试住宅小电梯运送沙发"""
        # 住宅电梯参数（老旧小区）
        elevator = (1.0, 0.8, 2.0, 500)
        
        # 三人沙发
        cargo = (2.1, 0.9, 0.85, 120)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        # 沙发太长，应该无法直接放入
        self.assertFalse(result['can_load'])  # 负值应该被拒绝  # 零尺寸应该被拒绝
    
    def test_diagonal_fit_scenario(self):
        """测试对角线装载场景"""
        # 稍大的电梯
        elevator = (2.0, 1.8, 2.5, 1500)
        
        # 长条形货物，通过斜放可以放入
        cargo = (2.0, 0.8, 0.5, 100)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        # 通过斜放应该可以放入
        self.assertTrue(result['can_load'])
    
    def test_door_width_limitation(self):
        """测试门宽度限制"""
        # 标准电梯
        elevator = (1.6, 1.4, 2.3, 1200)
        
        # 货物宽度超过门宽
        cargo = (1.0, 1.1, 1.0, 200)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        # 货物太宽，无法通过门
        self.assertFalse(result['can_load'])
    
    def test_weight_limit_exceeded(self):
        """测试超重情况"""
        elevator = (2.0, 1.8, 2.4, 1000)
        
        cargo = (1.5, 1.0, 1.0, 1200)  # 超过电梯载重
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        self.assertFalse(result['can_load'])
    
    def test_tall_item_scenario(self):
        """测试超高物品"""
        elevator = (1.8, 1.5, 2.3, 1500)
        
        # 超高物品
        cargo = (1.0, 0.8, 2.5, 150)  # 超过电梯高度
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        self.assertFalse(result['can_load'])
    
    def test_exact_fit_scenario(self):
        """测试精确匹配场景"""
        elevator = (2.5, 2.0, 2.8, 1000)
        
        cargo = (1.95, 1.45, 1.95, 800)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        # 应该可以放入，但有安全间隙警告
        self.assertTrue(result['can_load'])
    
    def test_empty_elevator_scenario(self):
        """测试空电梯情况"""
        elevator = (1.5, 1.2, 2.2, 1000)
        
        cargo = (0.1, 0.1, 0.1, 1)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        
        self.assertTrue(result['can_load'])
        self.assertLess(result['utilizations']['weight'], 100)
        self.assertLess(result['utilizations']['volume'], 100)

class TestEdgeCases(unittest.TestCase):
    """测试边界情况和异常情况"""
    
    def setUp(self):
        self.calculator = ElevatorCalculator()
    
    def test_zero_dimensions(self):
        """测试零尺寸输入"""
        elevator = (1.5, 1.2, 2.0, 1000)
        
        cargo = (0, 0.5, 0.5, 100)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        self.assertFalse(result['can_load'])
    
    def test_negative_values(self):
        """测试负值输入"""
        elevator = (1.5, 1.2, 2.0, 1000)
        
        cargo = (-1.0, 0.5, 0.5, 100)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        self.assertFalse(result['can_load'])
    
    def test_very_large_cargo(self):
        """测试极大货物"""
        elevator = (2.0, 1.5, 2.5, 2000)
        
        cargo = (10.0, 5.0, 3.0, 5000)
        
        result = self.calculator.check_elevator_capacity(elevator, cargo)
        self.assertFalse(result['can_load'])
        self.assertGreaterEqual(len(result['issues']), 2)  # 至少2个问题

def run_comprehensive_tests():
    """运行综合测试并输出结果"""
    print("=== 电梯货物装载计算器 - 实际场景测试 ===\n")
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试用例
    test_classes = [TestElevatorCalculatorRealScenarios, TestEdgeCases]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n=== 测试结果总结 ===")
    print(f"测试总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败详情:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误详情:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

def test_real_world_scenarios():
    """测试真实世界场景并输出详细分析"""
    print("\n=== 真实世界场景详细分析 ===\n")
    
    calculator = ElevatorCalculator()
    
    # 场景1: 办公楼搬迁
    print("场景1: 办公楼搬迁 - 办公桌和文件柜")
    elevator1 = (1.6, 1.4, 2.3, 1000)
    cargo1 = (1.4, 0.7, 1.2, 150)
    result1 = calculator.check_elevator_capacity(elevator1, cargo1)
    
    print(f"结果: {'✓ 可以装载' if result1['can_load'] else '✗ 无法装载'}")
    print(f"重量利用率: {result1['utilizations']['weight']:.1f}%")
    print(f"空间利用率: {result1['utilizations']['volume']:.1f}%")
    if result1['issues']:
        print(f"问题: {', '.join(result1['issues'])}")
    print()
    
    # 场景2: 家庭搬家
    print("场景2: 家庭搬家 - 冰箱")
    elevator2 = (1.4, 1.1, 2.2, 800)
    cargo2 = (0.7, 0.7, 1.8, 120)
    result2 = calculator.check_elevator_capacity(elevator2, cargo2)
    
    print(f"结果: {'✓ 可以装载' if result2['can_load'] else '✗ 无法装载'}")
    print(f"重量利用率: {result2['utilizations']['weight']:.1f}%")
    print(f"空间利用率: {result2['utilizations']['volume']:.1f}%")
    if result2['issues']:
        print(f"问题: {', '.join(result2['issues'])}")
    print()
    
    # 场景3: 仓库货物
    print("场景3: 仓库货物 - 大型包装箱")
    elevator3 = (2.2, 1.8, 2.5, 2000)
    cargo3 = (2.0, 1.5, 1.8, 800)
    result3 = calculator.check_elevator_capacity(elevator3, cargo3)
    
    print(f"结果: {'✓ 可以装载' if result3['can_load'] else '✗ 无法装载'}")
    print(f"重量利用率: {result3['utilizations']['weight']:.1f}%")
    print(f"空间利用率: {result3['utilizations']['volume']:.1f}%")
    if result3['issues']:
        print(f"问题: {', '.join(result3['issues'])}")
    print()

if __name__ == "__main__":
    # 运行测试
    success = run_comprehensive_tests()
    
    # 运行真实场景分析
    test_real_world_scenarios()
    
    print("\n=== 程序实用性评估 ===")
    if success:
        print("✓ 所有测试通过 - 程序在实际场景中表现良好")
        print("✓ 考虑了重量、尺寸、对角线、人员因素")
        print("✓ 提供了详细的分析报告")
        print("✓ 适用于办公、家庭、商业等多种场景")
    else:
        print("✗ 部分测试失败 - 需要进一步优化")
    
    print("\n测试完成！请查看详细结果和实际场景分析。")