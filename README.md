# Controle de Concorrência em Banco de Dados

Este projeto gerencia múltiplas transações simultâneas em um banco de dados, evitando inconsistências e conflitos. Aqui você vai ver na prática como técnicas de controle de concorrência garantem que os dados permaneçam corretos e confiáveis, mesmo em ambientes altamente concorrentes.

# Estrutura do Algoritmo

📦 projeto
 ┣ 📂 app
 ┃ ┗ 📜 ... (códigos Flask)
 ┣ 📂 Class
 ┃ ┗ 📜 ... (lógica backend em Python)
 ┗ 📜 main.py

<p align="center">
<img width="460" height="95" alt="image" src="https://github.com/user-attachments/assets/8ac9379c-fb0d-4258-b5d9-eb37a9dfb924" />
</p>
O Algoritmo usa Python e Flask para conectar frontend e backend. A pasta app contém as rotas do Flask, a pasta Class guarda a lógica do backend, e o main.py organiza e integra tudo, garantindo que o frontend se comunique com o backend de forma eficiente.<br><br>
O backend do programa é estruturado da seguinte maneira:

<p align="center">
<img width="909" height="643" alt="image" src="https://github.com/user-attachments/assets/64e5e19c-5990-4fae-b61a-ea1cea535830" />
</p>

A classe "Transação" e "DataItemLockManager" 
# Transação 

Transações

# Layout da tela

<p align="center">
<img width="1600" height="740" alt="image" src="https://github.com/user-attachments/assets/e5f830e5-acff-4f6e-99cd-81b519dbf3c1" />
</p>
