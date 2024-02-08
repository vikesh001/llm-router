from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory



def evaluator(prompt):
    chat = ChatLiteLLM(model="palm/chat-bison", verbose=True)
    content = f"""
    You are my prompt complexity evaluator, assigning a rating from 1 to 10 based on the given prompt. The evaluator should categorize prompts with a rating less than 5 as simple and answerable by a kid, while those with a rating of 5 or more should be considered very complex. The system's primary function is to analyze the prompt's inherent complexity and provide a numerical rating without generating an actual response to the prompt.

    Give just a number; no need for an explanation. Provide only a rating to the prompt.
    just a numbe no need of explanation and a rating of 10 or more should be considered very complex. The system's primary function is to analyze the prompt's inherent complexity and provide a numerical rating without generating an actual response to the prompt.

    if the qustion is answerable by a 15 year old with basic knowledge, rate it under 5
    else if the question is more complex and topic specific rate it above 5 to 10
    if there is maths problem need more accuracy so rate above 5
    if the qustion trick no need to think of rating always give above 5
    if the qustion is riddle rate it 6
    just give me replay in integer 1 to 10
    -----------------------------------------------Prompt: {prompt}-----------------------------------------
    
    
    if there is maths problem need more accuracy so rate above 5
    """    
    messages = [
    HumanMessage(
        content=content 
        
    )
    ]
    output =chat(messages)
    numeric_part = ''.join(filter(str.isdigit, output.content))
    return numeric_part




def chater(mod,input):
    if int(mod) < 5:
        llm ="ollama/qwen:0.5b"
    elif int(mod) <= 10 and int(mod) >= 5:
        llm = "gemini/gemini-pro"
    else:
        llm="ollama/phi"
        
    chat = ChatLiteLLM(model=llm)       
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    chain = prompt | chat

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection_string="sqlite:///sqlite.db"
        ),
        input_messages_key="question",
        history_messages_key="history",
        
    )
    print(chain_with_history.invoke({"question": input}, config=config))
    print("-----------")
    print(llm)
i = 0
# This is where we configure the session id
while i==0:
    config = {"configurable": {"session_id": "123467899"}}
    prompt = input("Enter your value: ")    
    mod=evaluator(prompt) 
    print (mod)
    chater(mod, prompt)
    
