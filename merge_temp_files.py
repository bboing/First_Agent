import os
import pandas as pd
import glob
from datetime import datetime

def merge_temp_files():

    
    # temp_ 파일들 찾기
    temp_files = glob.glob("./docs/save_result/temp_*.xlsx")
    
    if not temp_files:
        print("❌ temp_로 시작하는 파일을 찾을 수 없습니다.")
        return
    
    print(f"📁 발견된 temp_ 파일 개수: {len(temp_files)}")
    
    # 파일들을 시간순으로 정렬 (파일명에 타임스탬프가 포함되어 있음)
    temp_files.sort()
    
    # 모든 데이터를 저장할 리스트
    all_data = []
    
    # 각 파일 읽기
    for i, file_path in enumerate(temp_files, 1):
        try:
            print(f"📖 읽는 중... ({i}/{len(temp_files)}) {os.path.basename(file_path)}")
            df = pd.read_excel(file_path)
            all_data.append(df)
            print(f"✅ {len(df)}개 행 추가됨")
        except Exception as e:
            print(f"❌ {file_path} 읽기 실패: {e}")
    
    if not all_data:
        print("❌ 읽을 수 있는 데이터가 없습니다.")
        return
    
    # 모든 데이터 합치기
    print("🔗 데이터 합치는 중...")
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # 중복 제거 (같은 파일명이 여러 번 처리된 경우)
    print("🧹 중복 제거 중...")
    initial_count = len(merged_df)
    merged_df = merged_df.drop_duplicates(subset=['파일명'], keep='last')
    final_count = len(merged_df)
    
    print(f"📊 중복 제거: {initial_count} → {final_count}개 행")
    
    # 최종 파일로 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"merged_temp_results_{timestamp}.xlsx"
    output_path = os.path.join("./docs/save_result", output_filename)
    
    merged_df.to_excel(output_path, index=False)
    
    print(f"✅ 합치기 완료: {output_path}")
    print(f"📊 총 {len(merged_df)}개 파일의 데이터가 저장됨")
    
    # temp_ 파일들 삭제 여부 확인
    response = input(f"\n🗑️ {len(temp_files)}개의 temp_ 파일들을 삭제하시겠습니까? (y/n): ")
    if response.lower() == 'y':
        deleted_count = 0
        for file_path in temp_files:
            try:
                os.remove(file_path)
                deleted_count += 1
                print(f"🗑️ 삭제됨: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ 삭제 실패: {file_path} - {e}")
        
        print(f"✅ {deleted_count}개 temp_ 파일 삭제 완료")
    else:
        print("📁 temp_ 파일들이 보존되었습니다.")

if __name__ == "__main__":
    merge_temp_files() 