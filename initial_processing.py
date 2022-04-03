import weight_methods


def ducts_frame_init(df):
    df['InsulationThickness_mm'] = df['Insulation thickness'].apply(lambda x: first_element(x))

    # Circular ducts
    circular_ducts_df = df[df['Size'].str.contains('ø')].copy(deep=True)
    circular_ducts_df['D'] = circular_ducts_df['Size'].apply(lambda size: diameter(size))
    weight_methods.circular_ducts_calc_thickness(circular_ducts_df)
    weight_methods.circular_ducts_calc_weight(circular_ducts_df)

    # Rectangular ducts
    rect_ducts_df = df[~df['Size'].str.contains('ø')].copy(deep=True)
    rect_ducts_df['A'] = rect_ducts_df['Size'].apply(lambda size: first_element(size))
    rect_ducts_df['B'] = rect_ducts_df['Size'].apply(lambda size: second_element(size))
    weight_methods.rect_ducts_calc_thickness(rect_ducts_df)
    weight_methods.rect_ducts_calc_weight(rect_ducts_df)

    return circular_ducts_df, rect_ducts_df


def pipes_frame_init(df):
    df['InsulationThickness_mm'] = df['Insulation thickness'].str.rstrip('mм ').astype(float)
    weight_methods.pipes_calc_thickness(df)
    weight_methods.pipes_calc_weight(df)


def cable_trays_frame_init(df):
    df['Width'] = df['Size'].apply(lambda size: first_element(size))
    df['Height'] = df['Size'].apply(lambda size: second_element(size))
    # TODO: calculate cable weight


# Splitting size strings
def first_element(size_string):
    return size_string.str.split('xх*', expand=True)[0].str.rstrip('mм ').astype(int)


def second_element(size_string):
    return size_string.str.split('xх*', expand=True)[1].str.rstrip('mм ').astype(int)


def diameter(size_string):
    return size_string.str.lstrip('ø').rstrip('mм ').astype(int)
