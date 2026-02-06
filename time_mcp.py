from datetime import datetime
from fastmcp import FastMCP, tool
import zoneinfo

mcp = FastMCP(
    name="time-mcp",
    description="Return current time with timezone and Chinese formatting",
)

@tool
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

    return (
        f"当前时区：{tz}\n"
        f"中文时间：{chinese_format}\n"
        f"ISO时间：{iso_format}"
    )

app = mcp.http_app()
