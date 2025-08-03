import json
import os
from collections import defaultdict
from python_commands import generate_dependencies_json, uninstalling_package

# Criar um mapa das dependências
def build_dependency_graph(tree_json):
    """
    Constrói um grafo de dependênicas e um mapa de quem depende de quem.
    Retorna:
        parant_map: dict {dependent_package_name: set_of_packages_it_depends_on}
        child_map: dict {dependency_name: set_of_packages_that_depend_on_it}
        all_packages: set of all package names found
    """

    parent_map = {}
    child_map = defaultdict(set)
    all_packages = set()

    def process_node_recursive(node, parent_name=None):
        # Acessar o nome do pacote a partir da chave 'package' ou diretamente no nó
        pkg_name = node.get('key', node.get('package', {}).get('key')).lower()
        if not pkg_name: # Ignorar nós sem chave
            return
        
        all_packages.add(pkg_name)

        # Se este nó tem um pai, registrar a relação
        if parent_name:
            if parent_name not in parent_map:
                parent_map[parent_name] = set()
            parent_map[parent_name].add(pkg_name)
            child_map[pkg_name].add(parent_name)

        # Percorrer as dependências
        for dep_node in node.get('dependencies', []):
            process_node_recursive(dep_node, pkg_name)
    
    # Inicia o processametno pelos pacotes de nível superior na lista
    for pkg_info in tree_json:
        process_node_recursive(pkg_info)
    
    return parent_map, child_map, all_packages

def get_uninstall_list_smart(target_package, parent_map, child_map, all_packages):
    """
    Gera uma lista de pacotes para desinstalar, incluindo o target_package
    e suas dependências que *não* são compartilhadas por outros pacotes instalados
    """
    target_package_lower = target_package.lower()

    if target_package_lower not in all_packages:
        print(f"Erro: O pacote '{target_package}' não foi encontrado na árvore de dependências.")
        return set()
    
    # 1º Coletar o pacote alvo e todas as suas dependências (diretas e transitivas)
    packages_to_consider_for_removal = set()
    queue = [target_package_lower]

    while queue:
        current_pkg = queue.pop(0)
        packages_to_consider_for_removal.add(current_pkg)

        # Adiciona as dependências do pacote atual à fila
        if current_pkg in parent_map:
            for dep in parent_map[current_pkg]:
                if dep not in packages_to_consider_for_removal:
                    queue.append(dep)
    
    # 2º Filtrar dependências que são compartilhadas por outros pacotes
    final_uninstall_list = set()
    for pkg_to_remove in packages_to_consider_for_removal:
        # Verifica se o pacote tem dependentes (i.e. é uuma dependência de algo)
        if pkg_to_remove in child_map:
            # Quais pacotes dependen do pkg_to_remove?
            dependents = child_map[pkg_to_remove]

            # Filtra os dependentes que não estão na nossa lista de remoção
            dependents_to_keep = {dep for dep in dependents if dep not in packages_to_consider_for_removal}

            # Se não sobrou nenhum dependent para manter, ele pode ser removido
            if not dependents_to_keep:
                final_uninstall_list.add(pkg_to_remove)
            # Caso contrário, é uma dependência compartilhada e deve ser mantida
        else:
            # Se o pacote não tem dependentes no grafo, ele pode ser removido
            final_uninstall_list.add(pkg_to_remove)
    
    return final_uninstall_list

# --- Parte principal do script ---
if __name__ == "__main__":

    json_filename = generate_dependencies_json('requirements.json') # Criando a lista de dependências instaladas no ambiente atualmente

    if not os.path.exists(json_filename):
        print(f"Erro: O arquivo '{json_filename}' não foi encontrado.")
        print("Certifique-se de ter rodado 'pipdeptree --json > requiri'")

    with open(json_filename, 'r', encoding='utf-8') as file:
        try:
            dependency_tree = json.load(file)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print(f"O arquivo 'requirements.sjon' pode estar vazio ou corrompido.")
            exit(1)

        # Constrói o grafo completo de dependências        
        parent_map, child_map, all_packages = build_dependency_graph(dependency_tree)

        # Solicita ao usuário o pacote a ser desinstalado
        print(f"Pacotes instalados no seu atual ambiente:")
        for package in parent_map:
            print(f"{package}")

        target_package = input('Digite o nome do pacote que você quer desinstalar (ex: pandas): ')


        # Gera a lista de pacotes para desinstalação inteligente
        packcages_to_uninstall = get_uninstall_list_smart(target_package, parent_map, child_map, all_packages)

        if packcages_to_uninstall:
            output_req_file = f"{target_package}_uninstall_reqs.txt"
            with open(output_req_file, 'w') as f:
                for pkg in sorted(list(packcages_to_uninstall)):
                    f.write(f"{pkg}\n")
            
            print(f"\nArquivo '{output_req_file}' gerado com sucess.")
            print(f"Os seguintes pacotes serão desinstalados: {', '.join(sorted(list(packcages_to_uninstall)))}")
            print(f"\nAgora você pode desinstalar o '{target_package}' e suas dependências exclusivas usando: ")
            uninstalling_package(output_req_file)
            # print(f"\n    pip uninstall -r {output_req_file} -y")
        else:
            print(f"\nNão foi possível gerar um arquivo de desinstalação para '{target_package}'.")