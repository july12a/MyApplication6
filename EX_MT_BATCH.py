# -*- coding: utf-8 -*-

'''
코드 정상 실행 -> rtn_cd = 'S', print(f'rtn_cd = {rtn_cd}')
코드 정상 실행 x -> rtn_cd = 'F', print(f'rtn_cd = {rtn_cd}')
'''




# ============================================================
# 환경 세팅
# ============================================================

import pandas as pd
import os
import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import EX_PY_MAIN as main

DIR = main.MT_DIR
print(DIR)
cursor = main.cursor
conn = main.conn
procOnly12 = main.procOnly12
move_file = main.move_file




# ============================================================
# 필요한 파일 READ
# ============================================================

file_pth1 = DIR +'MT_001/'
file_pth2 = DIR +'CC_001/'
file_pth3 = DIR +'CSV_000/'


file_list1 = os.listdir(file_pth1)
file_list1 = [file for file in file_list1 if file.find(".xlsx") !=-1] 

file_list2 = os.listdir(file_pth2)
file_list2 = [file for file in file_list2 if (file.find(".xls") !=-1) | (file.find(".xlsx") !=-1)] 
# file_list4 = os.listdir(file_pth2)
# file_list4 = [file for file in file_list4 if file.find(".xlsx") !=-1] 

file_list3 = os.listdir(file_pth3)
file_list3 = [file for file in file_list3 if file.find(".xlsx") !=-1] 

df1 = pd.DataFrame()
for file1 in file_list1 : 
    imsi = pd.read_excel(file_pth1 + file1)
    imsi['proc_file_name'] = file1
    df1 = pd.concat([df1, imsi])
    move_file(file_pth1, file1)

df2 = pd.DataFrame()
for file2 in file_list2 : 
    if (file2.find(".xlsx") !=-1) :
        imsi = pd.read_excel(file_pth2 + file2)
    elif (file2.find(".xls") !=-1) :
        imsi = pd.read_excel(file_pth2 + file2, engine = 'xlrd', header = None)
    
    imsi['proc_file_name'] = file2
    df2 = pd.concat([df2, imsi])
    move_file(file_pth2, file2)
# for file4 in file_list4 : 
#     imsi = pd.read_excel(file_pth2 + file4, header = None)
#     imsi['proc_file_name'] = file2
#     df2 = pd.concat([df2, imsi])
#     move_file(file_pth2, file4)

allowed_one_char_words = pd.DataFrame()
for file3 in file_list3 : 
    imsi = pd.read_excel(file_pth3 + file3)
    allowed_one_char_words = pd.concat([allowed_one_char_words, imsi])
allowed_one_char_words = allowed_one_char_words[allowed_one_char_words['err'] == 0]['voc_tit_keyword'].unique().tolist()




# ============================================================
# 함수 선언
# ============================================================

# 괄호 종류에 관계없이 그 안의 텍스트를 모두 제거
def remove_text_in_brackets(text):
    cleaned_text = re.sub(r'[\[\(\{][^\)\]\}]*[\)\]\}]', '', text)
    return cleaned_text

# 각 리스트에서 한글자 단어를 제외하고, allowed_words에 포함된 단어만 남기기
def filter_one_char_words(word_list, allowed_words):
    return [word for word in word_list if len(word) > 1 or word in allowed_words]

