import streamlit as st
import pandas as pd
import os
import json

result_path = "./results/results.json"


def json_to_df(data):
    rows = []
    for match in data:
        you_data = match['You']
        opponent_data = match['Opponent']
        result = match['Result']
        time = match['Time']
        
        # "You"のデータ
        you_row = {'Type': 'You', 'Result': result, 'Time': time}
        you_row.update(you_data)
        rows.append(you_row)
        
        # "Opponent"のデータ
        opponent_row = {'Type': 'Opponent', 'Result': result, 'Time': time}
        opponent_row.update(opponent_data)
        rows.append(opponent_row)
    
    return pd.DataFrame(rows)

def analyze_results(df_data):
    df = df_data

    #column = st.selectbox(label="column", options=df.columns, index=0)
    column = st.selectbox(label="column", options=df.columns, index=0)
    content = st.selectbox(label="content", options=df[column].drop_duplicates())
    
    # filtering
    analyze_df = df[df[column] == content]
    
    # Tags列を解析
    tags_series = analyze_df['Tags'].dropna().explode().str.strip()
    
    # 各タグの出現回数を集計
    tag_counts = tags_series.value_counts()
    
    # 集計結果をデータフレームに変換
    tag_counts_df = tag_counts.reset_index()
    tag_counts_df.columns = ['Tag', 'Count']
    tag_counts_df = tag_counts_df.sort_values(by='Count', ascending=False)
    
    # 出現回数の上位タグを表示
    st.write(tag_counts_df)
    
    # 出現回数の上位タグを棒グラフで表示
    st.bar_chart(tag_counts)

def init_ui():
    st.title("Analyzer")

def main():
    with open(result_path) as f:
        data = json.load(f)
        result_df = json_to_df(data)
        opp_df = result_df[result_df['Type'] == 'Opponent']
        cols = ['Time', 'Result', 'Tags','R-ARM','L-ARM','R-BACK','L-BACK', 'HEAD','CORE','ARM','LEG', 'BOOSTER','FCS', 'GENERATOR']   
        #cols = ['Time','Result','Tags'] + list(result_df.columns.difference(cols))

        st.write(opp_df[cols])
        opp_df["Time"] = pd.to_datetime(opp_df['Time'])
        toggle_on = st.sidebar.toggle("勝率を表示")
        if toggle_on:
            st.sidebar.write(f"総対戦数: {opp_df.shape[0]}")
            st.sidebar.write(f"勝利数: {opp_df[opp_df['Result'] == 'Win'].shape[0]}")
            st.sidebar.write(f"敗北数: {opp_df[opp_df['Result'] == 'Lose'].shape[0]}")
            st.sidebar.write(f"勝率: {opp_df[opp_df['Result'] == 'Win'].shape[0] / opp_df.shape[0] * 100:.1f}%")

            # 日付ごとの勝利数と敗北数をカウント
            win_counts = opp_df[opp_df['Result'] == 'Win']['Time'].value_counts().sort_index()
            lose_counts = opp_df[opp_df['Result'] == 'Lose']['Time'].value_counts().sort_index()
    
            # 全ての日付のインデックスを作成
            all_dates = pd.date_range(start=opp_df['Time'].min(), end=opp_df['Time'].max())
    
            # 勝利数と敗北数を全ての日付のインデックスに合わせる
            win_counts = win_counts.reindex(all_dates, fill_value=0)
            lose_counts = lose_counts.reindex(all_dates, fill_value=0)
    
            # DataFrameを作成
            counts_df = pd.DataFrame({'Win': win_counts, 'Lose': lose_counts})
    
            # st.bar_chartを使ってグラフを表示
            st.bar_chart(counts_df, color=["#FF0000", "#0000FF"])

        analyze_results(opp_df)

        # 日付ごとの対戦数をカウント
        #match_counts = opp_df['Time'].value_counts().sort_index()
        #st.bar_chart(match_counts)


if __name__ == "__main__":
    init_ui()
    main()
