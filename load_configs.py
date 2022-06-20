import json
from pathlib import Path


def load_config(config_file: str) -> dict:
    try:
        return json.load(open(config_file, "r", encoding="utf-8"))
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado.")
        config = {}
        config["jobs_folder"] = input(r"Localização da pasta de Entrada: ")
        config["output_folder"] = eval(input("Localização da pasta de Saída: "))
        config["layouts_folder"] = eval(input("Localização da pasta de Prints Layout: "))
        config["proofs_folder"] = eval(input("Localização da pasta de Provas Digitais: "))
    
        with open(Path(__file__).parent.joinpath(config_file), "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
        
        return config


cfg = load_config("teste.json")

for k, v in cfg.items():
    print(k, Path(v).parent)