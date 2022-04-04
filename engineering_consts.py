import yaml

with open("config.yaml", 'r', encoding='utf-8') as config_file:
    parsed_data = yaml.safe_load(config_file)


def map_dict_with_yaml(yaml_name, default_dict, other_dict=None):
    try:
        if other_dict is None:
            dictionary = regular_mapping(yaml_name)
        else:
            dictionary = complex_mapping(yaml_name, other_dict)
    except NameError:
        dictionary = default_dict
        print(yaml_name, Exception)
    except AttributeError:
        dictionary = default_dict
        print(yaml_name, Exception)
    return dictionary


def map_value_with_yaml(yaml_name, default_value=None):
    try:
        value = regular_mapping(yaml_name)
    except NameError:
        value = default_value
    return value


def regular_mapping(yaml_name):
    dictionary = parsed_data[yaml_name]
    return dictionary


def complex_mapping(yaml_name, other_dict):
    dictionary = regular_mapping(yaml_name)
    for key in dictionary.keys():
        try:
            dictionary[key] = other_dict[dictionary[key]]
        except KeyError:
            print(dictionary[key], ' -- not found in densities list')
    return dictionary


# defaults
density_def = {'steel': 7850,
               'insulation': 150,
               'water': 1000,
               'polypropylene': 1000,
               'copper': 2000}
thickness_by_diameter_def = {200: 0.5,
                             450: 0.7,
                             800: 0.9,
                             1250: 1.0,
                             1600: 1.2,
                             2000: 1.4}
thickness_by_width_def = {250: 0.5,
                          1000: 0.7,
                          2000: 0.9}
pipes_filling_ratio_def = {'RC_P_Polyethylene': 0.5,
                           'RC_CastIron_PAM': 0.5,
                           'RC_PVC_Gravity_Chemkor_SN8': 0.5,
                           'Труба стальная электросварная': 0.5}

density = map_dict_with_yaml('Densities', density_def)
thickness_by_diameter = map_dict_with_yaml('Thickness by diameter', thickness_by_diameter_def)
thickness_by_width = map_dict_with_yaml('Thickness by width', thickness_by_width_def)
pipes_filling_ratio = map_dict_with_yaml('Pipes filling ratios', pipes_filling_ratio_def)
cable_trays_filling_ratio = map_value_with_yaml('Cable trays filling ratio')
cables_average_density = map_value_with_yaml('Cables average density')

pipes_density_def = {'Steal': density['steel'],
                     'Steel': density['steel'],
                     'Электросварн': density['steel'],
                     'Iron': density['steel'],
                     'Cooper': density['copper'],
                     'Copper': density['copper'],
                     'PP-R': density['polypropylene'],
                     'ПЭ': density['polypropylene'],
                     'PE': density['polypropylene'],
                     'ABN': density['polypropylene'],
                     'Poly': density['polypropylene'],
                     'PVC': density['polypropylene']}

pipes_density = map_dict_with_yaml('Pipes densities', pipes_density_def, density)
insulation_density = map_dict_with_yaml('Insulation types', None, density)
