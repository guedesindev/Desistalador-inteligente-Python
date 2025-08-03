import os
import subprocess

def generate_dependencies_json(output_path):
    try:
        # Executa o pipdeptree e captura a saída
        result = subprocess.run(
            ['pipdeptree', '--json'],
            capture_output=True,
            text=True,
            check=True
        )

        # Salva a saída no arquivo JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)

        print(f"Arquivo '{output_path}' gerado com sucesso!")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o pipdeptree: {e}")
        print(f"Saída de erro: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O comando 'pipdeptree' não foi encontrado.Verifique se está instalado no seu PATH.")

def uninstalling_package(file_name):
    if not os.path.exists(file_name):
        print(f"Erro: o arquivo '{file_name}' não foi encontrado.")
    else:
        command = ['pip', 'uninstall', '-r', file_name, '-y']

        print(f'Executando o comando: {", ".join(command)}')

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            print("\nDesinstalação concluída com sucesso!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f'\nErro durante a desinstalação: {e}')
            print(f"Saída de erro: {e.stderr}")
        except FileNotFoundError:
            print(f"Erro: O comando 'pip' não foi encontrado. Certifique-se de que o ambiente virtual está ativado.")

