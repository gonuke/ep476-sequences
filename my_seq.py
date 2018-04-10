import yaml

import seq_driver

import seq_input


seq_driver.print_seq_dict(seq_driver.seq_driver_generic(seq_input.init_list, seq_input.length))

with open('seq_input.yml', 'r') as f:
    yaml_input = yaml.load(f)
print(yaml_input)

seq_driver.print_seq_dict(seq_driver.seq_driver_generic(yaml_input['init_list'], yaml_input['length']))
