from pyodide.http import pyfetch, FetchResponse
from typing import Optional, Any
import asyncio
import js

def handler(loop, context):
    js.console.error(context.message)
    js.console.error(context.exception)

    raise(context.exception)

pyscript.loop.set_exception_handler(handler)

async def request(url: str,
                  method: str = "GET",
                  body: Optional[str] = None,
                  headers: Optional[dict[str, str]] = None,
                  **fetch_kwargs: Any) -> FetchResponse:
    kwargs = {
        "method": method,
        "mode": "no-cors"
    }  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers
    kwargs.update(fetch_kwargs)

    response = await pyfetch(url, **kwargs)
    return response

async def get_barycenter(
        filename: str,
        base_url: str = "http://localhost:8001") -> dict[str, Any] | None:
    headers = {"Content-type": "application/json"}
    print("barycenter")
    response = await request(f"{base_url}/barycenter/?image_name={filename}",
                             headers=headers)
    
    body = await response.json()
    if body.status != 200:
        return None
    return body.msg

async def main():
    print('start')
    test = await get_barycenter("img.jpg")
    print(test)
    print("end")


asyncio.ensure_future(main())
