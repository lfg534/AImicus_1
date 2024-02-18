from helper import *
import streamlit as st
import uuid
import copy
import pandas as pd
# import openai
from requests.models import ChunkedEncodingError
from streamlit.components import v1
from voice_toolkit import voice_toolkit
import sys
from io import BytesIO
from docx import Document
from generate_docx import getdocx
from src import Dialogue_API

sys.path.append('.src')

st.set_page_config(page_title='AImicus', layout='wide', page_icon='🤖')
# 自定义元素样式
st.markdown(css_code, unsafe_allow_html=True)

#后端所需常数
Max_Stage = 6
# 标记原告信息、被告信息、诉讼请求、事情经过 所在阶段
Plaintiff_Stage = 1
Defendent_Stage = 2
Request_Stage = 3
What_Happened_Stage = 4
# 至多三轮对话
Max_Round = 3
# 存放信息

if "initial_settings" not in st.session_state:
    # 历史聊天窗口
    st.session_state["path"] = 'history_chats_file'
    st.session_state['history_chats'] = get_history_chats(st.session_state["path"])
    # ss参数初始化
    st.session_state['delete_dict'] = {}
    st.session_state['delete_count'] = 0
    st.session_state['voice_flag'] = ''
    st.session_state['user_voice_value'] = ''
    st.session_state['error_info'] = ''
    st.session_state["current_chat_index"] = 0
    st.session_state['message_stage'] = 0
    st.session_state['person_data'] = ''
    st.session_state['person_count'] = 0
    st.session_state['case_type'] = 0
    st.session_state['user_input_content'] = ''
    st.session_state['chat_id'] = ''
    st.session_state['is_final'] = 0

    
    # 读取全局设置
    if os.path.exists('./set.json'):
        with open('./set.json', 'r', encoding='utf-8') as f:
            data_set = json.load(f)
        for key, value in data_set.items():
            st.session_state[key] = value
    # 设置完成
    st.session_state["initial_settings"] = True

with st.sidebar:
    st.markdown("# 🤖 聊天窗口")
    # 创建容器的目的是配合自定义组件的监听操作
    chat_container = st.container()
    with chat_container:
        current_chat = st.radio(
            label='历史聊天窗口',
            format_func=lambda x: x.split('_')[0] if '_' in x else x,
            options=st.session_state['history_chats'],
            # label_visibility= "hidden",
            index=st.session_state["current_chat_index"],
            key='current_chat' + st.session_state['history_chats'][st.session_state["current_chat_index"]],
            # on_change=current_chat_callback  # 此处不适合用回调，无法识别到窗口增减的变动
        )

        st.session_state['chat_id'] = current_chat
        #print(current_chat)
        
        if current_chat +'message_stage' not in st.session_state:
        #if current_chat not in st.session_state:
            #print('看看会不会被复原')
            st.session_state[current_chat +'message_stage'] = st.session_state['message_stage']
            st.session_state[current_chat + 'person_data'] = st.session_state['person_data']
            st.session_state[current_chat + 'case_type'] = st.session_state['case_type'] 
            st.session_state[current_chat + 'is_final'] = st.session_state['is_final']
            st.session_state[current_chat + 'person_count'] = st.session_state['person_count']
            #print("第一次初始化该对话id的message_stage",st.session_state[current_chat +'message_stage'])
        else :
            pass
            #print("已经有之前的message_stage",st.session_state[current_chat +'message_stage'])
        
    st.write("---")


# 数据写入文件
def write_data(new_chat_name = current_chat):
    
    print('save_data 前 message_stage', st.session_state[current_chat +'message_stage'],)
    save_data(st.session_state["path"],
              new_chat_name, 
              st.session_state["history" + current_chat], 
              st.session_state[current_chat +'message_stage'],
              st.session_state[current_chat +'case_type'],
              st.session_state[current_chat + 'is_final'],
              st.session_state[current_chat + 'person_data'],
              st.session_state[current_chat + 'person_count']
              )

