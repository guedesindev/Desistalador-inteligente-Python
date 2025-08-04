# Desistalador-inteligente-Python
Um código para um gerenciador de pacotes python, cuja ideia é manter os ambientes de desenvolvimento organizados.

Não muito raro você inicia um ambiente de desenvolvimento Python, começa a instalar dependências, desinstala outras, e quando você se apercebe, o ambiente está aquela bagunça, um estoque de dependências instaladas juntamente com módulos que seu projeto nem usa. Por que isso acontece? ALguns módulos Python possui dependências que são instaladas, assim que os módulos dependentes são instalados. A ferramenta `pip` não faz um gerenciamento inteligente das dependências, quando você desinstala um módulo ela não remove as dependências juntamente com o módulo, o que finda por restar muitos pacotes inúteis ao seu ambiente/projeto.

Alguns resolvem este problema por usar o ambiente com o `pyenv` ou com `poetry` que são gerenciadores de dependências mais inteligentes que o `pip`. O que já resolve este problema. Mas eu pensei, por que não criar um script que já faz isso para mim? Assim, na tentativa de entender como o `poetry` funciona criei o `smart_uninstall.py` que é o resultado do meu entendimento da ferramenta `poetry`. Pode ser que eu tenha entendido errado o funcionamento? Sim posso ter entendido errado. Pode ser que o poetry funcione de forma mais simples? Sim pode ser que funcione de modo mais simples. Mas achei legal ter feito esse projeto e caso você que esteja vendo este repositório tenha sugestões de como realizar o gerenciamento de modo melhor, estou aceitando sugetões e ensinamentos. Sou inician em Python e não sou desenvolvedor profissional, e este é o meu script de gerenciamento de dependÊncias.

## Como Funciona?

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

```
