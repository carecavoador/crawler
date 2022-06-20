from sys import argv

options = [opt for opt in argv[1:] if opt.startswith("--")]
arguments = [arg for arg in argv[1:] if not arg.startswith("--")]

if "--config" in options:
    opt_index = argv.index("--config")
    config_file = argv[opt_idx+1]
    print(config_file)