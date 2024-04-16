from .variables import Variables


def setup_variables(project_root):
    vars = Variables(project_root)
    vars.write_env_variables()
    return vars
