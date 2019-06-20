# encoding=utf-8


def pinyin2ToneNumber(lineIn):
    """
    拼音转声调数字
    """
    assert type(lineIn) is str
    lineOut = lineIn

    # map (final) constanant+tone to tone+constanan
    mapConstTone2ToneConst = {
        'n1':  '1n',
        'n2':  '2n',
        'n3':  '3n',
        'n4':  '4n',
        'ng1': '1ng',
        'ng2': '2ng',
        'ng3': '3ng',
        'ng4': '4ng',
        'ng1': 'n1g',
        'ng2': 'n2g',
        'ng3': 'n3g',
        'ng4': 'n4g',
        'r1':  '1r',
        'r2':  '2r',
        'r3':  '3r',
        'r4':  '4r'
    }

    # map vowel+vowel+tone to vowel+tone+vowel
    mapVowelVowelTone2VowelToneVowel = {
        'ai1': 'a1i',
        'ai2': 'a2i',
        'ai3': 'a3i',
        'ai4': 'a4i',
        'ao1': 'a1o',
        'ao2': 'a2o',
        'ao3': 'a3o',
        'ao4': 'a4o',
        'ei1': 'e1i',
        'ei2': 'e2i',
        'ei3': 'e3i',
        'ei4': 'e4i',
        'ou1': 'o1u',
        'ou2': 'o2u',
        'ou3': 'o3u',
        'ou4': 'o4u'
    }

    # map vowel-number combination to unicode
    mapVowelTone2Unicode = {
        'a1': 'ā',
        'a2': 'á',
        'a3': 'ǎ',
        'a4': 'à',
        'e1': 'ē',
        'e2': 'é',
        'e3': 'ě',
        'e4': 'è',
        'i1': 'ī',
        'i2': 'í',
        'i3': 'ǐ',
        'i4': 'ì',
        'o1': 'ō',
        'o2': 'ó',
        'o3': 'ǒ',
        'o4': 'ò',
        'u1': 'ū',
        'u2': 'ú',
        'u3': 'ǔ',
        'u4': 'ù',
        'v1': 'ǖ',
        'v2': 'ǘ',
        'v3': 'ǚ',
        'v4': 'ǜ'
    }

    # mapVowelTone2Unicode
    for x, y in mapVowelTone2Unicode.items():
        lineOut = lineOut.replace(y, x).replace(y.upper(), x.upper())

    # mapVowelVowelTone2VowelToneVowel
    for x, y in mapVowelVowelTone2VowelToneVowel.items():
        lineOut = lineOut.replace(y, x).replace(y.upper(), x.upper())

    # first transform
    for x, y in mapConstTone2ToneConst.items():
        lineOut = lineOut.replace(y, x).replace(y.upper(), x.upper())

    return lineOut.replace('Ü', 'V').replace('ü', 'v')


def parsePinyin(pinyin):
    """
    解析拼音
    """
    shengmu = ["b", "p", "m", "f", "d", "t", "n", "l", "g", "k",
               "h", "j", "q", "x", "zh", "ch", "sh", "r", "z", "c", "s"]

    songqi = ["p", "t", "k", "c", "ch", "q"]

    kaikou = ["*i", "a", "o", "e", "er", "ai", "ei",
              "ao", "ou", "an", "en", "ang", "eng", "*ong"]

    bankaikou = ["yi", "i", "ya", "ia", "ye", "ie", "yao", "iao",
                 "you", "iu", "yan", "ian", "yin", "in", "yang", "iang",
                 "ying", "ing", "yong", "iong"]

    # 找出声调
    shengdiao = ""
    if pinyin[-1:].isnumeric():
        shengdiao = pinyin[-1:]
        pinyin = pinyin[0:len(pinyin)-1]

    # 找出声母
    py_sm = ""
    for sm in shengmu:
        if sm == pinyin[0]:
            py_sm = pinyin[0]
            break

        if sm == pinyin[0:2]:
            py_sm = pinyin[0:2]
            break
    # 找出韵母
    sm_len = len(py_sm)
    if sm_len > 0:
        yunmu = pinyin[sm_len:]
    else:
        yunmu = pinyin

    try:
        is_songqi = songqi.index(py_sm) > -1
    except ValueError:
        is_songqi = False

    is_kaikou = 0
    # 开口
    for kk in kaikou:
        if kk[0] == '*' and kk[1:] == yunmu[-len(kk[1:]):]:
            is_kaikou = 1
        elif kk == yunmu:
            is_kaikou = 1
    # 半开口
    for kk in bankaikou:
        if kk == yunmu:
            is_kaikou = 2
    
    return {
        "shengmu": py_sm,
        "yunmu": yunmu,
        "shengdiao": shengdiao,
        "songqi": is_songqi,
        "kaikou": is_kaikou
    }


def mid(content, start, end=None, clear=None):
    """
    字符串截取函数

    @param content      内容
    @param start        开始字符串   以括号"("开始且结尾的则按照正则表达式执行
    @param end          结束字符串   以括号"("开始且结尾的则按照正则表达式执行
    @param clear        清理
    @return string      截取之后的内容

    """
    if len(content) == 0 or len(start) == 0:
        return ''
    # start
    if start[0] == '(' and start[-1] == ')':
        start = re.search(start, content, re.I)
        if start == None:
            return ''
        else:
            start = start.group()

    # end
    if end and end[0] == '(' and end[-1] == ')':
        end = re.search(end, content, re.I)
        if end == None:
            end = ''
        else:
            end = end.group()

    # find start
    start_pos = content.find(start)
    if start_pos == -1 or end == '':
        return ''
    # substr
    if end == None:
        content = content[start_pos:]
    else:
        start_len = len(start)
        end_pos = content[start_pos + start_len:].find(end)
        if end_pos == -1:
            return ''
        else:
            content = content[start_pos +
                              start_len: end_pos + start_pos + start_len]

    # clear
    if isinstance(clear, list) or isinstance(clear, tuple):
        for rule in clear:
            if rule[0] == '(' and rule[-1] == ')':
                content = re.sub(rule, '', content, re.I | re.S)
            else:
                content = content.replace(rule, '')
    elif clear != None:
        if clear[0] == '(' and clear[-1] == ')':
            content = re.sub(clear, '', content, re.I | re.S)
        else:
            content = content.replace(clear, '')

    return content
