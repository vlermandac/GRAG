import subprocess


def error(message, b, c):
    level = "error"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def warning(message, b, c):
    level = "warn"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def info(message, b, c):
    level = "info"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def debug(message, b, c):
    level = "debug"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")
