import pandas as pd
import initial_processing

input_frame = pd.read_excel('Mega_022_02_TEST_DB_Lite2.xlsx', None)

# Decomposing
for sheet_name in list(input_frame.keys()):
    if str(sheet_name).casefold().__contains__('cable'):
        cables_df = input_frame[sheet_name]
        initial_processing.cable_trays_frame_init(cables_df)
    elif str(sheet_name).casefold().__contains__('duct'):
        ducts_df = input_frame[sheet_name]
        circular_ducts_df, rect_ducts_df = initial_processing.ducts_frame_init(ducts_df)
    elif str(sheet_name).casefold().__contains__('pipe'):
        pipes_df = input_frame[sheet_name]
        initial_processing.pipes_frame_init(pipes_df)

sum_df = pd.concat([cables_df, pipes_df, rect_ducts_df, circular_ducts_df])
sum_df['Weight_kg'] = sum_df['Length'] * sum_df['Weight_kg/m'] * 10 ** (-3)
print(sum_df['Weight_kg'].sum())