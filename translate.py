import asyncio
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import json
import random
import re
import sys
import time
from types import CoroutineType
from typing import Any
from bs4 import BeautifulSoup, Comment, Doctype
import os
import glob
from bs4.element import NavigableString, PageElement
import volcenginesdktranslate20250301.models
import volcenginesdktranslate20250301.models.translate_text_response
from my_log import log
from utils import timeCost
import ast

# from azure_openai_cli import call_chatgpt
import volcan_translate
import volcenginesdktranslate20250301

CHUNCK_SIZE = 4800


def contains_english(text: str):
    return re.search(r"[a-zA-Z]", text) is not None


pool = ThreadPoolExecutor(max_workers=os.cpu_count())


async def volcan_trans(arrays: dict[int, str]):
    """ 返回数据
    {
        'translation_list': [{'detected_source_language': '', 'translation': '关于FFmpeg'}, {'detected_source_language': '', 'translation': 'FFmpeg'}, {'detected_source_language': '', 'translation': '关于'}, {'detected_source_language': '', 'translation': '新闻'}, {'detected_source_language': '', 'translation': '下载'}, {'detected_source_language': '', 'translation': '文档'}],
        "ResponseMetadata": {
            "RequestId": "202004092306480100140440781F5D7119",
            "Action": "TranslateText",
            "Version": "2020-06-01",
            "Service": "translate",
            "Region": "cn-north-1",
            "Error": null
        }
    }"""
    time.sleep(0.1*random.randrange(1, 10))
    log(f"===> start call  volcenginesdk API arrays size={len(arrays)}")
    res: volcenginesdktranslate20250301.models.translate_text_response.TranslateTextResponse = volcan_translate_.translate_text(
        "en", "zh", list(arrays.values()))
    log(f"res={res.to_dict()} type={type(res)}")
    arry = res.to_dict().get("translation_list", [])
    # res={'translation_list': [{'detected_source_language': '', 'translation': '关于FFmpeg'}, {'detected_source_language': '', 'translation': 'FFmpeg'}, {'detected_source_language': '', 'translation': '关于'}, {'detected_source_language': '', 'translation': '新闻'}, {'detected_source_language': '', 'translation': '下载'}, {'detected_source_language': '', 'translation': '文档'}, {'detected_source_language': '', 'translation': '社区'}, {'detected_source_language': '', 'translation': '行为准则'}, {'detected_source_language': '', 'translation': '邮件列表'}, {'detected_source_language': '', 'translation': 'IRC'}, {'detected_source_language': '', 'translation': '论坛'}, {'detected_source_language': '', 'translation': '错误报告'}, {'detected_source_language': '', 'translation': '维基'}, {'detected_source_language': '', 'translation': '开发商'}, {'detected_source_language': '', 'translation': '源代码'}, {'detected_source_language': '', 'translation': '贡献'}, {'detected_source_language': '', 'translation': '命运'}, {'detected_source_language': '', 'translation': '代码覆盖率'}, {'detected_source_language': '', 'translation': '通过SPI提供资金'}, {'detected_source_language': '', 'translation': '更多'}, {'detected_source_language': '', 'translation': '捐赠'}, {'detected_source_language': '', 'translation': '聘请开发人员'}, {'detected_source_language': '', 'translation': '联系方式'}, {'detected_source_language': '', 'translation': '保安'}, {'detected_source_language': '', 'translation': '法律'}, {'detected_source_language': '', 'translation': '关于FFmpeg'}, {'detected_source_language': '', 'translation': 'FFmpeg是领先的多媒体框架，能够'}, {'detected_source_language': '', 'translation': '译码'}, {'detected_source_language': '', 'translation': '编码'}, {'detected_source_language': '', 'translation': '转码'}, {'detected_source_language': '', 'translation': '多路复用器'}, {'detected_source_language': '', 'translation': 'demux'}, {'detected_source_language': '', 'translation': '溪流'}, {'detected_source_language': '', 'translation': '过滤器'}, {'detected_source_language': '', 'translation': '和'}, {'detected_source_language': '', 'translation': '玩'}, {'detected_source_language': '', 'translation': '几乎任何东西\n人类和机器创造的。它支持最模糊的\n古老的格式直到最前沿。不管他们是不是\n由某个标准委员会、社区或公司设计。它是\n也高度可移植：FFmpeg编译、运行和通过我们的测试基础设施'}, {'detected_source_language': '', 'translation': '命运'}, {'detected_source_language': '', 'translation': 'LinuxMac OS X\nMicrosoft Windows、BSD、Solaris等下的各种构建\n环境、机器架构和配置。'}, {'detected_source_language': '', 'translation': '它包含libavcodec、libavutil、libavformat、libavfilter、libavments、\n应用程序可以使用的libswscale和libswresample。\n以及可用于\n最终用户'}, {'detected_source_language': '', 'translation': '转码'}, {'detected_source_language': '', 'translation': '和'}, {'detected_source_language': '', 'translation': '演奏'}, {'detected_source_language': '', 'translation': 'FFmpeg项目试图提供最好 的技术可能\n适用于应用程序开发人员和最终用户的解决方案。实现\n这是我们结合了可用的最佳免费软件选项。我们稍微\n支持我们自 己的代码，以保持对其他库的依赖度低，并\n最大化FFmpeg部分之间的代码共享。\n只要“最好”的问题不能回答，我们就支持两者\n供最 终用户选择的选项。'}, {'detected_source_language': '', 'translation': 'FFmpeg欢迎每个人，也欢迎所有的贡献。\n我们很高兴收到补丁，拉取请求，bug报告，捐赠\n或任何其他类型的贡献。'}, {'detected_source_language': '', 'translation': '安全性是重中 之重，代码审查始终与\n考虑安全。尽管由于大量代码接触\n不受信任的数据安全问题是不可避免的，因此我们提供\n在以下情况下尽快 更新我们最后一个稳定版本\n发现新的安全问题。'}, {'detected_source_language': '', 'translation': 'FFmpeg工具'}, {'detected_source_language': '', 'translation': 'ffmpeg'}, {'detected_source_language': '', 'translation': '一个'}, {'detected_source_language': '', 'translation': '命令行工具'}, {'detected_source_language': '', 'translation': '转换多媒体文件\n格式之间'}, {'detected_source_language': '', 'translation': '外放'}, {'detected_source_language': '', 'translation': '一个基于SDL和FFmpeg库的简单媒体播放器'}, {'detected_source_language': '', 'translation': '远红外探测器'}, {'detected_source_language': '', 'translation': '一个简单的多媒体流分析器'}, {'detected_source_language': '', 'translation': '面向开发人员的FFmpeg 库'}, {'detected_source_language': '', 'translation': 'libavutil'}, {'detected_source_language': '', 'translation': '是一个包含函数的库\n简化编程，包括随机数生成器、数据\n结构、数学例程、核心多媒体实用程序等等\n更多。'}, {'detected_source_language': '', 'translation': 'libavcodec'}, {'detected_source_language': '', 'translation': '是一个包含解码器和编码器的库\n用于音频/视频编解码器。'}, {'detected_source_language': '', 'translation': 'libavformat'}, {'detected_source_language': '', 'translation': '是一个包含解复用器和\n多媒体容器格式的混音器。'}, {'detected_source_language': '', 'translation': '软 件库'}, {'detected_source_language': '', 'translation': '是一个包含输入和输出的库\n用于抓取和渲染许多常见多媒体的设备\n输入/输出软件框架，包括Video4Linux、Video4Linux2、\nVfW和ALSA。'}, {'detected_source_language': '', 'translation': 'libavfilter'}, {'detected_source_language': '', 'translation': '是一个包含媒体过滤器的库。'}, {'detected_source_language': '', 'translation': '自由尺度'}, {'detected_source_language': '', 'translation': '是一个执行高度优化图像的库\n缩放和色彩空间/像素格式转换操作。'}, {'detected_source_language': '', 'translation': 'libswresample'}, {'detected_source_language': '', 'translation': '是一个执行高度优化的库\n音频重采样、重矩阵和样本格式转换操作。'}, {'detected_source_language': '', 'translation': '托管提供者'}, {'detected_source_language': '', 'translation': 'telepoint.bg'}]}
    # arry = res.get("translation_list", [])
    # log(f"arry={arry} type={type(arry)}")
    for index, (i, _) in enumerate(arrays.items()):
        # log(f"i={i} arry={arry}")
        if index < len(arry):
            arrays[i] = arry[index].get("translation")
        else:
            arrays[i] = ""

    return json.loads(json.dumps(arrays, ensure_ascii=False))


