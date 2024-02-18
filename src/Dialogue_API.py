import os
import json
import argparse
import sys
from utils import ProcessResponse, PromptGeneration
from gen_doc import generate_docx

"""

Message_Stage代表对话状态:
    0: 收到【案由类别】，返回【收到信息】和【询问原告信息】
    1: 收到【原告信息】，返回【报错+重新输入】或【询问被告信息】
    2: 收到【被告信息】，返回【报错+重新输入】或【询问诉讼请求】
    3: 收到【诉讼请求】，返回【报错+重新输入】或【询问案件经过】
    4: 收到【案件经过】，返回【报错+重新输入】或【一切OK 正在生成】
    
Case_Type代表案件类别：
    1: 借贷纠纷
    2: 机动车事故纠纷
    3: 其他案由
    4: 不符，重输【TODO】

"""

name_C2E = {
    '案由': 'type',
    '原告姓名': 'pl_name_',
    '原告民族': 'pl_race_',
    '原告住址': 'pl_home_',
    '原告身份证号': 'pl_id_',
    '原告电话号码': 'pl_phone_',
    "原告公司名称": 'pl_policy_name_',
    "原告企业负责人姓名": 'pl_agent_name_',
    "原告公司所在地址": 'pl_policy_address_',
    "原告企业负责人职务": 'pl_agent_job_',
    "原告企业负责人电话": 'pl_agent_phone',
    
    '被告姓名': 'de_name_',
    '被告民族': 'de_race_',
    '被告住址': 'de_home_',
    '被告身份证号': 'de_id_',
    '被告电话号码': 'de_phone_',
    '被告车牌号': 'de_carnum_',
    "被告公司名称": 'de_policy_name_',
    "被告企业负责人姓名": 'de_agent_name_',
    "被告公司所在地址": 'de_policy_address_',
    "被告企业负责人职务": 'de_agent_job_',
    "被告企业负责人电话": 'de_agent_phone',
    
    
}

def Str2Num(content:str):
    one = ['1', '一','壹','Ⅰ']
    two = ['2', '二', '两','俩','贰','Ⅱ']
    three = ['3', '三', '仨', '叁', 'Ⅲ']
    four = ['4', '四', '肆', 'Ⅳ']
    five = ['5', '五', '伍', 'Ⅴ']
    
    numbers = [one, two, three, four, five]

    for num in numbers:
        for elem in num:
            if elem in content:
                return int(num[0])# 1 2 3 4 5
    return -1

def ReturnAfterKnownCase(result_dict: dict, tmp_dict_dir: str, input_string: str = None, Message_Stage: int = None, Case_Type: int = None):
    """收到【案由类别】，返回【收到信息】和【询问原告信息】

    Args:
        result_dict (dict): 目前收到信息集合
        tmp_dict_dir (str): 收集信息JSON存储路径
        input_string (str, optional): 对话中收到的用户语句. Defaults to None.
        Message_Stage (int, optional): 取值为1. Defaults to None.
        Case_Type (int, optional): 案件类别. Defaults to None.

    Returns:
        _type_: 输出语句, Message_Stage, Case_Type
    """
    
    if "借贷" in input_string and "民间" in input_string:
        Case_Type = 1
        # result_dict["案由"] = "民间借贷纠纷"
        result_dict["type"] = "1"
    elif "交通事故" in input_string and "机动车" in input_string:
        Case_Type = 2
        # result_dict["案由"] = "机动车交通事故责任纠纷"
        result_dict["type"] = "2"
    else:
        Case_Type = 3
        # result_dict["案由"] = input_string
        result_dict["type"] = "3"

    with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, ensure_ascii=False, indent=2)

    pl_num_guide = PromptGeneration.GenAfterKnownCaseTypeGuide(Case_Type) + PromptGeneration.GenPlaintiffNumGuide()
    print('模型：'+pl_num_guide)
    Message_Stage = 1
    
    return pl_num_guide, Message_Stage, Case_Type

