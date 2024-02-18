import os
import json
import sys

def GenFirstGuide():
    prompt = "您好，我是由讯飞星火大模型支持的AI智能诉状生成小助手！只要您将必要信息提供给我，我就可以按您的要求生成一份合格准确的起诉状！\n\
现在，我需要知道您起诉的案由，也就是案件的主题。\n\
您可以回答：民间借贷纠纷，机动车交通事故责任纠纷，或其他您需处理的事故纠纷类型。\n"
    return prompt

def GenAfterKnownCaseTypeGuide(Case_Type):
    if Case_Type == 1:
        prompt = "好的，我已经知道了您的案由是：**民间借贷纠纷**。\n\n接下来我会向您提问生成起诉状所需的问题，请您按要求回答：\n\n"
    elif Case_Type == 2:
        prompt = "好的，我已经知道了您的案由是：**机动车交通事故责任纠纷**。\n\n接下来我会向您提问生成起诉状所需的问题，请您按要求回答：\n\n"
    elif Case_Type == 3:
        prompt = "好的，我已经知道了您的案由是：**其他纠纷类型**。\n\n接下来我会向您提问生成起诉状所需的问题，请您按要求回答：\n\n"

    return prompt

def GenErrorGuide():
    prompt = "不好意思，AImicus没有理解您的意思... \n\n可能是您填写的信息有**遗漏**，或**格式有错误**，导致系统没有识别。\n\n建议您补充缺失信息，或**严格按照我上面所说的格式** 详细完整地录入信息~~\n\n下面请您重新输入：\n\n"
    return prompt

def GenCaseTypeGuide():
    prompt = "现在，我需要知道您起诉的**案由**，也就是案件的主题。\n\n"\
            +"您可以回答：\n\n* **民间借贷纠纷** \n\n * **机动车交通事故责任纠纷** \n\n * 或：其他您需处理的事故纠纷类型。\n\n"
    return prompt

def GenPlaintiffNumGuide():
    prompt = "接下来我们需要了解关于**原告**的信息。\n\n请问本次案件有**几名原告**？\n\n P.S. 如果您的原告包含公司，一家公司算一名原告\n\n 如果有1名，请您输入：**1**；\n\n如果有2名，请您输入：**2**，以此类推。\n\n"
    return prompt

def GenPlaintiffInfoGuide():
    prompt = "下面请您输入原告的信息。\n\n"\
            +"如果本原告是**个人**（非公司），应该至少包括：姓名、民族、身份证号、住址（精确到门牌号）、电话号码。\n\n"\
            +"AImicus建议您按以下格式进行输入：\n\n"\
            +"* **姓名**：xxx \n\n * **民族**：xx族 \n\n * **身份证号**：xxxxxxxxxxxxxxxxxx \n\n * **住址**：xx省xx市xx区xxxx \n\n * **电话号码**：xxxxxxxxxxx\n\n"\
            +"如果本原告是**公司**（非个人），应该至少包括：公司名称、企业负责人姓名。如果有公司所在地址、企业负责人电话等信息就更好了。\n\n"\
            +"AImicus建议您按以下格式进行输入：\n"\
            +"* **公司名称**：xxx公司/xxx企业 \n\n * **企业负责人**：xxxxxxx \n\n * （公司所在地址：xxxxxxxxxxx） \n\n * （企业负责人电话：xxxxxx）\n"
    return prompt


def GenDefendantNumGuide():
    prompt = "接下来我们需要了解关于**被告**的信息。\n\n请问本次案件有**几名被告**？\n\n P.S. 如果您的被告包含公司，一家公司算一名被告\n\n 如果有1名，请您输入：**1**；\n\n如果有2名，请您输入：**2**，以此类推。\n\n"
    return prompt

def GenDefendantInfoGuide():
    prompt = "下面请您输入被告的信息。\n\n"\
            +"如果本被告是**个人**（非公司），应该至少包括：姓名、身份证号。如果有电话号码、住址（精确到门牌号）、民族等信息就更好了。\n\n"\
            +"AImicus建议您按以下格式进行输入：\n\n"\
            +"* **姓名**：xxx \n\n * **身份证号**：xxxxxxxxxxxxxxxxxx \n\n * （**民族**：xx族）\n\n * （**电话号码**：xxxxxxxxxxx）\n\n * （**住址**：xx省xx市xx区xxxx）\n\n"\
            +"如果本被告是**公司**（非个人），应该至少包括：公司名称、企业负责人姓名。如果有电话号码、住址（精确到门牌号）、民族等信息就更好了。\n\n"\
            +"AImicus建议您按以下格式进行输入：\n"\
            +"* **公司名称**：xxx公司/xxx企业 \n\n * **企业负责人**：xxxxxxx \n\n * （**企业负责人电话**：xxxxxx）\n\n * （**公司所在地址**：xxxxxxxxxxx） \n\n "
    return prompt

def GenAccuseRequestGuide(Case_Type):
    prompt = ""
    if Case_Type == 1:    
        prompt = "下面请您输入此次关于民间借贷的**诉讼请求**。\n\n 您的叙述应该至少包括：被告欠款**本金金额**、希望得到的**利息**总额。AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n"
    elif Case_Type == 2:
        prompt = "下面请您输入此次关于机动车交通事故责任的**诉讼请求**。\n\n 您的叙述应该至少包括：希望被告赔偿的各项**费用总和**。AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n"
    elif Case_Type == 3:
        prompt = "下面请您输入此次的**诉讼请求**。\n\n AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n\n"
    
    return prompt

def GenWholeStoryGuide(Case_Type):
    prompt = ""
    if Case_Type == 1:
        prompt = "下面请您输入此次关于民间借贷的**事情经过**，请条理清晰地描述**案件事实**和**起诉理由**。\n\n AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n\n"
    elif Case_Type == 2:
        prompt = "下面请您输入此次关于机动车交通事故责任的**事情经过**，请条理清晰地描述**案件事实**和**起诉理由**。\n\n AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n\n"
    elif Case_Type == 3:
        prompt = "下面请您输入此次案件的**事情经过**，请条理清晰地描述**案件事实**和**起诉理由**。\n\n AImicus温馨提示：您叙述得越详细，我为您生成的起诉状就越准确~\n\n"
    return prompt

def GenCourtGuide():
    prompt = "下面请您输入您希望将此案提交到哪个法院，比如：xx区人民法院。如果您不知道提交到哪个法院，您可以输入：“自动选择”，我们将为您推荐距离您的住址最近的可以受理案件的法院。\n"
    return prompt

def GenFinalGuide():
    prompt = "您已经填写了生成起诉状所需的全部信息！请稍加等待，正在为您生成起诉状文档......\n"
    return prompt

# 车牌号、对经过，案件的处理、被告信息不全的处理、被告人数量