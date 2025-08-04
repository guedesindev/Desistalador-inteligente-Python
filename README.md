# Desistalador-inteligente-Python
Um código para um gerenciador de pacotes python, cuja ideia é manter os ambientes de desenvolvimento organizados.

Não muito raro você inicia um ambiente de desenvolvimento Python, começa a instalar dependências, desinstala outras, e quando você se apercebe, o ambiente está aquela bagunça, um estoque de dependências instaladas juntamente com módulos que seu projeto nem usa. Por que isso acontece? ALguns módulos Python possui dependências que são instaladas, assim que os módulos dependentes são instalados. A ferramenta `pip` não faz um gerenciamento inteligente das dependências, quando você desinstala um módulo ela não remove as dependências juntamente com o módulo, o que finda por restar muitos pacotes inúteis ao seu ambiente/projeto.

Alguns resolvem este problema por usar o ambiente com o `pyenv` ou com `poetry` que são gerenciadores de dependências mais inteligentes que o `pip`. O que já resolve este problema. Mas eu pensei, por que não criar um script que já faz isso para mim? Assim, na tentativa de entender como o `poetry` funciona criei o `smart_uninstall.py` que é o resultado do meu entendimento da ferramenta `poetry`. Pode ser que eu tenha entendido errado o funcionamento? Sim posso ter entendido errado. Pode ser que o poetry funcione de forma mais simples? Sim pode ser que funcione de modo mais simples. Mas achei legal ter feito esse projeto e caso você que esteja vendo este repositório tenha sugestões de como realizar o gerenciamento de modo melhor, estou aceitando sugetões e ensinamentos. Sou inician em Python e não sou desenvolvedor profissional, e este é o meu script de gerenciamento de dependÊncias.

## Preparação do ambiente

Para mim é sempre mais fácil de entender algo, quando penso de modo prático utilizando exemplos. Então, vamos lá. Eu criei um ambiente virtual `.env`
obs.: Fiz tudo no ambiente windows, utilizando o terminal do windows, com o powershell como prompt de comandos.

```powershell
    python -m venv .env
    .env/Scripts/activate

    # se você usa linux provavelmente para ativar o ambiente virtual necessite usar o diretório /bin e não /Scripts.
    # .env/bin/activate
```

Há a possibilidade, caso você esteja utilizando o windwos (powershell) de o script de ativação do ambiente virtual falhar, neste caso precisa setar o executor de scripts para RemoteSigned ou Unrestricted execute o powershell como administrador e faça:
```powershell
    Set-ExecutionPolicy RemoteSigned
    # Ou Set-ExecutionPolicy Unrestricted
```

Para saber se já pode executar scripts pelo powersheel faça:
```powershell
    Get-ExecutionPolicy
```

Pronto, agora que já estamos com o powershell devidamente autorizado, ambiente virtual pode ser ativado. A primeira coisa que vamos fazer é verificar se o pip está devidamente atualizado:
```powershell
    python -m pip install --upgrade pip
```
Caso esteja atualizado ele dirá, ser não estiver, atualizará. 
Para nosso exercício, vamos instalar dois módulos: Pandas e Correios
```powershell
    pip install pandas correios
```
Após o processo de instalação, ambos os módulos estarão instalados e suas dependências estarão no ambiente virtual, faça o teste:
```powershell
    pip list
    Package         Version
    --------------- -----------
    correios        6.4.8
    numpy           2.3.2
    packaging       25.0
    pandas          2.3.1
    phonenumbers    9.0.10
    pillow          11.3.0
    pip             25.2
    pipdeptree      2.28.0
    python-dateutil 2.9.0.post0
    pytz            2025.2
    six             1.17.0
    tzdata          2025.2
```
Percebeu quantos módulos foram instalados? Mas por que tantos se nós apenas instalamos o pandas e o correios? Porque cada módulo que instalamos tem suas dependências e o pip as instala automaticamente. 

O problema agora é no momento da desinstalação, porque o pip não faz um gerenciamento das dependências de cada módulo. Por exemplo se eu te perguntar da lista de módulos acima, quais são as dependências do pandas e quais são as dependências do correios, você saberia dizer? E mesmo que saiba, quando desinstalar cada módulo, para que o ambiente fique limpo, precisaremos desinstalar todas as dependências manualmente, o que dá muito trabalho.

