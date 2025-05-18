from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from workflows.chatbot.handler import start_chatbot
# from workflows.prompt_chain.handler import start_promp_chain
# from workflows.parallelization.handler import start_parallelization
# from workflows.routing.handler import start_routing
# from workflows.orchestrator_worker.handler import start_orchestrator
# from workflows.evaluator_optimizer.handler import start_evaluator_optimizer
# from workflows.agent.handler import start_agent
# from workflows.rag.agentic_ai.handler import AgenticAI
# from workflows.sql.postgres.handler import OllamaPostgreSQLAgent
# from workflows.mcp_integration.handler import start_mcp_integration

from routers import chat, system

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This function is called when the application starts
    print("Starting up...")
    yield
    # This function is called when the application shuts down
    print("Shutting down...")

def create_app() -> FastAPI:
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

    # await start_mcp_integration()
    
    app = FastAPI(lifespan=lifespan)
    app.include_router(chat.router)
    app.include_router(system.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", lambda: print("Application started"))
    app.add_event_handler("shutdown", lambda: print("Application stopped"))

    return app

if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
