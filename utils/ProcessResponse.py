import os
import json
import sys

from src import SparkApi

def GetText(role, content):
    text = []
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def CleanData(content):
    content = content.replace("\n\n", "\n")
    content = content.replace("。", "")
    content = content.replace("[", "")
    content = content.replace("]", "")
    content = content.replace("(", "")
    content = content.replace(")", "")
    content = content.replace("（", "")
    content = content.replace("）", "")
    content = content.replace(" ", "")
    
    return content

def CheckCaseType(content, appid, api_key, api_secret, Spark_url, domain):
    print('用户：'+content)
    prompt = "你是一个法律专家。接下来我会跟你说一个案件的主题，案件的主题是："+content+"\n"\
            +"根据该案件主题，你需要帮我按照如下规则分类并输出：\n"\
            +"当此案件与民间借贷有关时，输出：[借贷民间纠纷]；\n"\
            +"当此案件与机动车交通事故责任纠纷有关时，输出：[机动车交通事故责任纠纷]；\n"\
            +"当判断过于困难时，输出：[无法判断]。\n"\
            +"例如，你可以输出的答案有：[借贷民间纠纷]、[机动车交通事故责任纠纷]、[无法判断]。\n"\
            +"你输出的格式必须是：[案由类别]。"\
            +"请注意，案件的主题是："+content+"\n"\
            +"你的输出是："
    SparkApi.answer = ""
    prompt = GetText("user", prompt)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
    info_response = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--案由判断结果："+info_response)
    if '无法' in info_response or 'xx' in info_response:
        return False, ""
    else:
        return True, CleanData(info_response)
    
def CheckNum(content, appid, api_key, api_secret, Spark_url, domain):
    prompt = " 你是一个法律专家。接下来的文本，是我之前问的“案件中有几个原告？”或“案件中有几个被告？”的回复。回复是："+content+"\n"\
            +" 注意！你的输出格式只有一个阿拉伯数字。例如：你认为有两个被告，你的输出格式是：[2]；或者：你认为有三个原告，你的输出格式是：[3]。"\
            +" 你的输出是："
    SparkApi.answer = ""
    prompt = GetText("user", prompt)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
    info_response = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--后台提取信息："+info_response)
    if '无法' in info_response or 'xx' in info_response:
        return False, ""
    else:
        return True, CleanData(info_response)

def CheckPlaintiff(content, appid, api_key, api_secret, Spark_url, domain):
    company = False
    prompt = ""
    
    if '公司' in content or '企业' in content:
        company = True

    if company:
        prompt = "你是一个数据处理员，需要按照规则对数据进行正确的处理。接下来，要知道的信息包括：该公司的名称，公司所在地址，企业负责人姓名，电话。其中该公司的名称、企业负责人姓名为*主要信息*；公司所在地、电话为*不必需信息*。"\
                +"你需要从用户给的回答中提取所有需要的信息。当*主要信息*无法获取，只在对应选项后输出“无法获取”；当*不必需信息*无法获取时，在这一项信息后面输出空格即可。如果用户回答了全部的信息，必须全部提取出来。\n"\
                +"用户给的回答是：\n"\
                + content\
                +"\n输出的格式如下：\n"\
                +"注意：如果有公司所在地址，但非省级行政区只有市、区没有省的情况下，输出时你必须利用中国地理知识补全省、市信息，最终使省级行政区满足 xx省xx市xx区xxxxxxxxxx 的格式，直辖市满足 xx市xx区xxxxxxxxxx 的格式。\n"\
                +"当*主要信息*无法获取，只在对应选项后输出“无法获取”；当*不必需信息*无法获取时，在这一项信息后面输出空格即可。\n"\
                +"再次强调，用户给的回答是：\n"\
                + content\
                +"\n输出的格式如下：\n"\
                +"[公司名称： ；公司所在地址：    ；企业负责人姓名： ；电话：    ]\n"
    else:
        prompt = "你是一个数据处理专家。接下来，我需要知道的信息包括：姓名、民族、身份证号、住址、电话号码。"\
            +"用户给的回答是："+content+"。你需要从用户给的回答中提取我所需要的信息，给我输出的格式是："\
            +" [姓名：xxx；民族：xx族；身份证号：xxxxxxxxxxxxxxxxxx；住址：xx省xx市xx区xxxxxxxxxx；电话号码：xxxxxxxxxxx]"\
            +"{示例1：用户回答：”我叫张全蛋，汉族，身份证号:350424200103180437，住址：合肥市高新区望川西路87号旺角小区12-2-305，电话号码18273889943"\
            +"输出：[姓名：张全蛋；民族：汉族；身份证号：350424200103180437；住址：合肥市高新区望川西路87号旺角小区12-2-305；电话号码：18273889943]"\
            +" 注意：在地址输入不全，例如：非省级行政区只有市、区没有省的情况下，输出时你必须利用中国地理知识补全省、市信息，最终使省级行政区满足 xx省xx市xx区xxxxxxxxxx 的格式，直辖市满足 xx市xx区xxxxxxxxxx 的格式。"\
            +" 注意：信息补全后，如果仍有信息缺失，或有信息不满足上述格式，你必须在冒号后输出无法获取。"\
            +" 你的输出是："
    SparkApi.answer = ""
    prompt = GetText("user", prompt)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
    info_response = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--后台提取信息："+info_response)
    if '无法' in info_response or 'xx' in info_response:
        return False, CleanData(info_response), int(company)
    else:
        return True, CleanData(info_response), int(company)

