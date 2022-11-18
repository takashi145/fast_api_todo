from fastapi import APIRouter
from fastapi import Response, Request, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from schemas import TodoRequest, TodoResponse
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import List
from fastapi_csrf_protect import CsrfProtect
from auth_utils import AuthJwtCsrf

router = APIRouter(
  prefix="/api/todo",
  tags=["todos"]
)

auth = AuthJwtCsrf()

@router.get('/', response_model=List[TodoResponse])
async def get_todos(request: Request):
  # auth.verify_jwt(request)
  res = await db_get_todos()
  return res

@router.post("/", response_model=TodoResponse, status_code=HTTP_201_CREATED)
async def create_todo(request: Request, response: Response, data: TodoRequest, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  res =  await db_create_todo(todo)
  response.set_cookie(
    key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True
  )
  if res:
    return res
  raise HTTPException(status_code=404, detail="create task failed")

@router.get("/{id}", response_model=TodoResponse)
async def get_single_todo(id: str, request: Request, response: Response):
  new_token, _ = auth.verify_update_jwt(request)
  res = await db_get_single_todo(id)
  response.set_cookie(
    key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"task is not found(id={id})"
  )

@router.put("/{id}", response_model=TodoResponse)
async def update_todo(request: Request, response: Response, id: str, data: TodoRequest, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  res = await db_update_todo(id, todo)
  response.set_cookie(
    key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"task is not found(id={id})"
  )

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_todo(request: Request, response: Response, id: str, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  res = await db_delete_todo(id)
  response.set_cookie(
    key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"task is not found(id={id})"
  )
