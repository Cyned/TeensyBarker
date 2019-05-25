import pdfkit
import requests
import os

from os.path import join as path_join, exists
from os import makedirs
from typing import Union

from config import MENUS_DIR
from app import parser_logger as logger


class FileSaver(object):
    """
    Class for the saving menus
    """

    # Save pdf options
    options = {'quiet': ''}

    def __init__(self, dirname: str):
        """
        :param dirname: name of the dir to push new files
        """
        self._root = path_join(MENUS_DIR, dirname)
        # If folder not exists - create
        if not exists(self.root):
            makedirs(self.root)

    @property
    def root(self) -> str:
        """ Get url """
        return self._root

    def save_url(self, path: str, file_name: str):
        """
        Saves file from url
        :param path: path to the object to save
        :param file_name: name of the file
        """
        if not path.startswith('http'):
            path = 'http://' + path
        try:
            response = requests.get(url=path)
        except Exception as e:
            raise e
        with open(path_join(self.root, file_name), "wb") as file:
            file.write(response.content)

    def save_pdf(self, url: str, file_name: str):
        """
        Saves pdf of the url
        :param url: url to save in pdf format
        :param file_name: name of the file to save into
        """
        if not url.startswith('http'):
            url = 'http://' + url
        # TODO replace
        file_name = file_name.replace(".html", "")
        file_name = f'{path_join(self.root, file_name)}.pdf'
        if exists(file_name):
            os.remove(file_name)
        try:
            pdfkit.from_url(url, file_name, options=self.options)
        except OSError as e:
            logger.error(f'Pdf not saved: {url}.\n{e}')
            os.remove(file_name)
