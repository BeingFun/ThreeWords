from src.constants.constants import Constants


def dump_config(key: str, value: bool):
    config_path = Constants.ROOT_PATH + r"\config\config.ini"
    with open(config_path, "r", encoding="utf-8") as file:
        config = file.readlines()
    new_config = []
    for line in config:
        if line[0] != "#" and line[0] != "[":
            if line.split(" = ")[0] == key:
                new_line = line.split(" = ")[0] + " = " + str(value) + "\n"
                new_config.append(new_line)
                continue
        new_config.append(line)
    config = "".join(new_config)
    with open(config_path, "w", encoding="utf-8") as file:
        file.write(config)