#-----------有些需要新命名的--------------
def reset_chat_name_fun(chat_name):
    # chat_name = chat_name + '_' + str(uuid.uuid4())
    current_chat_uid = current_chat[current_chat.rfind('_'):]
    new_name = filename_correction(chat_name)+current_chat_uid
    # new_name = filename_correction(chat_name)
    current_chat_index = st.session_state['history_chats'].index(current_chat)
    st.session_state['history_chats'][current_chat_index] = new_name
    st.session_state["current_chat_index"] = current_chat_index
    # 写入新文件
    write_data(new_name)
    # 转移数据
    st.session_state['history' + new_name] = st.session_state['history' + current_chat]
    #for item in ["context_select", "context_input", "context_level", *initial_content_all['paras']]:
        #st.session_state[item + new_name + "value"] = st.session_state[item + current_chat + "value"]
    remove_data(st.session_state["path"], current_chat)

#------------新建页面有些需要更新-----------
def create_chat_fun():
    st.session_state['history_chats'] = ['New Chat_' + str(uuid.uuid4())] + st.session_state['history_chats']
    st.session_state["current_chat_index"] = 0
    #在重新生成一个页面的时候,状态里面的stepid也要更新为第一步
    #先创建页面 然后生成唯一标识符号
    st.session_state['message_stage'] = 0
    st.session_state['person_count'] = 0
    st.session_state['case_type']  =  0
    st.session_state['person_data'] = ''


def delete_chat_fun():
    if len(st.session_state['history_chats']) == 1:
        chat_init = 'New Chat_' + str(uuid.uuid4())
        st.session_state['history_chats'].append(chat_init)
    pre_chat_index = st.session_state['history_chats'].index(current_chat)
    if pre_chat_index > 0:
        st.session_state["current_chat_index"] = st.session_state['history_chats'].index(current_chat) - 1
    else:
        st.session_state["current_chat_index"] = 0
    st.session_state['history_chats'].remove(current_chat)
    remove_data(st.session_state["path"], current_chat)


with st.sidebar:
    c1, c2 = st.columns(2)
    create_chat_button = c1.button('新建',  key='create_chat_button')
    if create_chat_button:
        create_chat_fun()
        js = """
            window.scrollTo({
            left: 0,
            top: 0,
            behavior: 'smooth'
        })
        """
        html = f'<script>{js}</script>'
        st.write(html, unsafe_allow_html=True)
        st.experimental_rerun()

    delete_chat_button = c2.button('删除', key='delete_chat_button')
    if delete_chat_button:
        delete_chat_fun()
        st.experimental_rerun()

with st.sidebar:
    if ("set_chat_name" in st.session_state) and st.session_state['set_chat_name'] != '':
        reset_chat_name_fun(st.session_state['set_chat_name'])
        st.session_state['set_chat_name'] = ''
        # st.session_state["initial_settings"] = True
        st.experimental_rerun()

    st.write("\n")
    st.write("\n")
    st.text_input("设定窗口名称：", key="set_chat_name", placeholder="点击输入")
    # st.selectbox("选择模型：", index=0, options=['gpt-3.5-turbo', 'gpt-4'], key="select_model")
    st.write("\n")
    st.caption("""
    - 双击页面可直接定位输入栏
    - Ctrl + Enter 可快捷提交问题
    """)
    # st.markdown('<a href="https://github.com/PierXuY/ChatGPT-Assistant" target="_blank" rel="ChatGPT-Assistant">'
    #             '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=ChatGPT Assistant" alt="GitHub">'
    #             '</a>', unsafe_allow_html=True)

# 加载数据
if "history" + current_chat not in st.session_state:
    for key, value in load_data(st.session_state["path"], current_chat).items():
        if key == 'history':
            st.session_state[key + current_chat] = value
        else:
            #for k, v in value.items():
                #st.session_state[k + current_chat + "value"] = v
            st.session_state[current_chat + key] = value
            #print("看看能不能提取到之前存储的message_stage",st.session_state[current_chat + "message_stage"])
                

# 保证不同chat的页面层次一致，否则会导致自定义组件重新渲染
container_show_messages = st.container()
container_show_messages.write("")
# 对话展示
with container_show_messages:
    if st.session_state["history" + current_chat]:
        show_messages(current_chat, st.session_state["history" + current_chat])

