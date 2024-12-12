import pandas as pd
import requests
import os
from pathlib import Path
import logging
from urllib.parse import urlparse
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_image(url, save_path):
    """
    下载单个图片
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
        
    except Exception as e:
        logging.error(f"下载图片失败 {url}: {str(e)}")
        return False

def process_images(input_file):
    """
    处理Excel文件并下载符合条件的封面图片
    """
    try:
        # 读取Excel文件
        logging.info(f"开始读取文件: {input_file}")
        df = pd.read_excel(input_file)
        
        # 检查必要的列是否存在
        required_columns = ['粉丝数', '互动量', '封面地址']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Excel文件中未找到'{col}'列")
        
        # 创建保存图片的目录
        save_dir = Path(os.path.dirname(input_file)) / 'cover_images'
        save_dir.mkdir(exist_ok=True)
        
        # 筛选符合条件的数据
        filtered_df = df[
            (df['粉丝数'] < 1000) & 
            (df['互动量'] > 100)
        ]
        
        logging.info(f"找到 {len(filtered_df)} 条符合条件的数据")
        
        # 下载图片
        success_count = 0
        for idx, row in filtered_df.iterrows():
            image_url = row['封面地址']
            if pd.isna(image_url):
                continue
                
            # 从URL中获取文件名，如果没有则使用索引
            url_path = urlparse(image_url).path
            file_name = os.path.basename(url_path)
            if not file_name or '.' not in file_name:
                file_name = f"image_{idx}.jpg"
            
            save_path = save_dir / file_name
            
            logging.info(f"正在下载第 {idx} 个图片: {image_url}")
            
            if download_image(image_url, save_path):
                success_count += 1
                
            # 添加延迟避免请求过快
            time.sleep(1)
        
        # 打印统计信息
        logging.info(f"下载完成！")
        logging.info(f"总共符合条件的数据: {len(filtered_df)}")
        logging.info(f"成功下载图片: {success_count}")
        logging.info(f"图片保存在: {save_dir}")
        
    except Exception as e:
        logging.error(f"处理文件时出错: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/processed_notes.xlsx'
    process_images(input_file) 