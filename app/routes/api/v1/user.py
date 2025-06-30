
from fastapi import APIRouter,Request,Depends,Query,HTTPException,Header
from app.schemas import filter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy import select,func
from app.models.configuration import Configuration
from app.models.user import User
from app.models.user_org import UserOrg
from sqlalchemy.orm import selectinload
from app.models.department import Department
from app.schemas.filter import SearchResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search_users(
    request: Request,
    username: str = Query(None),
    email: str = Query(None),
    phone: str = Query(None),
    position: str = Query(None),
    department: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    x_org_id: str = Header(..., alias="X-Org-ID"),
    db: AsyncSession = Depends(get_db)
):
    org_id = request.headers.get("X-Org-ID")
    if not org_id:
        raise HTTPException(status_code=400, detail="Missing X-Org-ID header")

    # Get organization config
    result = await db.execute(select(Configuration).filter(Configuration.org_id == int(org_id)))
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Organization config not found")

    # Build base query
    base_stmt = (
        select(User)
        .join(UserOrg, User.id == UserOrg.user_id)
        .filter(UserOrg.org_id == int(org_id))
        .options(selectinload(User.department))
    )

    # Apply filters
    if username:
        base_stmt = base_stmt.filter(User.username.ilike(f"%{username}%"))
    if email:
        base_stmt = base_stmt.filter(User.email.ilike(f"%{email}%"))
    if phone:
        base_stmt = base_stmt.filter(User.phone.ilike(f"%{phone}%"))
    if position:
        base_stmt = base_stmt.filter(User.position.ilike(f"%{position}%"))
    if department:
        base_stmt = base_stmt.join(Department).filter(Department.name.ilike(f"%{department}%"))

    # Get total count
    count_stmt = base_stmt.with_only_columns(func.count()).order_by(None)
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()

    # Apply pagination
    paginated_stmt = base_stmt.offset(offset).limit(limit)
    result = await db.execute(paginated_stmt)
    users = result.scalars().all()

    # Prepare output
    allowed_fields = set(config.user_search_columns)
    response_data = []

    for user in users:
        user_data = {}
        if "username" in allowed_fields:
            user_data["username"] = user.username
        if "email" in allowed_fields:
            user_data["email"] = user.email
        if "phone" in allowed_fields:
            user_data["phone"] = user.phone
        if "position" in allowed_fields:
            user_data["position"] = user.position
        if "department" in allowed_fields and user.department:
            user_data["department"] = user.department.name
        response_data.append(user_data)

    return {
        "data": response_data,
        "meta": {
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }