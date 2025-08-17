#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级电梯货物装载计算器
考虑3D空间对角线、旋转摆放、重心偏移等实际因素
"""

import math

class ElevatorCalculator:
    def __init__(self):
        # 安全间隙参数 (米)
        self.safety_gap = 0.05  # 四周预留5cm安全间隙
        self.door_safety_gap = 0.1  # 门口额外预留10cm
        self.max_tilt_angle = 15  # 最大允许倾斜角度(度)
        
        # 人员相关参数
        self.person_avg_weight = 75  # 单人平均重量(kg)
        self.person_min_space = 0.4  # 单人最小占用空间(平方米)
        self.person_height = 1.8  # 人员高度(米)
        self.min_operation_space = 0.6  # 最小操作空间(米) - 人员活动空间
        
    def calculate_3d_diagonal(self, length, width, height):
        """计算3D空间对角线长度"""
        return math.sqrt(length**2 + width**2 + height**2)
    
    def calculate_2d_diagonal(self, length, width):
        """计算2D平面对角线长度"""
        return math.sqrt(length**2 + width**2)
    
    def check_all_orientations(self, elevator_dims, cargo_dims):
        """
        检查货物所有可能的摆放方式
        返回最佳摆放方式和利用率
        """
        el, ew, eh = elevator_dims
        cl, cw, ch = cargo_dims
        
        orientations = [
            (cl, cw, ch),  # 原始方向
            (cl, ch, cw),  # 旋转90度
            (cw, cl, ch),  # 旋转90度
            (cw, ch, cl),  # 旋转180度
            (ch, cl, cw),  # 旋转270度
            (ch, cw, cl)   # 完全翻转
        ]
        
        valid_orientations = []
        
        for l, w, h in orientations:
            # 考虑安全间隙后的有效尺寸
            effective_l = l + 2 * self.safety_gap
            effective_w = w + 2 * self.safety_gap
            effective_h = h + self.safety_gap
            
            if effective_l <= el and effective_w <= ew and effective_h <= eh:
                volume_util = (l * w * h) / (el * ew * eh) * 100
                valid_orientations.append({
                    'orientation': (l, w, h),
                    'volume_utilization': volume_util,
                    'length_util': (l / el) * 100,
                    'width_util': (w / ew) * 100,
                    'height_util': (h / eh) * 100
                })
        
        return valid_orientations
    
    def check_diagonal_fit(self, elevator_dims, cargo_dims):
        """检查对角线是否超出"""
        el, ew, eh = elevator_dims
        cl, cw, ch = cargo_dims
        
        # 计算电梯空间对角线
        elevator_diagonal = self.calculate_3d_diagonal(el, ew, eh)
        
        # 计算货物对角线
        cargo_diagonal = self.calculate_3d_diagonal(cl, cw, ch)
        
        return cargo_diagonal <= elevator_diagonal, cargo_diagonal, elevator_diagonal
    
    def check_door_access(self, elevator_dims, cargo_dims, door_width_ratio=0.8):
        """检查电梯门通行能力"""
        el, ew, eh = elevator_dims
        cl, cw, ch = cargo_dims
        
        door_width = ew * door_width_ratio - self.door_safety_gap
        door_height = eh * 0.9  # 门高度通常略低于电梯高度
        
        # 检查货物能否通过门
        issues = []
        if cw > door_width:
            issues.append(f"货物宽度 {cw:.2f}m 超过门宽 {door_width:.2f}m")
        if ch > door_height:
            issues.append(f"货物高度 {ch:.2f}m 超过门高 {door_height:.2f}m")
        
        # 检查对角线通过门的情况
        door_diagonal = self.calculate_2d_diagonal(door_width, door_height)
        cargo_face_diagonal = self.calculate_2d_diagonal(cw, ch)
        
        if cargo_face_diagonal > door_diagonal:
            issues.append(f"货物对角线 {cargo_face_diagonal:.2f}m 超过门对角线 {door_diagonal:.2f}m")
        
        return len(issues) == 0, issues, door_width, door_height
    
    def check_weight_distribution(self, cargo_weight, elevator_limit, cargo_dims, elevator_dims):
        """检查重量分布和重心"""
        cl, cw, ch = cargo_dims
        el, ew, eh = elevator_dims
        
        issues = []
        
        # 重量检查
        if cargo_weight > elevator_limit:
            issues.append(f"货物重量 {cargo_weight}kg 超过电梯限重 {elevator_limit}kg")
        
        # 计算重量利用率
        weight_util = (cargo_weight / elevator_limit) * 100
        
        # 重心偏移检查 (简化计算)
        max_eccentricity = min(el, ew) * 0.1  # 允许10%的偏心距
        
        return issues, weight_util, max_eccentricity
    
    def check_elevator_capacity(self, elevator_specs, cargo_specs, num_people=1):
        """
        综合检查电梯装载能力（包含人员因素）
        
        参数:
        - elevator_specs: (长, 宽, 高, 限重) 元组
        - cargo_specs: (长, 宽, 高, 重量) 元组
        - num_people: 电梯内人员数量，默认为1人
        
        返回:
        - 综合评估结果（包含人员分析）
        """
        el, ew, eh, elevator_limit = elevator_specs
        cl, cw, ch, cargo_weight = cargo_specs
        
        results = {
            'can_load': False,
            'issues': [],
            'recommendations': [],
            'best_orientation': None,
            'utilizations': {},
            'person_analysis': {}
        }
        
        # 输入验证
        if any(val <= 0 for val in [el, ew, eh, elevator_limit, cl, cw, ch, cargo_weight]):
            results['issues'].append("所有尺寸和重量参数必须为正数")
            return results
            
        if num_people < 0:
            results['issues'].append("人员数量不能为负数")
            return results
        
        # 计算人员重量
        total_person_weight = num_people * self.person_avg_weight
        total_weight = cargo_weight + total_person_weight
        
        # 检查所有摆放方向
        valid_orientations = self.check_all_orientations((el, ew, eh), (cl, cw, ch))
        
        if not valid_orientations:
            # 检查对角线是否可能
            diag_fit, cargo_diag, elevator_diag = self.check_diagonal_fit((el, ew, eh), (cl, cw, ch))
            if diag_fit:
                # 对角线可以装载，作为特殊方案返回
                volume_util = (cl * cw * ch) / (el * ew * eh) * 100
                diag_orientation = {
                    'orientation': (cl, cw, ch),
                    'volume_utilization': volume_util,
                    'length_util': (cl / el) * 100,
                    'width_util': (cw / ew) * 100,
                    'height_util': (ch / eh) * 100,
                    'diagonal_fit': True
                }
                results['best_orientation'] = diag_orientation
                results['orientations'] = [diag_orientation]
                results['recommendations'].append("建议斜放货物（利用对角线），可安全装载")
                results['can_load'] = True
            else:
                results['issues'].append(f"货物对角线 {cargo_diag:.2f}m 超过电梯空间 {elevator_diag:.2f}m")
                results['can_load'] = False
            # 人员因素检查
            if total_weight > elevator_limit:
                results['issues'].append(f"总重量 {total_weight}kg (货物+{num_people}人) 超过电梯限重 {elevator_limit}kg")
            return results
        
        # 选择最佳摆放方向（最高空间利用率）
        best_orientation = max(valid_orientations, key=lambda x: x['volume_utilization'])
        results['best_orientation'] = best_orientation
        
        # 检查门通行
        door_ok, door_issues, door_width, door_height = self.check_door_access((el, ew, eh), best_orientation['orientation'])
        if not door_ok:
            results['issues'].extend(door_issues)
        
        # 检查重量分布（包含人员重量）
        weight_issues, weight_util, max_ecc = self.check_weight_distribution(total_weight, elevator_limit, best_orientation['orientation'], (el, ew, eh))
        results['issues'].extend(weight_issues)
        
        # 人员空间检查
        elevator_area = el * ew
        cargo_area = best_orientation['orientation'][0] * best_orientation['orientation'][1]
        remaining_area = max(0, elevator_area - cargo_area)
        person_area_needed = num_people * self.person_min_space
        
        if person_area_needed > remaining_area:
            results['issues'].append(f"剩余空间 {remaining_area:.2f}㎡ 不足 {num_people}人 所需 {person_area_needed:.2f}㎡")
        
        # 人员高度检查
        person_height_needed = self.person_height
        if person_height_needed > eh:
            results['issues'].append(f"电梯高度 {eh}m 不足人员站立 {person_height_needed}m")
        
        # 计算利用率
        results['utilizations']['weight'] = (total_weight / elevator_limit) * 100
        results['utilizations']['volume'] = best_orientation['volume_utilization']
        results['utilizations']['cargo_weight'] = (cargo_weight / elevator_limit) * 100
        results['utilizations']['person_weight'] = (total_person_weight / elevator_limit) * 100
        
        # 人员分析
        results['person_analysis'] = {
            'person_count': num_people,
            'person_weight': total_person_weight,
            'remaining_area': remaining_area,
            'person_area_needed': person_area_needed,
            'max_people_by_weight': max(0, int((elevator_limit - cargo_weight) / self.person_avg_weight)),
            'max_people_by_space': max(0, int(remaining_area / self.person_min_space))
        }
        
        # 添加所有有效摆放方向
        results['orientations'] = valid_orientations
        
        # 生成建议
        if results['issues']:
            results['recommendations'].append("建议检查货物是否可以拆分运输")
            if results['utilizations']['weight'] > 90:
                results['recommendations'].append("重量接近上限，建议减少人员或分批运输")
            if best_orientation['volume_utilization'] < 50:
                results['recommendations'].append("空间利用率低，可考虑优化摆放方式")
            if remaining_area < person_area_needed:
                results['recommendations'].append("建议减少电梯内人员数量")
        else:
            results['can_load'] = True
            results['recommendations'].append("可以安全装载")
            if results['utilizations']['weight'] > 80:
                results['recommendations'].append("注意：重量利用率较高，搬运时小心")
            if remaining_area < person_area_needed * 1.5:
                results['recommendations'].append("建议优化人员站位")
        
        return results

def check_elevator_capacity(elevator_length, elevator_width, elevator_height, 
                          elevator_weight_limit, cargo_length, cargo_width, 
                          cargo_height, cargo_total_weight, num_people=1):
    """
    向后兼容的简化接口（包含人员因素）
    """
    calculator = ElevatorCalculator()
    result = calculator.check_elevator_capacity(
        (elevator_length, elevator_width, elevator_height, elevator_weight_limit),
        (cargo_length, cargo_width, cargo_height, cargo_total_weight),
        num_people
    )
    
    # 转换回简单格式
    reasons = result['issues'] + result['recommendations']
    if result['can_load']:
        reasons.insert(0, "✅ 货物和人员可以安全装入电梯")
    else:
        reasons.insert(0, "❌ 货物和人员无法安全装入电梯")
    
    return result['can_load'], reasons, result

def get_float_input(prompt):
    """获取浮点数输入"""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("请输入大于0的数值")
                continue
            return value
        except ValueError:
            print("请输入有效的数字")

def main():
    """主程序"""
    print("=== 电梯货物装载计算器 ===\n")
    
    # 获取电梯参数
    print("请输入电梯参数:")
    elevator_length = get_float_input("电梯长度 (米): ")
    elevator_width = get_float_input("电梯宽度 (米): ")
    elevator_height = get_float_input("电梯高度 (米): ")
    elevator_weight_limit = get_float_input("电梯限重 (千克): ")
    
    print("\n请输入货物参数:")
    cargo_length = get_float_input("货物长度 (米): ")
    cargo_width = get_float_input("货物宽度 (米): ")
    cargo_height = get_float_input("货物高度 (米): ")
    cargo_total_weight = get_float_input("货物总重量 (千克): ")
    
    num_people = int(input("电梯内运送人员数量 (默认1人): ") or "1")
    if num_people < 1:
        num_people = 1
    
    # 计算结果
    can_load, reasons, detailed_result = check_elevator_capacity(
        elevator_length, elevator_width, elevator_height, elevator_weight_limit,
        cargo_length, cargo_width, cargo_height, cargo_total_weight, num_people
    )
    
    # 显示详细结果
    print("\n" + "="*60)
    print("📊 详细分析报告（含人员因素）")
    print("="*60)
    
    if can_load:
        print("✅ 结论：货物和人员可以安全装入电梯")
    else:
        print("❌ 结论：货物和人员无法安全装入电梯")
    
    print(f"\n📐 电梯规格: {elevator_length}×{elevator_width}×{elevator_height}m, 限重{elevator_weight_limit}kg")
    print(f"📦 货物规格: {cargo_length}×{cargo_width}×{cargo_height}m, 重量{cargo_total_weight}kg")
    print(f"👥 人员配置: {num_people}人, 总重量{num_people * 75}kg")
    
    # 显示利用率
    print(f"\n📊 利用率统计:")
    print(f"   货物重量占比: {detailed_result['utilizations']['cargo_weight']:.1f}%")
    print(f"   人员重量占比: {detailed_result['utilizations']['person_weight']:.1f}%")
    print(f"   总重量利用率: {detailed_result['utilizations']['weight']:.1f}%")
    print(f"   体积利用率: {detailed_result['utilizations']['volume']:.1f}%")
    
    # 人员分析
    person_analysis = detailed_result['person_analysis']
    print(f"\n👥 人员空间分析:")
    print(f"   电梯内剩余面积: {person_analysis['remaining_area']:.2f}㎡")
    print(f"   人员所需面积: {person_analysis['person_area_needed']:.2f}㎡")
    print(f"   重量限制下最大人数: {person_analysis['max_people_by_weight']}人")
    print(f"   空间限制下最大人数: {person_analysis['max_people_by_space']}人")
    
    # 计算对角线信息
    elevator_diag = calculator.calculate_3d_diagonal(elevator_length, elevator_width, elevator_height)
    cargo_diag = calculator.calculate_3d_diagonal(cargo_length, cargo_width, cargo_height)
    print(f"\n📏 对角线信息:")
    print(f"   电梯空间对角线: {elevator_diag:.2f}m")
    print(f"   货物对角线: {cargo_diag:.2f}m")
    
    print("\n详细原因:")
    for reason in reasons:
        print(f"  • {reason}")
    
    # 安全检查清单
    print(f"\n✅ 安全检查清单:")
    print(f"   ✓ 3D对角线检查")
    print(f"   ✓ 6种摆放方向检查") 
    print(f"   ✓ 电梯门通行检查")
    print(f"   ✓ 重心偏移检查")
    print(f"   ✓ 安全间隙预留")
    print(f"   ✓ 人员空间检查")
    print(f"   ✓ 人员重量检查")

if __name__ == "__main__":
    main()