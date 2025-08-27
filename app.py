# Importa as bibliotecas necessárias.
# 'pyngrok' é para criar um túnel para o servidor local, expondo-o publicamente (útil para testes ou demonstrações).
# 'torch' é a biblioteca principal para deep learning, usada pelo modelo.
from pyngrok import ngrok
import torch

# A linha abaixo é um comentário que informa ao Chainlit para criar um túnel ngrok,
# expondo a porta 8080. Isso permite que você acesse a interface do chat de qualquer lugar.
print("ngrokhttp://localhost:8080")

# Importa as classes necessárias das bibliotecas transformers e langchain.
# 'AutoModelForCausalLM' e 'AutoTokenizer' são usadas para carregar o modelo Jamba e seu tokenizador.
# 'pipeline' simplifica a inferência do modelo.
# As classes 'langchain' são para construir a cadeia de conversação, memória e prompts.
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import chainlit as cl

# O decorador '@cl.on_chat_start' indica que esta função será executada
# automaticamente quando uma nova sessão de chat for iniciada.
@cl.on_chat_start
async def start():
    # Define o nome do modelo que será carregado do Hugging Face Hub.
    model_name_or_path = "lightblue/Jamba-v0.1-chat-multilingual"

    try:
        # Tenta carregar o tokenizador e o modelo do Jamba.
        # 'use_fast=True' usa uma versão mais rápida do tokenizador.
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            device_map="auto",  # 'device_map="auto"' move o modelo para a GPU ou CPU automaticamente.
            trust_remote_code=False,  # Define se o código remoto do modelo é confiável.
            revision="main"
        )
    except Exception as e:
        # Se ocorrer um erro (por exemplo, falta de GPU ou pacotes), envia uma mensagem de erro ao usuário.
        await cl.Message(content=f"Error loading model: {e}. Make sure you have installed the required packages: `pip install torch transformers` and have a compatible GPU/CPU setup.").send()
        return

    # Cria um 'pipeline' para simplificar a geração de texto.
    # Define parâmetros como o número máximo de novos tokens, temperatura e penalidades,
    # que controlam a criatividade e a repetição do modelo.
    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )

    # Converte o pipeline do Hugging Face em um objeto LangChain LLM.
    llm = HuggingFacePipeline(pipeline=pipe)

    # Adaptação do template para o formato de chat do Jamba.
    # Este template define a estrutura da conversa para o modelo,
    # incluindo instruções para o sistema e formatação para o histórico e a nova entrada do usuário.
    template = """<|im_start|>system
You are a helpful assistant that provides information and engages in casual conversation. Respond naturally to user queries and provide useful information.<|im_end|>
<|im_start|>user
{history}
Human: {input}
<|im_end|>
<|im_start|>assistant
Assistant:"""

    # Cria o objeto PromptTemplate com as variáveis de entrada.
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    
    # Adiciona memória à conversa. 'ConversationBufferWindowMemory' mantém
    # o histórico das últimas 'k' interações (aqui, k=3).
    memory = ConversationBufferWindowMemory(k=3, memory_key="history")

    # Cria a cadeia de conversação principal do LangChain.
    # Ela combina o prompt, o LLM e a memória para gerenciar a conversa.
    llm_chain = ConversationChain(
        prompt=prompt, 
        llm=llm, 
        memory=memory,
        verbose=True  # 'verbose=True' exibe os detalhes de execução no console, útil para depuração.
    )

    # Armazena a cadeia de conversação na sessão do usuário.
    # Isso permite que ela seja acessada em outras funções, como em '@cl.on_message'.
    cl.user_session.set("llm_chain", llm_chain)
    # Envia uma mensagem inicial para o usuário, indicando que o modelo foi carregado.
    await cl.Message(content="Model loaded. How can I help you today?").send()

# O decorador '@cl.on_message' indica que esta função será executada
# toda vez que o usuário enviar uma mensagem.
@cl.on_message
async def main(message: cl.Message):
    # Recupera a cadeia de conversação da sessão do usuário.
    llm_chain = cl.user_session.get("llm_chain")
    
    # Chama a cadeia de conversação de forma assíncrona com a mensagem do usuário.
    # 'callbacks' permite que o Chainlit mostre o progresso do processamento.
    res = await llm_chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])
    
    # Envia a resposta gerada pelo modelo de volta para a interface de chat.
    await cl.Message(content=res["response"]).send()