# Controle de Concorrência em Banco de Dados

Este projeto gerencia múltiplas transações simultâneas em um banco de dados, evitando inconsistências e conflitos. Aqui você vai ver na prática como técnicas de controle de concorrência garantem que os dados permaneçam corretos e confiáveis, mesmo em ambientes altamente concorrentes.

# Estrutura do Algoritmo

<p align="center">
<img width="377" height="192" alt="image" src="https://github.com/user-attachments/assets/60822029-cd1e-4963-84d1-bea3250dc329" />
</p>

Este projeto segue uma arquitetura orientada a objetos e está organizado da seguinte forma: <br>

- app/ – Contém o código do framework Flask, responsável por gerenciar o backend em Python e estabelecer a comunicação com o frontend por meio de rotas.
- Class/ – Reúne as classes e métodos em Python que compõem a lógica de negócio do backend.
- main.py – Atua como ponto central do projeto, organizando e integrando os métodos da pasta Class/ com as rotas da pasta app/, estabelecendo assim a conexão entre frontend e backend.

O backend do programa é estruturado da seguinte maneira:

<p align="center">
<img width="909" height="643" alt="image" src="https://github.com/user-attachments/assets/64e5e19c-5990-4fae-b61a-ea1cea535830" />
</p>

# 1. Transação 

No algoritmo, as transações são representadas pela classe `Transações`, que armazena:

- **Itens de dados** individuais da transação
- **Nome da transação**
- **Lista global** contendo os itens de dados de todas as transações
- **Lista de transações em estado de encolhimento**

Cada transação mantém seus próprios itens de dados para futuras operações, como write_lock.
Esses itens são comparados com os itens de dados gerenciados pela classe `Data Item Lock Manager` para evitar conflitos e corrigir possíveis erros, como no exemplo abaixo:
<p align="center">
<img width="213" height="294" alt="image" src="https://github.com/user-attachments/assets/179d867d-e659-47a3-972a-bdc87d00b79a" />
</p>
Para facilitar o entendimento: sempre que atualizamos um item de dado em uma transação, essa atualização é refletida tanto na lista de itens da própria transação quanto na classe `Data Item Lock Manager`.

- Se `X` for atualizado, o `X` da `Transação` também será atualizado.
- Ao mesmo tempo, o `X` em `Data Item Lock Manager` receberá o novo valor.

### Cenário de conflito 

No exemplo da imagem acima, quando a Transação 2 tentar executar um write-item novamente, o sistema irá verificar:
- Se o valor de `X` na `Transação` for diferente do valor de `X` em `Data Item Lock Manager`, o usuário receberá a seguinte mensagem:

```text
Operação não pode ser realizada, o X foi alterado. Para prosseguir, leia o valor atualizado de X na Transação 2.
```

Esse controle evita que dados desatualizados sobrescrevam informações recentes, garantindo a **consistência** do sistema.

# Data Item Lock Manager

Além de tornar possível que transações só façam operações com itens atualizados, o Data Item Lock Manager é responsável por praticamente todo o correto funcionamento do algoritmo. <br>
O Data Item Lock Manager possui as seguintes variáveis:
- **count**: contador para a criação de novas variáveis.
- **data_items**: items de dados, onde os valores desses itens são sempre o mais recente realizado pelas transações.
- **lock_register**: registro de locks, guarda apenas registros de write_lock e read_lock 
- **complete_lock_register**: registro de locks completo: além de guardar os registros de write_lock, read_lock e unlock, guarda read_item, write_item, incremento e decremento, todas as ações são acompanhadas da data e horário em que foram realizadas.
- **array_position**: posição da lista de item específico, essa variável é utilizada para armazenar uma posição de array para uma determinada consulta que alguma das funções esteja tentando realizar. Geralmente o array_position aponta para um registro de lock específico, essa função será explicada de maneira menos abstrata mais a frente.

# 1. Funções

## Lock de modo múltiplo e encolhimento

<img width="1123" height="579" alt="image" src="https://github.com/user-attachments/assets/bb9cc831-6684-435e-b31c-406d2e62ce92" />

Tanto o bloqueio exclusivo, como o bloqueio compartilhado, são chamados na **main** como mostrado no código acima. Após validar se a transação não está em fase de encolhimento, o write_lock da classe “Data Item Lock Manager” é chamado para tentar realizar a ação. Caso a transação esteja em fase de encolhimento, uma mensagem é mostrada no log da interface para o usuário, explicando a impossibilidade de write_lock devido a fase de encolhimento. <br>

Por meio do encapsulamento de funções, muitas das funções do algoritmo estão sempre chamando outras, é dessa maneira que as validações das regras de bloqueio ocorrem e tornam possível o correto funcionamento no FrontEnd. Na função "write_lock" da imagem anterior, são chamadas outras funções como:

-**increment_lock**
-**get_error**: Essa função é responsável por recuperar um erro que tenha acontecido
-**has_exclusive_lock**: Confere se há algum bloqueio exclusivo em um item de dado específico, caso tenha, ele define o valor do item “array_position” da classe, como o número da lista do lock_register onde aquele item está guardado, assim sendo possível acessar informações como: quem está bloqueando um item. 

# Layout da tela

<p align="center">
<img width="1600" height="740" alt="image" src="https://github.com/user-attachments/assets/e5f830e5-acff-4f6e-99cd-81b519dbf3c1" />
</p>
