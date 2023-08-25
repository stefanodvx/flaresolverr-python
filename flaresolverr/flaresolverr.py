import httpx

class FlareSolverr:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

        self.http = httpx.AsyncClient()

    @staticmethod
    def parse_cookies(cookies: list) -> dict:
        return {
            cookie["name"]: cookie["value"]
            for cookie in cookies
        }
    
    async def resolve(self, query: dict) -> dict | None:
        r = await self.http.post(
            f"http://{self.hostname}:{self.port}/v1",
            headers={"Content-Type": "application/json"},
            json=query
        )
        response = r.json()
        if response["status"] != "ok":
            raise Exception("FlareSolverr not OK")
        return response["solution"]

    async def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        data: dict = None,
        cookies: dict = None,
        flare_data: dict = None,
        timeout: int = 10
    ) -> httpx.Response | None:
        solution = await self.resolve(flare_data or {"cmd": "request.get", "url": url})
        headers = (headers or {}) | solution["headers"] | {"User-Agent": solution["userAgent"]}
        cookies = (cookies or {}) | FlareSolverr.parse_cookies(solution["cookies"])
        return await self.http.request(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            data=data,
            timeout=timeout
        )