# 核查是否有对话需要删除
if any(st.session_state['delete_dict'].values()):
    for key, value in st.session_state['delete_dict'].items():
        try:
            deleteCount = value.get("deleteCount")
        except AttributeError:
            deleteCount = None
        if deleteCount == st.session_state['delete_count']:
            delete_keys = key
            st.session_state['delete_count'] = deleteCount + 1
            delete_current_chat, idr = delete_keys.split('>')
            df_history_tem = pd.DataFrame(st.session_state["history" + delete_current_chat])
            df_history_tem.drop(index=df_history_tem.query("role=='user'").iloc[[int(idr)], :].index, inplace=True)
            df_history_tem.drop(index=df_history_tem.query("role=='assistant'").iloc[[int(idr)], :].index, inplace=True)
            st.session_state["history" + delete_current_chat] = df_history_tem.to_dict('records')
            write_data()
            st.experimental_rerun()


def callback_fun(arg):
    # 连续快速点击新建与删除会触发错误回调，增加判断
    if ("history" + current_chat in st.session_state) and ("frequency_penalty" + current_chat in st.session_state):
        write_data()
        st.session_state[arg + current_chat + "value"] = st.session_state[arg + current_chat]


def clear_button_callback():
    st.session_state['history' + current_chat] = []
    write_data()


def save_set(arg):
    st.session_state[arg + "_value"] = st.session_state[arg]
    with open("./set.json", 'w', encoding='utf-8') as f:
        json.dump({"open_voice_toolkit_value": st.session_state['open_voice_toolkit']}, f)


# 输入内容展示
area_user_svg = st.empty()
area_user_content = st.empty()
# 回复展示
area_gpt_svg = st.empty()
area_gpt_content = st.empty()
# 报错展示
area_error = st.empty()

st.write("\n")
st.header('AImicus - 起诉状生成小助手')
tap_input, tab_func = st.tabs(['💬 对话', '🛠️ 功能'])

