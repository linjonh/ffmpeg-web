
import json

# from azure_openai_cli import call_chatgpt

# arr=[]
# arr.append('hello')
# arr.append('this is a test arry')
# res=call_chatgpt(prompt=f"翻译下数组里的文案，返回数组：{arr}")
# print(res)

arr="['关于FFmpeg', 'FFmpeg', '关于我们', '新闻', '下载', '文档', '社区', '行为准则', '邮件列表', 'IRC频道', '论坛', '缺陷报告', '维基', '开发者', '源代码', '参与贡献', 'FATE测试套件', '代码覆盖率', '通过SPI获得资助', '更多', '捐赠', '聘请开发者', '联系我们', '安全公告', '法律声明', '关于FFmpeg', 'FFmpeg是领先的多媒体框架，能够进行','解码','编码','转码','封装','解封装','流传输','滤镜处理','以及','播放','人类和机器创造的几乎所有内容。它支持从最晦涩的古老格式到前沿技术。无论这些格式是由标准委员会、社区还是企业设计的。该框架还具有高度可移植性：FFmpeg可在Linux、Mac OS X、Microsoft Windows、BSD系统、Solaris等多种构建环境、硬件架构及配置下编译运行并通过我们的自动化测试体系FATE','跨平台支持覆盖Linux, Mac OS X,\n  Microsoft Windows, BSDs, Solaris等操作系统，适应各种构建环境、机器架构和配置。','包含可供应用程序调用的libavcodec、libavutil、libavformat、libavfilter、libavdevice、\n  libswscale与libswresample库。同时提供终端用户使用的ffmpeg、ffplay及\n  ffprobe工具用于','转码','和','播放','FFmpeg项目致力于为应用开发者和最终用户提供技术层面最优的解决方案。为此我们整合了现有最佳的免费软件方案。我们会优先使用自有代码以降低对其他库的依赖，并最大化FFmpeg各组件间的代码复用率。当\"最佳\"选择难以决断时，我们会同时支持多种方案让终端用户自主抉择。','欢迎所有人参与FFmpeg项目并贡献力量。我们乐于接收补丁、拉取请求、缺陷报告、捐赠及其他任何形式的贡献。','安全性是我们的首要考量，代码审查始终以安全为导向。然而由于涉及处理非可信数据的代码量极为庞大，安全问题在所难免。因此发现新漏洞时我们会尽快为最新稳定版提供更新修复。','FFmpeg工具集', 'ffmpeg','一款','命令行工具','用于多媒体格式转换','ffplay','基于SDL和FFmpeg库的简易媒体播放器','ffprobe','基础的多媒体流分析工具','开发者使用的FFmpeg库', 'libavutil','该库提供编程辅助功能，包含随机数生成器、数据结构、数学例程、核心多媒体实用工具等。','libavcodec','音视频编解码器库，内含各类音频/视频编码器和解码器。','libavformat','多媒体容器格式处理库，包含解封装与封装组件。','libavdevice','设备输入输出库，支持从Video4Linux、Video4Linux2、VfW、ALSA等常见多媒体框架采集和渲染数据。','libavfilter','媒体滤镜处理库', 'libswscale','高性能图像缩放及色彩空间/像素格式转换库', 'libswresample','高效音频重采样、声道重塑与样本格式转换库', '托管服务由','telepoint.bg提供']"

rep=arr.replace("['","").replace("']","").split("',")
for r in rep:
    string = r.strip()
    index=string.find("'")
    print(f"====> {string[index+1:]}")
# array=json.loads(rep)
# print(array)

my_dic:dict={}
my_dic2:dict={}

for i,s in enumerate(rep):
    my_dic[i]=s    
    my_dic2[i]=s    
print(json.dumps(my_dic,indent=4,ensure_ascii=False))
for (k,v),d in zip(my_dic.items(),my_dic2):
    print(f"{k} : {v} ==> {d}")


