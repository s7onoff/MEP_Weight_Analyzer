import weight_methods


def ducts_frame_init(df):
    df['InsulationThickness_mm'] = first_element(df['Insulation thickness'])

    # Circular ducts
    circular_ducts_df = df[df['Size'].str.contains('ø')].copy(deep=True)
    circular_ducts_df['D'] = diameter(circular_ducts_df['Size'])
    weight_methods.circular_ducts_calc_thickness(circular_ducts_df)
    weight_methods.circular_ducts_calc_weight(circular_ducts_df)

    # Rectangular ducts
    rect_ducts_df = df[~df['Size'].str.contains('ø')].copy(deep=True)
    rect_ducts_df['A'] = first_element(rect_ducts_df['Size'])
    rect_ducts_df['B'] = second_element(rect_ducts_df['Size'])
    weight_methods.rect_ducts_calc_thickness(rect_ducts_df)
    weight_methods.rect_ducts_calc_weight(rect_ducts_df)

    return circular_ducts_df, rect_ducts_df


def pipes_frame_init(df):
    df['InsulationThickness_mm'] = first_element(df['Insulation thickness'])
    df['D'] = diameter(df['Outside diameter'])
    df['d'] = diameter(df['Inside diameter'])
    weight_methods.pipes_calc_thickness(df)
    weight_methods.pipes_calc_weight(df)


def cable_trays_frame_init(df):
    df['Width'] = first_element(df['Size'])
    df['Height'] = second_element(df['Size'])
    weight_methods.cable_trays_calc_weight(df)


# Splitting size strings
def first_element(ds):
    return ds.str.split('xх*', expand=True)[0].astype(str).str.replace(',', '.').str.rstrip('mм ').astype(float)


def second_element(ds):
    return ds.str.split('xх*', expand=True)[1].astype(str).str.replace(',', '.').str.rstrip('mм ').astype(float)


def diameter(ds):
    return ds.astype(str).str.replace(',', '.').str.lstrip('ø').str.rstrip('mм ').astype(float)
