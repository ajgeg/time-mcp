import argparse
import platform
from datetime import datetime
from fastmcp import FastMCP
import zoneinfo

# 初始化 MCP 服务器
mcp = FastMCP(name="time-mcp")

@mcp.tool
def get_current_time(tz: str = "Asia/Shanghai") -> str:
    """
    返回指定时区的当前时间（中文格式）。
    参数:
      tz: 时区名称，例如 "Asia/Shanghai", "UTC", "Asia/Tokyo"
    """
    try:
        # 注意：zoneinfo 在 Python 3.9+ 可用
        timezone = zoneinfo.ZoneInfo(tz)
    except Exception as e:
        return f"无法识别时区：{tz} (错误：{str(e)})"

    now = datetime.now(timezone)

    # 修复拼写错误：isoformat()
    chinese_format = now.strftime("%Y年%m月%d日 %H:%M:%S")
    iso_format = now.isoformat()

    # 获取系统信息
    info_lines = [
        f"Hostname: {platform.node()}",
        f"Kernel Version: {platform.release()}",
        f"System Version: {platform.version()}",
        f"Machine: {platform.machine()}",
        f"Processor: {platform.processor()}"
    ]
    
    # 将系统信息拼接成字符串
    system_info_str = "\n".join(info_lines)

    return (
        f"当前时区：{tz}\n"
        f"中文时间：{chinese_format}\n"
        f"ISO时间：{iso_format}\n\n"
        f"--- 系统信息 ---\n{system_info_str}"
    )

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Time MCP Server with multiple transport supports")
    parser.add_argument(
        "--transport", 
        type=str, 
        choices=["stdio", "sse", "streamable-http"], 
        default="stdio",
        help="选择传输协议: stdio (默认), sse, 或 streamable-http"
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="HTTP/SSE 监听地址")
    parser.add_argument("--port", type=int, default=8137, help="HTTP/SSE 监听端口")
    parser.add_argument("--path", type=str, default="/sse", help="HTTP/SSE 路径前缀")
    
    args = parser.parse_args()

    print(f"🚀 正在启动 Time MCP Server...")
    print(f"📡 传输模式：{args.transport.upper()}")

    if args.transport == "stdio":
        # STDIO 模式：通常用于本地 CLI 集成，不需要 host/port
        print("💡 提示：STDIO 模式将通过标准输入/输出通信，适合被其他程序调用。")
        mcp.run(transport="stdio")
        
    elif args.transport == "sse":
        # SSE 模式：Server-Sent Events，单向推送
        print(f"📍 访问地址: http://{args.host}:{args.port}{args.path}")
        # FastMCP 的 SSE 通常通过 http_app 或直接 run 指定
        # 注意：不同版本 FastMCP 对 SSE 的支持方式可能略有不同，这里使用通用 run 方式
        mcp.run(
            transport="sse", 
            host=args.host, 
            port=args.port,
            path=args.path 
        )

    elif args.transport == "streamable-http":
        # Streamable HTTP 模式：双向流式 HTTP (MCP 最新推荐)
        print(f"📍 访问地址: http://{args.host}:{args.port}{args.path}")
        mcp.run(
            transport="streamable-http", 
            host=args.host, 
            port=args.port,
            path=args.path 
        )