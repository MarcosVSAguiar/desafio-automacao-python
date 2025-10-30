# =================================================================
# DESAFIO DE AUTOMAÇÃO DIGITAL: GESTÃO DE PEÇAS E QUALIDADE
# Código Python Unificado (Fases 1 a 4)
# =================================================================

from collections import Counter # Necessário para a contagem de motivos de reprovação

LIMITE_CAIXA = 10 # Capacidade máxima de peças por caixa 

# =================================================================
# FASE 1: Estrutura Base e Variáveis Globais
# =================================================================

class Peca:
    """
    Representa uma peça industrial com seus atributos e status de qualidade (id, peso, cor e comprimento).
    """
    def __init__(self, id, peso, cor, comprimento):
        self.id = id
        self.peso = peso
        self.cor = cor.lower()
        self.comprimento = comprimento
        self.status = "PENDENTE"
        self.motivo_reprovacao = [] # Lista para armazenar múltiplos motivos de reprovação

    def __str__(self):
        """Retorna uma representação amigável do objeto."""
        return f"ID: {self.id} | Status: {self.status} | Peso: {self.peso}g | Cor: {self.cor} | Comp.: {self.comprimento}cm"

# Variáveis Globais de Estado (O "Banco de Dados" do Sistema)
PECAS_REPROVADAS = [] 
CAIXA_ATUAL = [] 
CAIXAS_FECHADAS = []

# =================================================================
# Lógica de Avaliação de Qualidade (Fase 1)
# =================================================================

def avaliar_peca(peca: Peca) -> str:
    """
    Avalia a peça com base nos critérios de qualidade.
    """
    
    aprovado = True
    
    # 1. Avaliação do Peso (entre 95g e 105g)
    if not (95.0 <= peca.peso <= 105.0):
        aprovado = False
        peca.motivo_reprovacao.append("Peso fora do limite (95g-105g)")
        
    # 2. Avaliação da Cor (azul ou verde)
    if peca.cor not in ['azul', 'verde']:
        aprovado = False
        peca.motivo_reprovacao.append(f"Cor inválida: {peca.cor} (esperado: azul ou verde)")
        
    # 3. Avaliação do Comprimento (entre 10cm e 20cm)
    if not (10.0 <= peca.comprimento <= 20.0):
        aprovado = False
        peca.motivo_reprovacao.append("Comprimento fora do limite (10cm-20cm)")
        
    # Define o status final
    if aprovado:
        peca.status = "APROVADA"
    else:
        peca.status = "REPROVADA"
        
    return peca.status

# =================================================================
# Gerenciamento de Fluxo (Fase 2)
# =================================================================

def gerenciar_caixas(peca_aprovada):
    """
    Armazena peças e fecha a caixa ao atingir 10 peças.
    """
    global CAIXA_ATUAL
    global CAIXAS_FECHADAS
    
    CAIXA_ATUAL.append(peca_aprovada)
    print(f"\n✅ Peça {peca_aprovada.id} adicionada à caixa atual. ({len(CAIXA_ATUAL)}/{LIMITE_CAIXA})")
    
    # Fecha a caixa quando atinge a capacidade máxima
    if len(CAIXA_ATUAL) == LIMITE_CAIXA:
        CAIXAS_FECHADAS.append(CAIXA_ATUAL.copy()) 
        print(f"\n📦 CAIXA FECHADA! Capacidade máxima atingida: {LIMITE_CAIXA} peças.")
        print(f"Total de caixas fechadas: {len(CAIXAS_FECHADAS)}")
        
        CAIXA_ATUAL.clear() # Inicia uma nova caixa
        print("Iniciando nova caixa.")

