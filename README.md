# Projeto Arthorias – Controle de Braço Robótico por Visão Computacional

Este repositório contém o código-fonte do Trabalho de Conclusão de Curso (TCC) de **João Vitor Messias da Cruz Damasio**, desenvolvido no Instituto Federal Catarinense – Campus Fraiburgo.  
O projeto explora a integração entre **visão computacional**, **aprendizado de máquina leve**, e **robótica**, implementando um **braço robótico controlado por gestos**, alinhado aos conceitos fundamentais da **Indústria 4.0**.

---

## 🧠 Objetivo

Desenvolver um sistema capaz de interpretar **gestos manuais capturados pela câmera** utilizando **MediaPipe + OpenCV**, convertendo essas informações em **comandos de movimento** para um **braço robótico baseado em servomotores**, controlado via **Arduino / RP2040**.

---

## ⚙️ Tecnologias Utilizadas

### **Visão Computacional**
- **MediaPipe Hands** – rastreamento de 21 pontos da mão
- **MediaPipe Pose** – rastreamento de ombro, cotovelo e punho
- **OpenCV** – captura de vídeo e processamento de imagem
- **NumPy** – cálculo de vetores, distâncias e interpolações

### **Robótica / Hardware**
- **Arduino / RP2040**
- **PyFirmata / ConfigurableFirmata**
- **Servomotores padrão (0–180°)**

### **Linguagem**
- **Python 3.11+**

---

## 📦 Estrutura do Projeto

```
arthorias/
│── main.py # Loop principal e captura de câmera
│── servo.py # Controle dos servos com Firmata
│── opencv.py # Funções visuais auxiliares
│── requirements.txt # Dependências
│── README.md # Este arquivo
```


---

## 🛠️ Instalação

### 1. Clone este repositório:
```bash
git clone https://github.com/joaovitormessias/arthorias
cd arthorias
```

### 2. Crie e ative um ambiente virtual (opcional, recomendado):
```
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências:

```
pip install -r requirements.txt
```
### 4. Instale e carregue o ConfigurableFirmata no Arduino/RP2040:

```
No Arduino IDE → Arquivo > Exemplos > Firmata > ConfigurableFirmata
Carregue o código e conecte via USB.
```
---

## Execução

Com o microcontrolador conectado, execute:

```
python3 main.py
```

A janela será aberta exibindo:

- A detecção da mão e do braço

- As conexões gráficas (landmarks)

- Os comandos em graus enviados aos servos

Pressione *Q* para sair.

---

## Como funciona o mapeamento dos gestos?

- Abertura/fechamento dos dedos → baseia-se na distância entre landmarks (ex.: 4–2, 8–6)

- Rotação do antebraço → calculada pela normal da palma via produto vetorial

- Aproximação do braço → deriva do movimento do eixo Z do punho

- Ângulos são filtrados por média exponencial e limitados entre 0° e 180°, garantindo estabilidade

---

## 📊 Aplicações do Projeto

- Interfaces naturais (HCI)

- Robótica educacional

- Automação industrial leve

- Estudos de prototipação em I4.0

- Bases para sistemas de teleoperação

---

## 📄 Licença

Este projeto é parte de um Trabalho de Conclusão de Curso, portanto:

- Pode ser utilizado para fins educacionais

- Pode ser modificado e estudado livremente

- Não é permitido uso comercial sem autorização

---

## 📚 Principais referências

- MediaPipe Documentation

- OpenCV Python Docs

- PyFirmata

- Arduino

---

## 👤 Autor

*João Vitor Messias da Cruz Damasio*
Tecnologia em Análise e Desenvolvimento de Sistemas
Instituto Federal Catarinense – Campus Fraiburgo  ​
