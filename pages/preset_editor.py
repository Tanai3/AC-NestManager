import streamlit as st
import pandas as pd
import os
import json

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

preset_file = os.path.join(data_dir, "ac_preset.json") 
def load_preset(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path) as f:
            return json.load(f)
    else:
        st.error(f"File not found: {json_file_path}")
        return pd.DataFrame()

ac_preset = load_preset(preset_file)

def load_unit_info(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

def selected_df(base_df, unit, selected_unit):
    return base_df[base_df[unit] == selected_unit]

def load_and_select_unit(unit_name, file_path, selected_unit_dict, selected_unit_index_dict, index=0):
    df = load_unit_info(file_path)
    selected_unit = st.sidebar.selectbox(unit_name, df[unit_name].tolist(), index=index)
    index_position = df[df[unit_name] == selected_unit].index[0]
    selected_unit_index_dict[unit_name] = int(index_position)
    select_df = selected_df(df, unit_name, selected_unit)
    selected_unit_dict[unit_name] = select_df
    st.write(select_df)
    return df, select_df, selected_unit_dict, selected_unit_index_dict

def calc_total(selected_dict, param, include_list: list = None, exclude_list: list = None):
    total = 0
    for key, value in selected_dict.items():
        if include_list is not None:
            if key in include_list:
                total = total + value[param].unique()
        else:
            if exclude_list is not None and key in exclude_list:
                continue
            total = total + value[param].unique()
    return total

def init_ui():
    st.title("AC6 Assembly Simulator")
    st.sidebar.title("Your Assembly")

#if __name__ == "__main__":
def main():
    select_preset = st.selectbox("Preset", ac_preset.keys(), index=0, key="preset_you")
    selected_unit_dict = {}
    selected_unit_index_dict = {}

    with st.expander("Show all unit"):
        _, selected_head_df, selected_unit_dict, selected_unit_index_dict  = load_and_select_unit("HEAD", head_file, selected_unit_dict, selected_unit_index_dict ,index=ac_preset[select_preset]["HEAD"])
        _, selected_core_df, selected_unit_dict, selected_unit_index_dict_= load_and_select_unit("CORE", core_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["CORE"])
        _, selected_arm_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("ARM", arm_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["ARM"])
        _, selected_leg_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("LEG", leg_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["LEG"])
        _, selected_bst_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("BOOSTER", bst_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["BOOSTER"])
        _, selected_fcs_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("FCS", fcs_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["FCS"])
        _, selected_gen_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("GENERATOR", gen_file, selected_unit_dict, selected_unit_index_dict,index=ac_preset[select_preset]["GENERATOR"])
        r_arm_df, selected_r_arm_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("R-ARM", r_arm_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["R-ARM"])
        l_arm_df, selected_l_arm_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("L-ARM", l_arm_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["L-ARM"])
        #selected_r_back_df, selected_unit_dict = load_and_select_unit("R-BACK", r_back_file, selected_unit_dict)
        #selected_l_back_df, selected_unit_dict = load_and_select_unit("L-BACK", l_barck_file, selected_unit_dict)

        if ac_preset[select_preset]["R-Hunger"] == "Yes": 
            r_hunger_index = 0
        else: 
            r_hunger_index = 1
        hunger_right_enable = st.sidebar.radio("WeaponHunger_R-BACK", ["Yes","No"], index=r_hunger_index)
        if hunger_right_enable == "Yes":
            r_back_df = r_arm_df
            selected_r_back = st.sidebar.selectbox("R-BACK", r_back_df["R-ARM"].tolist(), index=ac_preset[select_preset]["R-BACK"])
            selected_r_back_df = selected_df(r_back_df, "R-ARM", selected_r_back)
            selected_unit_dict["R-BACK"] = selected_r_back_df
            index_position = r_arm_df[r_arm_df["R-ARM"] == selected_r_back].index[0]
            selected_unit_index_dict["R-BACK"] = int(index_position)
            st.write(selected_r_back_df)
     
        else:
            _, selected_r_back_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("R-BACK", r_back_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["R-BACK"])
    
        if ac_preset[select_preset]["L-Hunger"] == "Yes": 
            l_hunger_index = 0
        else: 
            l_hunger_index = 1
        hunger_left_enable = st.sidebar.radio("WeaponHunger_SHOULDER_LEFT", ["Yes","No"], index=l_hunger_index)
        if hunger_left_enable == "Yes":
            l_back_df = l_arm_df
            selected_l_back = st.sidebar.selectbox("L-BACK", l_back_df["L-ARM"].tolist(), index=ac_preset[select_preset]["L-BACK"])
            selected_l_back_df = selected_df(l_back_df, "L-ARM", selected_l_back)
            selected_unit_dict["L-BACK"] = selected_l_back_df
            index_position = l_arm_df[l_arm_df["L-ARM"] == selected_l_back].index[0]
            selected_unit_index_dict["L-BACK"] = int(index_position)
            st.write(selected_l_back_df)
     
        else:
            _, selected_l_back_df, selected_unit_dict, selected_unit_index_dict = load_and_select_unit("L-BACK", l_barck_file, selected_unit_dict, selected_unit_index_dict, index=ac_preset[select_preset]["L-BACK"])

    st.divider()
    total_ap = calc_total(selected_dict=selected_unit_dict, param="AP", include_list=["HEAD","CORE","ARM","LEG"])
    total_kinetic_def = calc_total(selected_dict=selected_unit_dict, param="Anti-Kinetic Defense", include_list=["HEAD","CORE","ARM","LEG"])
    total_energy_def = calc_total(selected_dict=selected_unit_dict, param="Anti-Energy Defense", include_list=["HEAD","CORE","ARM","LEG"])
    total_explosive_def = calc_total(selected_dict=selected_unit_dict, param="Anti-Explosive Defense", include_list=["HEAD","CORE","ARM","LEG"])
    total_stability = calc_total(selected_dict=selected_unit_dict, param="Attitude Stability", include_list=["HEAD","CORE","LEG"])
    total_weight = calc_total(selected_dict=selected_unit_dict, param="Weight") 
    #total_arm_carrying = 0
    total_arm_load = calc_total(selected_dict=selected_unit_dict, param="Weight", include_list=["WEAPONRIGHT","WEAPONLEFT"])
    total_load = calc_total(selected_dict=selected_unit_dict, param="Weight", exclude_list=["LEG"])
    total_en_load = calc_total(selected_dict=selected_unit_dict, param="EN Load", exclude_list=["GENERATOR"])
    total_en_output = selected_gen_df["EN Output"].unique()[0] * (selected_core_df["Generator Output"].unique()[0] / 100)
    en_supply = 1500 + (total_en_output - total_en_load) * 25 / 6 if total_en_output - total_en_load < 1800 else 9000 + (total_en_output - total_en_load - 1800) * 75 / 17
    en_supply = 100 if en_supply < 100 else en_supply
    en_recharge_delay = "{:.2f}".format(1000/(int(selected_core_df["Generator Supply"].iloc[0]) * ((int(selected_gen_df["EN Recharge"].iloc[0]) / 100))))

    total_df = pd.DataFrame(
            {
                "name": ["Total AP(総耐久)", "Total Kinetic Defense(耐弾防御)", "Total Energy Defense(耐EN防御)", "Total Explosive Defense(耐爆防御)", "Total Attitude Stability(姿勢安定性能)", "EN Capacity(EN容量)", "EN Supply(EN供給効率)", "EN Recovery Delay(EN補充遅延)", "Total Weight(総重量)", "Total Arm Load(腕部積載合計)", "Arm Load Limit(腕部積載上限)", "Total Load(積載合計)","Load Limit(積載上限)","EN Load(EN負荷合計)", "EN OUTPUT(EN出力)"],
                "total": [int(total_ap), int(total_kinetic_def), int(total_energy_def), int(total_explosive_def), int(total_stability), int(selected_gen_df["EN Capacity"].iloc[0]), int(en_supply), f"{en_recharge_delay}", int(total_weight), int(total_arm_load), int(selected_arm_df["Arms Load Limit"].iloc[0]),int(total_load), int(selected_leg_df["Load Limit"].iloc[0]),int(total_en_load), int(total_en_output)]
                #"total": [total_ap, total_kinetic_def, total_energy_def, total_explosive_def, total_stability, total_weight, total_load, int(selected_leg_df["Load Limit"].iloc[0]), total_en_load, total_en_output]
            } 
        )
    st.dataframe(total_df, column_config={"name": "AC SPEC", "total": "TOTAL"})
    if int(total_load) > int(selected_leg_df["Load Limit"].iloc[0]):
        st.write("積載超過")
    if int(total_arm_load) > int(selected_arm_df["Arms Load Limit"].iloc[0]):
        st.write("腕部積載超過")
    if int(total_en_load) > int(total_en_output):
        st.write("EN出力低下")
    #beta
    st.divider()
    st.write("※以下は参考値")
    en_recovery_delay = "{:.2f}".format(1000/(selected_gen_df["Supply Recovery"].unique()[0]*selected_core_df["Generator Supply"].unique()[0]*0.01))
    hovering_speed = 350 * float(selected_leg_df["Hovering Correction"].unique()[0]) if total_weight < 70000 else (350 - (total_weight - 70000) / 500) * float(selected_leg_df["Hovering Correction"].unique()[0])
    # ホバリング、AB速度
    beta_df = pd.DataFrame(
        {
            "name":["EN Recovery Delay(EN復元遅延)", "Hovering Speed(ホバリング速度)"],
            "total":[f"{en_recovery_delay}s", int(hovering_speed)]

        }
    )
    st.dataframe(beta_df, column_config={"name": "AC SPEC", "total": "TOTAL"})
    #unit_list = ["HEAD", "CORE", "ARM", "LEG", "BOOSTER", "FCS", "GENERATOR", "R-ARM", "L-ARM", "R-BACK", "L-BACK"]
    preset_name = st.text_input("Preset Name", key="name")
    if st.button("Add Preset"):
        selected_unit_index_dict["R-Hunger"] = hunger_right_enable
        selected_unit_index_dict["L-Hunger"] = hunger_left_enable
        new_data = {f"{preset_name}": selected_unit_index_dict}
        ac_preset.update(new_data)

        with open(preset_file, 'w') as file:
            json.dump(ac_preset, file, indent=4)

        st.write(ac_preset)


if __name__ == "__main__":
    init_ui()
    main()
