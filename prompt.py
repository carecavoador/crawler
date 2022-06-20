def prompt_user(prompt: str, choices: list) -> str:
    while True:
        print(prompt)
        choice = input("> ").lower()
        if choice in choices:
            return choice
        print("Opção inválida.")


resposta = prompt_user("Digite sim para sair.", ["sim", "nao"])
print(resposta)