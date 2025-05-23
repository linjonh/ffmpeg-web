import asyncio
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import json
import re
from types import CoroutineType
from typing import Any
from bs4 import BeautifulSoup, Comment, Doctype
import os
import glob
from bs4.element import NavigableString, PageElement
from utils import timeCost
import ast

from azure_openai_cli import call_chatgpt


def contains_english(text: str):
    return re.search(r"[a-zA-Z]", text) is not None


pool = ThreadPoolExecutor(max_workers=os.cpu_count())


def append_task(task: list, text_array: dict[int, str]):
    # return task.append(sync_api(prompt=f"翻译下数组里的文案，返回数组：{text_array}"))
    if len(text_array) == 0:
        return None
    print(f"翻译源数组大小：size{len(text_array)}")
    json_str = json.dumps(text_array, ensure_ascii=False).replace("'", "&apos;")
    prompt = f"翻译下数json的values文案，直接返回翻译后的json，不要输出markdown，要纯json文本格式输出，转义的字符保持原样输出：{json_str}"
    return task.append(call_chatgpt(prompt=prompt, is_data_json=True))


async def handle_html_file(html: str, base_name: str):
    soup = BeautifulSoup(html, "html.parser")
    leng = 0
    chunk_size = 0
    task = []
    text_array: dict[int, str] = {}
    translate_arry: dict[int, str] = {}
    childs = soup.descendants
    nodes: dict[int, PageElement] = {}
    for i, node in enumerate(childs):
        if (
            isinstance(node, NavigableString)
            and not isinstance(node, Comment)
            and not isinstance(node, Doctype)
        ):
            parent = node.parent
            if parent.name in [
                "script",
                "style",
                "noscript",
                "pre",
                "code",
                "samp",
                "template",
            ]:
                print("skip script, style, noscript ")
                continue

            text = node.strip()
            if not text or not contains_english(text):
                # print(f"skip no english word text=[{text}]")
                continue
            leng += len(text)
            text_array[i] = text
            nodes[i] = node
            if chunk_size < 10_000:
                chunk_size += len(text)
            else:
                chunk_size = 0
                append_task(task, text_array)
                text_array.clear()
                # print(f"替换文本: {text} -> {translation_dict[text]}")
    if chunk_size > 0 and chunk_size < 10_000:
        append_task(task, text_array)

    all_results = await asyncio.gather(*task)
    for i, rep in enumerate(all_results):
        # json_str=rep.replace("\"","\\\"").replace("'","\"")
        print(f"{i} {type(rep)} rep={rep}")
        if rep is None:
            print(f"{i} rep is None")
            continue
        # ast.literal_eval(rep)
        translate_arry.update(rep)
    print(f"===> translate_arry={translate_arry}")
    for i, node in nodes.items():
        node: PageElement
        print(f"【{i}】before {node}")
        text = translate_arry.get(str(i), "").strip()
        if text != "":
            node.replace_with(text)
            print(f"【{i}】after ====> {text}")
        else:
            print(f"【{i}】after ====> not tranlate")
    with open(f"{docs_path_cn}/{base_name}", "w", encoding="utf-8") as f:
        # Comment:
        string: str = str(soup)
        # string: str = soup.prettify()
        f.write(string)
    # 为了统计文件字数
    # with open('words_length.txt', 'a') as f:
    #     # Comment:
    #     f.write(f"{base_name:<30} words={leng:>12,}\n")
    # end overwrite file
    print(f"total text size={leng:>12,}")

    return leng


# async def start_trans(text: list) -> str:
#     trans_txt = call_chatgpt(prompt=f"翻译下数组里的文案，返回数组：{text}", is_data_json=False)
#     # node.replace_with(trans_txt)
#     # print(f"node: {node} string=【{trans_txt}】")
#     arry=json.loads(trans_txt)
#     return arry

docs_path = "./htdocs"
docs_path_cn = "./htdocs_cn"
if __name__ == "__main__":

    @timeCost
    def main():
        os.makedirs(docs_path_cn, exist_ok=True)
        # 复制文件
        os.system(f"cp -r {docs_path}/. {docs_path_cn}/.")
        list_files = glob.glob(f"{docs_path}/*.html")
        list.sort(list_files)
        length = 0
        str_length = 0
        pool = ThreadPoolExecutor(
            max_workers=os.cpu_count(), thread_name_prefix="trans_file_thread"
        )
        jobs = []
        for item in list_files:  # import os
            print(item)
            base_name = os.path.basename(item)
            with open(item, "r") as f:
                # Comment:
                data = f.read()
                length += len(data)
                jobs.append(pool.submit(asyncio.run, handle_html_file(data, base_name)))
        for job in futures.as_completed(jobs):
            str_length += job.result()
            print(
                f"{base_name:<30} read size={len(data):>12,}    total size={length:>12,} string_len={str_length:>12,}"
            )

    main()
