from wordfreq import zipf_frequency

import json


def dump_wordfreq_ja():
    f_dict = {}

    with open("tmp/jmdict.json", "r", encoding="utf8") as f:
        obj = json.load(f)
        for w in obj["words"]:
            for v in _load_jmdict_entries(w):
                f_dict.setdefault(v, zipf_frequency(v, "ja"))

    with open("tmp/jmnedict.json", "r", encoding="utf8") as f:
        obj = json.load(f)
        for w in obj["words"]:
            for v in _load_jmdict_entries(w):
                f_dict.setdefault(v, zipf_frequency(v, "ja"))

    for k, _ in set(filter(lambda kv: kv[1] == 0, f_dict.items())):
        del f_dict[k]

    with open("public/wordfreq_ja.json", "w", encoding="utf8") as f:
        json.dump(f_dict, f, ensure_ascii=False, indent=0)


def _load_jmdict_entries(w):
    if w["kanji"]:
        for k in w["kanji"]:
            yield k["text"]
    else:
        for k in w["kana"]:
            yield k["text"]


def dump_wordfreq_zh():
    f_dict = {}

    for v in _load_cedict():
        f_dict.setdefault(v, zipf_frequency(v, "zh"))

    for k, _ in set(filter(lambda kv: kv[1] == 0, f_dict.items())):
        del f_dict[k]

    with open("public/wordfreq_zh.json", "w", encoding="utf8") as f:
        json.dump(f_dict, f, ensure_ascii=False, indent=0)


def _load_cedict():
    for ln in open("tmp/cedict_ts.u8", "r", encoding="utf8"):
        if ln[0] == "#":
            continue

        trad, simp, _ = ln.split(" ", 2)

        yield simp

        if trad != simp:
            yield trad


if __name__ == "__main__":
    dump_wordfreq_zh()
    dump_wordfreq_ja()