def ReturnNum(result_dict, tmp_dict_dir, input_string, Message_Stage, Case_Type, appid, api_key, api_secret, Spark_url, domain):
    if Message_Stage == 1:
        print('用户：'+input_string)
        with open(tmp_dict_dir, 'r', encoding='utf-8') as file:
            result_dict = json.load(file)
        cur_pl_num = 0
        for k in result_dict.keys():
            if 'pl_name' in k or 'pl_policy_name' in k:
                cur_pl_num += 1
        if 'pl_num' in result_dict.keys():
            return int(result_dict['pl_num']), cur_pl_num, True
        else:
            result_dict['pl_num'] = Str2Num(input_string)
            print(result_dict['pl_num'])
            with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
                json.dump(result_dict, file, ensure_ascii=False, indent=2)
            return result_dict['pl_num'], cur_pl_num, False
    # chat_id= 名字+_+uid 
    elif Message_Stage == 2:
        print('用户：'+input_string)
        with open(tmp_dict_dir, 'r', encoding='utf-8') as file:
            result_dict = json.load(file)
        cur_de_num = 0
        for k in result_dict.keys():
            if 'de_name' in k or 'de_policy_name' in k:
                cur_de_num += 1
        if 'de_num' in result_dict.keys():
            return int(result_dict['de_num']), cur_de_num, True
        else:
            result_dict['de_num'] = Str2Num(input_string)
            print(result_dict['de_num'])
            with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
                json.dump(result_dict, file, ensure_ascii=False, indent=2)
            return int(result_dict['de_num']), cur_de_num, False

def ReturnCheckMore(result_dict, tmp_dict_dir, collected_info, total_num, cur_num, input_string=None, Message_Stage=None, Case_Type=None):
    if Message_Stage == 1:
        Cur_Num_Guide = "现在请您输入第"+str(cur_num+2)+"个原告（人或公司）的信息：\n\n"
        Next_pl_Guide = PromptGeneration.GenPlaintiffInfoGuide()
        Next_Guide = Cur_Num_Guide + Next_pl_Guide
        print('模型：'+Next_Guide)
        info_list = collected_info.split('；')
        for info in info_list:
            if '：' not in info:
                continue
            result_dict[name_C2E['原告'+ProcessResponse.CleanData(info.split('：')[0])]+str(cur_num+1)] = ProcessResponse.CleanData(info.split('：')[1])
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
        return Next_Guide, Message_Stage, Case_Type
    elif Message_Stage == 2:
        Cur_Num_Guide = "现在请您输入第"+str(cur_num+2)+"个被告（人或公司）的信息：\n\n"
        Next_de_Guide = PromptGeneration.GenDefendantInfoGuide()
        Next_Guide = Cur_Num_Guide + Next_de_Guide
        print('模型：'+Next_Guide)
        info_list = collected_info.split('；')
        for info in info_list:
            if '：' not in info:
                continue
            result_dict[name_C2E['被告'+ProcessResponse.CleanData(info.split('：')[0])]+str(cur_num+1)] = ProcessResponse.CleanData(info.split('：')[1])
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
        return Next_Guide, Message_Stage, Case_Type

