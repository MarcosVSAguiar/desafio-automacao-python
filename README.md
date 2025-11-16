⚙️ Desafio de Automação Digital: Gestão de Peças e Qualidade
🎯 Objetivo do Projeto
Este sistema em Python simula uma solução de automação digital para uma linha de produção, substituindo a inspeção manual de peças industriais. O foco é na avaliação automática de qualidade, gerenciamento de estoque em lotes (caixas) e geração de relatórios para rastreabilidade da produção.

🚀 Funcionalidades Chave do Sistema
O programa é conduzido por um Menu Interativo que permite executar as seguintes operações :
Opção,Funcionalidade,Descrição
1,Cadastrar nova peça,"Coleta os dados (ID, Peso, Cor, Comprimento) e imediatamente inicia a avaliação de qualidade."
2,Listar peças reprovadas,Exibe todas as peças que falharam na inspeção e o(s) motivo(s) exato(s) da reprovação[cite: 20].
3,Remover peça cadastrada,"Permite a manutenção do sistema, removendo peças da lista de reprovadas mediante inserção do ID."
4,Listar caixas fechadas,Mostra o total de caixas que atingiram o limite de 10 peças e detalha as peças na caixa atual (em andamento)[cite: 16].
5,Gerar relatório final,"Compila os totais de produção (Aprovadas, Reprovadas, Caixas Utilizadas) e estatísticas de motivos de falha [cite: 19-21]."
🧠 Como o Sistema Funciona (Lógica Detalhada)
1. Estrutura de Dados (OO)
O sistema utiliza uma Classe Peca para representar cada item de produção. Cada objeto armazena: id, peso, cor, comprimento, status (APROVADA/REPROVADA) e uma lista motivo_reprovacao para rastrear falhas múltiplas. O estado do sistema é mantido em listas globais (CAIXA_ATUAL, CAIXAS_FECHADAS, PECAS_REPROVADAS).

2. Regras de Qualidade
A função de avaliação aplica três condições lógicas simultâneas para aprovação :

Peso: Entre 95g e 105g.

Cor: Azul ou Verde.

Comprimento: Entre 10cm e 20cm. Se qualquer critério falhar, a peça é marcada como REPROVADA e o motivo é registrado.

3. Gerenciamento de Caixas
Peças aprovadas são adicionadas à lista CAIXA_ATUAL. A lógica de controle verifica continuamente o tamanho desta lista.

Se len(CAIXA_ATUAL) atinge 10 peças, o conteúdo é copiado para a lista CAIXAS_FECHADAS, e a CAIXA_ATUAL é limpa para iniciar o próximo lote.


💻 Como Executar o Programa em Python
Para rodar o sistema no seu ambiente local, siga estas instruções:

Pré-requisitos
Python 3.10+ instalado no seu sistema (verifique com python --version).

Passos para Execução
Clone o Repositório: Abra o terminal na pasta desejada e clone o projeto:
git clone https://github.com/Kbsadebroca/desafio-automacao-python.git
Acesse o Diretório: Navegue para a pasta principal do projeto.
cd desafio-automacao-python
Execute o Script: Inicie o programa principal:
python automacao_industrial.py
Obs: O nome do arquivo principal pode variar (e.g., main.py ou automacao_industrial.py) dependendo da sua estrutura. Utilize o nome correto do arquivo que contém a função menu_principal().

Interação: O Menu Interativo será exibido, permitindo a gestão das peças.

🌟 Exemplo de Fluxo (Entradas e Saídas)
Ação,Opção,Entradas Típicas (Exemplo),Saída Esperada
Peça Aprovada,1,Peso: 101.5 / Cor: azul / Comp: 18,✅ Peça P1 adicionada à caixa atual. (1/10)
Peça Reprovada,1,Peso: 110 / Cor: preto / Comp: 12,"❌ Peça REPROVADA! Motivo(s): Peso fora do limite (95g-105g), Cor inválida: preto..."
Fechamento,1 (Décima peça aprovada),Peso: 98 / Cor: verde / Comp: 15,📦 CAIXA FECHADA! Total de caixas fechadas: 1. Iniciando nova caixa.
Relatório,5,Nenhuma,Exibição do relatório consolidado e estatísticas de falha.
