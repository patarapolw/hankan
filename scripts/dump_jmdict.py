import webview

from urllib.request import urlretrieve
from zipfile import ZipFile
from pathlib import Path


def run_in_webview():
    def eval_jmdict_links(r):
        def extract(k: str):
            print(f"Extracting {k}")

            url = r[k]
            zip_file = Path("public") / f"{k}.zip"
            json_folder = Path("tmp")

            urlretrieve(url, zip_file)

            with ZipFile(zip_file) as z:
                info = z.filelist[0]
                z.extract(info, json_folder)

                json_src = json_folder / info.filename
                json_dst = json_folder / f"{k}.json"

                json_dst.unlink(missing_ok=True)
                json_src.rename(json_dst)

        extract("jmdict")
        extract("jmnedict")
        extract("kanjidic2")

        print("Done")
        win.destroy()

    win.evaluate_js(
        "new Promise((resolve) => setTimeout(() => resolve(getJMDictLinks()), 1000))",
        eval_jmdict_links,
    )


win = webview.create_window("Dump JMDict", "http://localhost:33126", hidden=True)
webview.start(run_in_webview)
