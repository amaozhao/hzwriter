import json
from collections import defaultdict

# --- 配置 ---
input_file = "idiom.json"
output_file = "idiom.js"

print(f"开始处理成语文件: {input_file}")

# 1. 读取原始JSON文件
try:
    with open(input_file, "r", encoding="utf-8") as f:
        idiom_list = json.load(f)
    print(f"成功读取了 {len(idiom_list)} 条成语数据。")
except FileNotFoundError:
    print(f"错误：找不到输入文件 {input_file}！请确保文件存在于同一目录下。")
    exit()
except json.JSONDecodeError:
    print(f"错误：{input_file} 文件不是一个有效的JSON格式！")
    exit()
except Exception as e:
    print("错误：读取文件时发生未知错误！")
    print(e)
    exit()

# 2. 创建一个字典，用于按汉字聚合所有成语
# defaultdict 会在key不存在时，自动创建一个空列表
char_to_idioms_map = defaultdict(list)

# 3. 遍历每一条成语数据
for idiom_obj in idiom_list:
    if not isinstance(idiom_obj, dict) or "word" not in idiom_obj:
        continue

    idiom_word = idiom_obj["word"]

    # 提取成语中的所有独立汉字
    # 使用set可以自动去重，确保每个字只处理一次
    unique_chars_in_idiom = set(idiom_word)

    # 为每个汉字，将当前成语添加到它的列表中
    for char in unique_chars_in_idiom:
        # 过滤掉非汉字字符（如逗号）
        if "\u4e00" <= char <= "\u9fff":
            char_to_idioms_map[char].append(idiom_word)

print(f"成功将成语按 {len(char_to_idioms_map)} 个独立汉字进行了分组。")

# 4. 将聚合后的字典转换为JS文件内容
try:
    json_string = json.dumps(dict(char_to_idioms_map), ensure_ascii=False, indent=2)
    file_content = f"const IDIOM_DICTIONARY = {json_string};"
except Exception as e:
    print("错误：将数据转换为JSON字符串时失败！")
    print(e)
    exit()

# 5. 写入新的JS文件
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"转换成功！新的成语数据文件已保存为: {output_file}")
except Exception as e:
    print(f"错误：写入 {output_file} 文件失败！")
    print(e)