# TF-IDF 점수 threshold점 이상의 키워드만 남기기(순서고려)
def get_filtered_keywords(dataframe, tfidf_matrix, vectorizer, threshold=0.3):
    filtered_items = []  # 각 문서에서 TF-IDF 점수 n 이상인 단어를 저장할 리스트
    
    for i in range(tfidf_matrix.shape[0]):
        doc = tfidf_matrix[i]  # 문서별 TF-IDF 벡터 가져오기
        # 문서별 단어와 그에 해당하는 TF-IDF 점수를 리스트로 저장
        doc_keywords = dataframe['clean_voc_tit_keyword'][i]  # 원본 단어 리스트
        
        filtered_keywords = []
        
        # 각 단어에 대해 TF-IDF 점수를 확인
        for word in doc_keywords:
            word_idx = vectorizer.vocabulary_.get(word)  # 단어가 TF-IDF 벡터화된 단어 목록에 있는지 확인
            if word_idx is not None:
                word_tfidf_score = doc[0, word_idx]  # 해당 단어의 TF-IDF 점수
                
                # TF-IDF 점수가 threshold 이상이면 해당 단어를 필터링
                if word_tfidf_score >= threshold:
                    filtered_keywords.append(word)
        
        filtered_items.append(filtered_keywords)  # 필터링된 단어들 추가
    
    return filtered_items

# 2-gram으로 키워드 조합
def extract_2gram(keywords, vectorizer):
    if not keywords:
        return []
    if len(keywords) == 1:
        return keywords  # 1개의 단어가 있으면 그대로 반환
    text = ' '.join(keywords)
    try:
        n_grams = vectorizer.fit_transform([text])  # 2-gram 추출
        return vectorizer.get_feature_names_out()  # 2-gram 리스트 반환
    except ValueError:  # 2-gram을 추출할 수 없을 경우 빈 리스트 반환
        return keywords




# ============================================================
# df1 DB insert
# ============================================================