def cadastrar_nova_peca(proximo_id):
    """
    Opção 1: Coleta dados e inicia o ciclo de avaliação/armazenamento.
    """
    print(f"\n--- 📝 Cadastro da Peça ID: P{proximo_id} ---")
    
    try:
        # Recebe os dados de cada peça produzida
        peso = float(input("Digite o peso da peça em gramas (95g-105g): "))
        cor = input("Digite a cor da peça (azul ou verde): ")
        comprimento = float(input("Digite o comprimento da peça em cm (10cm-20cm): "))
        
        peca = Peca(id=f"P{proximo_id}", peso=peso, cor=cor, comprimento=comprimento)
        
        status = avaliar_peca(peca) # Avalia automaticamente se a peça está aprovada ou reprovada
        
        if status == "APROVADA":
            gerenciar_caixas(peca)
        else:
            PECAS_REPROVADAS.append(peca)
            print("❌ Peça REPROVADA!")
            # Total de peças reprovadas e o motivo da reprovação 
            print(f"Motivo(s): {', '.join(peca.motivo_reprovacao)}")
            
    except ValueError:
        print("\n⚠️ Erro de entrada. Peso e Comprimento devem ser valores numéricos. Tente novamente.")
    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro inesperado: {e}")

# =================================================================
# Menu Interativo e Funções de Manutenção (Fase 3)
# =================================================================

def listar_pecas():
    """
    Opção 2: Lista as peças reprovadas.
    """
    print("\n--- 🔎 LISTA DE PEÇAS REPROVADAS ---")
    if not PECAS_REPROVADAS:
        print("🎉 Não há peças reprovadas no sistema.")
        return

    print(f"Total de Peças Reprovadas: {len(PECAS_REPROVADAS)}\n")

    for i, peca in enumerate(PECAS_REPROVADAS, 1):
        motivos = ", ".join(peca.motivo_reprovacao)
        print(f"[{i}] {peca}")
        print(f"     Motivos: {motivos}")
        print("-" * 40)

def remover_peca():
    """
    Opção 3: Permite remover uma peça reprovada (manutenção).
    """
    print("\n--- 🗑️ REMOVER PEÇA CADASTRADA (Foco em Reprovadas) ---")
    
    if not PECAS_REPROVADAS:
        print("Não há peças reprovadas para remover.")
        return
        
    id_remover = input("Digite o ID da peça a ser removida (Ex: P10): ").upper()
    
    peca_encontrada = next((peca for peca in PECAS_REPROVADAS if peca.id == id_remover), None)
            
    if peca_encontrada:
        PECAS_REPROVADAS.remove(peca_encontrada)
        print(f"\n✅ Peça ID {id_remover} removida com sucesso.")
    else:
        print(f"\n❌ Erro: Peça com ID {id_remover} não encontrada na lista de reprovadas.")

def listar_caixas_fechadas():
    """
    Opção 4: Lista as caixas fechadas e a situação da caixa atual.
    """
    print("\n--- 📦 LISTA DE CAIXAS FECHADAS ---")

    if not CAIXAS_FECHADAS:
        print("Nenhuma caixa foi fechada ainda.")
    else:
        # Quantidade de caixas utilizadas
        print(f"Total de Caixas Fechadas: {len(CAIXAS_FECHADAS)}\n")
        
        for i, caixa in enumerate(CAIXAS_FECHADAS, 1):
            ids_pecas = [peca.id for peca in caixa]
            print(f"Caixa N° {i} (FECHADA, {LIMITE_CAIXA} peças):")
            print(f"   Peças (IDs): {', '.join(ids_pecas)}")
            print("-" * 40)
            
    print(f"\nStatus da CAIXA ATUAL (Em andamento): {len(CAIXA_ATUAL)}/{LIMITE_CAIXA} peças.")
    if CAIXA_ATUAL:
        ids_atuais = [peca.id for peca in CAIXA_ATUAL]
        print(f"   Peças (IDs): {', '.join(ids_atuais)}")

# =================================================================
# Relatório Final e Encerramento (Fase 4)
# =================================================================

