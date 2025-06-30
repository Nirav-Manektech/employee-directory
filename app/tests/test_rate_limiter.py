import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from app.middleware.Ratelimiter import RateLimiterMiddleware


@pytest.fixture
def test_app():
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"message": "ok"}

    app.add_middleware(RateLimiterMiddleware)
    return app


@pytest.mark.asyncio
async def test_rate_limit_under_limit(test_app):
    transport = ASGITransport(app=test_app)  
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res1 = await ac.get("/test", headers={"X-Org-ID": "123"})
        assert res1.status_code == 200
        res2 = await ac.get("/test", headers={"X-Org-ID": "123"})
        assert res2.status_code == 200


@pytest.mark.asyncio
async def test_rate_limit_exceeded(test_app):
    transport = ASGITransport(app=test_app)  
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.get("/test", headers={"X-Org-ID": "abc"})
        await ac.get("/test", headers={"X-Org-ID": "abc"})
        res = await ac.get("/test", headers={"X-Org-ID": "abc"})
        print("Response====>",res.status_code)
        assert res.status_code == 429


@pytest.mark.asyncio
async def test_different_org_id_separate_limit(test_app):
    transport = ASGITransport(app=test_app)  
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.get("/test", headers={"X-Org-ID": "org1"})
        await ac.get("/test", headers={"X-Org-ID": "org1"})

        res = await ac.get("/test", headers={"X-Org-ID": "org2"})
        assert res.status_code == 200
