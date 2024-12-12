import pandas as pd
from collections import Counter
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def analyze_hashtags(input_file, output_file):
    """
    分析话题标签，统计出现频率最高的50个话题
    """
    try:
        # 读取Excel文件
        logging.info(f"开始读取文件: {input_file}")
        df = pd.read_excel(input_file)
        
        # 检查话题标签列是否存在
        hashtag_column = '话题标签'  # 根据实际列名调整
        if hashtag_column not in df.columns:
            raise ValueError(f"Excel文件中未找到'{hashtag_column}'列")
        
        # 用于存储所有话题
        all_hashtags = []
        
        # 处理每行的话题
        total = len(df)
        for idx, row in enumerate(df[hashtag_column]):
            logging.info(f"正在处理第 {idx+1}/{total} 行的话题")
            
            if pd.isna(row):  # 跳过空值
                continue
                
            # 分割话题并清理
            hashtags = [tag.strip().replace('#', '') for tag in row.split(',')]
            # 添加到列表中
            all_hashtags.extend(hashtags)
        
        # 统计频率
        hashtag_counter = Counter(all_hashtags)
        
        # 获取前50个最常见的话题
        top_50_hashtags = hashtag_counter.most_common(50)
        
        # 写入结果到txt文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("话题标签统计结果 (Top 50):\n")
            f.write("=" * 50 + "\n\n")
            for idx, (tag, count) in enumerate(top_50_hashtags, 1):
                f.write(f"{idx}. #{tag}: {count}次\n")
        
        # 打印统计信息
        logging.info(f"分析完成，结果已保存至: {output_file}")
        logging.info(f"共处理 {total} 行数据")
        logging.info(f"共发现 {len(hashtag_counter)} 个不同话题")
        logging.info("\n频率最高的10个话题:")
        for tag, count in top_50_hashtags[:10]:
            logging.info(f"#{tag}: {count}次")
            
    except Exception as e:
        logging.error(f"处理文件时出错: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/processed_notes.xlsx'
    output_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/top_hashtags.txt'
    
    analyze_hashtags(input_file, output_file) 