# 📋 Guia de Configuração e Execução: Portfólio Pessoal & Microserviço de Notificação

Este documento apresenta o passo a passo completo e detalhado para clonar, configurar, executar e testar o ecossistema composto por dois projetos Django independentes desenvolvidos para a disciplina de Sistemas Desenvolvidos em Web:

1. **Portfólio Pessoal:** Aplicação cliente principal operando na porta `8000`.
2. **Microserviço de Notificação:** Serviço autônomo de mensageria operando na porta `8001`.

A arquitetura segue o princípio de microsserviços, onde cada aplicação possui seu próprio código fonte, banco de dados isolado (`db.sqlite3`) e ciclo de implantação, comunicando-se exclusivamente via requisições HTTP REST com autenticação por Headers (`X-Api-Key` e `X-User-Id`).

---

## 🏗️ Visão Geral da Arquitetura

```text
┌────────────────────────────────┐         Requisições HTTP (Polling)         ┌────────────────────────────────┐
│       Projeto Portfólio        │ ─────────────────────────────────────────> │   Microserviço Notificação     │
│       (Porta Local: 8000)      │ <───────────────────────────────────────── │       (Porta Local: 8001)      │
│  - Django Templates            │          Headers: X-Api-Key                │  - Django REST Framework       │
│  - Polling JS (Cada 5s)        │                   X-User-Id                │  - Banco de Dados Próprio      │
└────────────────────────────────┘                                            └────────────────────────────────┘

```

##  Guia de Execução: Portfólio e Microsserviço de Notificações

Este guia detalha os passos necessários para executar o ecossistema do projeto, que está dividido em dois repositórios distintos:

* **Repositório 1 (Portfólio):** [https://github.com/FelipePereiraN/portifolio-django-felipepereiradonascimento](https://github.com/FelipePereiraN/portifolio-django-felipepereiradonascimento) (Roda na porta 8000).
* **Repositório 2 (Microsserviço):** [https://github.com/FelipePereiraN/notificacao_ms](https://github.com/FelipePereiraN/notificacao_ms) (Roda na porta 8001).

---

## 1. Configurando o Microsserviço de Notificações (Repositório 2 - Porta 8001)

O microsserviço é o sistema independente que armazena as notificações, controla a leitura e fornece a API REST. Ele deve ser configurado **primeiro**.

1. **Clone o repositório do microsserviço:**
```bash
git clone https://github.com/FelipePereiraN/notificacao_ms
cd notificacao_ms



2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

```


3. **Instale as dependências** (certifique-se de que `django`, `djangorestframework` e `django-cors-headers` estejam incluídos):
```bash
pip install django djangorestframework django-cors-headers

```


4. **Aplique as migrações** para criar o banco de dados independente do serviço:
```bash
python manage.py migrate

```


5. **Crie um superusuário** para gerenciar os dados no Django Admin:
```bash
python manage.py createsuperuser

```


6. **Inicie o servidor** especificamente na porta **8001**:
```bash
python manage.py runserver 8001

```



### 🔑 Passo Fundamental: Gerando a Chave de Acesso (Hash)

A comunicação entre os sistemas é feita via *headers* HTTP e exige uma chave gerada pelo microsserviço.

* Acesse o Django Admin do microsserviço: `http://127.0.0.1:8001/admin/`.
* Crie uma nova **Empresa** (ex: "Portfolio UAST").
* Um **hash de 16 caracteres** será gerado automaticamente. **Copie este hash**, pois você precisará colá-lo no código do portfólio.

---

## 2. Configurando o Portfólio (Repositório 1 - Porta 8000)

O portfólio consumirá esse microsserviço para exibir notificações em tempo real usando *polling*.

1. **Em um novo terminal**, clone o repositório do portfólio:
```bash
git clone https://github.com/FelipePereiraN/portifolio-django-felipepereiradonascimento
cd portifolio-django-felipepereiradonascimento

```


2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

```


3. **Instale as dependências** do projeto principal:
```bash
pip install -r requirements.txt

```


4. **Configure a Chave de Acesso:** Abra o arquivo `settings.py` (dentro da pasta de configurações do portfólio) e atualize a variável `NOTIFICACAO_MS_API_KEY` com o **hash que você copiou no passo anterior**:
```python
NOTIFICACAO_MS_URL = 'http://127.0.0.1:8001'
NOTIFICACAO_MS_API_KEY = 'COLE_O_SEU_HASH_AQUI'  # Atualize esta linha

```


5. **Aplique as migrações e crie um superusuário** (se for a primeira vez rodando o portfólio na sua máquina):
```bash
python manage.py migrate
python manage.py createsuperuser

```


6. **Inicie o servidor** na porta padrão **8000**:
```bash
python manage.py runserver

```



---

## 3. Testando a Integração

Para que o teste funcione corretamente, **os dois servidores (8000 e 8001) devem estar rodando simultaneamente em terminais separados**.

| Passo | Ação | Resultado Esperado |
| --- | --- | --- |
| **1. Login** | Acesse `http://127.0.0.1:8000/admin/` e faça login. Volte para a página principal do portfólio. | O sino de notificações deve aparecer no menu de navegação. |
| **2. Conexão** | Observe o ícone do sino na interface do portfólio. | Deve exibir **0** (verde), indicando conexão bem-sucedida e ausência de mensagens não lidas. |
| **3. Criar Notificação** | No Admin do microsserviço (`http://127.0.0.1:8001/admin/`), crie um *Target* e vincule uma nova *Notification* usando o `user_id` correspondente ao seu usuário logado no portfólio. | A notificação será salva no banco do microsserviço. |
| **4. Polling Automático** | Aguarde na aba do portfólio sem atualizar a página. | Em até **5 segundos**, o JavaScript fará o *polling* e o *badge* atualizará para vermelho, mostrando a quantidade de mensagens criadas. |
| **5. Leitura** | Clique no sino para abrir o dropdown e clique em cima da notificação não lida. | Uma requisição `PATCH` será enviada marcando-a como lida e atualizando o contador dinamicamente. |
| **6. Queda de Conexão** | No terminal do microsserviço (8001), aperte `Ctrl+C` para derrubar o servidor. | O *badge* mudará para um **X** (cinza), demonstrando o tratamento de falha na comunicação. |
