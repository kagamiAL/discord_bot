constants_table = {
    
    'repeat_ping_cool_down': 3600,
    
}

def get_constant(constant_name: str):
    return constants_table[constant_name]

def modify_constant(constant_name: str, new_value: str):
    print(type(constants_table[constant_name]))
    if (type(constants_table[constant_name]) == int):
        new_value = int(new_value)
    constants_table[constant_name] = new_value
