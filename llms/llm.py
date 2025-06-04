from typing import Union
from llms.llm_provider import LLMProvider, LLMProviderName
from llms.providers.ollama import OllamaChain
from llms.providers.bedrock import BedrockChain
from models.llm_settings import LLMSettings

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from models.chain_response_type import ChainResponseType

class LLM:
    model_names = [
        'ollama:llama3.2',
        'bedrock:claude-3-sonnet'
    ]

    def create_chain(self, settings:LLMSettings) -> LLMProvider:
        provider = self._get_provider_by_model_name(settings.model_name)
        if provider is None:
            raise ValueError(f'Unknown model name : {settings.model_name}')

        if provider == LLMProviderName.OLLAMA:
            chain = OllamaChain()
        elif provider == LLMProviderName.BEDROCK:
            chain = BedrockChain()

        chain.create(settings)

        if len(chain.settings.tools) > 0:
            chain.model = chain.model.bind_tools(chain.settings.tools)
        
        if chain.settings.structured is not None:
            chain.llm = chain.model.with_structured_output(schema=chain.settings.structured, method='json_schema')
            print(f'set with_structured_output: {chain.settings.structured}')
        else:
            chain.llm = chain.settings.prompt | chain.model
            print('not set with_structured_output')

        if chain.settings.chain_response_type == ChainResponseType.STRING:
            chain.llm = chain.llm | StrOutputParser()
        elif chain.settings.chain_response_type == ChainResponseType.JSON:
            chain.llm = chain.llm | JsonOutputParser()
        else:
            # Default based on 
            # https://python.langchain.com/api_reference/core/messages.html
            pass
    
        return chain

    def _get_provider_by_model_name(self, target_model_name) -> Union[LLMProviderName, None]:
        is_exists = False
        provider = None
        target_model_name = target_model_name.split(':')[0]
        for model in self.model_names:
            [model_provider, model_name] = model.split(':')
            is_exists = model_name in target_model_name \
               or target_model_name in model_name \
               or target_model_name == model_name
            
            if is_exists:
                provider = model_provider
                break
        return provider