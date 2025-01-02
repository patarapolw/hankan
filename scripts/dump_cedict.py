from urllib.request import urlretrieve
from pathlib import Path
from zipfile import ZipFile



def dump_cedict():
    zipPath = Path('public') / "cedict_1_0_ts_utf-8_mdbg.zip"

    url = "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip"
    print("Downloading {} from {}".format(zipPath, url))
    urlretrieve(url, zipPath)


    tmp_root = Path("tmp")
    tmp_root.mkdir(exist_ok=True)

    filename = "cedict_ts.u8"
    cedict = tmp_root / filename


    with ZipFile(zipPath) as z:
        z.extract(cedict.name, path=cedict.parent)


if __name__ == "__main__":
    dump_cedict()
