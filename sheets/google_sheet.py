from __future__ import print_function
import socket
from google.oauth2.credentials import Credentials

# from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# from google.auth.transport.requests import Request


class GoogleSheet:
    """Access Google Sheet using the Python Google Sheet API"""

    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    SERVICE_ACCOUNT_FILE = settings.BASE_DIR / "keys.json"

    creds = None
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    def __init__(self, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
        socket.setdefaulttimeout(50)
        self.SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_ID
        self.SAMPLE_RANGE_NAME = SAMPLE_RANGE_NAME
        self.sheet = self.service.spreadsheets()

    def read_sheet(self, last=False, integer=False):
        """
        Reads data from a google sheet

        Last = True: Will get the last value in the sheet, default is False.

        Integer = True: Will return the integer of the last value in the sheet, default is False.

        """
        try:
            result = (
                self.sheet.values()
                .get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.SAMPLE_RANGE_NAME)
                .execute()
            )
            values = result.get("values", [])
            if last:
                try:
                    values = values[-1]
                    value = str(values).replace("[", "").replace("]", " ").replace("'", " ")
                    if integer:
                        values = int(value)
                    else:
                        values = str(value)
                except Exception:
                    values = "0"

            return values
        except HttpError:
            return 0

    def clear_sheet(self):
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.SAMPLE_RANGE_NAME
            ).execute()
        except Exception:
            pass

    def append_sheet_column(self, data):
        try:
            values = GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).read_sheet()
            v = values
            if data == 0:
                data = "O/S"
            if data == 0.1:
                data = "I/S"
            v.append([f"{data}"])

            request = self.sheet.values().update(
                spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                range=self.SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body=dict(values=values),
            )
            request.execute()
        except Exception:
            pass

    def append_sheet_row(self, data):
        try:
            v_list = []
            values = GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).read_sheet()
            v = values
            for i in v:
                for j in i:
                    v_list.append(j)
                if data == 0:
                    data = "O/S"
                if data == 0.1:
                    data = "I/S"
                v_list.append(f"{data}")
                values = [v_list]
                GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).clear_sheet()
                self.sheet.values().append(
                    spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                    range=self.SAMPLE_RANGE_NAME,
                    valueInputOption="USER_ENTERED",
                    insertDataOption="OVERWRITE",
                    body=dict(values=values),
                ).execute()
        except Exception:
            pass

    def remove_last_sheet_column(self, n=0):
        try:
            data = 1
            if n >= data:
                data = n
            values = GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).read_sheet()
            GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).clear_sheet()
            v = values

            if data > 1:
                for _ in range(data + 1):
                    v.pop()
            else:
                v.pop()
            request = self.sheet.values().append(
                spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                range=self.SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body=dict(values=values),
            )
            request.execute()
        except Exception:
            pass

    def remove_last_sheet_row(self, n):
        try:
            data = 1
            if n >= data:
                data = n
            sec_list = []
            values = GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).read_sheet()
            v = values
            for i in v:
                for j in i:
                    sec_list.append(j)
            for _ in range(data):
                sec_list.pop()
            values = [sec_list]
            GoogleSheet(self.SAMPLE_SPREADSHEET_ID, self.SAMPLE_RANGE_NAME).clear_sheet()
            request = self.sheet.values().update(
                spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                range=self.SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED",
                # insertDataOption="OVERWRITE",
                body=dict(values=values),
            )
            request.execute()
        except Exception:
            pass
