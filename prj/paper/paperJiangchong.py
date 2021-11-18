import pandas as pd
import jieba
import synonyms

# 更改比例 小 中 大 s m l
# 更改程度 小 中 大 s m l


def change(text, rate=1, level=2):
    i = 0
    while(i < level):
        i += 1
        seg_list = list(jieba.cut(text, cut_all=False))
        for i in range(len(seg_list)):
            s = seg_list[i]
            try:
                if synonyms.nearby(s)[0] != None:
                    s = synonyms.nearby(s)[0][2]
            except:
                pass
            seg_list[i] = s

        text = ''.join(seg_list)
    return text


if __name__ == '__main__':
    while True:
        print(change(input(), level=2))