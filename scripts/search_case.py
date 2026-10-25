#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业数据对标分析 - 联网搜索模块
功能：搜索同行业高相似度企业案例
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from urllib.parse import quote


class CaseSearcher:
    """企业案例搜索器"""
    
    def __init__(self):
        """初始化搜索器"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_results = []
        
    def search_company_cases(self, company_name: str, industry: str) -> List[Dict]:
        """
        搜索企业案例
        
        Args:
            company_name: 企业名称
            industry: 所属行业
            
        Returns:
            案例列表
        """
        cases = []
        
        # 构建搜索关键词
        search_keywords = [
            f"{company_name} 数据应用 成功案例",
            f"{company_name} 数字化转型 经营成果",
            f"{company_name} 行业报告 数据驱动",
            f"{company_name} {industry} 案例",
            f"{company_name} 商业模式 数据"
        ]
        
        for keyword in search_keywords:
            try:
                results = self._search_baidu(keyword)
                cases.extend(results)
            except Exception as e:
                print(f"搜索关键词 '{keyword}' 失败: {e}")
                continue
        
        return cases
    
    def _search_baidu(self, keyword: str, num_results: int = 5) -> List[Dict]:
        """
        使用百度搜索
        
        Args:
            keyword: 搜索关键词
            num_results: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        results = []
        
        # 百度搜索URL
        search_url = f"https://www.baidu.com/s?wd={quote(keyword)}&rn={num_results}"
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取搜索结果
                for item in soup.find_all('div', class_='result c-container')[:num_results]:
                    result = self._parse_search_result(item, keyword)
                    if result:
                        results.append(result)
                        
        except Exception as e:
            print(f"搜索失败: {e}")
            
        return results
    
    def _parse_search_result(self, item: BeautifulSoup, keyword: str) -> Optional[Dict]:
        """
        解析搜索结果
        
        Args:
            item: 搜索结果HTML元素
            keyword: 搜索关键词
            
        Returns:
            解析后的结果字典
        """
        try:
            # 提取标题
            title_elem = item.find('h3')
            if not title_elem:
                return None
                
            title = title_elem.get_text().strip()
            title_link = title_elem.find('a')
            url = title_link.get('href', '') if title_link else ''
            
            # 提取摘要
            abstract_elem = item.find('div', class_='c-abstract')
            abstract = abstract_elem.get_text().strip() if abstract_elem else ''
            
            # 提取更多摘要
            if not abstract:
                abstract_elem = item.find('span', class_='c-span')
                abstract = abstract_elem.get_text().strip() if abstract_elem else ''
            
            return {
                'title': title,
                'url': url,
                'abstract': abstract,
                'keyword': keyword,
                'content': ''
            }
            
        except Exception as e:
            print(f"解析搜索结果失败: {e}")
            return None
    
    def fetch_page_content(self, url: str) -> str:
        """
        获取网页内容
        
        Args:
            url: 网页URL
            
        Returns:
            网页文本内容
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 移除脚本和样式
                for script in soup(['script', 'style']):
                    script.decompose()
                    
                # 获取文本
                text = soup.get_text()
                
                # 清理文本
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:5000]  # 限制长度
                
        except Exception as e:
            print(f"获取网页内容失败: {e}")
            
        return ''
    
    def extract_case_info(self, content: str, company_name: str) -> Dict:
        """
        从网页内容中提取案例信息
        
        Args:
            content: 网页内容
            company_name: 企业名称
            
        Returns:
            提取的案例信息
        """
        case_info = {
            'company_name': company_name,
            'data_usage': '',
            'business_model': '',
            'key_actions': [],
            'performance': '',
            'success_factors': []
        }
        
        # 提取数据使用相关描述
        data_patterns = [
            r'(数据应用|数据资源|数据处理|数据驱动|数字化转型).{0,100}',
            r'(大数据|数据分析|数据挖掘|数据仓库).{0,100}',
            r'(用户行为|交易数据|库存数据|运营数据).{0,100}'
        ]
        
        for pattern in data_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                case_info['data_usage'] = '；'.join(matches[:3])
                break
        
        # 提取盈利模式相关描述
        model_patterns = [
            r'(商业模式|盈利模式|收入来源|成本结构).{0,100}',
            r'(营收|利润|增长率|ROI).{0,100}'
        ]
        
        for pattern in model_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                case_info['business_model'] = '；'.join(matches[:3])
                break
        
        # 提取关键动作
        action_patterns = [
            r'(实施|采取|引入|建设|开发).{0,50}(系统|平台|机制|策略|方案)',
            r'(优化|提升|改善|增强).{0,50}(效率|效果|性能|指标)'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                case_info['key_actions'] = [m[0] + m[1] for m in matches[:5]]
                break
        
        # 提取经营成果
        performance_patterns = [
            r'(营收|利润|用户数|增长率|复购率).{0,30}([0-9]+[%]?)',
            r'(提升|增长|提高).{0,30}([0-9]+[%]?)'
        ]
        
        for pattern in performance_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                case_info['performance'] = '；'.join([str(m) for m in matches[:5]])
                break
        
        # 提取成功因素
        factor_patterns = [
            r'(成功|关键|核心|重要).{0,50}(因素|原因|策略|方法)',
            r'(因为|由于|得益于).{0,50}(数据|技术|模式|创新)'
        ]
        
        for pattern in factor_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                case_info['success_factors'] = [m[0] + m[1] for m in matches[:5]]
                break
        
        return case_info
    
    def search_industry_cases(self, industry: str, num_cases: int = 10) -> List[Dict]:
        """
        搜索行业案例
        
        Args:
            industry: 行业名称
            num_cases: 案例数量
            
        Returns:
            案例列表
        """
        cases = []
        
        # 行业搜索关键词
        search_keywords = [
            f"{industry} 成功案例",
            f"{industry} 数字化转型",
            f"{industry} 数据应用",
            f"{industry} 商业模式创新"
        ]
        
        for keyword in search_keywords:
            try:
                results = self._search_baidu(keyword, num_results=num_cases // 4 + 1)
                
                for result in results:
                    # 获取网页内容
                    content = self.fetch_page_content(result['url'])
                    result['content'] = content
                    
                    # 提取案例信息
                    case_info = self.extract_case_info(content, '行业案例')
                    result['case_info'] = case_info
                    
                    cases.append(result)
                    
            except Exception as e:
                print(f"搜索行业 '{industry}' 失败: {e}")
                continue
            
            if len(cases) >= num_cases:
                break
        
        return cases[:num_cases]


def main():
    """主函数 - 测试用"""
    searcher = CaseSearcher()
    
    # 测试搜索
    company = "小米"
    industry = "电子制造"
    
    print(f"搜索公司 '{company}' 的案例...")
    cases = searcher.search_company_cases(company, industry)
    
    print(f"\n找到 {len(cases)} 个案例:")
    for i, case in enumerate(cases, 1):
        print(f"\n{i}. {case['title']}")
        print(f"   URL: {case['url']}")
        print(f"   摘要: {case['abstract'][:100]}...")
        
        # 获取网页内容
        if case['url']:
            content = searcher.fetch_page_content(case['url'])
            case_info = searcher.extract_case_info(content, company)
            print(f"   数据使用: {case_info['data_usage'][:100]}...")


if __name__ == "__main__":
    main()