def append_task(task: list, text_array: dict[int, str], trans_method: str = "volcan"):
    # return task.append(sync_api(prompt=f"翻译下数组里的文案，返回数组：{text_array}"))
    arrays = text_array.copy()
    if len(arrays) == 0:
        return None
    for i, text in arrays.items():
        # log(f"i={i} text={text}")
        if len(text) > CHUNCK_SIZE:
            # log(f"i={i} text length > {CHUNCK_SIZE} text={text}")
            arrays[i] = text[:CHUNCK_SIZE]
            arrays[i + 1] = text[CHUNCK_SIZE:]
    log(f"翻译源数组大小：size={len(arrays.values())}")
    if trans_method == "chatgpt":
        json_str = json.dumps(
            arrays, ensure_ascii=False).replace("'", "&apos;")
        prompt = f"翻译下数json的values文案，直接返回翻译后的json，不要输出markdown，要纯json文本格式输出，转义的字符保持原样输出：{json_str}"
        # return task.append(call_chatgpt(prompt=prompt, is_data_json=True))
    elif trans_method == "volcan":
        return task.append(volcan_trans(arrays))
    else:
        raise ValueError("不支持的翻译方法！")


async def handle_html_file(html: str, base_name: str, method: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    count_leng = 0
    chunk_size = 0
    task = []
    text_will_trans_array: dict[int, str] = {}
    translated_arry: dict[int, str] = {}
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
                "em"
            ]:
                log("skip script, style, noscript ")
                continue

            text = node.strip()
            if not text or not contains_english(text):
                # log(f"skip no english word text=[{text}]")
                continue
            # 需要把dict 的key也要算进字符数
            size = len({f"{i}": text})
            count_leng += size
            # TextList[String] 待翻译列表列表长度不超过16 总文本长度不超过5000字符
            if len(text_will_trans_array) < 16 and chunk_size+size < CHUNCK_SIZE:
                chunk_size += size
            else:
                chunk_size = 0
                append_task(task, text_will_trans_array, method)
                text_will_trans_array.clear()
            # 后置递增添加
            text_will_trans_array[i] = text
            nodes[i] = node
    if chunk_size > 0 and chunk_size < CHUNCK_SIZE:
        append_task(task, text_will_trans_array, method)

    all_results = await asyncio.gather(*task)
    log(f"all_results={len(all_results)} type={type(all_results)}")
    for i, rep in enumerate(all_results):
        # json_str=rep.replace("\"","\\\"").replace("'","\"")
        log(f"{i} {type(rep)} rep={rep}")
        if rep is None:
            log(f"{i} rep is None")
            continue
        # ast.literal_eval(rep)
        translated_arry.update(rep)
    log(f"===> translate_arry={translated_arry}")
    for i, node in nodes.items():
        node: PageElement
        log(f"【{i}】before {node}")
        text = translated_arry.get(str(i), "").strip()
        if text != "":
            node.replace_with(text)
            log(f"【{i}】after ====> {text}")
        else:
            log(f"【{i}】after ====> not tranlate")
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
        log(f"【save file】: {docs_path_cn}/{base_name} total text size={count_leng:>12,}")

    return count_leng


