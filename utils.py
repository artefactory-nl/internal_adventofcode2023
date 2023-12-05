def read_input(path: str) -> list[str]:
    with open(path, 'r') as file:
        return [line.replace("\n", "") for line in file.readlines()]