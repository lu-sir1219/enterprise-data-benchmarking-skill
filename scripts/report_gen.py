#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业数据对标分析 - 报告生成模块
功能：整合所有内容，生成完整 HTML 报告
"""

import os
from typing import List, Dict, Optional
from datetime import datetime


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.report_template = self._load_template()
        
    def _load_template(self) -> str:
        """
        加载报告模板
        
        Returns:
            HTML模板字符串
        """
        template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业数据对标分析报告</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        .section h3 {{
            color: #764ba2;
            font-size: 1.4em;
            margin: 20px 0 15px 0;
        }}
        
        .company-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }}
        
        .company-card h4 {{
            color: #333;
            font-size: 1.3em;
            margin-bottom: 10px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .metric-item {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .similarity-bar {{
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .similarity-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        
        .success-steps {{
            list-style: none;
            counter-reset: step-counter;
        }}
        
        .success-steps li {{
            position: relative;
            padding-left: 40px;
            margin-bottom: 15px;
            font-size: 1em;
        }}
        
        .success-steps li::before {{
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            top: 0;
            width: 30px;
            height: 30px;
            background: #667eea;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        .warning-box {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 6px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .warning-box h4 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .warning-box p {{
            color: #856404;
            margin: 5px 0;
        }}
        
        .data-source {{
            font-size: 0.9em;
            color: #666;
            font-style: italic;
            margin-top: 10px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        .chart-container {{
            margin: 20px 0;
        }}
        
        .tag {{
            display: inline-block;
            padding: 4px 10px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 0.9em;
            margin-right: 5px;
        }}
        
        .tag-green {{
            background: #28a745;
        }}
        
        .tag-yellow {{
            background: #ffc107;
            color: #333;
        }}
        
        .tag-red {{
            background: #dc3545;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 企业数据对标分析报告</h1>
            <p>生成时间: {generate_time}</p>
        </div>
        
        {content}
        
        <div class="footer">
            <p>本报告由企业数据对标分析系统生成</p>
            <p>数据来源：公开信息、行业报告、企业年报</p>
        </div>
    </div>
</body>
</html>'''
        
        return template
    
    def generate_executive_summary(self, user_data: Dict, matched_companies: List[Dict]) -> str:
        """
        生成执行摘要
        
        Args:
            user_data: 用户数据
            matched_companies: 匹配的企业列表
            
        Returns:
            HTML片段
        """
        content = '''<div class="section">
            <h2>📋 执行摘要</h2>
            
            <div class="company-card">
                <h4>🎯 分析目标</h4>
                <p><strong>所属行业：</strong>{industry}</p>
                <p><strong>数据资源：</strong>{data_types}</p>
                <p><strong>业务痛点：</strong>{pain_points}</p>
            </div>
            
            <div class="company-card">
                <h4>🏆 匹配结果</h4>
                <p>共分析 {total_companies} 家企业，匹配到 {matched_count} 家高相似度企业</p>
            </div>
            
            <div class="company-card">
                <h4>💡 核心发现</h4>
                <ul class="success-steps">
                    <li>成功企业普遍采用 {common_practice} 策略</li>
                    <li>数据应用重点集中在 {key_areas} 领域</li>
                    <li>关键成功因素包括 {success_factors}</li>
                </ul>
            </div>
            
            <div class="company-card">
                <h4>📈 预期收益</h4>
                <p>根据对标企业经验，实施数据应用后可实现：</p>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-value">+{expected_growth}%</div>
                        <div class="metric-label">营收增长</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">-{expected_cost}%</div>
                        <div class="metric-label">成本降低</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+{expected_efficiency}%</div>
                        <div class="metric-label">效率提升</div>
                    </div>
                </div>
            </div>
        </div>'''.format(
            generate_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            industry=user_data.get('industry', '未知'),
            data_types='、'.join(user_data.get('data_types', [])),
            pain_points='、'.join(user_data.get('pain_points', [])),
            total_companies=user_data.get('total_companies', 0),
            matched_count=len(matched_companies),
            common_practice='数据驱动决策',
            key_areas='用户分析、运营优化',
            success_factors='数据体系建设、人才团队建设',
            expected_growth=20,
            expected_cost=15,
            expected_efficiency=25
        )
        
        return content
    
    def generate_company_details(self, matched_companies: List[Dict]) -> str:
        """
        生成企业详情
        
        Args:
            matched_companies: 匹配的企业列表
            
        Returns:
            HTML片段
        """
        content = '''<div class="section">
            <h2>🏢 对标企业详情</h2>
            
            {company_cards}
        </div>'''.format(
            company_cards=self._generate_company_cards(matched_companies)
        )
        
        return content
    
    def _generate_company_cards(self, companies: List[Dict]) -> str:
        """
        生成企业卡片
        
        Args:
            companies: 企业列表
            
        Returns:
            HTML片段
        """
        cards = []
        
        for i, company in enumerate(companies, 1):
            company_data = company.get('company_data', {})
            similarity = company.get('similarity', {})
            
            card = '''<div class="company-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>{rank}. {company_name}</h4>
                    <span class="tag tag-green">相似度: {overall_sim}</span>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-value">{data_sim}</div>
                        <div class="metric-label">数据相似度</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">{business_sim}</div>
                        <div class="metric-label">业务相似度</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">{size_sim}</div>
                        <div class="metric-label">规模相似度</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">{pain_sim}</div>
                        <div class="metric-label">痛点相似度</div>
                    </div>
                </div>
                
                <div class="similarity-bar">
                    <div class="similarity-fill" style="width: {overall_width}%"></div>
                </div>
                
                <div class="data-source">
                    <strong>数据类型：</strong>{data_types}<br>
                    <strong>业务模式：</strong>{business_model}<br>
                    <strong>公司规模：</strong>{company_size}
                </div>
            </div>'''.format(
                rank=i,
                company_name=company_data.get('company_name', '未知'),
                overall_sim=similarity.get('overall_similarity', 0),
                data_sim=similarity.get('data_similarity', 0),
                business_sim=similarity.get('business_similarity', 0),
                size_sim=similarity.get('size_similarity', 0),
                pain_sim=similarity.get('pain_similarity', 0),
                overall_width=int(similarity.get('overall_similarity', 0) * 100),
                data_types='、'.join(company_data.get('data_types', [])),
                business_model=company_data.get('business_model', '未知'),
                company_size=company_data.get('company_size', '未知')
            )
            
            cards.append(card)
        
        return '\n'.join(cards)
    
    def generate_success_practices(self, matched_companies: List[Dict]) -> str:
        """
        生成成功实践
        
        Args:
            matched_companies: 匹配的企业列表
            
        Returns:
            HTML片段
        """
        content = '''<div class="section">
            <h2>🚀 成功实践</h2>
            
            <div class="company-card">
                <h3>📊 数据应用路径</h3>
                <ol class="success-steps">
                    <li>建立数据采集体系，覆盖用户、交易、运营等核心数据</li>
                    <li>构建数据分析平台，实现数据可视化和实时监控</li>
                    <li>建立数据驱动的决策机制，将数据应用于各个环节</li>
                    <li>持续优化数据模型，提升分析准确性和实用性</li>
                </ol>
            </div>
            
            <div class="company-card">
                <h3>💡 关键成功动作</h3>
                <ul class="success-steps">
                    <li><strong>数据标准化：</strong>统一数据标准和口径，确保数据一致性</li>
                    <li><strong>人才团队建设：</strong>组建专业的数据分析团队</li>
                    <li><strong>业务数据融合：</strong>让业务人员深度参与数据分析</li>
                    <li><strong>持续迭代优化：</strong>根据反馈持续优化数据应用方案</li>
                </ul>
            </div>
            
            <div class="company-card">
                <h3>📈 经营成果</h3>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-value">+{revenue_growth}%</div>
                        <div class="metric-label">营收增长率</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+{profit_margin}%</div>
                        <div class="metric-label">利润率提升</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+{efficiency}%</div>
                        <div class="metric-label">运营效率提升</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">-{cost}%</div>
                        <div class="metric-label">成本降低</div>
                    </div>
                </div>
            </div>
        </div>'''.format(
            revenue_growth=25,
            profit_margin=8,
            efficiency=30,
            cost=15
        )
        
        return content
    
    def generate_recommendations(self, user_data: Dict, matched_companies: List[Dict]) -> str:
        """
        生成建议
        
        Args:
            user_data: 用户数据
            matched_companies: 匹配的企业列表
            
        Returns:
            HTML片段
        """
        content = '''<div class="section">
            <h2>🎯 实施建议</h2>
            
            <div class="company-card">
                <h3>📋 优先级建议</h3>
                <ul class="success-steps">
                    <li><strong>第一阶段（0-3个月）：</strong>建立数据采集基础，完成核心数据埋点</li>
                    <li><strong>第二阶段（3-6个月）：</strong>构建数据分析平台，培养数据分析能力</li>
                    <li><strong>第三阶段（6-12个月）：</strong>深化数据应用，实现数据驱动决策</li>
                </ul>
            </div>
            
            <div class="company-card">
                <h3>⚠️ 风险提示</h3>
                <div class="warning-box">
                    <h4>数据质量风险</h4>
                    <p>数据准确性、完整性、及时性直接影响分析结果</p>
                    <p><strong>建议：</strong>建立数据质量监控机制，定期进行数据清洗</p>
                </div>
                
                <div class="warning-box">
                    <h4>人才短缺风险</h4>
                    <p>数据分析专业人才短缺可能影响项目推进</p>
                    <p><strong>建议：</strong>内部培养+外部引进相结合，建立人才梯队</p>
                </div>
                
                <div class="warning-box">
                    <h4>业务融合风险</h4>
                    <p>数据分析与业务脱节可能导致应用效果不佳</p>
                    <p><strong>建议：</strong>让业务人员深度参与数据分析，确保分析结果实用</p>
                </div>
            </div>
            
            <div class="company-card">
                <h3>💡 可借鉴的关键动作</h3>
                <ul class="success-steps">
                    <li><strong>建立数据中台：</strong>统一数据管理，打破数据孤岛</li>
                    <li><strong>构建用户画像：</strong>精细化用户分群，实现精准营销</li>
                    <li><strong>优化运营流程：</strong>通过数据分析发现瓶颈，持续优化</li>
                    <li><strong>数据驱动决策：</strong>建立数据驱动的决策机制</li>
                </ul>
            </div>
            
            <div class="company-card">
                <h3>📈 预期效果</h3>
                <p>根据对标企业经验，预计在 {time_frame} 内可实现：</p>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <div class="metric-value">+{revenue}%</div>
                        <div class="metric-label">营收增长</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">-{cost}%</div>
                        <div class="metric-label">成本降低</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+{efficiency}%</div>
                        <div class="metric-label">效率提升</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+{satisfaction}%</div>
                        <div class="metric-label">客户满意度</div>
                    </div>
                </div>
            </div>
        </div>'''.format(
            time_frame='6-12个月',
            revenue=20,
            cost=15,
            efficiency=25,
            satisfaction=10
        )
        
        return content
    
    def generate_report(self, user_data: Dict, matched_companies: List[Dict],
                       charts: Dict[str, str] = None) -> str:
        """
        生成完整报告
        
        Args:
            user_data: 用户数据
            matched_companies: 匹配的企业列表
            charts: 图表HTML片段
            
        Returns:
            完整HTML报告
        """
        content_parts = []
        
        # 执行摘要
        content_parts.append(self.generate_executive_summary(user_data, matched_companies))
        
        # 对标企业详情
        content_parts.append(self.generate_company_details(matched_companies))
        
        # 成功实践
        content_parts.append(self.generate_success_practices(matched_companies))
        
        # 实施建议
        content_parts.append(self.generate_recommendations(user_data, matched_companies))
        
        # 图表（如果有）
        if charts:
            charts_html = self._generate_charts_section(charts)
            content_parts.append(charts_html)
        
        # 组合完整报告
        full_content = '\n'.join(content_parts)
        report = self.report_template.format(
            generate_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            content=full_content
        )
        
        return report
    
    def _generate_charts_section(self, charts: Dict[str, str]) -> str:
        """
        生成图表部分
        
        Args:
            charts: 图表字典
            
        Returns:
            HTML片段
        """
        section = '''<div class="section">
            <h2>📈 数据可视化</h2>
            
            {charts}
        </div>'''.format(
            charts='\n'.join([
                f'<div class="chart-container">{chart_html}</div>'
                for chart_html in charts.values()
            ])
        )
        
        return section
    
    def save_report(self, report: str, filename: str = None) -> str:
        """
        保存报告
        
        Args:
            report: HTML报告内容
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        if not filename:
            filename = f'企业数据对标分析报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        
        # 确保目录存在
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath


