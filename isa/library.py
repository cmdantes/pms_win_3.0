from datetime import datetime


class Library:
    def timeanddateconversion(data):
        return datetime.strptime(data, '%m/%d/%Y').strftime('%Y-%m-%d')