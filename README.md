# FBDS_DOWNLOAD
Este projeto contém um script em Python capaz de baixar automaticamente todos os arquivos disponíveis no diretório público da FBDS para o estado da Paraíba, acessando subpastas de forma recursiva e realizando downloads em paralelo para máxima performance. O objetivo é facilitar a obtenção dos dados disponibilizados em:
https://geo.fbds.org.br/

O script identifica diretórios, navega por eles e baixa todos os arquivos encontrados, mantendo a mesma estrutura de pastas localmente.

**Funcionalidades**
- Varredura automática de diretórios e subdiretórios
- Preserva a estrutura de pastas original
- Download paralelo com ThreadPoolExecutor
- Verificação de links válidos
- Criação automática das pastas necessárias
- Evita baixar arquivos repetidos
- Compatível com qualquer diretório HTML simples (estilo Apache/NGINX)

**Requisitos**
Antes de executar, instale as dependências:

`pip install requests beautifulsoup4`
