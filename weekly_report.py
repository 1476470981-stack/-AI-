"""
自动周报生成器 v0.1
- 输入：交互式问答（4 个问题）
- 处理：调 DeepSeek API，用周报 Prompt 模板
- 输出：把周报存到 Markdown 文件
"""

import os
import sys
from datetime import datetime
from openai import OpenAI

# 1. 读 API Key（从环境变量）
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("❌ 没找到 DEEPSEEK_API_KEY 环境变量")
    print("👉 请先在 PowerShell 里运行：")
    print('   $env:DEEPSEEK_API_KEY="sk-你的key"')
    sys.exit(1)

# 2. 交互式问答
print("=" * 50)
print("🤖 自动周报生成器 v0.1")
print("=" * 50)
print("\n我会问你 4 个问题，你回答就行。\n")

done = input("📝 本周完成的事情（多件用 ; 分隔）：")
clients = input("👥 见过的客户：")
data = input("📊 关键数据（销量/吨数/客单价）：")
problems = input("⚠️ 遇到的问题：")

# 3. 构建 Prompt
done_list = "\n".join([f"- {item.strip()}" for item in done.split(";") if item.strip()])

prompt = f"""你是化工/食品行业的资深销售助理。请帮销售员写一份给老板的周报。

【销售员本周输入】
- 本周完成的事情：
{done_list}
- 见过的客户：{clients}
- 关键数据：{data}
- 遇到的问题：{problems}

【写作要求】
1. 按"成果 + 数据 + 下周计划"三段式结构
2. 数据按吨位呈现，算 3 年均值（如果适用）
3. 简洁列表优先，不用长段落
4. 突出执行结果，不堆砌过程

【输出格式】
# 本周工作汇报
## 一、本周成果（按重要性排序）
- [数据/事实] + [对应的意义]
## 二、关键数据
- 销量：__ 吨
- 新增客户：__ 家
- 客单价：__ 元/kg
## 三、遇到的问题与对策
## 四、下周计划
- ...
"""

# 4. 调 API
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
print("\n⏳ AI 正在写周报...\n")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)

weekly_report = response.choices[0].message.content

# 5. 打印 + 保存
print("=" * 50)
print("📋 生成的周报：")
print("=" * 50)
print(weekly_report)
print()

date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"weekly_report_{date_str}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# 周报 - {date_str}\n\n")
    f.write(weekly_report)

print(f"✅ 周报已保存到 {filename}")