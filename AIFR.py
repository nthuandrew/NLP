import streamlit as st
from load_css import local_css
import pandas as pd

local_css("style.css")
excel_data_df1 = pd.read_excel('A1_二次標註_網路危機訊息標註_1100927_second_labeled.xlsx', sheet_name='contents')
excel_data_df2 = pd.read_excel('網路危機_A1_電腦斷句_討論標註_全_修正完成.xlsx', sheet_name='Merged')
excel_data_df3 = pd.read_excel('網路危機_A1_危機程度.xlsx', sheet_name='資料統整(編號)')

Titles = excel_data_df1['Title'][:].tolist()
TextIDs = excel_data_df1['TextID'][:].tolist()
TextTimes = excel_data_df1['TextTime'][:].tolist()
Authors = excel_data_df1['Author'][:].tolist()
Level = excel_data_df3['Crisis_Level'][:].tolist()


original_contents = excel_data_df1['Content(remove_tag)'][:].tolist()

sentences = excel_data_df2['Sentence'][:].tolist()
labels = excel_data_df2['標註代碼'][:].tolist()


article = st.selectbox('Choose an article', Titles)
key_i = int(excel_data_df3["index"][0])


title_col1, title_col2, title_col3 = st.columns([18,2,2])

with title_col1:
    st.title("網路危機文章偵測系統")

with title_col2:
    st.markdown("\n")    
    st.markdown("\n")
    button_previous = st.button("上一篇")
    if(button_previous):
        if key_i > 0:
            key_i -= 1
            article = Titles[key_i]
            button = False
with title_col3:
    st.markdown("\n")    
    st.markdown("\n")
    button_next = st.button("下一篇")
    if(button_next):
        key_i += 1
        article = Titles[key_i]
        button = False

article = Titles[key_i]
level_index = excel_data_df3["Title"].to_list().index(article)

to_show = 0
category = ""
if Level[level_index] == 3:
    category = "A (危機程度高：有自傷自殺行為)"
elif Level[level_index] == 2:
    category = "B (危機程度中：有自傷自殺意念)"
elif Level[level_index] == 1:
    category = "C (危機程度低：有憂鬱負向情緒)"
else:
    category = "0 (無危機狀況)"



excel_data_df3["index"][0] = key_i

excel_data_df3.to_excel('網路危機_A1_危機程度.xlsx', sheet_name='資料統整(編號)')

# print(key_i, level_index)

with st.sidebar:
    title = "文章標題: " + Titles[key_i]
    level = "<div><span class='category'>" + "危機程度: " + category + "</span></div>" 
    textid = "<div><span class='highlight'>" + "文章ID: " + str(TextIDs[key_i]) + "</span></div>" 
    texttime = "<div><span class='highlight'>" + "發佈時間: " + str(TextTimes[key_i]) + "</span></div>" 
    author = "文章作者: " + Authors[key_i]
    st.header(title)
    st.markdown(level, unsafe_allow_html=1)
    st.markdown(textid, unsafe_allow_html=1)
    st.markdown(texttime, unsafe_allow_html=1)
    st.markdown(author)
    # to_show = st.checkbox('是否呈現標註結果分類文字')
    st.subheader("標註分類與統計： ")
    container_total = st.container()
    for i in range(7):
        if i == 0:
            container0 = st.container()
        elif i == 1:
            container1 = st.container()
        elif i == 2:
            container2 = st.container()
        elif i == 3:
            container3 = st.container()
        elif i == 4:
            container4 = st.container() 
        elif i == 5:
            container5 = st.container()
        else:
            container6 = st.container()
            for j in range(3):
                st.markdown("\n")         

col2, col1 = st.columns([30, 30])
with col1:
    st.header("原始網路文章")
    st.markdown(original_contents[key_i])

with col2:
    st.header("標註後網路文章")
    New_titles = excel_data_df2['Title'][:].tolist()
    # print(len(New_titles), New_titles[:10])
    now_title_id = New_titles.index(article)
    now_title_end = now_title_id
    for single_title in New_titles[now_title_id:]:
        if single_title == article:
            now_title_end += 1
        else:
            break
    now_sentences = sentences[now_title_id:now_title_end]
    now_labels = labels[now_title_id:now_title_end]
    # print(len(now_sentences))
    tem_stastic = [0]*7
    for i in range(len(now_sentences)):
        lab = now_labels[i]
        sen = str(now_sentences[i])
        if lab == 0 or lab == 7:
            s = "<div><span class='highlight zero'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("無標註")
            tem_stastic[6] += 1 
        elif lab == 1:
            s = "<div><span class='highlight one'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("自殺與憂鬱(認知或情緒)")
            tem_stastic[1] += 1  
        elif lab == 2:
            s = "<div><span class='highlight two'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("無助或無望(認知或情緒)")
            tem_stastic[2] += 1
        elif lab == 3:
            s = "<div><span class='highlight three'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("正向文字(認知或情緒)")
            tem_stastic[3] += 1 
        elif lab == 4:
            s = "<div><span class='highlight four'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("其他負向文字(情緒)")
            tem_stastic[4] += 1
        elif lab == 5:
            s = "<div><span class='highlight five'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:            
                st.caption("生理反應或醫療狀況(認知或行為)") 
            tem_stastic[5] += 1
        elif lab == 6:
            s = "<div><span class='highlight six'>" + sen + "</span></div>"
            st.markdown(s, unsafe_allow_html=1)
            if to_show:
                st.caption("自殺行為(行為)")
            tem_stastic[0] += 1
    total = str(sum(tem_stastic))
    s0 = "<span class='highlight six'>" + "自殺行為(行為)‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[0]) + "</span>" + "句(" + str(round(100*tem_stastic[0]/sum(tem_stastic))) + "%)</span></div>"
    s1 = "<span class='highlight one'>" + "自殺與憂鬱(認知或情緒)‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[1]) + "</span>" + "句(" + str(round(100*tem_stastic[1]/sum(tem_stastic))) + "%)</span></div>"    
    s2 = "<span class='highlight two'>" + "無助或無望(認知或情緒)‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[2]) + "</span>" + "句(" + str(round(100*tem_stastic[2]/sum(tem_stastic))) + "%)</span></div>"
    s3 = "<span class='highlight three'>" + "正向文字(認知或情緒)‧‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[3]) + "</span>" + "句(" + str(round(100*tem_stastic[3]/sum(tem_stastic))) + "%)</span></div>"
    s4 = "<span class='highlight four'>" + "其他負向文字(情緒)‧‧‧‧‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[4]) + "</span>" + "句(" + str(round(100*tem_stastic[4]/sum(tem_stastic))) + "%)</span></div>"
    s5 = "<span class='highlight five'>" + "生理反應或醫療狀況(認知或行為)‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[5]) + "</span>" + "句(" + str(round(100*tem_stastic[5]/sum(tem_stastic))) + "%)</span></div>"
    s6 = "<span class='highlight zero'>" + "無標註‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧‧" + "<span class='highlight bold'>" + str(tem_stastic[6]) + "</span>" + "句(" + str(round(100*tem_stastic[6]/sum(tem_stastic))) + "%)</span></div>"
    s_total = "總句數： " + total + "句"
    container_total.text(s_total)
    container0.caption(s0, unsafe_allow_html=1)
    container1.caption(s1, unsafe_allow_html=1)
    container2.caption(s2, unsafe_allow_html=1)
    container3.caption(s3, unsafe_allow_html=1)
    container4.caption(s4, unsafe_allow_html=1)
    container5.caption(s5, unsafe_allow_html=1)
    container6.caption(s6, unsafe_allow_html=1)

