#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业数据对标分析 - 可视化模块
功能：生成交互式可视化图表
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Optional
from plotly.subplots import make_subplots


class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self):
        """初始化可视化器"""
        self.chart_count = 0
        
    def create_metrics_comparison(self, companies: List[Dict], metrics: List[str], 
                                  title: str = "核心指标对比") -> str:
        """
        创建核心指标对比图（柱状图/雷达图）
        
        Args:
            companies: 公司数据列表
            metrics: 指标名称列表
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies or not metrics:
            return ""
        
        # 准备数据
        company_names = [c.get('company_name', '未知') for c in companies]
        
        # 创建柱状图
        fig = go.Figure()
        
        for metric in metrics:
            values = [c.get(metric, 0) for c in companies]
            fig.add_trace(go.Bar(
                name=metric,
                x=company_names,
                y=values,
                text=values,
                textposition='auto',
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="公司",
            yaxis_title="数值",
            barmode='group',
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_growth_trend(self, companies: List[Dict], 
                           time_series: Dict[str, List[Dict]],
                           title: str = "增长趋势图") -> str:
        """
        创建增长趋势图（折线图）
        
        Args:
            companies: 公司列表
            time_series: 时间序列数据，格式：{company_name: [{date, value}, ...]}
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies or not time_series:
            return ""
        
        fig = go.Figure()
        
        for company_name, series in time_series.items():
            if not series:
                continue
                
            dates = [s.get('date', '') for s in series]
            values = [s.get('value', 0) for s in series]
            
            fig.add_trace(go.Scatter(
                name=company_name,
                x=dates,
                y=values,
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=8),
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="时间",
            yaxis_title="数值",
            height=500,
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_profit_analysis(self, companies: List[Dict], 
                               title: str = "盈亏分析图") -> str:
        """
        创建盈亏分析图（瀑布图/面积图）
        
        Args:
            companies: 公司数据列表
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies:
            return ""
        
        # 准备数据
        company_names = [c.get('company_name', '未知') for c in companies]
        revenues = [c.get('revenue', 0) for c in companies]
        costs = [c.get('cost', 0) for c in companies]
        profits = [c.get('profit', 0) for c in companies]
        
        # 创建瀑布图
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('收入构成瀑布图', '利润分析瀑布图')
        )
        
        # 收入构成
        fig.add_trace(go.Waterfall(
            name="收入",
            orientation="v",
            x=["总收入"],
            y=[sum(revenues)],
            measure=["absolute"],
            text=[f"¥{sum(revenues)/10000:.1f}亿"],
            textposition="outside"
        ), row=1, col=1)
        
        # 利润分析
        fig.add_trace(go.Waterfall(
            name="利润",
            orientation="v",
            x=["收入", "成本", "利润"],
            y=[sum(revenues), -sum(costs), sum(profits)],
            measure=["relative", "relative", "total"],
            text=[f"+¥{sum(revenues)/10000:.1f}亿", 
                  f"-¥{sum(costs)/10000:.1f}亿",
                  f"¥{sum(profits)/10000:.1f}亿"],
            textposition="outside"
        ), row=1, col=2)
        
        fig.update_layout(
            title=title,
            height=500,
            showlegend=False
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_radar_chart(self, companies: List[Dict], 
                          metrics: List[str],
                          title: str = "雷达图对比") -> str:
        """
        创建雷达图对比
        
        Args:
            companies: 公司数据列表
            metrics: 指标名称列表
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies or not metrics:
            return ""
        
        fig = go.Figure()
        
        for company in companies:
            company_name = company.get('company_name', '未知')
            values = [company.get(metric, 0) for metric in metrics]
            
            fig.add_trace(go.Scatterpolar(
                name=company_name,
                r=values,
                theta=metrics,
                fill='toself'
            ))
        
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([max([c.get(m, 0) for m in metrics]) for c in companies]) * 1.2]
                )),
            showlegend=True,
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_comparison_matrix(self, companies: List[Dict], 
                                x_metric: str, y_metric: str,
                                title: str = "指标矩阵图") -> str:
        """
        创建指标矩阵图（散点图）
        
        Args:
            companies: 公司数据列表
            x_metric: X轴指标
            y_metric: Y轴指标
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies:
            return ""
        
        x_values = [c.get(x_metric, 0) for c in companies]
        y_values = [c.get(y_metric, 0) for c in companies]
        company_names = [c.get('company_name', '未知') for c in companies]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            text=company_names,
            mode='markers+text',
            textposition='top center',
            marker=dict(
                size=12,
                color=list(range(len(companies))),
                colorscale='Viridis',
                showscale=True
            )
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_metric,
            yaxis_title=y_metric,
            height=500,
            hovermode='closest'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_performance_dashboard(self, companies: List[Dict], 
                                    title: str = "经营成果仪表盘") -> str:
        """
        创建经营成果仪表盘（多个图表组合）
        
        Args:
            companies: 公司数据列表
            title: 图表标题
            
        Returns:
            HTML字符串
        """
        if not companies:
            return ""
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "营收对比", "利润率分析", 
                "用户增长", "成本结构"
            ),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        company_names = [c.get('company_name', '未知') for c in companies]
        revenues = [c.get('revenue', 0) for c in companies]
        profits = [c.get('profit', 0) for c in companies]
        users = [c.get('users', 0) for c in companies]
        costs = [c.get('cost', 0) for c in companies]
        
        # 营收对比
        fig.add_trace(go.Bar(
            x=company_names,
            y=revenues,
            name="营收",
            marker_color='lightblue'
        ), row=1, col=1)
        
        # 利润率分析
        profit_rates = [p/r*100 if r > 0 else 0 for r, p in zip(revenues, profits)]
        fig.add_trace(go.Bar(
            x=company_names,
            y=profit_rates,
            name="利润率",
            marker_color='lightgreen'
        ), row=1, col=2)
        
        # 用户增长
        fig.add_trace(go.Bar(
            x=company_names,
            y=users,
            name="用户数",
            marker_color='lightcoral'
        ), row=2, col=1)
        
        # 成本结构
        fig.add_trace(go.Pie(
            labels=['收入', '成本', '利润'],
            values=[sum(revenues), sum(costs), sum(profits)],
            name="成本结构"
        ), row=2, col=2)
        
        fig.update_layout(
            title=title,
            height=800,
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')


def main():
    """主函数 - 测试用"""
    visualizer = DataVisualizer()
    
    # 测试数据
    test_companies = [
        {'company_name': '公司A', 'revenue': 10000, 'cost': 7000, 'profit': 3000, 'users': 50000},
        {'company_name': '公司B', 'revenue': 8000, 'cost': 5500, 'profit': 2500, 'users': 40000},
        {'company_name': '公司C', 'revenue': 12000, 'cost': 8000, 'profit': 4000, 'users': 60000},
    ]
    
    # 测试各个图表
    print("测试核心指标对比图...")
    html1 = visualizer.create_metrics_comparison(
        test_companies, 
        ['revenue', 'profit'],
        "营收与利润对比"
    )
    print(f"生成图表1: {len(html1)} 字符")
    
    print("\n测试增长趋势图...")
    time_series = {
        '公司A': [{'date': '2023-01', 'value': 8000}, {'date': '2023-06', 'value': 10000}],
        '公司B': [{'date': '2023-01', 'value': 6000}, {'date': '2023-06', 'value': 8000}],
    }
    html2 = visualizer.create_growth_trend(test_companies, time_series, "增长趋势")
    print(f"生成图表2: {len(html2)} 字符")
    
    print("\n测试盈亏分析图...")
    html3 = visualizer.create_profit_analysis(test_companies, "盈亏分析")
    print(f"生成图表3: {len(html3)} 字符")
    
    print("\n测试雷达图...")
    html4 = visualizer.create_radar_chart(
        test_companies,
        ['revenue', 'profit', 'users'],
        "指标雷达图"
    )
    print(f"生成图表4: {len(html4)} 字符")
    
    print("\n测试指标矩阵图...")
    html5 = visualizer.create_comparison_matrix(
        test_companies,
        'revenue', 'profit',
        "营收-利润矩阵"
    )
    print(f"生成图表5: {len(html5)} 字符")
    
    print("\n测试经营成果仪表盘...")
    html6 = visualizer.create_performance_dashboard(test_companies, "经营成果仪表盘")
    print(f"生成图表6: {len(html6)} 字符")
    
    print("\n所有测试完成！")


if __name__ == "__main__":
    main()
