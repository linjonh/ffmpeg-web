
import json

from azure_openai_cli import call_chatgpt

arr=[]
arr.append('hello')
arr.append('this is a test arry')
res=call_chatgpt(prompt=f"翻译下数组里的文案，返回数组：{arr}")
print(res)

