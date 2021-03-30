#!/usr/bin/env python

import fire
import requests
import subprocess


class History:
    """Catch al object to process m3u8 files"""

    def find(self, year: str, month: int, day: int):
        # https://ondemand-radio-cf-vrt.akamaized.net/audioonly/content/2021/02/21/20_De_Pr__Historie_210221120001_20210221120049_ondemand_128.mp4/20_De_Pr__Historie_210221120001_20210221120049_ondemand_128-audio=124625.m3u8
        month = f"{month:02}"
        day = f"{day:02}"
        short_year = str(year)[2:]
        uri = "https://ondemand-radio-cf-vrt.akamaized.net/audioonly/content"
        print(uri)
        for bsec in range(1, 60):
            for esec in range(1, 60):
                if bsec >= esec:
                    continue
                url = f"{year}/{month}/{day}/20_De_Pr__Historie_{short_year}{month}{day}1200{bsec}_{year}{month}{day}1200{esec}_ondemand_128.mp4/20_De_Pr__Historie_{short_year}{month}{day}1200{bsec}_{year}{month}{day}1200{esec}_ondemand_128-audio=124625.m3u8"
                rs = requests.get(f"{uri}/{url}")
                if rs.status_code == 200:
                    print(f"GOT IT: {url}")
                    return url
                else:
                    print(f"CHECKING: {url}", end="\r", flush=True)

        raise Exception("No m3u8 found :(")


    def download(self, year: str, month: int, day: int, url: str = None):
        """Download De Pré History"""
        filename = f"{year}-{month:02}-{day:02}.mp4"
        found_url = url if url else self.find(year, month, day)
        cmd = f"ffmpeg -i '{found_url}' -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {filename}"
        print(cmd)
        subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    fire.Fire(History)
