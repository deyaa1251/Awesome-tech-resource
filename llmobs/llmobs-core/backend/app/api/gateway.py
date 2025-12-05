from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from app.core.db import get_db
from app.models import Plugin, User
from app.api.auth import get_current_user

router = APIRouter()


@router.api_route(
    "/{plugin_slug}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway_proxy(
    plugin_slug: str,
    path: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Reverse proxy to plugin services.
    Routes requests to the appropriate plugin based on slug.
    """
    # Get plugin from database
    result = await db.execute(select(Plugin).filter(Plugin.slug == plugin_slug))
    plugin = result.scalar_one_or_none()
    if not plugin or not plugin.is_active:
        raise HTTPException(status_code=404, detail="Plugin not found or inactive")
    
    # Build target URL
    target_url = f"{plugin.url}/{path}"
    
    # Forward the request
    async with httpx.AsyncClient() as client:
        try:
            # Prepare headers
            headers = dict(request.headers)
            headers.pop("host", None)  # Remove host header
            
            # Forward request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query_params,
                content=await request.body(),
            )
            
            # Return response
            return StreamingResponse(
                response.iter_bytes(),
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Error connecting to plugin service: {str(e)}",
            )


@router.get("/plugins", dependencies=[Depends(get_current_user)])
async def list_plugins(db: AsyncSession = Depends(get_db)):
    """List all active plugins."""
    result = await db.execute(select(Plugin).filter(Plugin.is_active == True))
    plugins = result.scalars().all()
    return [
        {
            "id": plugin.id,
            "name": plugin.name,
            "slug": plugin.slug,
            "description": plugin.description,
            "url": plugin.url,
        }
        for plugin in plugins
    ]
