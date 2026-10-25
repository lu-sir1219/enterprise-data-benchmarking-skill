#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业数据对标分析 - 企业匹配模块
功能：多维度匹配筛选相似企业
"""

import pandas as pd
from typing import List, Dict, Optional
from difflib import SequenceMatcher
import re


class CompanyMatcher:
    """企业相似度匹配器"""
    
    def __init__(self):
        """初始化匹配器"""
        self.industry_data = None
        self.cold_industry_data = None
        
    def load_industry_data(self, industry_file: str = None, 
                          cold_industry_file: str = None) -> None:
        """
        加载行业分类数据
        
        Args:
            industry_file: 行业分类文件路径
            cold_industry_file: 冷门行业分类文件路径
        """
        if industry_file:
            try:
                self.industry_data = pd.read_csv(industry_file)
            except Exception as e:
                print(f"加载行业分类文件失败: {e}")
        
        if cold_industry_file:
            try:
                self.cold_industry_data = pd.read_csv(cold_industry_file)
            except Exception as e:
                print(f"加载冷门行业分类文件失败: {e}")
    
    def calculate_data_similarity(self, user_data: Dict, company_data: Dict) -> float:
        """
        计算数据资源相似度
        
        Args:
            user_data: 用户数据特征
            company_data: 公司数据特征
            
        Returns:
            相似度分数 (0-1)
        """
        if not user_data or not company_data:
            return 0.0
        
        scores = []
        
        # 1. 数据类型相似度
        user_data_types = user_data.get('data_types', [])
        company_data_types = company_data.get('data_types', [])
        
        if user_data_types and company_data_types:
            type_match = self._calculate_list_similarity(user_data_types, company_data_types)
            scores.append(type_match * 0.4)
        
        # 2. 数据规模相似度
        user_scale = user_data.get('data_scale', 0)
        company_scale = company_data.get('data_scale', 0)
        
        if user_scale > 0 and company_scale > 0:
            scale_ratio = min(user_scale, company_scale) / max(user_scale, company_scale)
            scale_score = scale_ratio * 0.3
            scores.append(scale_score)
        
        # 3. 字段相似度
        user_fields = user_data.get('fields', [])
        company_fields = company_data.get('fields', [])
        
        if user_fields and company_fields:
            field_match = self._calculate_list_similarity(user_fields, company_fields)
            scores.append(field_match * 0.3)
        
        return sum(scores) if scores else 0.0
    
    def calculate_business_similarity(self, user_business: Dict, company_business: Dict) -> float:
        """
        计算业务模式相似度
        
        Args:
            user_business: 用户业务特征
            company_business: 公司业务特征
            
        Returns:
            相似度分数 (0-1)
        """
        if not user_business or not company_business:
            return 0.0
        
        scores = []
        
        # 1. 行业相似度
        user_industry = user_business.get('industry', '')
        company_industry = company_business.get('industry', '')
        
        if user_industry and company_industry:
            industry_match = self._calculate_industry_similarity(user_industry, company_industry)
            scores.append(industry_match * 0.5)
        
        # 2. 业务模式相似度
        user_model = user_business.get('business_model', '')
        company_model = company_business.get('business_model', '')
        
        if user_model and company_model:
            model_match = self._calculate_text_similarity(user_model, company_model)
            scores.append(model_match * 0.3)
        
        # 3. 规模相似度
        user_size = user_business.get('company_size', '')
        company_size = company_business.get('company_size', '')
        
        if user_size and company_size:
            size_match = self._calculate_size_similarity(user_size, company_size)
            scores.append(size_match * 0.2)
        
        return sum(scores) if scores else 0.0
    
    def calculate_size_similarity(self, user_size: str, company_size: str) -> float:
        """
        计算规模相似度
        
        Args:
            user_size: 用户公司规模
            company_size: 公司规模
            
        Returns:
            相似度分数 (0-1)
        """
        if not user_size or not company_size:
            return 0.0
        
        # 规模等级映射
        size_levels = {
            '小型': 1,
            '中型': 2,
            '大型': 3,
            '超大型': 4
        }
        
        user_level = size_levels.get(user_size, 0)
        company_level = size_levels.get(company_size, 0)
        
        if user_level == 0 or company_level == 0:
            return 0.5
        
        level_diff = abs(user_level - company_level)
        score = max(0, 1 - level_diff * 0.3)
        
        return score
    
    def calculate_pain_point_similarity(self, user_pains: List[str], 
                                       company_pains: List[str]) -> float:
        """
        计算痛点相似度
        
        Args:
            user_pains: 用户痛点列表
            company_pains: 公司痛点列表
            
        Returns:
            相似度分数 (0-1)
        """
        if not user_pains or not company_pains:
            return 0.0
        
        # 计算共同痛点数量
        common_pains = set(user_pains) & set(company_pains)
        total_pains = set(user_pains) | set(company_pains)
        
        if not total_pains:
            return 0.0
        
        similarity = len(common_pains) / len(total_pains)
        
        return similarity
    
    def _calculate_list_similarity(self, list1: List, list2: List) -> float:
        """
        计算列表相似度（Jaccard相似度）
        
        Args:
            list1: 列表1
            list2: 列表2
            
        Returns:
            相似度分数 (0-1)
        """
        if not list1 or not list2:
            return 0.0
        
        set1 = set(str(item).lower().strip() for item in list1)
        set2 = set(str(item).lower().strip() for item in list2)
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数 (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        # 使用 SequenceMatcher 计算相似度
        similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        return similarity
    
    def _calculate_industry_similarity(self, industry1: str, industry2: str) -> float:
        """
        计算行业相似度
        
        Args:
            industry1: 行业1
            industry2: 行业2
            
        Returns:
            相似度分数 (0-1)
        """
        if not industry1 or not industry2:
            return 0.0
        
        # 直接匹配
        if industry1.lower() == industry2.lower():
            return 1.0
        
        # 部分匹配
        if industry1.lower() in industry2.lower() or industry2.lower() in industry1.lower():
            return 0.8
        
        # 使用文本相似度
        return self._calculate_text_similarity(industry1, industry2)
    
    def calculate_overall_similarity(self, user_data: Dict, company_data: Dict) -> Dict:
        """
        计算综合相似度
        
        Args:
            user_data: 用户数据特征
            company_data: 公司数据特征
            
        Returns:
            包含各项相似度分数和综合分数的字典
        """
        # 计算各项相似度
        data_similarity = self.calculate_data_similarity(user_data, company_data)
        business_similarity = self.calculate_business_similarity(user_data, company_data)
        size_similarity = self.calculate_size_similarity(
            user_data.get('company_size', ''), 
            company_data.get('company_size', '')
        )
        pain_similarity = self.calculate_pain_point_similarity(
            user_data.get('pain_points', []),
            company_data.get('pain_points', [])
        )
        
        # 计算综合分数（加权平均）
        weights = {
            'data': 0.35,
            'business': 0.35,
            'size': 0.15,
            'pain': 0.15
        }
        
        overall = (
            data_similarity * weights['data'] +
            business_similarity * weights['business'] +
            size_similarity * weights['size'] +
            pain_similarity * weights['pain']
        )
        
        return {
            'data_similarity': round(data_similarity, 3),
            'business_similarity': round(business_similarity, 3),
            'size_similarity': round(size_similarity, 3),
            'pain_similarity': round(pain_similarity, 3),
            'overall_similarity': round(overall, 3),
            'weights': weights
        }
    
    def match_companies(self, user_data: Dict, candidates: List[Dict], 
                       top_n: int = 10) -> List[Dict]:
        """
        匹配最相似的企业
        
        Args:
            user_data: 用户数据特征
            candidates: 候选企业列表
            top_n: 返回前N个
            
        Returns:
            匹配结果列表（按相似度排序）
        """
        if not candidates:
            return []
        
        # 计算每个候选企业的相似度
        results = []
        for company in candidates:
            similarity = self.calculate_overall_similarity(user_data, company)
            results.append({
                'company_data': company,
                'similarity': similarity
            })
        
        # 按综合相似度排序
        results.sort(key=lambda x: x['similarity']['overall_similarity'], reverse=True)
        
        # 返回前N个
        return results[:top_n]
    
    def filter_by_threshold(self, results: List[Dict], threshold: float = 0.5) -> List[Dict]:
        """
        按相似度阈值过滤结果
        
        Args:
            results: 匹配结果列表
            threshold: 相似度阈值
            
        Returns:
            过滤后的结果列表
        """
        return [r for r in results if r['similarity']['overall_similarity'] >= threshold]


def main():
    """主函数 - 测试用"""
    matcher = CompanyMatcher()
    
    # 测试数据
    user_data = {
        'data_types': ['用户行为', '交易数据', '运营数据'],
        'data_scale': 1000000,
        'fields': ['user_id', 'pay_amount', 'order_date', 'product_id'],
        'industry': '综合电商',
        'business_model': '平台模式',
        'company_size': '大型',
        'pain_points': ['用户留存率低', '转化率不高', '数据孤岛']
    }
    
    candidates = [
        {
            'company_name': '公司A',
            'data_types': ['用户行为', '交易数据'],
            'data_scale': 800000,
            'fields': ['user_id', 'pay_amount', 'order_date'],
            'industry': '综合电商',
            'business_model': '平台模式',
            'company_size': '大型',
            'pain_points': ['用户留存率低', '转化率不高']
        },
        {
            'company_name': '公司B',
            'data_types': ['用户行为', '交易数据', '库存数据'],
            'data_scale': 1200000,
            'fields': ['user_id', 'pay_amount', 'order_date', 'product_id', 'stock'],
            'industry': '综合电商',
            'business_model': '平台模式',
            'company_size': '大型',
            'pain_points': ['用户留存率低', '数据孤岛']
        },
        {
            'company_name': '公司C',
            'data_types': ['社交数据', '内容数据'],
            'data_scale': 5000000,
            'fields': ['user_id', 'post_id', 'comment_id'],
            'industry': '社交',
            'business_model': '广告模式',
            'company_size': '超大型',
            'pain_points': ['内容审核压力大']
        }
    ]
    
    print("测试企业匹配...")
    results = matcher.match_companies(user_data, candidates, top_n=3)
    
    print(f"\n找到 {len(results)} 个匹配企业:")
    for i, result in enumerate(results, 1):
        company = result['company_data']['company_name']
        sim = result['similarity']
        
        print(f"\n{i}. {company}")
        print(f"   综合相似度: {sim['overall_similarity']}")
        print(f"   数据相似度: {sim['data_similarity']}")
        print(f"   业务相似度: {sim['business_similarity']}")
        print(f"   规模相似度: {sim['size_similarity']}")
        print(f"   痛点相似度: {sim['pain_similarity']}")


if __name__ == "__main__":
    main()