if len(df1) != 0 :
    # ============================================================
    # ex_mst_voc_list - df1
    # ============================================================

    # 임시 VOC_ID 생성
    mt1 = df1[['대분류', '중분류', '소분류', '제목', '접수일자', 'proc_file_name']].copy()
    val = pd.read_sql(f'''select nextval('voc_id_seq')''',con=conn)
    setval = val.values[0][0] + len(mt1)
    cursor.execute(f"SELECT setval('voc_id_seq', {setval}, true);")
    mt1['voc_id'] = range(val.values[0][0], val.values[0][0] + len(mt1))

    # 시간 컬럼 처리
    mt1['접수일자'] = mt1['접수일자'].astype(str)
    mt1['voc_reg_date'] = mt1['접수일자'].str[0:4] + mt1['접수일자'].str[5:7] + mt1['접수일자'].str[8:10]
    mt1['voc_reg_time'] = mt1['접수일자'].str[11:13] + mt1['접수일자'].str[14:16] + mt1['접수일자'].str[17:19]

    # 포멧 맞추기
    mt1['voc_clss_cd'] = 'MT'
    mt1['voc_cont'] = ''
    mt1['private_yn'] = 'N'
    mt1['process_yn'] = 'N'
    mt1['use_yn'] = 'Y'

    # 대/중/소 분류 코드 붙이기
    # 예외처리
    mp = pd.read_sql(f'''SELECT * FROM ex_mt_voc_clss_master''',con=conn)
    mt1 = mt1.fillna('기타')
    mt1.loc[mt1['중분류'] == '하이패스 이용', '중분류'] = '하이패스이용'
    mt1.loc[mt1['중분류'] == '통행요금 납부', '중분류'] = '통행요금'
    mt1.loc[mt1['소분류'] == '지장물(분묘)보상', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '기타보상', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '잔여지(간접보상 )', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '부체도로', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '안전순찰원', '소분류'] = '기타'

    # 코드 매칭
    mp2 = mp[['l_clss_nm', 'l_clss_cd', 'm_clss_nm', 'm_clss_cd', 's_clss_nm', 's_clss_cd']].drop_duplicates(['l_clss_cd', 'm_clss_cd', 's_clss_cd'])
    mt1 = pd.merge(mt1, mp2, how = 'left', left_on = ['대분류', '중분류', '소분류'], right_on = ['l_clss_nm', 'm_clss_nm', 's_clss_nm'])
    mt1.rename(columns = {'제목' : 'voc_tit'}, inplace = True)

    # DB insert
    df_list = mt1.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_list (voc_id, voc_clss_cd, voc_reg_date, voc_reg_time, voc_tit, voc_cont, private_yn, process_yn, l_clss_cd, m_clss_cd, s_clss_cd, use_yn)
        VALUES (%(voc_id)s, %(voc_clss_cd)s, %(voc_reg_date)s, %(voc_reg_time)s, %(voc_tit)s, %(voc_cont)s, %(private_yn)s, %(process_yn)s, %(l_clss_cd)s, %(m_clss_cd)s, %(s_clss_cd)s, %(use_yn)s)
        ON CONFLICT (voc_clss_cd, voc_reg_date, voc_reg_time, voc_tit) DO UPDATE 
        SET voc_id = EXCLUDED.voc_id,
            voc_cont = EXCLUDED.voc_cont,
            private_yn = EXCLUDED.private_yn,
            process_yn = EXCLUDED.process_yn,
            l_clss_cd = EXCLUDED.l_clss_cd,
            m_clss_cd = EXCLUDED.m_clss_cd,
            s_clss_cd = EXCLUDED.s_clss_cd,
            use_yn = EXCLUDED.use_yn
    ''', df_list)

    conn.commit()




    # ============================================================
    # ex_mt_voc_tit_keyword - df1
    # ============================================================

    mt2 = mt1[['voc_id', 'voc_tit', 'voc_reg_date', 'proc_file_name']].copy()

    # 괄호안에 모든 문자 제거
    mt2['voc_tit'] = mt2['voc_tit'].apply(lambda x : remove_text_in_brackets(x))

    # 단어 추출
    okt = Okt()
    mt2['voc_tit_keyword'] = mt2['voc_tit'].apply(lambda x: okt.nouns(str(x)))

    # 중복제거
    mt2['voc_tit_keyword'] = mt2['voc_tit_keyword'].apply(lambda x: list(dict.fromkeys(x)))

    # 각 리스트에서 한글자 단어를 제외하고, allowed_one_char_words에 포함된 단어만 남기기
    mt2['clean_voc_tit_keyword'] = mt2['voc_tit_keyword'].apply(lambda x: filter_one_char_words(x, allowed_one_char_words))

    # TF-IDF
    mt2['tfidf'] = [' '.join(nouns_list) for nouns_list in mt2['clean_voc_tit_keyword']]
    vectorizer = TfidfVectorizer(min_df=1, max_df=1.0, token_pattern=r'\b\w+\b') # 한글자포함
    tfidf_matrix = vectorizer.fit_transform(mt2['tfidf'])
    top_keywords = get_filtered_keywords(mt2, tfidf_matrix, vectorizer)
    mt2['top_keywords'] = top_keywords

    # 테이블 형식 맞추기
    gram_1 = mt2.explode('top_keywords')[['voc_id', 'top_keywords', 'voc_reg_date', 'proc_file_name']]
    gram_1.rename(columns = {'top_keywords' : 'voc_tit_keyword'}, inplace = True)

    # seq 생성
    gram_1['voc_tit_keyword_seq'] = gram_1.groupby('voc_id').cumcount() + 1
    gram_1 = gram_1[gram_1['voc_tit_keyword'].notnull()]

    # DB insert
    df_list = gram_1.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_tit_keyword (voc_id, voc_tit_keyword_seq, voc_tit_keyword)
        VALUES (%(voc_id)s, %(voc_tit_keyword_seq)s, %(voc_tit_keyword)s)
    ''', df_list)

    conn.commit()




    # ============================================================
    # ex_mt_voc_tit_keyword_2gram - df1
    # ============================================================

    # 단어 두개씩 합치기
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 2))
    mt2['top_keywords_2gram'] = mt2['top_keywords'].apply(lambda x: extract_2gram(x, vectorizer))

    # 테이블 형식 맞추기
    mt2 = mt2.explode('top_keywords_2gram')[['voc_id', 'top_keywords_2gram', 'voc_reg_date', 'proc_file_name']]
    mt2.rename(columns = {'top_keywords_2gram' : 'voc_tit_keyword'}, inplace = True)

    # seq 생성
    mt2['voc_tit_keyword_seq'] = mt2.groupby('voc_id').cumcount() + 1
    mt2 = mt2[mt2['voc_tit_keyword'].notnull()]

    # DB insert
    df_list = mt2.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_tit_keyword_2gram (voc_id, voc_tit_keyword_seq, voc_tit_keyword)
        VALUES (%(voc_id)s, %(voc_tit_keyword_seq)s, %(voc_tit_keyword)s)
    ''', df_list)

    conn.commit()




    # ============================================================
    # ex_mt_voc_keyword_frequency - df1
    # ============================================================

    # mt3 = mt2[['voc_tit_keyword', 'voc_reg_date', 'proc_file_name']].copy()
    # proc_file_name_list = mt3['proc_file_name'].unique().tolist()

    # result = pd.DataFrame()
    # for i in proc_file_name_list :
    #     a = mt3[mt3['proc_file_name'] == i]
    #     a['voc_reg_date'] = a['voc_reg_date'].astype(int)
    #     a['proc_st_date'] = a['voc_reg_date'].min()
    #     a['proc_ed_date'] = a['voc_reg_date'].max()

    #     a['keyword_cnt'] = 1
    #     a = a.groupby(['proc_file_name', 'proc_st_date', 'proc_ed_date', 'voc_tit_keyword']).sum()['keyword_cnt'].reset_index()
    #     a['proc_type'] = 1

    #     result = pd.concat([result, a])
    # result.rename(columns = {'voc_tit_keyword' : 'keyword'}, inplace = True)

    # # DB insert
    # df_list = result.to_dict('records')
    # cursor.executemany('''
    #     INSERT INTO ex_mt_voc_keyword_frequency (proc_file_name, proc_type, proc_st_date, proc_ed_date, keyword, keyword_cnt)
    #     VALUES (%(proc_file_name)s, %(proc_type)s, %(proc_st_date)s, %(proc_ed_date)s, %(keyword)s, %(keyword_cnt)s)
    #     ON CONFLICT (proc_file_name, proc_type, proc_st_date, proc_ed_date, keyword) DO UPDATE 
    #     SET keyword_cnt = EXCLUDED.keyword_cnt
    # ''', df_list)

    # conn.commit()




