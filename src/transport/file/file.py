from typing import Annotated
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Response, Request
from models import User
from services.auth import auth_service
from services.make_info_for_html import FileDo
from config.config import tmp
from typing import Union

router = APIRouter(
    tags=['Load Files'],
    prefix="/file"
)


@router.post("/")
async def load_file(current_user: Annotated[User, Depends(auth_service.current_user)], file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Not an Excel file.")
    await FileDo.save_file(current_user.login, file)
    return Response(status_code=200)


@router.get("/")
async def get_files(request: Request, current_user: Annotated[User, Depends(auth_service.current_user)]):
    return tmp.TemplateResponse("users_file.html",
                                context={"request": request, "data": FileDo.get_files(login=current_user.login)})


@router.get("/{filename}")
async def get_sheets(filename: str, request: Request,
                     current_user: Annotated[User, Depends(auth_service.current_user)]):
    FileDo.true_file(filename, current_user.login)
    return tmp.TemplateResponse("sheets.html",
                                context={"request": request,
                                         "data": FileDo.get_sheets(login=current_user.login, file_name=filename),
                                         "filename": filename})


@router.get("/{filename}/{sheet}")
async def get_sheet_random_info(filename: str, sheet: str, request: Request,
                                current_user: Annotated[User, Depends(auth_service.current_user)]):
    try:
        FileDo.true_file(filename, current_user.login)
        return tmp.TemplateResponse("random.html",
                                    context={"request": request,
                                             "data": FileDo.get_sheet_random_info(login=current_user.login,
                                                                                  file_name=filename, sheet=sheet),
                                             "filename": filename,
                                             "sheet": sheet})
    except IndexError:
        return tmp.TemplateResponse("400.html",
                                    context={"request": request})


@router.delete("/{filename}/{sheet}/{id}")
async def delete_question(filename: str, sheet: str, id: Union[int, str], que: str,
                          request: Request, current_user: Annotated[User, Depends(auth_service.current_user)]):
    FileDo.true_file(filename, current_user.login)
    return FileDo.delete_question(login=current_user.login, file_name=filename, sheet=sheet, id=id, que=que)


@router.delete("/{filename}")
async def delete_file(filename: str, request: Request,
                      current_user: Annotated[User, Depends(auth_service.current_user)]):
    FileDo.true_file(filename, current_user.login)
    return FileDo.delete_file(login=current_user.login, file_name=filename)
