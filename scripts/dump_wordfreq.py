from wordfreq import zipf_frequency
from regex import Regex

import json


def dump_wordfreq_zh():
    re_han = Regex(r"^\p{Han}+$")
    f_dict = {}

    for v in _load_vocab():
        if not re_han.fullmatch(v):
            continue

        if v in f_dict:
            continue

        f = zipf_frequency(v, "zh")
        f_dict[v] = f

    for k, _ in set(filter(lambda kv: kv[1] == 0, f_dict.items())):
        del f_dict[k]

    with open("public/wordfreq_zh.json", "w", encoding="utf8") as f:
        json.dump(f_dict, f, ensure_ascii=False, indent=0)


def _load_vocab():
    for ln in open("tmp/cedict_ts.u8", "r", encoding="utf8"):
        if ln[0] == "#":
            continue

        trad, simp, _ = ln.split(" ", 2)

        yield simp

        if trad != simp:
            yield trad


if __name__ == "__main__":
    dump_wordfreq_zh()
