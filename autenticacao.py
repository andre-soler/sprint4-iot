import cv2
import os
import time
from datetime import datetime
import json 
import random 
import numpy as np

# --- CONFIGURAÇÃO E DADOS DE PERSISTÊNCIA ---
CADASTRO_IMAGEM_PATH = "rosto_cadastrado_poc.jpg"
USUARIO_DATA_PATH = "usuario_data.txt"

# Variável global para armazenar o perfil
perfil_usuario = {}

def abrir_webcam():
    """Tenta abrir a webcam com diferentes índices para máxima compatibilidade."""
    for i in range(5):
        cap = cv2.VideoCapture(i)
        # Tenta definir uma resolução padrão para estabilizar as coordenadas de simulação
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if cap.isOpened():
            print(f"[CÂMERA] Webcam aberta com sucesso no índice {i}.")
            return cap
    
    print("ERRO CRÍTICO: Não foi possível acessar a webcam em nenhum índice (0-4).")
    return None

# --- FUNÇÕES DE LÓGICA DE NEGÓCIO (IoB) ---

def salvar_dados_usuario(nome, sobrenome, idade):
    """Salva os dados do usuário usando JSON."""
    global perfil_usuario
    perfil_usuario = {
        "nome": nome,
        "sobrenome": sobrenome,
        "idade": idade,
        "score_risco": "ALTO", 
        "user_id": 42
    }
    with open(USUARIO_DATA_PATH, 'w') as f:
        json.dump(perfil_usuario, f)
    print(f"[SUCESSO] Dados do usuário salvos: {nome} {sobrenome}, {idade} anos.")

def carregar_dados_usuario():
    """Carrega os dados do usuário usando JSON."""
    global perfil_usuario
    if os.path.exists(USUARIO_DATA_PATH):
        try:
            with open(USUARIO_DATA_PATH, 'r') as f:
                data = json.load(f)
                perfil_usuario = data
            return True
        except Exception as e:
            perfil_usuario = {}
            return False
    return False

def consultar_ia_preventiva():
    """SIMULA o Serviço de IA Preventiva."""
    if not perfil_usuario:
        return "Erro: Perfil de usuário não carregado.", [], "INDEFINIDO"

    nome = perfil_usuario['nome']
    score = perfil_usuario.get('score_risco', 'ALTO')
    
    mensagem_alerta = f"ALERTA IoB, {nome}! Seu Score de Risco ({score}) está alto. Lembre-se do seu compromisso financeiro e evite sites de apostas."
    
    opcoes_investimento = [
        "1. Tesouro Direto (Baixo Risco) - ReVeste Sugere 80% do valor da aposta",
        "2. Fundo de Renda Fixa (Segurança) - ReVeste Sugere 10%",
        "3. LCI/LCA (Isento de Imposto) - ReVeste Sugere 10%"
    ]
    
    return mensagem_alerta, opcoes_investimento, score

# --- MÓDULOS FACIAIS (SIMULAÇÃO DINÂMICA) ---

