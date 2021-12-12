import pymongo
import openpyxl
import os
import pandas
from pandas import DataFrame
from pathlib import Path


def make_database_name(excel_file_path: str) -> str:
    return Path(excel_file_path).stem


def import_excel_to_db(mongo_client: pymongo.mongo_client, excel_file_path: str):
    # get a list of sheets
    wb = openpyxl.load_workbook(filename=excel_file_path)
    sheets = wb.sheetnames

    # use the filename as the database name
    database_name = make_database_name(excel_file_path)
    print(f"database name: {database_name}")

    # Read from the Excel file
    xlfile: pandas.ExcelFile = pandas.ExcelFile(excel_file_path)

    db = mongo_client[database_name]

    for sheet in sheets:
        print(f"importing {sheet}")
        imported_data_frame: DataFrame = pandas.read_excel(xlfile, sheet_name=sheet)
        current_collection = db[sheet]

        for row in imported_data_frame.iterrows():
            row_dict = row[1].to_dict()
            # row_dict.pop("Unnamed: 0")
            current_collection.insert_one(row_dict)



