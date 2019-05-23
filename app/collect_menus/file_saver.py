import pdfkit
import os

from os.path import join as path_join, exists
from os import makedirs
from typing import Union

from config import MENUS_DIR


class FileSaver(object):
    """
    Class for the saving menus
    """

    # Save pdf options
    options = {"quiet": ""}

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

    def save_content(self, content: Union[bytes, bytearray], file_name: str):
        """
        Saves file from url
        :param content: html content to write into the file
        :param file_name: name of the file
        """
        with open(path_join(self.root, file_name), "wb") as file:
            file.write(content)

    def save_pdf(self, url: str, file_name: str):
        """
        Save pdf of the url
        :param url: url to save in pdf format
        :param file_name: name of the file to save into
        """
        # TODO replace
        file_name = file_name.replace(".html", "")
        file_name = f'{path_join(self.root, file_name)}.pdf'
        if exists(file_name):
            os.remove(file_name)
        pdfkit.from_url(url, file_name, options=self.options)
