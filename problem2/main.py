import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def main():
    # Set Korean font
    # Try to find NanumGothic, otherwise fallback
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
    else:
        # Fallback to system default or sans-serif, might not show Korean correctly
        plt.rc('font', family='sans-serif')
    
    plt.rcParams['axes.unicode_minus'] = False

    file_path = 'population.csv'
    
    # 1. Read file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("File not found.")
        return

    # 2. Filter columns
    # Keep only relevant columns: Region, Gender, Age, Year, GeneralHouseholdMembers
    target_cols = ['행정구역별(시군구)', '성별', '연령별', '시점', '일반가구원']
    # Check if columns exist
    if not all(col in df.columns for col in target_cols):
        print(f"Missing columns. Available: {df.columns}")
        return
        
    df = df[target_cols]

    # 3. Filter Year >= 2015
    df = df[df['시점'] >= 2015]

    # Define Age Groups to keep (exclude summaries)
    exclude_ages = ['합계', '15~64세', '65세이상']
    ordered_ages = ['15세미만', '15~19세', '20~24세', '25~29세', '30~34세', '35~39세', 
                    '40~44세', '45~49세', '50~54세', '55~59세', '60~64세', '65~69세', 
                    '70~74세', '75~79세', '80~84세', '85세이상']
    
    # --- Task 1: Male/Female by Year (Total Age) ---
    print("=== 2015년 이후 연도별 남/여 일반가구원 통계 ===")
    df_gender_year = df[
        (df['성별'].isin(['남자', '여자'])) & 
        (df['연령별'] == '합계')
    ]
    # Pivot to show Year x Gender
    stats_gender_year = df_gender_year.pivot_table(index='시점', columns='성별', values='일반가구원', aggfunc='sum')
    print(stats_gender_year)
    print("\n")

    # --- Task 2: Age by Year (Total Gender) ---
    print("=== 2015년 이후 연도별 연령별(계) 일반가구원 통계 ===")
    df_age_year = df[
        (df['성별'] == '계') & 
        (df['연령별'].isin(ordered_ages))
    ]
    # Pivot to show Year x Age
    stats_age_year = df_age_year.pivot_table(index='시점', columns='연령별', values='일반가구원', aggfunc='sum')
    # Reorder columns
    stats_age_year = stats_age_year[ordered_ages]
    print(stats_age_year)
    print("\n")

    # --- Task 3: Graph of Male/Female by Age (Latest Year) ---
    latest_year = df['시점'].max()
    print(f"=== {latest_year}년 남/여 연령별 일반가구원 그래프 생성 ===")
    
    df_graph = df[
        (df['시점'] == latest_year) &
        (df['성별'].isin(['남자', '여자'])) &
        (df['연령별'].isin(ordered_ages))
    ]
    
    # Pivot for plotting: Index=Age, Columns=Gender
    plot_data = df_graph.pivot_table(index='연령별', columns='성별', values='일반가구원', aggfunc='sum')
    plot_data = plot_data.reindex(ordered_ages)
    
    plt.figure(figsize=(12, 6))
    plt.plot(plot_data.index, plot_data['남자'], marker='o', label='남자')
    plt.plot(plot_data.index, plot_data['여자'], marker='s', label='여자')
    
    plt.title(f'{latest_year}년 연령별 일반가구원 (남/여)')
    plt.xlabel('연령')
    plt.ylabel('일반가구원 수')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_file = 'gender_age_graph.png'
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    main()
