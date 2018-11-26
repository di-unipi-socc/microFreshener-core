


def get_node_type(ruamel_commented_map):
    return ruamel_commented_map['type'] 

def get_requirements(ruamel_commented_map):
    #return ruamel_commented_map['requirements'] ? 
    return ruamel_commented_map['requirements'] if 'requirements' in ruamel_commented_map else []
