# Projeto ReVeste: Módulo Biométrico e Intervenção IoB (IoT & IoB POC)

## 🎯 Objetivo da POC

Este módulo demonstra a **integração mínima exigida** de IOB (Inteligência do Comportamento) no projeto ReVeste.

O objetivo é simular um login biométrico por reconhecimento facial (usando a câmera) que, ao ser concluído com sucesso, **dispara uma ação de intervenção proativa** da IA (o IoB). A ação é o alerta sobre o alto risco de apostas e a sugestão de investimentos alternativos.

## 💻 Requisitos

Você precisará ter o **Python 3.x** e as bibliotecas listadas abaixo instaladas.

1.  **Python 3.x**
2.  **OpenCV (cv2):** Para acessar a câmera, desenhar o contorno (simulado) e capturar a imagem do cadastro.
3.  **Módulos Padrão:** `os`, `time`, `datetime`, `json`, `random`.

## ⚙️ Instalação das Dependências

Instale a biblioteca `opencv-python` via pip:

```bash
pip install opencv-python
