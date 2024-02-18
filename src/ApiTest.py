from .SparkApi import *

# 以下密钥信息从控制台获取
appid = "2173dc2a"  # 填写控制台中获取的 APPID 信息
api_secret = "M2U2OGJkMDcxMWE2N2ZlMzMzMzFkNzRk"  # 填写控制台中获取的 APISecret 信息
api_key = "5b400ef7f4ce29160d6aa1f9e98efecc"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“generalv2”
# domain="plugin"  #search版本
domain = "generalv2"  # v2.0版本
# domain = "general"   # v1.5版本



# 云端环境的服务地址
# Spark_url="ws://spark-api-knowledge.xf-yun.com/v2.1/multimodal"  #search环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址


text = []

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

if __name__ == '__main__':
    text.clear
    while (1):
        Input = input("\n" + "我:")
        question = checklen(getText("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        getText("assistant", SparkApi.answer)
        # print(str(text))
# 你是一个数据处理员，收到数据后必须按照我要求的格式进行处理。我在下一轮对话会给你一段文本，从文本中，你需要提取出[姓名],[性别],[出生年月日],[联系电话],[住址]。我的要求是：在我给你这段文本后，你输出一个字典，字典里的值包括：姓名、性别（一个字，男或女）、出生年月日（以"xxxx-xx-xx"的形式，x代表阿拉伯数字）、联系电话（以11位数字的形式）、住址（以xx省xx市xx区的形式，如果只给了部分地址，请你依靠中国的地理知识自己补上省市区）。输出字典的键包括："姓名"、"性别"、"出生年月日"、"联系电话"、"住址"，按顺序与前面提到的值对应。比如说，一个满足条件的输出是：{"姓名": "张二小", "性别": "男", "出生年月日": "1999-09-23", "联系电话": "14829408214", "住址": "江苏省南京市秦淮区"}，按照这样的格式输出即可。如果你明白我的意思，请回复1，我会在下一轮对话给你需要处理的文本。
# 我是一个70岁的老头，我叫张大大先生，我的身体一直不太好，因为我出生就贫血。您不是一直要我的联系方式吗，是19873562532.我是在1947年八月9号出生在广州的，但是后来我举家搬迁，后来到了苏州姑苏区，一直住到现在。{"姓名": "张二小", "性别": "男", "出生年月日": "1999-09-23", "联系电话": "14829408214", "住址": "江苏省南京市秦淮区"}，按照这样的格式输出即可。

# 你是一个问问题的专家。在一次案件中，你需要知道原告的姓名、性别、联系电话，身份证号，住址，被告的姓名、性别、联系电话、身份证号、住址。你需要引导我按顺序说出这些信息，每次询问的信息不能超过3个。请输出你要问的问题，输出格式：<output>问题1：xxx; 问题2：xxx; 问题3：xxx</output>。务必注意：每次询问的信息不能超过3个！