import dicts_methods
import engineering_consts as ec
import math


# --- Ducts ---

# Circular ducts
def circular_ducts_calc_thickness(df):
    df['Thickness_mm'] = df['D'].apply(lambda x:
                                       dicts_methods.find_by_ceil_in_dict(x, ec.thickness_by_diameter))


def circular_ducts_calc_weight(df):
    df['SelfWeight_kg/m'] = (df['Thickness_mm'] / 1000
                             * df['D'] * math.pi / 1000
                             * ec.density['steel'])
    df['InsulationDensity'] = df['Insulation Type'].map(ec.insulation_density)
    df['InsulationWeight_kg/m'] = insulation_weight_for_circular(df)
    df['Weight_kg/m'] = df['SelfWeight_kg/m'] + df['InsulationWeight_kg/m']


# Rectangular ducts
def rect_ducts_calc_thickness(df):
    df['Thickness_mm'] = df[['A', 'B']].max(axis=1).apply(lambda x:
                                                          dicts_methods.find_by_ceil_in_dict(x, ec.thickness_by_width))


def rect_ducts_calc_weight(df):
    df['SelfWeight_kg/m'] = (df['Thickness_mm'] / 1000
                             * (df['A'] + df['B']) * 2 / 1000
                             * ec.density['steel'])
    df['InsulationDensity'] = df['Insulation Type'].map(ec.insulation_density)
    df['InsulationWeight_kg/m'] = (df['InsulationThickness_mm'] / 1000
                                   * (df['A'] + df['B'] + df['InsulationThickness_mm'] * 2) * 2 / 1000
                                   * df['InsulationDensity'])
    df['Weight_kg/m'] = df['SelfWeight_kg/m'] + df['InsulationWeight_kg/m']


# --- Pipes ---


def pipes_calc_thickness(df):
    df['Thickness_mm'] = (df['D'] - df['d']) / 2.0


def pipes_calc_weight(df):
    df['MatDensity_kg/m3'] = df['Type name'].apply(
        lambda name: dicts_methods.find_text_inclusion_in_dict(name, ec.pipes_density, ec.density['steel']))
    df['SelfWeight_kg/m'] = (df['Thickness_mm'] / 1000
                             * df['D'] * math.pi / 1000
                             * df['MatDensity_kg/m3'])
    df['InsulationDensity'] = df['Insulation Type'].map(ec.insulation_density)
    df['InsulationWeight_kg/m'] = insulation_weight_for_circular(df)
    df['Filling_ratio'] = df['Type name'].apply(
        lambda name: dicts_methods.find_text_inclusion_in_dict(name, ec.pipes_filling_ratio, 1.0))
    df['FillerWeight_kg/m'] = (math.pi * (df['d'] / 1000) ** 2 / 4
                               * ec.density['water']
                               * df['Filling_ratio'])

    # TODO : add percentage of filling

    df['Weight_kg/m'] = (df['SelfWeight_kg/m']
                         + df['InsulationWeight_kg/m']
                         + df['FillerWeight_kg/m'])


# --- Cable Trays ---


def cable_trays_calc_weight(df):
    df['TrayWeight_kg/m'] = ((df['Width']
                              + df['Height'] * 2)
                             * ec.density['steel']
                             * 10 ** (-6)
                             )
    df['CableWeight_kg/m'] = (df['Width']
                              * df['Height']
                              * ec.cable_trays_filling_ratio
                              * ec.cables_average_density
                              * 10 ** (-6)
                              )
    df['Weight_kg/m'] = df['CableWeight_kg/m'] + df['TrayWeight_kg/m']


# --- Additional methods
def insulation_weight_for_circular(df):
    return (
            math.pi / 4
            * (
                    (df['D'] + 2 * df['InsulationThickness_mm']) ** 2
                    - df['D'] ** 2
            )
            * (10 ** (-6))
            * df['InsulationDensity']
    )
