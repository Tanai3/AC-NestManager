import streamlit as st
import pandas as pd
import os

data_dir = "./data/"
head_file = data_dir + "AC6-Unit - HEAD.csv"
core_file = data_dir + "AC6-Unit - CORE.csv"
arm_file = data_dir + "AC6-Unit - ARM.csv"
leg_file = data_dir + "AC6-Unit - LEG.csv"
bst_file = data_dir + "AC6-Unit - BOOSTER.csv"
fcs_file = data_dir + "AC6-Unit - FCS.csv"
gen_file = data_dir + "AC6-Unit - GENERATOR.csv"
r_arm_file = data_dir + "AC6-Unit - R-ARM.csv"
l_arm_file = data_dir + "AC6-Unit - L-ARM.csv"
r_back_file = data_dir + "AC6-Unit - R-BACK.csv"
l_barck_file = data_dir + "AC6-Unit - L-BACK.csv"

def load_unit_info(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

def selected_df(base_df, unit, selected_unit):
    return base_df[base_df[unit] == selected_unit]

def load_and_select_unit(unit_name, file_path, selected_unit_dict, id_key):
    df = load_unit_info(file_path)
    selected_unit = st.selectbox(unit_name, df[unit_name].tolist(), key=id_key)
    select_df = selected_df(df, unit_name, selected_unit)
    selected_unit_dict[unit_name] = select_df
    return df, select_df, selected_unit_dict

def select_preset():
    pass


def init_ui():
    st.title("AC6 Nest Manager")
    st.sidebar.title("")

def main():
    selected_unit_dict = {}

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("YOU")
        st.divider()
        _, selected_head_df, selected_unit_dict = load_and_select_unit("HEAD", head_file, selected_unit_dict, id_key="head-key")
        _, selected_core_df, selected_unit_dict = load_and_select_unit("CORE", core_file, selected_unit_dict, id_key="core-key")
        _, selected_arm_df, selected_unit_dict = load_and_select_unit("ARM", arm_file, selected_unit_dict, id_key="arm-key")
        _, selected_leg_df, selected_unit_dict = load_and_select_unit("LEG", leg_file, selected_unit_dict, id_key="leg-key")
        _, selected_bst_df, selected_unit_dict = load_and_select_unit("BOOSTER", bst_file, selected_unit_dict, id_key="booster-key")
        _, selected_fcs_df, selected_unit_dict = load_and_select_unit("FCS", fcs_file, selected_unit_dict, id_key="fcs-key")
        _, selected_gen_df, selected_unit_dict = load_and_select_unit("GENERATOR", gen_file, selected_unit_dict, id_key="generator-key")
        r_arm_df, selected_r_arm_df, selected_unit_dict = load_and_select_unit("R-ARM", r_arm_file, selected_unit_dict, id_key="r-arm-key")
        l_arm_df, selected_l_arm_df, selected_unit_dict = load_and_select_unit("L-ARM", l_arm_file, selected_unit_dict, id_key="l-arm-key")

        hunger_right_enable = st.radio("WeaponHunger_R-BACK", ["Yes","No"], index=1, key="hunger-right-enable")
        if hunger_right_enable == "Yes":
            r_back_df = r_arm_df
            selected_r_back = st.selectbox("R-BACK", r_back_df["R-ARM"].tolist(), key="r-back-key")
            selected_r_back_df = selected_df(r_back_df, "R-ARM", selected_r_back)
            selected_unit_dict["R-BACK"] = selected_r_back_df
 
        else:
            _, selected_r_back_df, selected_unit_dict = load_and_select_unit("R-BACK", r_back_file, selected_unit_dict, id_key="r-back-key")

        hunger_left_enable = st.radio("WeaponHunger_SHOULDER_LEFT", ["Yes","No"], index=1, key="hunger-left-enable")
        if hunger_left_enable == "Yes":
            l_back_df = l_arm_df
            selected_l_back = st.selectbox("L-BACK", l_back_df["L-ARM"].tolist(), key="l-back-key")
            selected_l_back_df = selected_df(l_back_df, "L-ARM", selected_l_back)
            selected_unit_dict["L-BACK"] = selected_l_back_df
 
        else:
            _, selected_l_back_df, selected_unit_dict = load_and_select_unit("L-BACK", l_barck_file, selected_unit_dict, id_key="l-back-key")


    selected_opp_unit_dict = {}
    with col2:
        st.subheader("opponent")
        st.divider()
        _, selected_opp_head_df, selected_opp_unit_dict = load_and_select_unit("HEAD", head_file, selected_opp_unit_dict, id_key="opp-head-key")
        _, selected_opp_core_df, selected_opp_unit_dict = load_and_select_unit("CORE", core_file, selected_opp_unit_dict, id_key="opp-core-key")
        _, selected_opp_arm_df, selected_opp_unit_dict = load_and_select_unit("ARM", arm_file, selected_opp_unit_dict, id_key="opp-arm-key")
        _, selected_opp_leg_df, selected_opp_unit_dict = load_and_select_unit("LEG", leg_file, selected_opp_unit_dict, id_key="opp-leg-key")
        _, selected_opp_bst_df, selected_opp_unit_dict = load_and_select_unit("BOOSTER", bst_file, selected_opp_unit_dict, id_key="opp-bst-key")
        _, selected_opp_fcs_df, selected_opp_unit_dict = load_and_select_unit("FCS", fcs_file, selected_opp_unit_dict, id_key="opp-fcs-key")
        _, selected_opp_gen_df, selected_opp_unit_dict = load_and_select_unit("GENERATOR", gen_file, selected_opp_unit_dict, id_key="opp-gen-key")
        r_arm_df, selected_opp_r_arm_df, selected_opp_unit_dict = load_and_select_unit("R-ARM", r_arm_file, selected_opp_unit_dict, id_key="opp-r-arm-key")
        l_arm_df, selected_opp_l_arm_df, selected_opp_unit_dict = load_and_select_unit("L-ARM", l_arm_file, selected_opp_unit_dict, id_key="opp-l-arm-key")
    
        hunger_right_enable = st.radio("WeaponHunger_R-BACK", ["Yes","No"], index=1, key="opp-hunger-right-enable")
        if hunger_right_enable == "Yes":
            r_back_df = r_arm_df
            selected_opp_r_back = st.selectbox("R-BACK", r_back_df["R-ARM"].tolist(), key="opp-r-beck-key")
            selected_opp_r_back_df = selected_df(r_back_df, "R-ARM", selected_opp_r_back)
            selected_opp_unit_dict["R-BACK"] = selected_opp_r_back_df
    
        else:
            _, selected_opp_r_back_df, selected_opp_unit_dict = load_and_select_unit("R-BACK", r_back_file, selected_opp_unit_dict, id_key="opp-r-back-key")
    
        hunger_left_enable = st.radio("WeaponHunger_SHOULDER_LEFT", ["Yes","No"], index=1, key="opp-hunger-left-enable")
        if hunger_left_enable == "Yes":
            l_back_df = l_arm_df
            selected_opp_l_back = st.selectbox("L-BACK", l_back_df["L-ARM"].tolist(), key="opp-l-back-key")
            selected_opp_l_back_df = selected_df(l_back_df, "L-ARM", selected_opp_l_back)
            selected_opp_unit_dict["L-BACK"] = selected_opp_l_back_df
    
        else:
            _, selected_opp_l_back_df, selected_opp_unit_dict = load_and_select_unit("L-BACK", l_barck_file, selected_opp_unit_dict, id_key="opp-l-back-key")

if __name__ == "__main__":
    init_ui()
    main()