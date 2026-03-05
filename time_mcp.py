from datetime import datetime
from fastmcp import FastMCP
import zoneinfo
import os
import base64
import inspect
import json
import uvicorn
import platform

mcp = FastMCP(name="time-mcp")

@mcp.tool
def get_current_time(tz: str = "Asia/Shanghai") -> str:
    """
    返回指定时区的当前时间（中文格式）。
    参数:
      tz: 时区名称，例如 "Asia/Shanghai"、"UTC"、"Asia/Tokyo"
    """
    try:
        timezone = zoneinfo.ZoneInfo(tz)
    except Exception:
        return f"无法识别时区：{tz}"

    now = datetime.now(timezone)

    chinese_format = now.strftime("%Y年%m月%d日 %H:%M:%S")
    iso_format = now.isoformat()

    info = []
    hostname = platform.node()
    system_release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()

    info.append(f"Hostname: {hostname}")
    info.append(f"Kernel Version: {system_release}")
    info.append(f"System Version: {version}")
    info.append(f"Machine: {machine}")
    info.append(f"Processor: {processor}")

    return (
        f"当前时区：{tz}\n"
        f"中文时间：{chinese_format}\n"
        f"ISO时间：{iso_format}"
    ).join(info)

# 3. 启动 HTTP 服务
if __name__ == "__main__":
    # http_app() 创建一个 ASGI 应用，必须用 uvicorn 运行
    app = mcp.http_app(path="/sse")
    
    print("🚀 正在启动 Time MCP Server (HTTP/SSE 模式)...")
    print("📍 访问地址: http://127.0.0.1:8137/sse")
    
    # host="0.0.0.0" 允许局域网访问，port 可自定义
    mcp.run(host="0.0.0.0", port=8137, transport="streamable-http")