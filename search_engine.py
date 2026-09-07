"""
Integrated Search Engine with GPT and DeepSeek
Combines multiple AI models for enhanced search capabilities
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
import httpx
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """Available AI providers"""
    GPT = "gpt"
    DEEPSEEK = "deepseek"
    HYBRID = "hybrid"


class AISearchEngine:
    """
    Unified search engine combining GPT and DeepSeek models
    """

    def __init__(
        self,
        gpt_api_key: Optional[str] = None,
        deepseek_api_key: Optional[str] = None,
        gpt_model: str = "gpt-3.5-turbo",
        deepseek_model: str = "deepseek-chat",
    ):
        """
        Initialize the search engine with API keys
        
        Args:
            gpt_api_key: OpenAI API key (env: OPENAI_API_KEY)
            deepseek_api_key: DeepSeek API key (env: DEEPSEEK_API_KEY)
            gpt_model: GPT model name
            deepseek_model: DeepSeek model name
        """
        self.gpt_api_key = gpt_api_key or os.getenv("OPENAI_API_KEY")
        self.deepseek_api_key = deepseek_api_key or os.getenv("DEEPSEEK_API_KEY")
        self.gpt_model = gpt_model
        self.deepseek_model = deepseek_model

        self.gpt_endpoint = "https://api.openai.com/v1/chat/completions"
        self.deepseek_endpoint = "https://api.deepseek.com/chat/completions"

        logger.info("AISearchEngine initialized")

    async def search_gpt(
        self,
        query: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Search using GPT model
        
        Args:
            query: Search query
            context: Optional context/content to search within
            temperature: Model temperature (0-1)
            
        Returns:
            Search results from GPT
        """
        if not self.gpt_api_key:
            logger.error("GPT API key not configured")
            return {"error": "GPT API key not configured"}

        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful search and information retrieval assistant.",
                }
            ]

            if context:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Context:\n{context}",
                    }
                )

            messages.append({"role": "user", "content": query})

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.gpt_endpoint,
                    headers={
                        "Authorization": f"Bearer {self.gpt_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.gpt_model,
                        "messages": messages,
                        "temperature": temperature,
                    },
                    timeout=30.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "provider": "gpt",
                        "model": self.gpt_model,
                        "result": data["choices"][0]["message"]["content"],
                        "usage": data.get("usage"),
                        "status": "success",
                    }
                else:
                    logger.error(f"GPT API error: {response.status_code}")
                    return {
                        "error": f"GPT API returned status {response.status_code}",
                        "status": "failed",
                    }

        except Exception as e:
            logger.error(f"GPT search error: {str(e)}")
            return {"error": str(e), "status": "failed"}

    async def search_deepseek(
        self,
        query: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Search using DeepSeek model
        
        Args:
            query: Search query
            context: Optional context/content to search within
            temperature: Model temperature (0-1)
            
        Returns:
            Search results from DeepSeek
        """
        if not self.deepseek_api_key:
            logger.error("DeepSeek API key not configured")
            return {"error": "DeepSeek API key not configured"}

        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful search and information retrieval assistant.",
                }
            ]

            if context:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Context:\n{context}",
                    }
                )

            messages.append({"role": "user", "content": query})

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.deepseek_endpoint,
                    headers={
                        "Authorization": f"Bearer {self.deepseek_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.deepseek_model,
                        "messages": messages,
                        "temperature": temperature,
                    },
                    timeout=30.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "provider": "deepseek",
                        "model": self.deepseek_model,
                        "result": data["choices"][0]["message"]["content"],
                        "usage": data.get("usage"),
                        "status": "success",
                    }
                else:
                    logger.error(f"DeepSeek API error: {response.status_code}")
                    return {
                        "error": f"DeepSeek API returned status {response.status_code}",
                        "status": "failed",
                    }

        except Exception as e:
            logger.error(f"DeepSeek search error: {str(e)}")
            return {"error": str(e), "status": "failed"}

    async def search_hybrid(
        self,
        query: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Search using both GPT and DeepSeek models simultaneously
        
        Args:
            query: Search query
            context: Optional context/content to search within
            temperature: Model temperature (0-1)
            
        Returns:
            Combined search results from both providers
        """
        gpt_task = self.search_gpt(query, context, temperature)
        deepseek_task = self.search_deepseek(query, context, temperature)

        gpt_result, deepseek_result = await asyncio.gather(gpt_task, deepseek_task)

        return {
            "provider": "hybrid",
            "query": query,
            "results": {
                "gpt": gpt_result,
                "deepseek": deepseek_result,
            },
            "status": "success",
        }

    async def search(
        self,
        query: str,
        provider: AIProvider = AIProvider.HYBRID,
        context: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Unified search interface
        
        Args:
            query: Search query
            provider: Which provider to use (GPT, DeepSeek, or Hybrid)
            context: Optional context/content to search within
            temperature: Model temperature (0-1)
            
        Returns:
            Search results
        """
        if provider == AIProvider.GPT:
            return await self.search_gpt(query, context, temperature)
        elif provider == AIProvider.DEEPSEEK:
            return await self.search_deepseek(query, context, temperature)
        elif provider == AIProvider.HYBRID:
            return await self.search_hybrid(query, context, temperature)
        else:
            return {"error": f"Unknown provider: {provider}"}


# Synchronous wrapper for Flask
def search_sync(
    query: str,
    provider: str = "hybrid",
    context: Optional[str] = None,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """
    Synchronous wrapper for search engine (for Flask)
    
    Args:
        query: Search query
        provider: Provider to use ('gpt', 'deepseek', or 'hybrid')
        context: Optional context/content
        temperature: Model temperature (0-1)
        
    Returns:
        Search results
    """
    engine = AISearchEngine()
    provider_enum = AIProvider[provider.upper()]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            engine.search(query, provider_enum, context, temperature)
        )
        return result
    finally:
        loop.close()
