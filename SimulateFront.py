import json
import os
import sys
import json
import argparse

sys.path.append('..')
from src import Dialogue_API
from utils import ProcessResponse, PromptGeneration
Message_Stage, Case_Type = 0, 0

if __name__ == '__main__':
    chat_id = "NIUBEE"
    file_path = './data/TestDialogue3.json'
    out_dict_path = './gen_doc/result_dict_'+chat_id+'.json'
    is_debug = True
    # os.makedirs('./gen_doc/', exist_ok=True)
    # with open(out_dict_path, 'w', encoding='utf-8') as file:
    #     result_dict = json.dump({}, file, ensure_ascii=False)
    
    sentence_list = []
    print(PromptGeneration.GenFirstGuide())
    if is_debug:
        # while(1):
        #     data = input('用户：')
        #     Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type, chat_id)
        Max_Stage = 6
        
        # 标记原告信息、被告信息、诉讼请求、事情经过 所在阶段
        Plaintiff_Stage = 1
        Defendent_Stage = 2
        Request_Stage = 3
        What_Happened_Stage = 4

        
        # 至多三轮对话
        Max_Round = 3
        # 存放信息
        data = ""

        while Message_Stage <= Max_Stage:
            before_Message_Stage = Message_Stage

            # 原被告信息填充阶段
            if Message_Stage in [Plaintiff_Stage, Defendent_Stage]:
                for _ in range(Max_Round + 1):
                    data += (input('用户：') + ' ' )

                    Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type,Chat_ID = chat_id)
                    if before_Message_Stage != Message_Stage or is_Final == -1:
                        data = ''
                        break
                else:
                    data += '身份证：10000000000000， 电话111111000000， 民族汉族，住在北京市朝阳区北大街11号。'
                    Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type,Chat_ID=chat_id)
                data = ''

            # 诉求、事情经过与原因阶段
            if Message_Stage in [Request_Stage, What_Happened_Stage]:
                for _ in range(Max_Round + 1):
                    data += (input('用户：') + '；' )
                    Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type,Chat_ID=chat_id)
                    if before_Message_Stage != Message_Stage:
                        data = ''
                        break
                else:
                    if Case_Type == 1:
                        data += '所欠总金额100000万，利息合计1000000万'
                    elif Case_Type == 2:
                        data += '医疗费总计100000万，精神损失费100000万'
                    else:
                        data += ''

                    
                    Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type,Chat_ID=chat_id)
                data = ''

            # 其余阶段
            else:
                data += (input('用户：'))
                Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type,Chat_ID=chat_id)
                if before_Message_Stage != Message_Stage:
                    data = ''
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)['content']
                Return_String, Message_Stage, Case_Type, is_Final = Dialogue_API.GiveModelSentence(data, Message_Stage, Case_Type, chat_id)