def gerar_relatorio_final():
    """
    Opção 5: Gera o relatório consolidado.
    """
    
    # --- Cálculo de Totais ---
    total_caixas_fechadas = len(CAIXAS_FECHADAS)
    total_pecas_fechadas = total_caixas_fechadas * LIMITE_CAIXA
    total_pecas_caixa_atual = len(CAIXA_ATUAL)
    
    total_pecas_aprovadas = total_pecas_fechadas + total_pecas_caixa_atual # Total de peças aprovadas
    total_pecas_reprovadas = len(PECAS_REPROVADAS) # Total de peças reprovadas 
    total_pecas_processadas = total_pecas_aprovadas + total_pecas_reprovadas
    
    quantidade_caixas_utilizadas = total_caixas_fechadas
    if total_pecas_caixa_atual > 0:
        quantidade_caixas_utilizadas += 1 # Conta a caixa em andamento
        
    # --- Estatísticas de Reprovação ---
    motivos_contagem = Counter()
    for peca in PECAS_REPROVADAS:
        for motivo in peca.motivo_reprovacao:
            # Pega a primeira palavra do motivo (Peso, Cor, Comprimento)
            motivo_simples = motivo.split(' ')[0] 
            motivos_contagem[motivo_simples] += 1
            
    # =================================================================
    # EXIBIÇÃO DO RELATÓRIO
    # =================================================================
    
    print("\n" + "#" * 60)
    print("       📊 RELATÓRIO CONSOLIDADO DE PRODUÇÃO E QUALIDADE")
    print("#" * 60)
    
    print("\n[ TOTAIS GERAIS ]")
    print("-" * 25)
    print(f"Total de Peças Processadas: {total_pecas_processadas}")
    print(f"Total de Peças Aprovadas: {total_pecas_aprovadas}")
    print(f"Total de Peças Reprovadas: {total_pecas_reprovadas}")

    print("\n[ GESTÃO DE CAIXAS ]")
    print("-" * 25)
    print(f"Quantidade de Caixas FechADAS: {total_caixas_fechadas}")
    print(f"Quantidade de Caixas Utilizadas (Total): {quantidade_caixas_utilizadas} caixas") # Quantidade de caixas utilizadas
        
    print("\n[ MOTIVOS DE REPROVAÇÃO ]")
    print("-" * 25)
    if not motivos_contagem:
        print("Nenhuma reprovação registrada.")
    else:
        for motivo, contagem in motivos_contagem.items():
            # Total de peças reprovadas e o motivo da reprovação 
            print(f"Motivo '{motivo}': {contagem} falha(s)")
            
    print("\n" + "#" * 60)
    print("Sistema encerrado. Obrigado!")
    print("#" * 60)

# =================================================================
# Execução Principal (Menu Interativo)
# =================================================================

def menu_principal():
    """
    Função principal que gerencia o menu interativo.
    """
    proximo_id = 1
    
    while True:
        print("\n" + "=" * 50)
        print("🤖 DESAFIO DE AUTOMAÇÃO DIGITAL: GESTÃO DE PEÇAS")
        print("=" * 50)
        
        # --- LINHAS CORRIGIDAS ---
        # As citações foram movidas para comentários (iniciados com #)
        print("1. Cadastrar nova peça")         #
        print("2. Listar peças reprovadas")      #
        print("3. Remover peça cadastrada")      #
        print("4. Listar caixas fechadas")       #
        print("5. Gerar relatório final e Sair") #
        # --- FIM DA CORREÇÃO ---
        
        print("-" * 50)
        
        try:
            opcao = input("Selecione uma opção (1-5): ")
            
            if opcao == '1':
                cadastrar_nova_peca(proximo_id)
                proximo_id += 1
            elif opcao == '2':
                listar_pecas()
            elif opcao == '3':
                remover_peca()
            elif opcao == '4':
                listar_caixas_fechadas()
            elif opcao == '5':
                gerar_relatorio_final() 
                break 
            else:
                print("Opção inválida. Por favor, escolha um número de 1 a 5.")
                
        except Exception as e:
            print(f"\n⚠️ Ocorreu um erro no menu: {e}. Tente novamente.")

if __name__ == '__main__':
    menu_principal()