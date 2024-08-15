import os
from logger import Logger

from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableLambda


class Chatbot():
    def __init__(self, member='all'):
        self.logger = Logger(os.getenv('LOG_LEVEL'))
        self.member = member.lower()

        if self.member == 'all':
            pass
        elif self.member == 'pooh':
            pass
        elif self.member == 'tigger':
            pass
        elif self.member == 'piglet':
            pass
        elif self.member == 'eeyore':
            pass
        else:
            pass

        # =========================== #
        # initialise the objects here #
        # =========================== #
        self.retriever = retriever
        self.llm = llm
        self.prompt = prompt
        self.memory = ConversationBufferWindowMemory(
            k=3,
            ai_prefix=["Pooh", "Tigger", "Piglet", "Eeyore"]
        )

        self.logger.info("[Chatbot] Chatbot system is initialised")

    def __merge_docs(self, retrieved_docs):
        self.logger.info("[Chatbot] Merge documents")
        return "###\n\n".join([d.page_content for d in retrieved_docs])

    def __chain(self):
        self.logger.info("[Chatbot] Create chain")
        holmes_chain_memory = RunnableParallel({
            "context": self.retriever | self.__merge_docs,
            "query": RunnablePassthrough(),
            "history": RunnableLambda(self.memory.load_memory_variables) | itemgetter('history')
        }) | {
            "answer": self.prompt | self.llm | StrOutputParser(),
            "context": itemgetter("context"),
            "prompt": self.prompt
        }
        return holmes_chain_memory

    def __chat(self, query):
        self.logger.info("[Chatbot] Start chat")
        holmes_chain_memory = self.__chain()
        self.logger.info("[Chatbot] Successfully chained")
        result = holmes_chain_memory.invoke(query)
        self.logger.info("[Chatbot] Successfully invoked chat")
        self.memory.save_context({'query': query}, {"answer": result["answer"]})
        self.logger.info("[Chatbot] Saved the chat history")

        print(result["prompt"].messages[0].content.split("###")[-1] + result['answer'])

    def run(self):
        self.logger.info("[Chatbot] Chatbot system is running")

        user = input("Could you tell us your name please?\n")

        while True:
            query = input(f"[{user}] ")

            if query.lower() in ['exit', 'finish']:
                break

            self.__chat(query)
