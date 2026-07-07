"""
百度新闻首页爬虫
抓取百度新闻首页的所有新闻标题和链接，保存到 news.csv
"""

import requests
from bs4 import BeautifulSoup
import csv

# 请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# CSV 输出文件路径
CSV_FILE = "news.csv"


def fetch_news():
    """抓取百度新闻首页，返回 (标题, 链接) 列表"""
    url = "https://news.baidu.com/"
    try:
        # 发送 GET 请求
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()  # 非 2xx 状态码会抛异常
        resp.encoding = "utf-8"  # 明确指定编码
    except requests.RequestException as e:
        print(f"[错误] 网络请求失败: {e}")
        return []

    # 用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(resp.text, "html.parser")

    news_list = []
    # 百度新闻首页的新闻链接通常在 a 标签中，类名包含 "title" 或位于特定区域
    # 策略：提取所有带 href 的 a 标签，过滤出新闻链接
    for a_tag in soup.find_all("a", href=True):
        title = a_tag.get_text(strip=True)
        href = a_tag["href"]

        # 跳过空标题或过短的文本（非新闻条目）
        if not title or len(title) < 6:
            continue

        # 过滤掉 javascript 链接和锚点链接
        if href.startswith("javascript:") or href.startswith("#"):
            continue

        # 百度新闻的链接可能是相对路径，补全为绝对 URL
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = "https://news.baidu.com" + href

        news_list.append((title, href))

    return news_list


def save_to_csv(news_list):
    """将新闻列表写入 CSV 文件"""
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["标题", "链接"])  # 写表头
        writer.writerows(news_list)
    print(f"[完成] 共抓取 {len(news_list)} 条新闻，已保存到 {CSV_FILE}")


def main():
    print("[开始] 正在抓取百度新闻首页...")
    news = fetch_news()
    if news:
        save_to_csv(news)
        # 打印前 5 条
        print("\n[前5条新闻]")
        for i, (title, link) in enumerate(news[:5], 1):
            print(f"{i}. {title}")
            print(f"   链接: {link}\n")
    else:
        print("[提示] 未抓取到任何新闻。")


if __name__ == "__main__":
    main()
