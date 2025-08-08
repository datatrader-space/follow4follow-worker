import os
import re
import platform
import subprocess
import requests
import zipfile,shutil
import io
class ChromeDriverCheckerandDownloader:
    def __init__(self):
        self.reporter=''
        self.task=''
    def extract_version_registry(self, output):
        """Extracts the Chrome version from the registry output."""
        try:
            google_version = ""
            for letter in output[output.rindex("DisplayVersion    REG_SZ") + 24 :]:
                if letter != "\n":
                    google_version += letter
                else:
                    break
            version = google_version.strip()
            self.reporter.report_performance(end_point='extract_version_registry', type='chrome_registry_version_found',  task=self.task if self.task else None, service='browser', data_point='extract_version_registry')
            return version
        except TypeError as e:
            self.reporter.report_performance(end_point='extract_version_registry', type='failed_to_extract_registry_version', traceback=str(e), task=self.task if self.task else None, service='browser', data_point='extract_version_registry')
            return None

    def extract_version_folder(self):
        """Extracts the Chrome version from the folder name.

        Check if the Chrome folder exists in the x32 or x64 Program Files folders.
        """
        for i in range(2):
            path = "C:\\Program Files" + (" (x86)" if i else "") + "\\Google\\Chrome\\Application"
            if os.path.isdir(path):
                paths = [f.path for f in os.scandir(path) if f.is_dir()]
                for path in paths:
                    filename = os.path.basename(path)
                    pattern = "\d+\.\d+\.\d+\.\d+"
                    match = re.search(pattern, filename)
                    if match and match.group():
                        version = match.group(0)
                        self.reporter.report_performance(end_point='extract_version_folder', type='chrome_folder_version_found', task=self.task if self.task else None, service='browser', data_point='extract_version_folder')
                        return version

        self.reporter.report_performance(end_point='extract_version_folder', type='chrome_folder_not_found', task=self.task if self.task else None, service='browser', data_point='extract_version_folder')
        return None

    def get_chrome_version(self):
        """Gets the Chrome version."""
        version = None
        install_path = None
        from sys import platform
        try:
            if platform == "linux" or platform == "linux2":
                # linux
                install_path = "/usr/bin/google-chrome"
            elif platform == "darwin":
                # OS X
                install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
            elif platform == "win32":
                # Windows...
                try:
                    # Try registry key.
                    stream = os.popen(
                        'reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"'
                    )
                    output = stream.read()
                    version = self.extract_version_registry(output)
                except Exception as e:
                    # Try folder path.
                    self.reporter.report_performance(end_point='get_chrome_version', type='registry_query_failed', traceback=str(e), task=self.task if self.task else None, service='browser', data_point='get_chrome_version')
                    version = self.extract_version_folder()
        except Exception as ex:
            self.reporter.report_performance(end_point='get_chrome_version', type='get_chrome_version_exception', traceback=str(ex), is_error=True, task=self.task if self.task else None, service='browser', data_point='get_chrome_version')
            print(ex)

        try:
            version = os.popen(f"{install_path} --version").read().strip("Google Chrome ").strip() if install_path else version
            if version:
                self.reporter.report_performance(end_point='get_chrome_version', type='command_line_version_found', task=self.task if self.task else None, service='browser', data_point='get_chrome_version')

        except Exception as e:
            self.reporter.report_performance(end_point='get_chrome_version', type='command_line_version_check_failed', traceback=str(e), task=self.task if self.task else None, service='browser', data_point='get_chrome_version')

        if version:
            self.reporter.report_performance(end_point='get_chrome_version', type='chrome_version_found', task=self.task if self.task else None, service='browser', data_point='get_chrome_version')
        else:
            self.reporter.report_performance(end_point='get_chrome_version', type='chrome_version_not_found', task=self.task if self.task else None, service='browser', data_point='get_chrome_version')

        return version
    def get_chromedriver_version(self, assets_dir="assets"):
        """Gets the installed ChromeDriver version from a specific directory."""
        chromedriver_path = os.path.join(os.getcwd(), assets_dir, "chromedriver")
        if os.name == 'nt':
            chromedriver_path += '.exe'

        try:
            output = subprocess.check_output([chromedriver_path, "--version"], stderr=subprocess.STDOUT, encoding='utf-8')
            version_match = re.search(r'ChromeDriver (\d+\.\d+\.\d+\.\d+)', output)
            if version_match:
                version = version_match.group(1)
                self.reporter.report_performance(end_point='get_chromedriver_version', type='chromedriver_version_found', task=self.task if self.task else None, service='browser', data_point='get_chromedriver_version')
                return version
            else:
                self.reporter.report_performance(end_point='get_chromedriver_version', type='chromedriver_version_match_not_found', task=self.task if self.task else None, service='browser', data_point='get_chromedriver_version')
                return None
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.reporter.report_performance(end_point='get_chromedriver_version', type='chromedriver_not_found_or_version_error', traceback=str(e), is_error=True, task=self.task if self.task else None, service='browser', data_point='get_chromedriver_version')
            return None

    def download_chromedriver(self, chrome_version):
        """Downloads the latest ChromeDriver for the given Chrome major version."""
        try:
            system = platform.system()
            arch = "win64"

            if system == "Windows":
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
                chromedriver_filename = "chromedriver.exe"
            elif system == "Linux":
                arch = "linux64"
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/linux64/chromedriver-linux64.zip"
                chromedriver_filename = "chromedriver"
            elif system == "Darwin":
                arch = "mac-x64"
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/mac-x64/chromedriver-mac-x64.zip"
                chromedriver_filename = "chromedriver"
            else:
                self.reporter.report_performance(end_point='download_chromedriver', type='unsupported_os', task=self.task if self.task else None, service='browser', data_point='download_chromedriver')
                print(f"Unsupported operating system: {system}")
                return False

            self.reporter.report_performance(end_point='download_chromedriver', type='downloading_chromedriver',  task=self.task if self.task else None, service='browser', data_point='download_chromedriver')
            assets_path = os.path.join(os.getcwd(), 'assets')
            temp_extraction_path = os.path.join(os.getcwd(), "temp_chromedriver")
            os.makedirs(temp_extraction_path, exist_ok=True)
            response = requests.get(download_url, stream=True)
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            for file_info in zip_file.infolist():
                if file_info.filename.endswith(chromedriver_filename):
                    zip_file.extract(file_info.filename, path=temp_extraction_path)
                    extracted_chromedriver_path = os.path.join(temp_extraction_path, file_info.filename)
                    target_chromedriver_path = os.path.join(assets_path, chromedriver_filename)

                    if os.path.exists(target_chromedriver_path):
                        os.remove(target_chromedriver_path)

                    shutil.move(extracted_chromedriver_path, target_chromedriver_path)
                    shutil.rmtree(temp_extraction_path)
                    break

            self.reporter.report_performance(end_point='download_chromedriver', type='chromedriver_downloaded_and_extracted', task=self.task if self.task else None, service='browser', data_point='download_chromedriver')
            print(f"ChromeDriver downloaded and extracted as {chromedriver_filename}")
            return True

        except Exception as e:
            self.reporter.report_performance(end_point='download_chromedriver', type='chromedriver_download_error', traceback=str(e), is_error=True, task=self.task if self.task else None, service='browser', data_point='download_chromedriver')
            print(f"Error downloading ChromeDriver: {e}")
            return False

    def check_and_download_chromedriver(self):
        """Checks Chrome and ChromeDriver versions and downloads if necessary."""
        chrome_version = self.get_chrome_version()
        chromedriver_version = self.get_chromedriver_version()

        if not chrome_version:
            print("Could not determine Chrome version.")
            return

   

        if not chromedriver_version:
            print("ChromeDriver not found. Downloading...")
            self.download_chromedriver(chrome_version)
            return

        chrome_major = chrome_version.split(".")[0]
        chromedriver_major = chromedriver_version.split(".")[0]

        if chrome_major != chromedriver_major:
            print(f"Chrome version ({chrome_version}) and ChromeDriver version ({chromedriver_version}) mismatch. Downloading...")
            if self.download_chromedriver(chrome_version):
                return True
            else:
                return False
        else:
            return True
