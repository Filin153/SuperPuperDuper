import logging
import random
import os
from typing import Union

import pandas as pd
from pandas.io.excel import ExcelWriter
from fastapi import HTTPException, File
import shutil


class FileInfo:

    @staticmethod
    def get_files(login: str):
        try:
            os.mkdir(f"file/{login}/")
        except FileExistsError:
            pass

        return os.listdir(f"file/{login}/")

    @staticmethod
    def get_sheets(login: str, file_name: str):
        return pd.ExcelFile(f"file/{login}/{file_name}").sheet_names

    @staticmethod
    def get_sheet_random_info(login: str, file_name: str, sheet: str):
        res = {}
        df = pd.read_excel(f"file/{login}/{file_name}", sheet_name=sheet, engine="openpyxl")
        res["count"] = len(df)
        val = random.choice(df.values.tolist())
        res['data'] = {
            "Номер вопроса": val[0],
            "ФИО": val[1],
            "Место работы/учёбы": val[2],
            "Должность/курс": val[3],
            "Вопрос": val[4],
        }
        return res


class FileAction:
    @staticmethod
    def delete_question(login: str, file_name: str, sheet: str, id: Union[int, str], que: str) -> bool:
        """
        Удаляет значение строку по ID из эксель sheet
        :param login:
        :param file_name:
        :param sheet:
        :param id:
        :return: bool
        """
        try:
            id = int(id)
        except Exception:
            pass

        path = f"file/{login}/{file_name}"
        path_tmp = f"file/{login}/tmp_{file_name}"
        shutil.copy(path, path_tmp)

        df = pd.read_excel(path_tmp, sheet_name=sheet, engine="openpyxl")

        logging.debug(id)
        logging.debug(que)
        if id != "NaN" and not (id is None):
            df = df[df['№ п/п'] != id]
        else:
            df = df[df['Вопрос'] != que]
        df.dropna(subset=["ФИО", "Место работы/учёбы"], inplace=True)

        with ExcelWriter(path) as writer:
            rex = pd.ExcelFile(path_tmp)

            sheets = rex.sheet_names
            sheets.remove(sheet)
            logging.debug(sheets)
            for old_sheet in sheets:
                pd.read_excel(path_tmp, sheet_name=old_sheet, engine="openpyxl").to_excel(writer, sheet_name=old_sheet, index=False, engine="openpyxl")

            df.to_excel(writer, sheet_name=sheet, index=False, engine="openpyxl")
        df = None

        try:
            os.remove(path_tmp)
        except Exception as e:
            logging.error(e)
        return True

    @staticmethod
    def delete_file(login: str, file_name: str) -> bool:
        os.remove(f"file/{login}/{file_name}")
        return True

    @staticmethod
    async def save_file(login: str, file: File):
        with open(f"file/{login}/{file.filename}", "wb") as f:
            file_data = await file.read()
            f.write(file_data)
        return True


class FileDo(FileInfo, FileAction):
    @staticmethod
    def true_file(file_name: str, login: str):
        logging.debug(file_name)
        logging.debug(login)
        logging.debug(os.listdir(f"file/{login}"))
        if file_name not in os.listdir(f"file/{login}"):
            raise HTTPException(status_code=404, detail="Not found")