def desenhar_contorno_dinamico(frame, cor_contorno, fator_movimento, w_quadrado, h_quadrado):
    """Desenha um retângulo que simula o contorno da cabeça/rosto, com movimento aleatório."""
    H, W, _ = frame.shape
    
    # Centro do Frame
    center_x, center_y = W // 2, H // 2
    
    # ⚠️ NOVO AJUSTE: Move o centro verticalmente para cima para atingir o rosto
    AJUSTE_VERTICAL = -40 
    
    # Cálculo de movimento aleatório para simular a procura 
    if fator_movimento > 0:
        offset_x = random.randint(-fator_movimento, fator_movimento)
        offset_y = random.randint(-fator_movimento, fator_movimento)
    else:
        # Fica travado no centro ajustado
        offset_x, offset_y = 0, 0
        
    # Coordenadas do canto superior esquerdo (x, y)
    x = center_x - w_quadrado // 2 + offset_x
    y = center_y - h_quadrado // 2 + offset_y + AJUSTE_VERTICAL # Aplica o ajuste vertical
    
    # Coordenadas do canto inferior direito (x+w, y+h)
    x_fim = x + w_quadrado
    y_fim = y + h_quadrado
    
    # 1. Desenha o Retângulo (cv2.rectangle)
    cv2.rectangle(frame, (x, y), (x_fim, y_fim), cor_contorno, 2)
    
    # 2. Texto de status 
    if fator_movimento > 0:
        cv2.putText(frame, "PROCURANDO...", (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, cor_contorno, 1)
    else:
        cv2.putText(frame, "RECONHECIDO", (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, cor_contorno, 1)

    return frame


def realizar_cadastro():
    """Pede os dados, salva o perfil e simula a captura da biometria com contorno dinâmico."""
    print("\n--- 1. CADASTRO DE PERFIL ---")
    
    nome = input("Digite seu nome: ")
    sobrenome = input("Digite seu sobrenome: ")
    idade = input("Digite sua idade: ")
    
    if not (nome and sobrenome and idade.isdigit()):
        print("Dados inválidos. Tente novamente.")
        return
        
    salvar_dados_usuario(nome, sobrenome, int(idade)) 
    
    video_capture = abrir_webcam()
    if not video_capture: return
    
    print("\n[CADASTRO FACIAL] Olhe para a área delimitada e pressione 'C' para SALVAR.")
    
    # Tamanho ajustado para simular o rosto: 150x200
    w_quadrado, h_quadrado = 150, 200 
    
    while True:
        ret, frame = video_capture.read()
        if not ret: break
        
        cor = (0, 255, 255) # Amarelo: Procurando
        
        # Simula o movimento de procura (fator_movimento > 0)
        frame = desenhar_contorno_dinamico(frame, cor, fator_movimento=20, w_quadrado=w_quadrado, h_quadrado=h_quadrado)
        
        texto_instrucao = "Pressione 'C' para Cadastrar Biometria"
        cv2.putText(frame, texto_instrucao, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, cor, 2)
        cv2.imshow('ReVeste - Módulo de Cadastro Facial (DINÂMICO)', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(CADASTRO_IMAGEM_PATH, frame)
            print(f"[SUCESSO] Imagem de cadastro de '{perfil_usuario['nome']}' salva.")
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    video_capture.release(); cv2.destroyAllWindows()


def autenticar_e_entrar():
    """Simula o login biométrico com contorno dinâmico e trava o acesso."""
    
    if not carregar_dados_usuario() or not os.path.exists(CADASTRO_IMAGEM_PATH):
        print("\nERRO: Nenhum perfil ou rosto cadastrado. Por favor, escolha a Opção 1 primeiro.")
        return
        
    video_capture = abrir_webcam()
    if not video_capture: return
    
    nome_completo = f"{perfil_usuario['nome']} {perfil_usuario['sobrenome']}"
    print(f"\n[LOGIN FACIAL] Olá, {nome_completo}. Pressione 'L' para validar a entrada no App.")
    
    # Tamanho ajustado para simular o rosto: 150x200
    w_quadrado, h_quadrado = 150, 200
    
    # 1. FASE DE PROCURA (Movimento)
    tempo_inicio_procura = time.time()
    PROCURA_DURACAO = 2 # Tempo em segundos
    
    while time.time() - tempo_inicio_procura < PROCURA_DURACAO:
        ret, frame = video_capture.read()
        if not ret: break
        
        # Quadrado se movendo (fator_movimento > 0)
        frame = desenhar_contorno_dinamico(frame, (0, 165, 255), fator_movimento=10, w_quadrado=w_quadrado, h_quadrado=h_quadrado) # Laranja
        
        cv2.putText(frame, "PROCURANDO ROSTO CADASTRADO...", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 165, 255), 2)
        cv2.imshow('ReVeste - Módulo de Autenticação Facial (DINÂMICO)', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            video_capture.release(); cv2.destroyAllWindows(); return
    
    # 2. FASE DE RECONHECIMENTO (Quadrado Travado)
    print("Rosto detectado e travado. Pressione 'L' para autenticar.")
    
    while True:
        ret, frame = video_capture.read()
        if not ret: break
        
        # Quadrado travado no centro (fator_movimento = 0)
        frame = desenhar_contorno_dinamico(frame, (0, 255, 0), fator_movimento=0, w_quadrado=w_quadrado, h_quadrado=h_quadrado) # Verde
        
        texto_instrucao = f"RECONHECIDO! Pressione 'L' para Entrar no App"
        cv2.putText(frame, texto_instrucao, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('ReVeste - Módulo de Autenticação Facial (DINÂMICO)', frame)
        
        # GATILHO DE LOGIN MANUAL
        if cv2.waitKey(1) & 0xFF == ord('l'):
            
            # --- PROVA DE CONCEITO: Disparo da Lógica IoB ---
            mensagem_alerta, opcoes_investimento, score_risco = consultar_ia_preventiva()

            # 2. Exibe o Resultado (Entrada no App e Intervenção)
            print("\n=======================================================")
            print(f"ACESSO LIBERADO: Bem-vindo(a) ao ReVeste, {perfil_usuario['nome']}!")
            print("=======================================================")
            
            print(f"SCORE DE RISCO (IoB): {score_risco}")
            print(f"MENSAGEM DE ALERTA: {mensagem_alerta}")
            
            print("\n--- OPÇÕES DE INVESTIMENTO SUGERIDAS (Personalizadas) ---")
            for opcao in opcoes_investimento:
                print(f"  - {opcao}")
            print("----------------------------------------------------------")

            # Feedback visual final
            cv2.putText(frame, "ACESSO CONCEDIDO!", (50, 80), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
            cv2.imshow('ReVeste - Módulo de Autenticação Facial (FINAL)', frame)

            time.sleep(10) 
            video_capture.release(); cv2.destroyAllWindows()
            return

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    video_capture.release(); cv2.destroyAllWindows()


def menu_principal():
    """Menu principal para Cadastro e Login."""
    carregar_dados_usuario() 
    
    while True:
        print("\n--- ReVeste: Módulo Biométrico/IoB Completo (FINAL) ---")
        if perfil_usuario:
            print(f"** PERFIL ATIVO: {perfil_usuario['nome']} {perfil_usuario['sobrenome']} **")
        else:
            print("** NENHUM PERFIL CADASTRADO **")

        print("1. Cadastrar Perfil (Dados Pessoais + Biometria Simples)")
        print("2. Entrar no App (Biometria Facial + Intervenção IoB)")
        print("3. Sair")
        
        escolha = input("Escolha uma opção (1, 2 ou 3): ")
        
        if escolha == '1':
            realizar_cadastro()
            
        elif escolha == '2':
            autenticar_e_entrar()
                
        elif escolha == '3':
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()