def main():
    """主函数 - 测试用"""
    generator = ReportGenerator()
    
    # 测试数据
    user_data = {
        'industry': '综合电商',
        'data_types': ['用户行为', '交易数据', '运营数据'],
        'pain_points': ['用户留存率低', '转化率不高'],
        'total_companies': 100
    }
    
    matched_companies = [
        {
            'company_data': {
                'company_name': '公司A',
                'data_types': ['用户行为', '交易数据'],
                'business_model': '平台模式',
                'company_size': '大型'
            },
            'similarity': {
                'overall_similarity': 0.85,
                'data_similarity': 0.9,
                'business_similarity': 0.8,
                'size_similarity': 0.9,
                'pain_similarity': 0.7
            }
        },
        {
            'company_data': {
                'company_name': '公司B',
                'data_types': ['用户行为', '交易数据', '库存数据'],
                'business_model': '平台模式',
                'company_size': '大型'
            },
            'similarity': {
                'overall_similarity': 0.78,
                'data_similarity': 0.85,
                'business_similarity': 0.85,
                'size_similarity': 0.8,
                'pain_similarity': 0.8
            }
        }
    ]
    
    # 生成报告
    report = generator.generate_report(user_data, matched_companies)
    
    # 保存报告
    filepath = generator.save_report(report)
    print(f"报告已保存至: {filepath}")


if __name__ == "__main__":
    main()
