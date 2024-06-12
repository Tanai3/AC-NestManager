import streamlit as st
import pandas as pd
import os
import json
import datetime

data_dir = "./data/"
files = {
    "HEAD": data_dir + "AC6-Unit - HEAD.csv",
    "CORE": data_dir + "AC6-Unit - CORE.csv",
    "ARM": data_dir + "AC6-Unit - ARM.csv",
    "LEG": data_dir + "AC6-Unit - LEG.csv",
    "BOOSTER": data_dir + "AC6-Unit - BOOSTER.csv",
    "FCS": data_dir + "AC6-Unit - FCS.csv",
    "GENERATOR": data_dir + "AC6-Unit - GENERATOR.csv",
    "R-ARM": data_dir + "AC6-Unit - R-ARM.csv",
    "L-ARM": data_dir + "AC6-Unit - L-ARM.csv",
    "R-BACK": data_dir + "AC6-Unit - R-BACK.csv",
    "L-BACK": data_dir + "AC6-Unit - L-BACK.csv"
}
preset_file = os.path.join(data_dir, "ac_preset.json") 

def load_preset(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path) as f:
            return json.load(f)
    else:
        st.error(f"File not found: {json_file_path}")
        return pd.DataFrame()

ac_preset = load_preset(preset_file)
result_dir = "./results/"

def load_unit_info(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def selected_df(base_df, unit, selected_unit):
    return base_df[base_df[unit] == selected_unit]

def load_and_select_unit(unit_name, file_path, selected_unit_dict, id_key, index=0):
    df = load_unit_info(file_path)
    if df.empty:
        return df, pd.DataFrame(), selected_unit_dict
    if len(df[unit_name].tolist()) < index:
        index = 0
    selected_unit = st.selectbox(unit_name, df[unit_name].tolist(), key=id_key, index=index)
    select_df = selected_df(df, unit_name, selected_unit)
    selected_unit_dict[unit_name] = select_df[unit_name].unique()[0]
    return df, select_df, selected_unit_dict


def save_result(selected_unit_dict, selected_opp_unit_dict, result):
    result_file_path = os.path.join(result_dir, "results.json")
    # ディレクトリが存在しない場合は作成
    os.makedirs(result_dir, exist_ok=True)
    result_dict = {}
    result_dict["You"] = selected_unit_dict
    result_dict["Opponent"] = selected_opp_unit_dict
    result_dict["Result"] = result
    result_dict["Time"] = datetime.datetime.now().strftime("%Y/%m/%d")
    st.json(json.dumps(result_dict))

    try:
        with open(result_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    
    data.append(result_dict)

    try:
        with open(result_file_path, "w") as f:
            json.dump(data, f, indent=4)
            st.success("Result saved successfully!")
    except Exception as e:
        st.error(f"Error: {e}")


def create_unit_selection(column, unit_prefix, selected_unit_dict, preset_dict):
    for unit_name in files.keys():
        file_path = files[unit_name]
        if unit_name in ["R-BACK", "L-BACK"]:
            if unit_name == "R-BACK":
                hunger_index = preset_dict["R-Hunger"]
            elif unit_name == "L-BACK":
                hunger_index = preset_dict["L-Hunger"]
            hunger_index = 0 if hunger_index == "Yes" else 1
            hunger_enable = st.radio(f"WeaponHunger_{unit_prefix}-{unit_name}", ["Yes", "No"], index=hunger_index, key=f"{unit_prefix}-{unit_name.lower()}-hunger-enable")
            if hunger_enable == "Yes":
                back_unit_name = unit_name.replace("BACK", "ARM")
                back_file_path = files[back_unit_name]
                #_, _, selected_unit_dict = load_and_select_unit(back_unit_name, back_file_path, selected_unit_dict, id_key=f"{unit_prefix}-{unit_name.lower()}")
                df = load_unit_info(back_file_path)
                selected_unit = st.selectbox(unit_name, df[back_unit_name].tolist(), key=f"{unit_prefix}-{unit_name.lower()}-back", index=preset_dict[unit_name])
                select_df = selected_df(df, back_unit_name, selected_unit)
                selected_unit_dict[unit_name] = select_df[back_unit_name].unique()[0]
            else:
                _, _, selected_unit_dict = load_and_select_unit(unit_name, file_path, selected_unit_dict, id_key=f"{unit_prefix}-{unit_name.lower()}", index=preset_dict[unit_name])
        else:
            _, _, selected_unit_dict = load_and_select_unit(unit_name, file_path, selected_unit_dict, id_key=f"{unit_prefix}-{unit_name.lower()}", index=preset_dict[unit_name])
    return selected_unit_dict

def init_ui():
    st.title("AC6 Nest Manager")
    st.sidebar.title("")

def main():
    selected_unit_dict = {}
    selected_opp_unit_dict = {}


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("YOU")
        select_preset = st.selectbox("Preset", ac_preset.keys(), index=0, key="preset_you")
        with st.expander("Your assembly"):
            selected_unit_dict = create_unit_selection(col1, "you", selected_unit_dict, ac_preset[select_preset])

    with col2:
        st.subheader("Opponent")
        select_opp_preset = st.selectbox("Preset", ac_preset.keys(), index=0, key="preset_opp")
        with st.expander("Opponent's assembly"):
            selected_opp_unit_dict = create_unit_selection(col2, "opp", selected_opp_unit_dict, ac_preset[select_opp_preset])

    st.divider()
    st.subheader("Match Result")
    result = st.radio("Result", ["Win", "Lose", "Draw"], key="result")
    if st.button("Save Result"):
        save_result(selected_unit_dict, selected_opp_unit_dict, result)

if __name__ == "__main__":
    init_ui()
    main()
