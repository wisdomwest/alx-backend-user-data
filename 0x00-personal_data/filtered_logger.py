#!/usr/bin/env python3
'''filtered_logger module'''

import logging
from typing import List
import re
from os import environ
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    for field in fields:
        message = re.sub(rf'{field}=(.+?){separator}',
                         f'{field}={redaction}{separator}', message)

    return message


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns a connector to the database'''
    connect = mysql.connector.connect(
        host=environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=environ.get('PERSONAL_DATA_DB_NAME'),
        user=environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    )

    return connect


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Redacting Formatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Redacting Formatter class"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def main() -> None:
    '''main function'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    logger = get_logger()

    for row in cursor:
        data = ''
        for i in range(len(row)):
            data += f"{cursor.column_names[i]}={row[i]}; "
        logger.info(data)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