def ReturnCheckOK(result_dict, tmp_dict_dir, collected_info, cur_num=None, input_string=None, Message_Stage=None, Case_Type=None):
    """收到用户【传入的信息】，检查合格，返回下一个【询问】

    Args:
        result_dict (dict): 目前收到信息集合
        tmp_dict_dir (str): 收集信息JSON存储路径
        collected_info (_type_): 用户语句经过处理后，收集的信息
        input_string (str, optional): 对话中收到的用户语句. Defaults to None.
        Message_Stage (int, optional): 对话状态. Defaults to None.
        Case_Type (int, optional): 案件类别. Defaults to None.

    Returns:
        _type_: 输出语句, Message_Stage, Case_Type
    """

    print('用户：'+input_string)
    if Message_Stage == 1: # 【原告阶段】CheckOK
        Message_Stage = 2 # 转【被告阶段】
        Next_Guide = PromptGeneration.GenDefendantNumGuide()
        print('模型：'+Next_Guide)
        info_list = collected_info.split('；')
        for info in info_list:
            if '：' not in info:
                continue
            result_dict[name_C2E['原告'+ProcessResponse.CleanData(info.split('：')[0])]+str(cur_num+1)] = ProcessResponse.CleanData(info.split('：')[1])
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
    elif Message_Stage == 2: # 【被告阶段】CheckOK
        Message_Stage =  3 # 转【诉讼请求】
        Next_Guide = PromptGeneration.GenAccuseRequestGuide(Case_Type)
        print('模型：'+Next_Guide)
        info_list = collected_info.split('；')
        for info in info_list:
            if '：' not in info:
                continue
            result_dict[name_C2E['被告'+ProcessResponse.CleanData(info.split('：')[0])]+str(cur_num+1)] = ProcessResponse.CleanData(info.split('：')[1])
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
    elif Message_Stage == 3:
        Message_Stage =  4
        Next_Guide = PromptGeneration.GenWholeStoryGuide(Case_Type)
        print('模型：'+Next_Guide)
        result_dict['requests'] = collected_info
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
    elif Message_Stage == 4:
        Message_Stage = 5
        Next_Guide = PromptGeneration.GenCourtGuide()
        print('模型：'+Next_Guide)
        result_dict['case'] = collected_info
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
    elif Message_Stage == 5:
        Message_Stage = 6
        Next_Guide = PromptGeneration.GenFinalGuide()
        print('模型：'+Next_Guide)
        result_dict['court'] = collected_info
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
    
    return Next_Guide, Message_Stage, Case_Type

def ReturnRegenerate(result_dict, tmp_dict_dir, input_string=None, Message_Stage=None, Case_Type=None, Need_Time=None):
    """收到【传入的信息】，检查不合格，返回【报错+重新输入提示】

    Args:
        result_dict (dict): 目前收到信息集合
        tmp_dict_dir (str): 收集信息JSON存储路径
        collected_info (_type_): 用户语句经过处理后，收集的信息
        input_string (str, optional): 对话中收到的用户语句. Defaults to None.
        Message_Stage (int, optional): 对话状态. Defaults to None.
        Case_Type (int, optional): 案件类别. Defaults to None.

    Returns:
        _type_: 输出语句, Message_Stage, Case_Type
    """
    
    print('用户：'+input_string)
    
    error_guide = PromptGeneration.GenErrorGuide()
    print('模型：'+error_guide)
    
    Need_Time = 1
    if Message_Stage == 0:
        regenerate_guide = PromptGeneration.GenCaseTypeGuide()
        print('模型：'+regenerate_guide)
        if 'CaseType_Times' not in result_dict.keys():
            result_dict['CaseType_Times'] = 1
        else:
            result_dict['CaseType_Times'] += 1
        Need_Time = result_dict['CaseType_Times']
    elif Message_Stage == 1:
        regenerate_guide = PromptGeneration.GenPlaintiffInfoGuide()
        if 'pl_Times' not in result_dict.keys():
            result_dict['pl_Times'] = 1
        else:
            result_dict['pl_Times'] += 1
        Need_Time = result_dict['pl_Times']
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
        print('模型：'+ input_string + '\n' + error_guide)
        # return input_string + '\n' + error_guide + '\n' + regenerate_guide, Message_Stage, Case_Type, Need_Time
        return input_string + '\n' + error_guide, Message_Stage, Case_Type, Need_Time
    elif Message_Stage == 2:
        regenerate_guide = PromptGeneration.GenDefendantInfoGuide()
        if 'de_Times' not in result_dict.keys():
            result_dict['de_Times'] = 1
        else:
            result_dict['de_Times'] += 1
        Need_Time = result_dict['de_Times']
        with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=2)
        print('模型：'+ input_string + '\n' + error_guide)
        # return input_string + '\n' + error_guide + '\n' + regenerate_guide, Message_Stage, Case_Type, Need_Time
        return input_string + '\n' + error_guide, Message_Stage, Case_Type, Need_Time
    elif Message_Stage == 3:
        regenerate_guide = PromptGeneration.GenAccuseRequestGuide(Case_Type)
        print('模型：'+regenerate_guide)
        if 'AccuseRequest_Times' not in result_dict.keys():
            result_dict['AccuseRequest_Times'] = 1
        else:
            result_dict['AccuseRequest_Times'] += 1
        Need_Time = result_dict['AccuseRequest_Times']
    elif Message_Stage == 4:
        regenerate_guide = PromptGeneration.GenWholeStoryGuide(Case_Type)
        print('模型：'+regenerate_guide)
        if 'WholeStory_Times' not in result_dict.keys():
            result_dict['WholeStory_Times'] = 1
        else:
            result_dict['WholeStory_Times'] += 1
        Need_Time = result_dict['WholeStory_Times']
    elif Message_Stage == 5:
        regenerate_guide = PromptGeneration.GenCourtGuide()
        print('模型：'+regenerate_guide)
        if 'Court_Times' not in result_dict.keys():
            result_dict['Court_Times'] = 1
        else:
            result_dict['Court_Times'] += 1
        Need_Time = result_dict['Court_Times']
        
    with open(tmp_dict_dir, 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, ensure_ascii=False, indent=2)
    return error_guide + '\n' + regenerate_guide, Message_Stage, Case_Type, Need_Time
        