# ============================================================
# df2 DB insert
# ============================================================

if len(df2) != 0 :
    # ============================================================
    # ex_mst_voc_list - df2
    # ============================================================

    # 데이터 프레임 형태로 변환
    mt1 = df2.drop([0, 1], axis = 1)
    mt1 = mt1[mt1[2].notnull()]
    mt1.columns = mt1.loc[5].tolist()
    mt1 = mt1[mt1['팀'] != '팀']
    mt1.rename(columns = {mt1.columns[len(mt1.columns)-1] : 'proc_file_name'}, inplace = True)

    # 임시 VOC_ID 생성
    mt1 = mt1[['대분류', '중분류', '소분류', '상담이력', '상담일자', '상담시간', 'proc_file_name']]
    val = pd.read_sql(f'''select nextval('voc_id_seq')''',con=conn)
    setval = val.values[0][0] + len(mt1)
    cursor.execute(f"SELECT setval('voc_id_seq', {setval}, true);")
    mt1['voc_id'] = range(val.values[0][0], val.values[0][0] + len(mt1))

    # 시간 컬럼 처리
    mt1['voc_reg_date'] = mt1['상담일자'].str[0:4] + mt1['상담일자'].str[5:7] + mt1['상담일자'].str[8:10]
    mt1['voc_reg_time'] = mt1['상담시간'].str[0:2] + mt1['상담시간'].str[3:5] + mt1['상담시간'].str[6:8]

    # 포멧 맞추기
    mt1['voc_clss_cd'] = 'CC'
    mt1['voc_cont'] = ''
    mt1['private_yn'] = 'N'
    mt1['process_yn'] = 'N'
    mt1['use_yn'] = 'Y'

    # 대/중/소 분류 코드 붙이기
    # 예외처리
    mp = pd.read_sql(f'''SELECT * FROM ex_mt_voc_clss_master''',con=conn)
    mt1 = mt1.fillna('기타')
    mt1.loc[mt1['중분류'] == '하이패스 이용', '중분류'] = '하이패스이용'
    mt1.loc[mt1['중분류'] == '통행요금 납부', '중분류'] = '통행요금'
    mt1.loc[mt1['소분류'] == '지장물(분묘)보상', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '기타보상', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '잔여지(간접보상 )', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '부체도로', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '안전순찰원', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '기 타', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '잔여지(간접보상)', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '규정속도', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '통합 콜센터 테스트', '소분류'] = '기타'
    mt1.loc[mt1['소분류'] == '기 타', '소분류'] = '기타'

    # 코드 매칭
    mp2 = mp[['l_clss_nm', 'l_clss_cd', 'm_clss_nm', 'm_clss_cd', 's_clss_nm', 's_clss_cd']].drop_duplicates(['l_clss_cd', 'm_clss_cd', 's_clss_cd'])
    mt1 = pd.merge(mt1, mp2, how = 'left', left_on = ['대분류', '중분류', '소분류'], right_on = ['l_clss_nm', 'm_clss_nm', 's_clss_nm'])
    mt1.rename(columns = {'상담이력' : 'voc_tit'}, inplace = True)

    # DB insert
    df_list = mt1.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_list (voc_id, voc_clss_cd, voc_reg_date, voc_reg_time, voc_tit, voc_cont, private_yn, process_yn, l_clss_cd, m_clss_cd, s_clss_cd, use_yn)
        VALUES (%(voc_id)s, %(voc_clss_cd)s, %(voc_reg_date)s, %(voc_reg_time)s, %(voc_tit)s, %(voc_cont)s, %(private_yn)s, %(process_yn)s, %(l_clss_cd)s, %(m_clss_cd)s, %(s_clss_cd)s, %(use_yn)s)
        ON CONFLICT (voc_clss_cd, voc_reg_date, voc_reg_time, voc_tit) DO UPDATE 
        SET voc_id = EXCLUDED.voc_id,
            voc_cont = EXCLUDED.voc_cont,
            private_yn = EXCLUDED.private_yn,
            process_yn = EXCLUDED.process_yn,
            l_clss_cd = EXCLUDED.l_clss_cd,
            m_clss_cd = EXCLUDED.m_clss_cd,
            s_clss_cd = EXCLUDED.s_clss_cd,
            use_yn = EXCLUDED.use_yn
    ''', df_list)
    conn.commit()




    # ============================================================
    # ex_mt_voc_tit_keyword - df2
    # ============================================================

    mt2 = mt1[['voc_id', 'voc_tit', 'voc_reg_date', 'proc_file_name']].copy()

    # 괄호안에 모든 문자 제거
    mt2['voc_tit'] = mt2['voc_tit'].apply(lambda x : remove_text_in_brackets(x))

    # 단어 추출
    okt = Okt()
    mt2['voc_tit_keyword'] = mt2['voc_tit'].apply(lambda x: okt.nouns(str(x)))

    # 중복제거
    mt2['voc_tit_keyword'] = mt2['voc_tit_keyword'].apply(lambda x: list(dict.fromkeys(x)))

    # 각 리스트에서 한글자 단어를 제외하고, allowed_one_char_words에 포함된 단어만 남기기
    mt2['clean_voc_tit_keyword'] = mt2['voc_tit_keyword'].apply(lambda x: filter_one_char_words(x, allowed_one_char_words))

    # TF-IDF
    mt2['tfidf'] = [' '.join(nouns_list) for nouns_list in mt2['clean_voc_tit_keyword']]
    vectorizer = TfidfVectorizer(min_df=1, max_df=1.0, token_pattern=r'\b\w+\b') # 한글자포함
    tfidf_matrix = vectorizer.fit_transform(mt2['tfidf'])
    top_keywords = get_filtered_keywords(mt2, tfidf_matrix, vectorizer)
    mt2['top_keywords'] = top_keywords

    # 테이블 형식 맞추기
    gram_1 = mt2.explode('top_keywords')[['voc_id', 'top_keywords', 'voc_reg_date', 'proc_file_name']]
    gram_1.rename(columns = {'top_keywords' : 'voc_tit_keyword'}, inplace = True)

    # seq 생성
    gram_1['voc_tit_keyword_seq'] = gram_1.groupby('voc_id').cumcount() + 1
    gram_1 = gram_1[gram_1['voc_tit_keyword'].notnull()]

    # DB insert
    df_list = gram_1.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_tit_keyword (voc_id, voc_tit_keyword_seq, voc_tit_keyword)
        VALUES (%(voc_id)s, %(voc_tit_keyword_seq)s, %(voc_tit_keyword)s)
    ''', df_list)

    conn.commit()




    # ============================================================
    # ex_mt_voc_tit_keyword_2gram - df2
    # ============================================================

    # 단어 두개씩 합치기
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(2, 2))
    mt2['top_keywords_2gram'] = mt2['top_keywords'].apply(lambda x : extract_2gram(x, vectorizer))

    # 테이블 형식 맞추기
    mt2 = mt2.explode('top_keywords_2gram')[['voc_id', 'top_keywords_2gram', 'voc_reg_date', 'proc_file_name']]
    mt2.rename(columns = {'top_keywords_2gram' : 'voc_tit_keyword'}, inplace = True)

    # seq 생성
    mt2['voc_tit_keyword_seq'] = mt2.groupby('voc_id').cumcount() + 1
    mt2 = mt2[mt2['voc_tit_keyword'].notnull()]

    # DB insert
    df_list = mt2.to_dict('records')
    cursor.executemany('''
        INSERT INTO ex_mt_voc_tit_keyword_2gram (voc_id, voc_tit_keyword_seq, voc_tit_keyword)
        VALUES (%(voc_id)s, %(voc_tit_keyword_seq)s, %(voc_tit_keyword)s)
    ''', df_list)

    conn.commit()




    # ============================================================
    # ex_mt_voc_keyword_frequency - df2
    # ============================================================

    # mt3 = mt2[['voc_tit_keyword', 'voc_reg_date', 'proc_file_name']].copy()
    # proc_file_name_list = mt3['proc_file_name'].unique().tolist()

    # result = pd.DataFrame()
    # for i in proc_file_name_list :
    #     a = mt3[mt3['proc_file_name'] == i]
    #     a['voc_reg_date'] = a['voc_reg_date'].astype(int)
    #     a['proc_st_date'] = a['voc_reg_date'].min()
    #     a['proc_ed_date'] = a['voc_reg_date'].max()

    #     a['keyword_cnt'] = 1
    #     a = a.groupby(['proc_file_name', 'proc_st_date', 'proc_ed_date', 'voc_tit_keyword']).sum()['keyword_cnt'].reset_index()
    #     a['proc_type'] = 1

    #     result = pd.concat([result, a])
    # result.rename(columns = {'voc_tit_keyword' : 'keyword'}, inplace = True)

    # DB insert
    # df_list = result.to_dict('records')
    # cursor.executemany('''
    #     INSERT INTO ex_mt_voc_keyword_frequency (proc_file_name, proc_type, proc_st_date, proc_ed_date, keyword, keyword_cnt)
    #     VALUES (%(proc_file_name)s, %(proc_type)s, %(proc_st_date)s, %(proc_ed_date)s, %(keyword)s, %(keyword_cnt)s)
    #     ON CONFLICT (proc_file_name, proc_type, proc_st_date, proc_ed_date, keyword) DO UPDATE 
    #     SET keyword_cnt = EXCLUDED.keyword_cnt
    # ''', df_list)

    # conn.commit()




#
print(f'rtn_cd = {main.rtn_cd}')
print(f'rtn_msg = {main.rtn_msg}')


cursor.close()
conn.close()
