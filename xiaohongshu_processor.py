import pandas as pd
from bs4 import BeautifulSoup
import requests
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_note(url, headers):
    """
    抓取单个小红书笔记的详情和话题
    """
    try:
        # 添加随机延迟避免被封
        time.sleep(2)
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取笔记详情
        detail_elem = soup.find(id='detail-desc')
        detail = detail_elem.text.strip() if detail_elem else ''
        
        # 获取话题标签
        hashtags = []
        hashtag_elems = soup.find_all(id='hash-tag')
        for elem in hashtag_elems:
            hashtags.append(elem.text.strip())
        
        return detail, ','.join(hashtags)
        
    except Exception as e:
        logging.error(f"处理URL时出错: {url}")
        logging.error(f"错误信息: {str(e)}")
        return '', ''

def process_xiaohongshu_notes(input_path, output_path, headers):
    """
    处理小红书笔记Excel文件
    """
    try:
        # 读取Excel文件
        logging.info(f"开始读取文件: {input_path}")
        df = pd.read_excel(input_path)
        
        # 获取URL列名(第一列)
        url_column = df.columns[0]
        
        # 创建新列存储结果
        df['笔记详情'] = ''
        df['笔记话题'] = ''
        
        # 处理每个URL
        total = len(df)
        for idx, url in enumerate(df[url_column]):
            logging.info(f"正在处理第 {idx+1}/{total} 个URL: {url}")
            
            detail, hashtags = scrape_note(url, headers)
            df.at[idx, '笔记详情'] = detail
            df.at[idx, '笔记话题'] = hashtags
        
        # 保存结果
        logging.info(f"正在保存结果到: {output_path}")
        df.to_excel(output_path, index=False)
        logging.info("处理完成!")
        
    except Exception as e:
        logging.error(f"处理Excel文件时出错: {str(e)}")

if __name__ == "__main__":
    # 配置请求头
    headers = {
        'Cookie': 'abRequestId=0ddc1356-0953-5904-9366-717ee77f8d3b; webBuild=4.46.0; xsecappid=xhs-pc-web; a1=193b12b735ds6ibomoul8zwrwclkgzcm2c4fr662330000321116; webId=788f61cfe35688f5ddb2ff5d089c4400; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; sec_poison_id=65486042-9365-401c-92fe-1e206ffb1843; acw_tc=0a4ad2fc17338442361687947e8e5d5c83787f281555795aa91fb468e60ec9; unread={%22ub%22:%22641fd40f0000000013001f44%22%2C%22ue%22:%2263db829c000000000d014eb1%22%2C%22uc%22:20}; web_session=030037a06b097830d012401b20204a66298f16; gid=yjqDyJDW0iJYyjqDyJDWqSKK2fMK3Dl6l71Y4JquEFES1iq8TkuS6F888qJyyyK8Si2i24qS',  # 替换为实际的cookie
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    input_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/xiaohongshu.xlsx'
    output_file = '/Users/liyihang/Downloads/cursortest/xiaohongshu/xiaohongshu_processed.xlsx'
    
    process_xiaohongshu_notes(input_file, output_file, headers) 