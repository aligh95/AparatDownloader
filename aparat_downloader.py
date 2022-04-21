import os, uuid, requests
from typing import Optional
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument('--disable-logging')

qualities = {
    '144': 0,
    '240': 1,
    '360': 2,
    '480': 3,
    '720': 4,
    '1080': 5
}


class AparatVideoError(Exception):
    pass

class AparatDownloader:

    def __init__(self, url, download_path: Optional[str] = None,
                 selenium_path: Optional[str] = None, hide_window: Optional[bool] = False) -> None:
        self._download_path = download_path
        execute_path = "./selenium/chromedriver.exe"
        if selenium_path and os.path.isfile(selenium_path):
            execute_path = selenium_path
        try:
            option.headless = hide_window
            self._driver = webdriver.Chrome(options=option, executable_path=execute_path)
            self._driver.get(url)
            self._content = WebDriverWait(self._driver, 10).until(
                lambda driver: driver.find_element_by_tag_name("video")).parent
        except TimeoutException:
            raise AparatVideoError("video doesn't exist :(")
        self._extract_all_links()
        self.available_qualities = self._get_qualities()

    def __del__(self):
        if self._driver:
            self._driver.close()

    def download_best_quality(self) -> str:
        if self.available_qualities and len(list(self.available_qualities)) > 0:
            return self.download(self.available_qualities[0])
        return ""

    def download(self, quality: str) -> str:
        if not self._download_path:
            self._download_path = f'{os.getcwd()}//downloads//'
        if not os.path.isdir(self._download_path):
            try:
                os.mkdir(self._download_path)
            except Exception as ex:
                print('Error in create directory ->', ex)
                return ""
        if quality in self.available_qualities:
            return self._download_file(self._qualities[quality], self._download_path)
        else:
            print(f'this quality({quality}) not exist in this video')
            return ""

    def _download_file(self, file_url: str, download_path: str) -> str:
        try:
            file_name = f'{download_path}//{str(uuid.uuid4())}.mp4'
            r = requests.get(file_url, allow_redirects=True)
            if r.status_code == 200:
                open(file_name, 'wb').write(r.content)
            return file_name
        except Exception as ex:
            print(f'Error in downloading -> {ex}')
            return ""

    def _extract_all_links(self):
        download_btn = self._content.find_element_by_css_selector("[aria-label=download]")
        download_btn.click()
        self._content = WebDriverWait(self._content, 10).until(lambda driver: driver.find_element_by_id("144p")).parent
        self._qualities = {}
        for video_quality in list(qualities.keys()):
            try:
                self._qualities[video_quality] = self._content.find_element_by_id(f"{video_quality}p").get_attribute(
                    'href')
            except Exception as ex:
                print(f'Error : {ex}')
                pass

    def _get_qualities(self):
        return list(self._qualities.keys())
