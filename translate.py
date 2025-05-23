import asyncio
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import json
import re
from bs4 import BeautifulSoup, Comment, Doctype
import os
import glob
from bs4.element import NavigableString, PageElement
from utils import timeCost



from azure_openai_cli import call_chatgpt


def contains_english(text: str):
    return re.search(r"[a-zA-Z]", text) is not None


pool = ThreadPoolExecutor(max_workers=os.cpu_count())


def append_task(task, text_array:list):
    # return task.append(sync_api(prompt=f"翻译下数组里的文案，返回数组：{text_array}"))
    if len(text_array)==0:
        return None
    print(f"翻译源数组大小：size{len(text_array)}")
    return task.append(call_chatgpt(prompt=f"翻译下数组里的文案，数组元素个数{len(text_array)}，直接返回数组，返回的数组元素个数也要一致。数组元素都用单引号，不要输出markdown，要纯文本格式输出：{text_array}"))


async def handle_html_file(html: str, base_name: str):
    soup = BeautifulSoup(html, "html.parser")
    leng = 0
    chunk_size = 0
    task = []
    text_array: list[str] = []
    translate_arry = []
    childs = soup.descendants
    nodes = []
    for i,node in enumerate(childs):
        if (
            isinstance(node, NavigableString)
            and not isinstance(node, Comment)
            and not isinstance(node, Doctype)
        ):
            parent = node.parent
            if parent.name in ["script", "style", "noscript","pre","code","samp","template"]:
                print("skip script, style, noscript ")
                continue

            text = node.strip()
            if not text or not contains_english(text):
                # print(f"skip no english word text=[{text}]")
                continue
            leng += len(text)
            text_array.append(text)
            nodes.append(node)
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
        print(f"{i} rep={type(rep)}")
        if rep is None:
            print(f"{i} rep is None")
            continue
        rep = (rep.replace("['", "").replace("[", "").replace("']", "")
                .replace("'\n]", "").replace("]", "").replace("'\n", "").strip().split("',"))
        print(f"===> size= {len(rep)} extend: {rep} ")
        translate_arry.extend(rep)
    print(f"===> translate_arry={translate_arry}")
    for node, text in zip(nodes, translate_arry):
        print(f"before {node.text}")
        text = text.strip()
        index = text.find("'")
        # print(f"====> {text[index+1:]}")
        text = text[index + 1 :]
        node.replace_with(text)
        print(f"after ====> {text}")
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
        for item in list_files:  # import os
            print(item)
            base_name = os.path.basename(item)
            with open(item, "r") as f:
                # Comment:
                data = f.read()
                length += len(data)
                str_length += asyncio.run(handle_html_file(data, base_name))
                print(
                    f"{base_name:<30} read size={len(data):>12,}    total size={length:>12,} string_len={str_length:>12,}"
                )

    main()