def CheckDefendant(content, appid, api_key, api_secret, Spark_url, domain):
    
    company = False
    prompt = ""
    
    if '公司' in content or '企业' in content:
        company = True

    if company:
        prompt = "你是一个数据处理员，需要按照规则对数据进行正确的处理。接下来，要知道的信息包括：该公司的名称，公司所在地址，企业负责人姓名，电话。其中该公司的名称、企业负责人姓名为*主要信息*；公司所在地、电话为*不必需信息*。"\
                +"你需要从用户给的回答中提取所有需要的信息。当*主要信息*无法获取，只在对应选项后输出“无法获取”；当*不必需信息*无法获取时，在这一项信息后面输出空格即可。如果用户回答了全部的信息，必须全部提取出来。\n"\
                +"用户给的回答是：\n"\
                + content\
                +"\n输出的格式如下：\n"\
                +"[公司名称：；公司所在地址：    ；企业负责人姓名：；企业负责人电话：    ]\n"\
                +"注意：如果有公司所在地址，但非省级行政区只有市、区没有省的情况下，输出时你必须利用中国地理知识补全省、市信息，最终使省级行政区满足 xx省xx市xx区xxxxxxxxxx 的格式，直辖市满足 xx市xx区xxxxxxxxxx 的格式。\n"\
                +"当*主要信息*无法获取，只在对应选项后输出“无法获取”；当*不必需信息*无法获取时，在这一项信息后面输出空格即可。\n"\
                +"再次强调，用户给的回答是：\n"\
                + content\
                +"\n输出的格式如下：\n"\
                +"[公司名称： ；公司所在地址：    ；企业负责人姓名： ；企业负责人电话：    ]\n"
    else:
        prompt = "你是一个数据处理员，需要按照规则对数据进行正确的处理。接下来，要知道的信息包括：被告人的姓名、民族、身份证号、住址、电话号码。其中被告人的姓名、身份证号为*主要信息*；民族、住址、电话为*不必需信息*。"\
            +"你需要从用户给的回答中提取所有需要的信息。当*主要信息*无法获取，你必须在*主要信息*的冒号后输出“无法获取”；当*不必需信息*无法获取时，在这一项*不必需信息*冒号后面输出空格即可。\n"\
            +"用户给的回答是："+content+"。你需要从用户给的回答中提取我所需要的信息，给我输出的格式是："\
            +" [姓名：xxx；民族：xx族；身份证号：xxxxxxxxxxxxxxxxxx；住址：xx省xx市xx区xxxxxxxxxx；电话号码：xxxxxxxxxxx]"\
            +"示例1：用户回答：姓名：张全蛋，汉族，身份证号:350424200103180437，住址：合肥市高新区望川西路87号旺角小区12-2-305，电话号码18273889943"\
            +" 输出：[姓名：张全蛋；民族：汉族；身份证号：350424200103180437；住址：合肥市高新区望川西路87号旺角小区12-2-305；电话号码：18273889943]"\
            +"示例2：用户回答：姓名：高启盛，住址：京海市旧厂街12-2-305，电话号码18273889943"\
            +" 输出：[姓名：高启盛；民族： ；身份证号：无法获取；住址：京海市旧厂街12-2-305；电话号码：18273889943]"\
            +"示例3：用户回答：姓名：高启强，身份证号：140102196704031923"\
            +" 输出：[姓名：高启强；民族： ；身份证号：140102196704031923；住址： ；电话号码： ]"\
            +" 注意：在地址输入不全，例如：非省级行政区只有市、区没有省的情况下，输出时你必须利用中国地理知识补全省、市信息，最终使省级行政区满足 xx省xx市xx区xxxxxxxxxx 的格式，直辖市满足 xx市xx区xxxxxxxxxx 的格式。"\
            +" 注意：当*不必需信息*无法获取时，在这一项*不必需信息*冒号后面输出空格即可；信息补全后，如果仍有*主要信息*缺失，或有*主要信息*不满足上述格式，你必须在*主要信息*的冒号后输出“无法获取”"\
            +" 你的输出是："
    SparkApi.answer = ""
    prompt = GetText("user", prompt)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
    info_response = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--后台提取信息："+info_response)
    if '无法' in info_response or 'xx' in info_response:
        return False, CleanData(info_response), int(company)
    else:
        return True, CleanData(info_response), int(company)
    

