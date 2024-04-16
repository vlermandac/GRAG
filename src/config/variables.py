import yaml


class Variables:
    def __init__(self, project_root):
        self.project_root = project_root
        self.list = self.parse_config_file()

    def parse_config_file(self):
        with open(f'{self.project_root}/config.yml', 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        return cfg

    def write_env_variables(self):
        with open(f'{self.project_root}.env', 'w') as file:
            for element in self.list['env-variables']:
                for key, value in element.items():
                    file.write(f'{key.upper()}={value}\n')
