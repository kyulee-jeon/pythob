import pandas as pd
import numpy as np
import os
import base64
import ast
 
def waveform_parser(csv_path, save_dir, chunksize=1000):
    """
    대용량 CSV 파일을 청크 단위로 처리하는 함수
    Parameters:
    - csv_path: CSV 파일 경로
    - save_dir: 결과 파일을 저장할 디렉토리
    - chunksize: 한 번에 처리할 행의 수
    """
    # CSV 파일을 청크 단위로 읽기
    try:
        for chunk_number, df in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
            for i, row in df.iterrows():
                try:
                    pt_no = str(row['subject_id'])
                    m_date = str(row['measured_datetime']).replace('-','').replace(':','').split('.')[0].replace(' ','_')
                    fname = f"{pt_no}_{m_date}.csv"
                    print(f"Processing {fname}")
 
                    waveform = row['waveform_raw']
                    waveform = ast.literal_eval(waveform)
                    lead_data = waveform['LeadData']
 
                    if lead_data:
                        result_dict = {}
                        for x in lead_data:
                            waveform = x['WaveFormData']
                            laupd = float(x['LeadAmplitudeUnitsPerBit'])
                            waveform_decoded = base64.b64decode(waveform)
                            waveform_decoded = np.array(array.array('h', waveform_decoded))
                            waveform_decoded = (waveform_decoded*laupd).astype(int)
                            result_dict[x['LeadID']] = waveform_decoded
                        lead8_df = pd.DataFrame.from_dict(result_dict)
                        output_path = os.path.join(save_dir, fname)
                        lead8_df.to_csv(output_path, index=False)
                except Exception as Argument:
                    with open('bug.txt', 'a') as f:
                        try:
                            if type(fname) == str:
                                f.write(f'{i} / {fname} : {str(Argument)}\n')
                                print(f'{i} / {fname} raised error : {str(Argument)}')
                            else:
                                f.write(f'{i} : {str(Argument)}\n')
                                print(f'{i} raised error : {str(Argument)}')
                        except:
                            f.write(f'{i} : {str(Argument)}\n')
                            print(f'{i} raised error : {str(Argument)}')
            print(f'Chunk {chunk_number+1} processed')
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
 
if __name__ == "__main__":
    # 사용 예시
    csv_path = "your_input.csv"  # 입력 CSV 파일 경로
    save_dir = "output_directory"  # 결과 저장 디렉토리
    # 저장 디렉토리가 없으면 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 함수 실행
    waveform_parser(csv_path, save_dir, chunksize=1000)