with tab_func:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("清空对话",  on_click=clear_button_callback)
    with c2:
        btn = st.download_button(
            label="导出对话",
            data=download_history(st.session_state['history' + current_chat]),
            file_name=f'{current_chat.split("_")[0]}.md',
            mime="text/markdown",
            
        )
    with c3:
        #print('tap_input_test')
        if st.session_state[current_chat + 'is_final'] == 1:
            CHAT_ID = st.session_state[ 'chat_id']
            #这里要获取json路径
            chat_id = CHAT_ID[CHAT_ID.rfind('_')+1:]
            print('chatid: '+chat_id)
            json_id = 'result_dict_' + chat_id + '.json'
            print(json_id)
            VALUE_UNK = getdocx(f"./output/{json_id}",CHAT_ID) 

            if VALUE_UNK == 1:
                #这里其实应该等于chat_id
                document = Document(f'./output/起诉状_{CHAT_ID}.docx')
                buffer = BytesIO()
                document.save(buffer)
                st.download_button('下载起诉状', 
                           buffer.getvalue(), 
                           file_name= f'起诉状_{CHAT_ID}.docx', 
                           mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                           disabled = False,
                          )
            else :
                st.download_button('下载起诉状', BytesIO().getvalue(), file_name=f'起诉状_{CHAT_ID}.docx', mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document', disabled=True)
                # st.write("起诉状生成失败，请重新尝试。")
        else:
            # print('tap_input_false')
            pass
    st.write("\n")
    # st.markdown("自定义功能：")
    c2 = st.columns(1)[0]
    with c2:
        if "open_voice_toolkit_value" in st.session_state:
            default = st.session_state["open_voice_toolkit_value"]
        else:
            default = True
        st.checkbox("开启语音输入功能", value=default, key='open_voice_toolkit',
                    on_change=save_set, args=('open_voice_toolkit',))
with tap_input:
    def input_callback():
        if st.session_state['user_input_area'] != "":
            # 修改窗口名称
            user_input_content = st.session_state['user_input_area']
            df_history = pd.DataFrame(st.session_state["history" + current_chat])
            if df_history.empty or len(df_history.query('role!="system"')) == 0:
                new_name = extract_chars(user_input_content, 18)
                reset_chat_name_fun(new_name)


    with st.form("input_form", clear_on_submit=True):
        user_input = st.text_area("**输入：**", key="user_input_area",
                                  help="内容将以Markdown格式在页面展示，建议遵循相关语言规范，同样有利于小助手正确读取，例如："
                                       "\n- 代码块写在三个反引号内，并标注语言类型"
                                       "\n- 以英文冒号开头的内容或者正则表达式等写在单反引号内",
                                  value=st.session_state['user_voice_value'])
        submitted = st.form_submit_button("确认提交",  on_click=input_callback)
    if submitted:
        st.session_state['user_input_content'] = user_input
        st.session_state['user_voice_value'] = ''
        st.experimental_rerun()

    if "open_voice_toolkit_value" not in st.session_state or st.session_state["open_voice_toolkit_value"]:
        # 语音输入功能
        vocie_result = voice_toolkit()
        #print('vocie_result: %s', vocie_result)
        #print('session_state voice value %s', st.session_state['user_voice_value'])
        # vocie_result会保存最后一次结果
        if (vocie_result and vocie_result['voice_result']['flag'] == 'interim') or st.session_state['voice_flag'] == "interim":
            st.session_state['voice_flag'] = 'interim'
            st.session_state['user_voice_value'] = vocie_result['voice_result']['value']
            if vocie_result['voice_result']['flag'] == 'final':
                st.session_state['voice_flag'] = 'final'
                st.experimental_rerun()
    #print('tap_input')


def get_model_input():
    # 需输入的历史记录
    context_level = st.session_state['context_level' + current_chat]
    history = (get_history_input(st.session_state["history" + current_chat], context_level) +
               [{"role": "user", "content": st.session_state['pre_user_input_content']}])
    for ctx in [st.session_state['context_input' + current_chat],
                set_context_all[st.session_state['context_select' + current_chat]]]:
        if ctx != "":
            history = [{"role": "system", "content": ctx}] + history
    # 设定的模型参数
    '''
    paras = {
        "temperature": st.session_state["temperature" + current_chat],
        "top_p": st.session_state["top_p" + current_chat],
        "presence_penalty": st.session_state["presence_penalty" + current_chat],
        "frequency_penalty": st.session_state["frequency_penalty" + current_chat],
    }
    '''
    #return history, paras
    return history

def backend(req):
    #current_chat_message_stage = st.session_state[current_chat + 'message_stage']
    current_chat_case_type = st.session_state[current_chat + 'case_type']
    current_chat_chat_id = st.session_state['chat_id']
    current_chat_is_final = st.session_state[current_chat + 'is_final']
    current_chat_person_data = st.session_state[current_chat + 'person_data']
    current_chat_person_count = st.session_state[current_chat + 'person_count']
    print("current_chat_person_data", st.session_state[current_chat + 'person_data'])
    Message_Stage = st.session_state[current_chat + 'message_stage']

    before_Message_Stage = Message_Stage
            # 原被告信息填充阶段
    if Message_Stage in [Plaintiff_Stage, Defendent_Stage]:
        # print('_____________',current_chat_person_count, current_chat_person_data)
        if current_chat_person_count < Max_Round - 1: # < 2
            #data += (input('用户：') + ' ' )
            #这里不用做什么额外判定 因为只有到了原告多轮对话才会在这里 做好data的实时更新就行
            data = current_chat_person_data
            data += req
            Return_String, Message_Stage, Case_Type, person_count, is_change_people = Dialogue_API.GiveModelSentence(data, Message_Stage, current_chat_case_type, current_chat_chat_id)
            if before_Message_Stage != Message_Stage or is_change_people == 1:
                data = ''
                person_count = 0
                # break
        else:
            data = current_chat_person_data
            data += '身份证：10000000000000， 电话111111000000， 民族汉族，住在北京市朝阳区北大街11号。'
            Return_String, Message_Stage, Case_Type, person_count, _ = Dialogue_API.GiveModelSentence(data, Message_Stage,current_chat_case_type, current_chat_chat_id)
            data = ''
            person_count = 0
            return Return_String, Message_Stage, Case_Type, person_count, data
        # data = ''
        return Return_String, Message_Stage, Case_Type, person_count, data

            # 诉求、事情经过与原因阶段
    if Message_Stage in [Request_Stage, What_Happened_Stage]:
        if current_chat_person_count < Max_Round - 1:
            data = current_chat_person_data
            data += req
            Return_String, Message_Stage, Case_Type, person_count, _ = Dialogue_API.GiveModelSentence(data, Message_Stage, current_chat_case_type, current_chat_chat_id)
            if before_Message_Stage != Message_Stage:
                data = ''
                person_count = 0
                # break
            else:
                return Return_String, Message_Stage, Case_Type, person_count, data
        else:
            data = current_chat_person_data
            if Case_Type == 1:
                data += '所欠总金额100000万，利息合计1000000万'
            elif Case_Type == 2:
                data += '医疗费总计100000万，精神损失费100000万'
            else:
                data += ''
            Return_String, Message_Stage, Case_Type, person_count, _ = Dialogue_API.GiveModelSentence(data, Message_Stage, current_chat_case_type, current_chat_chat_id)
            return Return_String, Message_Stage, Case_Type, person_count, data
        # data = ''
        return Return_String, Message_Stage, Case_Type, person_count, data
            # 其余阶段
    else:
        data = req
        Return_String, Message_Stage, Case_Type, person_count, _ = Dialogue_API.GiveModelSentence(data, Message_Stage, current_chat_case_type,current_chat_chat_id)
        if before_Message_Stage != Message_Stage:
            data = ''
            return Return_String, Message_Stage, Case_Type, person_count, data
        else:
            return Return_String, Message_Stage, Case_Type, person_count, data
    

if st.session_state['user_input_content'] != '':
    if 'r' in st.session_state:
        st.session_state.pop("r")
        st.session_state[current_chat + 'report'] = ""
    st.session_state['pre_user_input_content'] = st.session_state['user_input_content']
    st.session_state['user_input_content'] = ''

    # 临时展示
    show_each_message(st.session_state['pre_user_input_content'], 'user', 'tem',
                      [area_user_svg.markdown, area_user_content.markdown])
    
    #获取用户所说的话
    req = st.session_state['pre_user_input_content']
    #调用接口
    with st.spinner("🤔"):
        r , message_stage , case_type, person_count, person_data = backend(req)
        st.session_state[current_chat + 'message_stage'] = message_stage
        st.session_state[current_chat + 'person_count'] = person_count
        print("后端返回的personcount",person_count)
        st.session_state[current_chat + 'case_type'] = case_type
        st.session_state[current_chat + 'is_final'] = 1
        #目前person_data还是用了用户的输入
        print("person_data",person_data)
        print("---------------------------")
        st.session_state[current_chat + 'person_data'] = person_data
        st.session_state["chat_of_r"] = current_chat
        st.session_state["r"] = r
        st.experimental_rerun()



if ("r" in st.session_state) and (current_chat == st.session_state["chat_of_r"]):
    if current_chat + 'report' not in st.session_state:
        st.session_state[current_chat + 'report'] = ""

    try:
        st.session_state[current_chat + 'report'] = st.session_state["r"]
        show_each_message(st.session_state['pre_user_input_content'], 'user', 'tem',
                                  [area_user_svg.markdown, area_user_content.markdown])
        show_each_message(st.session_state[current_chat + 'report'], 'assistant', 'tem',
                                  [area_gpt_svg.markdown, area_gpt_content.markdown])

        
    except ChunkedEncodingError:
        area_error.error("网络状况不佳，请刷新页面重试。")
    # 应对stop情形
    except Exception:
        pass
    else:
        # 保存内容
        st.session_state["history" + current_chat].append(
            {"role": "user", "content": st.session_state['pre_user_input_content']})
        st.session_state["history" + current_chat].append(
            {"role": "assistant", "content": st.session_state[current_chat + 'report']})
        write_data()
    # 用户在网页点击stop时，ss某些情形下会暂时为空
    if current_chat + 'report' in st.session_state:
        st.session_state.pop(current_chat + 'report')
    if 'r' in st.session_state:
        st.session_state.pop("r")
        st.experimental_rerun()

# 添加事件监听
v1.html(js_code, height=0)
#xxxxxxxx