Para facilitar nosso trabalho e completar nosso ambiente instalaremos um pacote que é excelente para gerenciamento dos pacotes instalados: `pipdeptree`
```powershell
   pip install pipdeptree
```

## Como funciona?
A primeira coisa que o smart_uninstall faz é criar um grafo dos módulos e suas dependências transitivas, e para isso utiliza-se do módulo pipdeptree (https://pypi.org/project/pipdeptree/). Olha só como o pipdeptree mostra a lista de módulos e suas dependências como uma árvore de diretórios:
```powershell
   pipdeptree
   correios==6.4.8
   ├── phonenumbers [required: Any, installed: 9.0.10]
   └── pillow [required: Any, installed: 11.3.0]
   pandas==2.3.1
   ├── numpy [required: >=1.26.0, installed: 2.3.2]
   ├── python-dateutil [required: >=2.8.2, installed: 2.9.0.post0]
   │   └── six [required: >=1.5, installed: 1.17.0]
   ├── pytz [required: >=2020.1, installed: 2025.2]
   └── tzdata [required: >=2022.7, installed: 2025.2]
   pipdeptree==2.28.0
   ├── packaging [required: >=24.1, installed: 25.0]
   └── pip [required: >=24.2, installed: 25.2]
```
E agora o smart_uninstall usa essa estrutura para criar os grafos e permitir que o usuário escolha qual módulo desinstalar. Assim que o usuário executa o script, a lista de módulos instalados no ambiente é apresentada, o usuário deve digitar o módulo que deseja desinstalar, o smart_uninstall realiza a desinstalação do módulo e suas dependências.
```powershell
   python smart_uninstall.py
   Arquivo 'requirements.json' gerado com sucesso!
   Pacotes instalados no seu atual ambiente:
   correios
   pandas
   pipdeptree
   python-dateutil
Digite o nome do pacote que você quer desinstalar (ex: pandas):
```

Perceba que um arquivo `requirements.json` é criado este arquivo é um txt, na estrutura JSON - JavaScript Object Notation, onde as chaves primárias são os módulos e listas são de dependencias são associados às chaves primárias, se quiser, encerre a aplicçaão do smart_uninstal com `CRTL+C` e veja o conteúdo do arquivo requirements.json:
```powershell
   type requirements.json
   [
    {
        "package": {
            "key": "correios",
            "package_name": "correios",
            "installed_version": "6.4.8"
        },
        "dependencies": [
            {
                "key": "phonenumbers",
                "package_name": "phonenumbers",
                "installed_version": "9.0.10",
                "required_version": "Any"
            },
            {
                "key": "pillow",
                "package_name": "pillow",
                "installed_version": "11.3.0",
                "required_version": "Any"
            }
        ]
    },
    {
        "package": {
            "key": "numpy",
            "package_name": "numpy",
            "installed_version": "2.3.2"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "packaging",
            "package_name": "packaging",
            "installed_version": "25.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pandas",
            "package_name": "pandas",
            "installed_version": "2.3.1"
        },
        "dependencies": [
            {
                "key": "numpy",
                "package_name": "numpy",
                "installed_version": "2.3.2",
                "required_version": ">=1.26.0"
            },
            {
                "key": "python-dateutil",
                "package_name": "python-dateutil",
                "installed_version": "2.9.0.post0",
                "required_version": ">=2.8.2"
            },
            {
                "key": "pytz",
                "package_name": "pytz",
                "installed_version": "2025.2",
                "required_version": ">=2020.1"
            },
            {
                "key": "tzdata",
                "package_name": "tzdata",
                "installed_version": "2025.2",
                "required_version": ">=2022.7"
            }
        ]
    },
    {
        "package": {
            "key": "phonenumbers",
            "package_name": "phonenumbers",
            "installed_version": "9.0.10"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pillow",
            "package_name": "pillow",
            "installed_version": "11.3.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pip",
            "package_name": "pip",
            "installed_version": "25.2"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pipdeptree",
            "package_name": "pipdeptree",
            "installed_version": "2.28.0"
        },
        "dependencies": [
            {
                "key": "packaging",
                "package_name": "packaging",
                "installed_version": "25.0",
                "required_version": ">=24.1"
            },
            {
                "key": "pip",
                "package_name": "pip",
                "installed_version": "25.2",
                "required_version": ">=24.2"
            }
        ]
    },
    {
        "package": {
            "key": "python-dateutil",
            "package_name": "python-dateutil",
            "installed_version": "2.9.0.post0"
        },
        "dependencies": [
            {
                "key": "six",
                "package_name": "six",
                "installed_version": "1.17.0",
                "required_version": ">=1.5"
            }
        ]
    },
    {
        "package": {
            "key": "pytz",
            "package_name": "pytz",
            "installed_version": "2025.2"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "six",
            "package_name": "six",
            "installed_version": "1.17.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "tzdata",
            "package_name": "tzdata",
            "installed_version": "2025.2"
        },
        "dependencies": []
    }
]
```

Veja que alguns pacotes (chaves primárias) têm a lista `dependencies` vazia, outros possui outros objetos populando a lista. A partir desta estrutura que o smart_uninstall cria o grafo de pacotes e suas dependências para que o usuário selecione o módulo que deseja desinstalar, e então saiba quais dependências transitivas devem ser desinstaladas também.

Também é interessante perceber que quando smart_uninstall é executado pelo interpretador python, ele apresenta para o usuário a lista de pacotes principais estão disponíveis.

Mas e se dois módulos fizerem uso da mesma dependência?
Por exemplo, suponhamos que o pandas e correios necessitem da dependência six (o que não é o caso). E aí, quando o `smart_uninstall` for desinstalar o correios e suas dependências, não afetará o funcionamento do pandas, excluindo uma dependência comum aos dois módulos? A maravilha é que o `smart_uninstall` faz a verificação se certa dependência a ser desinstalada afetará o funcionamento de outro módulo e então tal dependência é retirada da lista de pacotes a serem desinstalados. Muito smart, não é mesmo?

Agora vamos experimentar o `smart_uninstal` para desinstalar o módulo correios no nosso ambiente de teste.
```powershell
    python smart_uninstall.py
   Arquivo 'requirements.json' gerado com sucesso!
   Pacotes instalados no seu atual ambiente:
   correios
   pandas
   pipdeptree
   python-dateutil
   Digite o nome do pacote que você quer desinstalar (ex: pandas): correios

   Arquivo 'correios_uninstall_reqs.txt' gerado com sucess.
   Os seguintes pacotes serão desinstalados: correios, phonenumbers, pillow

   Agora você pode desinstalar o 'correios' e suas dependências exclusivas usando:
   Executando o comando: pip, uninstall, -r, correios_uninstall_reqs.txt, -y

   Desinstalação concluída com sucesso!
   Found existing installation: correios 6.4.8
   Uninstalling correios-6.4.8:
      Successfully uninstalled correios-6.4.8
   Found existing installation: phonenumbers 9.0.10
   Uninstalling phonenumbers-9.0.10:
      Successfully uninstalled phonenumbers-9.0.10
   Found existing installation: pillow 11.3.0
   Uninstalling pillow-11.3.0:
      Successfully uninstalled pillow-11.3.0
```

Agora para verificar como está o ambiente vamos fazer o `pip list` e ver se há resíduos da instalação do módulo correios
```powershell
   pip list
   Package         Version
   --------------- -----------
   numpy           2.3.2
   packaging       25.0
   pandas          2.3.1
   pip             25.2
   pipdeptree      2.28.0
   python-dateutil 2.9.0.post0
   pytz            2025.2
   six             1.17.0
   tzdata          2025.2
```

Compare agora com a lista antes da desisntalação do pacote dos correios. Agora você pode testar módulos em sua aplicação, e caso não seja o que você esperava, fazer a desinstalação completa do módulo e suas dependências, mantendo o seu ambiente de desenvolvimento controlado e limpo. 

Outra coisa interessante lembra do arquivo `requirements.json`, depois da desinstalação completa, ele também é excluído. 

Espero que tenha gastado do script, Até mais! 👋
