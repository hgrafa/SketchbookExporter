import httpx
import asyncio
from rich import print


async def get_student(id: int | str = ''):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://localhost:3333/students/{id}')
        print(response.text)

asyncio.run(getStudentInfo(2))
