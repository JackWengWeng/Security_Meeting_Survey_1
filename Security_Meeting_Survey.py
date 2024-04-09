import requests
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 要发送的消息
message = '\n'
# LINE Notify 權杖
token = "C1I4WKMBpVzVzQNGesqEX9sZvjw5hqMjXIu1P7sCeDs"  # 填写Line token

def sendLineNotify(input_division, input_name, input_date_msg, message):

    # HTTP 標頭參數與資料
    headers = {"Authorization": "Bearer " + token}
    message += f'填報單位：{input_division}  \n填  報  人：{input_name}  \n召開日期/尚未規劃原因：{input_date_msg}'
    data = {'message': message}
    # 以 requests 发送 POST 请求
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

def main():
    # 隱藏網頁上方
    hide_streamlit_style = """<style>[data-testid="stToolbar"] {visibility: hidden !important;}footer {visibility: hidden !important;}</style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    
    st.header('保安防護聯繫會議調查', divider='rainbow')
    input_division = st.text_input('設施單位：')
    input_name = st.text_input('填報人：')
    status_option = st.checkbox('是否已召開或預定召開會議?')
  
    if status_option:
        input_date_msg = st.date_input("請填召開或預計召開日期") 
    else:
        input_date_msg = st.text_input('請填尚未規劃召開原因')

    with st.form("my_form"):
        # 每个表单必须有一个提交按钮。
        submitted = st.form_submit_button("確定提交")    

    if submitted:
        # 檢查必填欄位是否已填寫
        if input_division == '' or input_name == '' or (status_option and input_date_msg == '') or (not status_option and input_date_msg == ''):
            st.warning('請確認所有欄位已填寫完成！')
            return

        if status_option:
            st.write(f'填報單位：{input_division}  \n 填報人  ：{input_name}  \n 會議日期：{input_date_msg}')
            st.write("已提交成功，感謝您的協助")
            data = [input_division, input_name, input_date_msg.strftime('%Y-%m-%d'), '']
        else:
            st.write(f'填報單位：{input_division}  \n 填報人  ：{input_name}  \n 尚未規劃召開原因   ：{input_date_msg}')
            st.write("已提交成功，感謝您的協助")
            data = [input_division, input_name, '', input_date_msg]

        # 前置作業
        scopes = ["https://spreadsheets.google.com/feeds"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["cjson"], scopes)
        gss_client = gspread.authorize(credentials)

        # 開啟 Google Sheet 資料表
        spreadsheet_key = '1DrQOujc65OJdyupTL4WnhUBPoU_PRZWz2Hdyc131jjE' 
        sheet = gss_client.open_by_key(spreadsheet_key).sheet1

        sheet.append_row(data) 
        sendLineNotify(input_division, input_name, input_date_msg, message)

#起點起點入口
if __name__ == "__main__":
    main()
