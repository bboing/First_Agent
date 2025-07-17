from io import StringIO
from datetime import datetime

import pandas as pd
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")


def combined_markdown_and_bpmn(md_data, bpmn_data):
    left_df = markdown_to_dataframe(md_data)
    right_df = bpmn_to_dataframe(bpmn_data)

    merged_df = pd.merge(
        right_df,
        left_df,
        left_on=['Element ID', 'Participant Name'],      # 오른쪽 테이블의 컬럼명
        right_on=['2025-04-25', 'Process'],  # 왼쪽 테이블의 컬럼명
        how='outer',
        suffixes=('_right', '_left')
    )

    merged_df['Element ID'] = merged_df['Element ID'].fillna(merged_df['2025-04-25'])
    merged_df['Element Type'] = merged_df['Element Type'].fillna('Task')
    merged_df['Element Name'] = merged_df['Element Name'].fillna(merged_df['Task'])
    merged_df['Lane'] = merged_df['Lane'].fillna('Task_flow')
    merged_df = merged_df.drop(['Sequence Order', 'Notes', 'Process Custom Attributes', \
                                'Participant ID', 'Unnamed: 0', 'New ID (SNA)', 'ID', \
                                'Unnamed: 15'], axis=1)

    merged_df_sorted = merged_df.sort_values(by='Element ID')
    merged_df_sorted.to_excel(f"{BASE_DIR}/result/final_result/merged_table_result_{timestamp}.xlsx")

    return merged_df_sorted


def markdown_to_dataframe(md_data):
    lines = [line for line in md_data.strip().split('\n') if not line.startswith('| ---')]

    # 다시 문자열로 합쳐서 DataFrame 생성
    cleaned_text = '\n'.join(lines)
    df = pd.read_csv(StringIO(cleaned_text), sep='|', engine='python')

    # 앞뒤 공백 제거된 컬럼명과 데이터 처리
    df.columns = [col.strip() for col in df.columns]
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def bpmn_to_dataframe(bpmn_data):
    bpmn_data['Element ID'] = bpmn_data['Element ID'].apply(lambda x: x.replace("Activity_", "") if isinstance(x, str) else x)

    return bpmn_data