# 主接口
def GiveModelSentence(input_string:str = None, Message_Stage:int = None, Case_Type:int = None, Chat_ID:str = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--tmp_dict_dir',
                        type=str,
                        default='./output/result_dict_'+Chat_ID+'.json',
                        help='如果使用语句文件Debug，文件所在路径'
                        )
    parser.add_argument('--appid',
                        type=str,
                        default='f54bca1a',
                        help='填写控制台中获取的 APPID 信息'
                        )
    parser.add_argument('--api_secret',
                        type=str,
                        default='ZGJmMjY3YWFmNGY5N2Q1YWMwOGZlMjFh',
                        help='填写控制台中获取的 APISecret 信息'
                        )
    parser.add_argument('--api_key',
                        type=str,
                        default='2e7516edf376713eb5d99fc812a87ed5',
                        help='填写控制台中获取的 APIKey 信息'
                        )
    parser.add_argument('--domain',
                        type=str,
                        # default='plugin',
                        default='generalv2',
                        help='用于配置大模型版本，默认“generalv2”'
                        )
    parser.add_argument('--Spark_url',
                        type=str,
                        # default='ws://spark-api-knowledge.xf-yun.com/v2.1/multimodal',
                        default="ws://spark-api.xf-yun.com/v2.1/chat",
                        help='云端环境的服务地址'
                        )
    args = parser.parse_args()
    
    result_dict = {}
    os.makedirs('./output/', exist_ok=True)
    Need_Time = 0
    
    last_underscore_index = args.tmp_dict_dir.rfind('_')  # Find the index of the last underscore
    if last_underscore_index != -1:  # If an underscore is found
        args.tmp_dict_dir = args.tmp_dict_dir[last_underscore_index + 1:]
    args.tmp_dict_dir = './output/result_dict_' + args.tmp_dict_dir
    
    if Case_Type == 0:
        os.makedirs('./output/', exist_ok=True)
        with open(args.tmp_dict_dir, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=2)
    
    with open(args.tmp_dict_dir, 'r', encoding='utf-8') as file:
        result_dict = json.load(file)
    
    if Message_Stage == 0:
        check_result, collected_info = ProcessResponse.CheckCaseType(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if check_result:
            Next_Guide, Message_Stage, Case_Type = ReturnAfterKnownCase(result_dict, args.tmp_dict_dir, collected_info, Message_Stage, Case_Type)
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type)
        return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 1:
        pl_num, cur_pl_num, after_check = ReturnNum(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if after_check == False:
            print("好的，请您输入第1个原告（人或公司）的信息: \n" + PromptGeneration.GenPlaintiffInfoGuide())
            return "好的，请您输入第1个原告（人或公司）的信息: \n" + PromptGeneration.GenPlaintiffInfoGuide(), Message_Stage, Case_Type, Need_Time, 0
        check_result, collected_info, is_company = ProcessResponse.CheckPlaintiff(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if check_result:
            result_dict['pl_type_'+str(cur_pl_num+1)] = is_company
            with open(args.tmp_dict_dir, 'w', encoding='utf-8') as file:
                json.dump(result_dict, file, ensure_ascii=False, indent=2)
            if cur_pl_num+1 >= pl_num:
                Next_Guide, Message_Stage, Case_Type = ReturnCheckOK(result_dict, args.tmp_dict_dir, collected_info, cur_pl_num, input_string, Message_Stage, Case_Type)
            else:
                Next_Guide, Message_Stage, Case_Type = ReturnCheckMore(result_dict, args.tmp_dict_dir, collected_info, pl_num, cur_pl_num, input_string, Message_Stage, Case_Type)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 1
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, collected_info, Message_Stage, Case_Type)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 2:
        de_num, cur_de_num, after_check = ReturnNum(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if after_check == False:
            print("好的，请您输入第1个被告（人或公司）的信息: \n" + PromptGeneration.GenDefendantInfoGuide())
            return "好的，请您输入第1个被告（人或公司）的信息: \n" + PromptGeneration.GenDefendantInfoGuide(), Message_Stage, Case_Type, Need_Time, 0
        check_result, collected_info, is_company = ProcessResponse.CheckDefendant(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if check_result:
            result_dict['de_type_'+str(cur_de_num+1)] = is_company
            with open(args.tmp_dict_dir, 'w', encoding='utf-8') as file:
                json.dump(result_dict, file, ensure_ascii=False, indent=2)
            if cur_de_num+1 >= de_num:
                Next_Guide, Message_Stage, Case_Type = ReturnCheckOK(result_dict, args.tmp_dict_dir, collected_info, cur_de_num, input_string, Message_Stage, Case_Type)
            else:
                Next_Guide, Message_Stage, Case_Type = ReturnCheckMore(result_dict, args.tmp_dict_dir, collected_info, de_num, cur_de_num, input_string, Message_Stage, Case_Type)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 1
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, collected_info, Message_Stage, Case_Type)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 3:
        check_result, collected_info = ProcessResponse.CheckAccuseRequest(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain, Case_Type)
        if check_result:
            Next_Guide, Message_Stage, Case_Type = ReturnCheckOK(result_dict, args.tmp_dict_dir, collected_info, None, input_string, Message_Stage, Case_Type)
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type)
        return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 4:
        check_result, collected_info = ProcessResponse.CheckWholeStory(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain, Case_Type)
        if check_result:
            Next_Guide, Message_Stage, Case_Type = ReturnCheckOK(result_dict, args.tmp_dict_dir, collected_info, None, input_string, Message_Stage, Case_Type)
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type)
        return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 5:
        if "自动" in input_string:
            input_string = result_dict['pl_home_1']
        check_result, collected_info = ProcessResponse.CheckCourt(input_string, args.appid, args.api_key, args.api_secret, args.Spark_url, args.domain)
        if check_result:
            Next_Guide, Message_Stage, Case_Type = ReturnCheckOK(result_dict, args.tmp_dict_dir, collected_info, None, input_string, Message_Stage, Case_Type)
            # isFile = generate_docx.getdocx(args.tmp_dict_dir, Chat_ID)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
        else:
            Next_Guide, Message_Stage, Case_Type, Need_Time = ReturnRegenerate(result_dict, args.tmp_dict_dir, input_string, Message_Stage, Case_Type)
            return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    elif Message_Stage == 6:
        Next_Guide = "您的起诉状已经生成好，点击下载就可以啦！"
        print(Next_Guide)
        return Next_Guide, Message_Stage, Case_Type, Need_Time, 0
    
