from scrapegraphai.graphs import SmartScraperGraph
import asyncio
import concurrent.futures

# Set up the configuration for the SmartScraperGraph
graph_config = {
    "llm": {
        "model": "ollama/llama3.3",
        "base_url": "https://korea-chat.degpt.ai/api/v0/chat/completion/proxy",
        "model_provider": "self_hosted",
        "request_adapter": lambda data: {
            "messages": [{
                "role": "user",
                "content": data["prompt"]
            }],
            "model": "Llama3.3-70B",
            "project": "DecentralGPT",
            "stream": False
        },  
        "response_parser": lambda response: response.json()["choices"][0]["message"]["content"],
        "timeout": 60,
        "retry": {
            "attempts": 3,
            "delay": 2
        }
    },
    "verbose": True,
}

class WebApi:
    async def getWebGraph(self, website: str, prompt: str):
        try:
            # Create a SmartScraperGraph object
            smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=website,
                config=graph_config
            )

            # Assume there is a method to process data only
            loop = asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                # 在执行器中运行同步方法
                processed_data = await loop.run_in_executor(pool, smart_scraper_graph.run)

            return processed_data
        except Exception as e:
            print("=========================", e)
            return None
  
WebApiInstance = WebApi()