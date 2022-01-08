import yaml

stream = open("info.yml", 'r')
data = yaml.safe_load(stream)

milton_username = "BLAH"
milton_pass = "PASS"

data["fb_user"]["UserLogin"] = milton_username
data["fb_user"]["UserPassword"] = milton_pass

with open("info.yml", 'w') as yaml_file:
    yaml_file.write( yaml.dump(data, default_flow_style=False))
    print("done")