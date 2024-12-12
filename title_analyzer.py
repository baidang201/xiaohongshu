import pandas as pd
import jieba
import jieba.analyse
from collections import defaultdict
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def analyze_titles(input_file, output_file):
    """
    分析笔记标题，统计关键词频率并输出结果
    """
    try:
        # 读取Excel文件
        logging.info(f"开始读取文件: {input_file}")
        df = pd.read_excel(input_file)
        
        # 检查是否存在"笔记标题"列
        if '笔记标题' not in df.columns:
            raise ValueError("Excel文件中未找到'笔记标题'列")
        
        # 用于存储关键词到原标题的映射
        keyword_titles = defaultdict(list)
        # 用于存储关键词频率
        keyword_counts = defaultdict(int)
        
        # 处理每个标题
        total = len(df)
        for idx, title in enumerate(df['笔记标题']):
            if pd.isna(title):  # 跳过空标题
                continue
                
            logging.info(f"正在处理第 {idx+1}/{total} 个标题")
            
            # 提取关键词（取TOP3关键词）
            keywords = jieba.analyse.extract_tags(title, topK=3)
            
            # 更新统计信息
            for keyword in keywords:
                keyword_counts[keyword] += 1
                if title not in keyword_titles[keyword]:
                    keyword_titles[keyword].append(title)
        
        # 按频率排序
        sorted_keywords = sorted(keyword_counts.items(), 
                               key=lambda x: x[1], 
                               reverse=True)
        
        # 准备输出数据
        output_data = []
        for keyword, count in sorted_keywords:
            output_data.append({
                '关键词': keyword,
                '出现次数': count,
                '相关标题': '\n'.join(keyword_titles[keyword])
            })
        
        # 创建输出DataFrame并保存
        output_df = pd.DataFrame(output_data)
        output_df.to_excel(output_file, index=False)
        
        logging.info(f"分析完成，结果已保存至: {output_file}")
        
        # 打印一些统计信息
        logging.info(f"共处理标题 {total} 个")
        logging.info(f"提取关键词 {len(sorted_keywords)} 个")
        logging.info("\n频率最高的10个关键词:")
        for keyword, count in sorted_keywords[:10]:
            logging.info(f"{keyword}: {count}次")
            
    except Exception as e:
        logging.error(f"处理文件时出错: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/processed_notes.xlsx'
    output_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/title_analysis.xlsx'
    
    analyze_titles(input_file, output_file) 