def CheckAccuseRequest(content, appid, api_key, api_secret, Spark_url, domain, Case_Type):
    prompt = "你是一个文本处理专家。接下来，我需要知道的信息包括："
    # 借贷
    if Case_Type == 1:
        prompt += "具体金额、利息。"\
        + "当用户提到具体数目的金额时，输出：“金额”；当用户内容与利息相关时，输出：“利息”；"\
        + "注意，如果没提到对应的项目时，你不可以输出对应的词！"\
        + "例如用户说“还钱50万”，那么你只能输出“金额”。"\
        + "例如用户说“合计利息5万”，那么只能输出“利息”" \
        + "例如用户说：“本金10万，利息1万”，那么你需要输出“金额、利息”。"\
        + "例如用户所说内容与金额、利息无关，你需要输出：“无关”。" \
        + "注意，你只需要输出要求的内容，不要输出任何额外内容。"\
        + "用户给的回答是："+ content \
        + "你的输出是："

        SparkApi.answer = ""
        prompt = GetText("user", prompt)
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
        info_response = GetText("assistant", SparkApi.answer)[0]["content"]
        print("--后台提取信息："+info_response)
        
        if "金额" in info_response and "利息" in info_response:
            content += '并要求被告承担本次诉讼所有相关费用'
            # 传给星火转写成法律文书
            prompt_Request = "你是一名法律工作者，负责帮助客户撰写法律文书。下面是一段用户的诉求：" + content + "。把用户的诉求逐点用起诉状中法律诉求的形式重新表述。" \
            +"输出格式：\n1. 判令被告返还原告借款本金人民币xxx元。\n"\
            +"2. 判令被告支付原告逾期利息xxx元。\n"\
            +"3. 被告承担本次诉讼所有相关费用。\n"\
            + "你需要注意语言的书面化，避免口语化。只需输出“诉讼请求”部分，不要有额外内容。" #格式：1. 2. 3.            
            SparkApi.answer = ""
            prompt_Request = GetText("user", prompt_Request)
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt_Request)
            info_response_request = GetText("assistant", SparkApi.answer)[0]["content"]
            print("--后台提取信息："+info_response_request)
            return True, CleanData(info_response_request)
        
        # 后续改进：分别提示用户补齐缺失内容
        else: 
            return False, ""

    # 交通
    elif Case_Type == 2:
        prompt += "费用、补偿。"\
        + "用户给的回答是："+ content  \
        + "当用户提及相关内容时，输出：\"完整\"。\n"\
        + "注意，你只需要输出要求的内容，不要输出任何额外内容。你的输出是："

        SparkApi.answer = ""
        prompt = GetText("user", prompt)
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
        info_response = GetText("assistant", SparkApi.answer)[0]["content"]
        print("--后台提取信息："+info_response)

        if "完整" in info_response or ("补偿" in info_response and "费用" in info_response):
            # 传给星火转写成法律文书
            content += '并要求被告承担本次诉讼所有相关费用'
            prompt_Request = "你是一名法律工作者，负责帮助客户撰写法律文书。下面是一段用户的诉求：“" + content + "”  把用户需求逐点用数字分别列出，然后用书面语改写，注意符合法律文书风格。格式参考如下，注意只是按照格式结构输出。" \
            + "示例：用户提出：“别的我也不要什么，首先把我的医疗费5000交一下，然后住院住了10天，住院费2000，中间也没法干活，停工了，误工费3000。然后他还骂我，得跟我道歉，必须道歉，还要赔精神损失费100，加起来就是一万零一百块。”，你需要输出：\n " \
            + "1，赔偿医疗费用5000元人民币，住院费用2000元人民币 \n " \
            + "2，因交通事故导致的误工费3000元\n" \
            + "3，精神损失费100元。"
            SparkApi.answer = ""
            prompt_Request = GetText("user", prompt_Request)
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt_Request)
            info_response_request = GetText("assistant", SparkApi.answer)[0]["content"]
            print("--后台提取信息："+info_response_request)
            return True, CleanData(info_response_request)
        
        else :
            return False, ""

    # 其他
    else:
        prompt_Request = "你是一名法律工作者，负责帮助客户撰写法律文书。下面是一段用户的诉求：“" + content + "”  把用户需求逐点用数字分别列出，然后用书面语改写，注意符合法律文书风格。格式参考如下。" \
            + "例如，用户提出：“别的我也不要什么，首先把我的医疗费5000交一下，然后住院住了10天，住院费2000，中间也没法干活，停工了，误工费3000。然后他还骂我，得跟我道歉，必须道歉，还要赔精神损失费100，加起来就是一万零一百块。”，你需要输出：\n " \
            + "1，赔偿医疗费用5000元人民币，住院费用2000元人民币 \n " \
            + "2，因交通事故导致的误工费3000元\n" \
            + "3，精神损失费100元。"
        SparkApi.answer = ""
        prompt_Request = GetText("user", prompt_Request)
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt_Request)
        info_response_request = GetText("assistant", SparkApi.answer)[0]["content"]
        print("--后台提取信息："+info_response_request)
        info_response_request = info_response_request.replace("诉讼请求：", "")
        return True, CleanData(info_response_request)

