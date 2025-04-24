import asyncio
# from workflows.chatbot.handler import start_chatbot
# from workflows.prompt_chain.handler import start_promp_chain
# from workflows.parallelization.handler import start_parallelization
# from workflows.routing.handler import start_routing
# from workflows.orchestrator_worker.handler import start_orchestrator
# from workflows.evaluator_optimizer.handler import start_evaluator_optimizer
# from workflows.agent.handler import start_agent
# from workflows.rag.agentic_ai.handler import AgenticAI
# from workflows.sql.postgres.handler import OllamaPostgreSQLAgent
from workflows.mcp_integration.handler import start_mcp_integration

async def main():
    # start_chatbot()
    # start_promp_chain()
    # start_parallelization()
    # start_routing()
    # start_orchestrator()
    # start_evaluator_optimizer()
    # start_agent()

    # agentic_ai = AgenticAI()
    # agentic_ai.validate_prompt()
    # agentic_ai.start()

    # opa = OllamaPostgreSQLAgent()
    # opa.playground()

    await start_mcp_integration()

if __name__ == "__main__":
    asyncio.run(main())
