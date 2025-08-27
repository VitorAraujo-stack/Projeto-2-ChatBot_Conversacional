Chatbot 
Este é um chatbot interativo e multilíngue, construído para demonstrar a integração de modelos de linguagem de ponta com interfaces de usuário intuitivas. O projeto combina o poder do modelo Jamba com a versatilidade do Chainlit e a robustez do LangChain.

🚀 Tecnologias Utilizadas
Jamba-v0.1-chat-multilingual: O modelo de linguagem de ponta da Lightblue. Você pode facilmente trocar por outros modelos do Hugging Face para experimentar diferentes resultados.

Chainlit: Um framework para criar rapidamente interfaces de chat com um visual elegante.

LangChain: A estrutura que orquestra a lógica da conversa, gerencia a memória e o histórico.

Hugging Face Transformers: A biblioteca fundamental para o carregamento e uso do modelo.

Pyngrok: Ferramenta opcional para criar um túnel público para o seu servidor local, facilitando o acesso e a demonstração.

💻 Como Executar
Siga os passos abaixo para rodar o chatbot localmente.

Pré-requisitos
Certifique-se de ter o Python e os arquivos equeridos imstalados.
É altamente recomendado o uso de uma GPU compatível com CUDA para um bom desempenho.

Instalação
Clone este repositório:

Instale as dependências. É recomendado o uso de um ambiente virtual:
pip install -r requirements.txt
Execução
Execute o script principal:

chainlit run app.py
O Chainlit irá iniciar o servidor e abrir a interface do chat no seu navegador. Caso não abra, acesse http://localhost:8000. Se você tiver o pyngrok instalado, um túnel público será criado para acesso externo.

🔧 Customização
Uma das grandes vantagens deste projeto é a facilidade de customização. Para testar outros modelos de linguagem:

Abra o arquivo app.py.

Encontre a linha que define o nome do modelo:

Python

model_name_or_path = "lightblue/Jamba-v0.1-chat-multilingual"
Substitua o nome do modelo pelo que você deseja testar, por exemplo, o google/gemma-2b-it:

Python

model_name_or_path = "google/gemma-2b-it"
Salve o arquivo e execute o projeto novamente.

Observação: Alguns modelos podem exigir diferentes parâmetros de pipeline ou templates de prompt. Consulte a documentação do modelo escolhido no Hugging Face para garantir a compatibilidade.