# async def start_trans(text: list) -> str:
#     trans_txt = call_chatgpt(prompt=f"翻译下数组里的文案，返回数组：{text}", is_data_json=False)
#     # node.replace_with(trans_txt)
#     # log(f"node: {node} string=【{trans_txt}】")
#     arry=json.loads(trans_txt)
#     return arry

docs_path = "./htdocs"
docs_path_cn = "./htdocs_cn"
# docs_path = "../ffmpeg-docs-website"
# docs_path_cn = "../ffmpeg-docs-website/htdocs_cn"
if __name__ == "__main__":
    args = sys.argv
    method = "volcan"
    id = ""
    key = ""
    if len(args) > 1:
        method = args[1]
    if len(args) > 2:
        id = args[2]
    if len(args) > 3:
        key = args[3]
    log(f"method={method} id={id} key={key}")
    volcan_translate_ = volcan_translate.VolcanTranslate(id=id, key=key)

    @timeCost
    def main(method):
        # try:
        #     os.remove(docs_path_cn)
        # except Exception as e:
        #     log(f"remove {docs_path_cn} error={e}")
        # 创建目录
        os.makedirs(docs_path_cn, exist_ok=True)
        # 复制文件
        # os.system(f"rsync -av --exclude='*.html' {docs_path}/ {docs_path_cn}/")
        list_files = glob.glob(f"{docs_path}/*.html")
        log(f"list *.html files size= {len(list_files)}")
        list.sort(list_files)
        length = 0
        str_length = 0
        pool = ThreadPoolExecutor(
            max_workers=os.cpu_count(), thread_name_prefix="trans_file_thread"
        )
        jobs = []
        for item in list_files:  # import os
            log(f"===> start translate: {item}")
            base_name = os.path.basename(item)
            if os.path.exists(f"{docs_path_cn}/{base_name}"):
                log(f"===> file exist: {docs_path_cn}/{base_name}")
                continue
            with open(item, "r", encoding="utf-8") as f:
                # Comment:
                data = f.read()
                length += len(data)
                jobs.append(pool.submit(
                    asyncio.run, handle_html_file(data, base_name, method)))
        for job in futures.as_completed(jobs):
            str_length += job.result()
            log(
                f"===> complete trans file : {base_name:<30} read size={len(data):>12,}    total size={length:>12,} string_len={str_length:>12,}"
            )

    main(method)
