# generate_docx

## 功能

后端：读取 `infos.json`内容，生成DOCX文档，并返回一个True

> to do
>
> 1. 添加PDF输出，需要安装LibreOffice等
> 2. 加上诉讼代理人、保险公司（明天）

## 源码

generate_docx.py

### 调用

```
IsFile = getdocx(json_file_path, CHAT_ID)
# IsFile = True
```

### 输入

输入数据为已处理好格式的内容，存储在json文件中

```
infos.json

参数：
type：1 - 借贷，2 - 交通，3 - 其他
pl_num: 原告人数，默认为1
de_num：被告人数，默认为1

pl_name_1：原告姓名
pl_race_1：原告民族（无需填写“族”字）
pl_home_1：原告住址
pl_id_1：原告身份证号
pl_phone_1：原告手机号码

requests：诉讼请求
case：事实与理由

court：审理的人民法院
```

### 输出

起诉状_{CHAT_ID}.docx
