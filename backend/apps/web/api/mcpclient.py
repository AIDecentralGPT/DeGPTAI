import subprocess
import json
import os

mcp_key = os.getenv("MCP_API_KEY")
mcp_url = os.getenv("MCP_API_URL")

class McpClient:
  def __init__(self):
    self.api_key = mcp_key
    self.base_url = mcp_url
  
  def _call_tool(self, tool_name, params=None):
    cmd = [
      "npx",
      "-y",
      "misttrack@latest",
      "--key", self.api_key,
      "--base-url", self.base_url,
      tool_name
    ]
  
    try:
      # 将参数转为 JSON 并通过 stdin 传递
      input_str = json.dumps(params) if params else ""
      result = subprocess.run(
        cmd,
        input=input_str,
        capture_output=True,
        text=True,
        timeout=30
      )
    
      if result.returncode != 0:
        raise Exception(f"Tool execution failed: {result.stderr}")
      
      return json.loads(result.stdout)
   
    except json.JSONDecodeError:
      raise Exception("Invalid JSON response")
    except subprocess.TimeoutExpired:
      raise Exception("Request timed out")

  # 基础工具示例
  def get_address_overview(self, address):
    return self._call_tool(
      "mcp_misttrack_get_address_overview",
      {"address": address}
    )

  # 高级分析工具示例
  def analyze_transactions(self, coin, address, max_depth=1, **kwargs):
    params = {
      "coin": coin,
      "address": address,
      "max_depth": max_depth,
      **kwargs
    }
    return self._call_tool("analyze_transactions_recursive", params)
  
McpInstall = McpClient()