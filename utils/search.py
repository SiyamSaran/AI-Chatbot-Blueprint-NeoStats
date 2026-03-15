from config.config import TAVILY_API_KEY
try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

def perform_web_search(query: str, max_results: int = 3) -> str:
    """Perform a live web search using Tavily and return a summarized context string."""
    if not TAVILY_API_KEY:
        return "Web search is disabled because TAVILY_API_KEY is not set."
    
    if not TavilyClient:
        return "Web search is disabled because tavily-python is not installed."

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query, max_results=max_results, search_depth="basic")
        
        # Format the results into a context string
        results = response.get("results", [])
        if not results:
            return "No web results found."

        context_lines = []
        for i, res in enumerate(results):
            content = res.get("content", "")
            url = res.get("url", "")
            context_lines.append(f"[{i+1}] {content} (Source: {url})")

        return "\n".join(context_lines)

    except Exception as e:
        print(f"Web search error: {e}")
        return f"Web search failed: {e}"
