import pandas as pd
import json
import requests  # 确保导入了get_plot依赖的库

# 添加日志打印
print("1. 开始读取movies.csv数据...")
movies = pd.read_csv('/root/autodl-tmp/rag4rec/datarec/ml-32m/movies.csv')  # 注意：这里的路径是否正确？
print(f"成功读取数据，共{len(movies)}部电影，将处理前5000部...")

# 假设get_plot函数已定义（确保API_KEY已替换）
API_KEY = "cd97ea67b15b260cd57fb84edcf530ae"  # 必须替换！
def get_plot(title):
    print(f"正在获取电影《{title}》的剧情简介...")
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    res = requests.get(url).json()
    if res['results']:
        return res['results'][0].get('overview', '')
    return ""

# 批量获取剧情简介
print("2. 开始批量获取电影剧情简介（可能需要几分钟）...")
plots = {title: get_plot(title) for title in movies['title'][:5000]}
print("剧情简介获取完成！")

# 构建知识库
print("3. 开始构建电影知识库...")
kb = []
for idx, (_, row) in enumerate(movies.iloc[:5000].iterrows()):
    if idx % 100 == 0:  # 每处理100部电影打印一次进度
        print(f"已处理{idx}部电影...")
    kb.append({
        'item_id': row['movieId'],
        'title': row['title'],
        'genres': row['genres'],
        'text': f"{row['title']} is a {row['genres']} movie. {plots.get(row['title'], 'No plot available.')}"
    })

# 保存文件（确保data目录存在，不存在则创建）
import os
os.makedirs('../data', exist_ok=True)  # 假设data在上级目录，根据实际路径调整
print("4. 正在保存知识库到data/item_kb.json...")
json.dump(kb, open('../data/item_kb.json', 'w'), indent=2)
print("知识库构建完成！")