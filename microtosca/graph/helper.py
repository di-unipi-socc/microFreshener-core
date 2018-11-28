

def get_type(ruamel_commented_map):
    return ruamel_commented_map['type'] if 'type' in ruamel_commented_map else ''

def get_requirements(ruamel_commented_map):
    return ruamel_commented_map['requirements'] if 'requirements' in ruamel_commented_map else []

def get_members(ruamel_commented_map):
    return ruamel_commented_map['members'] if 'members' in ruamel_commented_map else []