def CheckWholeStory(content, appid, api_key, api_secret, Spark_url, domain,case_type): # 以原告被告口吻描述
    prompt_Request = "你是一个法律顾问。你需要根据用户的要求，生成正事实和理由部分的描写。注意：只需要输出事实和证据，以正规合法的格式输出。下面是一段用户的经历描述：\n"\
        + content\
        +"\n用书面语改写，注意符合法律文书风格。\n"\
        +"输出格式（事实与理由陈述）：\n"\
        +"1. xxx\n"\
        +"2. xxx\n"\
        +"3. xxx\n"\
        +"注意只能按照以上格式结构输出，且只能从经历描述当中提取信息，其中人称以原告、被告口吻描述。\n"
    SparkApi.answer = ""
    prompt_Request = GetText("user", prompt_Request)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt_Request)
    info_response_request = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--后台提取信息："+info_response_request)
    return True, CleanData(info_response_request)

def CheckCourt(content, appid, api_key, api_secret, Spark_url, domain):
    prompt = " 你是一个找法院的专家，接下来，我需要你根据我给出的文本，找出我应该去的法院。"\
            +" 如果我的文本中已经包含了某法院，你直接输出该法院名称"\
            +" 如果我的文本中只有一个地址，你需要输出离该地址最近的法院名称"\
            +" 我的文本是："+content\
            +" 你的输出只包含法院名称，例如“天津市第二中级人民法院”"\
            +" 你的输出是："
    SparkApi.answer = ""
    prompt = GetText("user", prompt)
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, prompt)
    info_response = GetText("assistant", SparkApi.answer)[0]["content"]
    print("--后台提取信息："+info_response)
    if '无法' in info_response or 'xx' in info_response:
        return False, ""
    else:
        return True, CleanData(info_response)