import os
import re
from load_config import loadConfig

def auto_correction(phrase, illegalEnds, corrctionslist, corrections):
    phrase = phrase.strip()
    if len(phrase) > 0:
        phrase = phrase[0].upper() + phrase[1:]
        
    while "  " in phrase:
        phrase = phrase.replace("  ", " ")

    for char in illegalEnds:
        if phrase.endswith(char):
            phrase = phrase.rstrip(char)

    for item in corrctionslist:
        if item in phrase:
            phrase = phrase.replace(item, corrections[item])
            print("find '" + item + "', replaced by " + corrections[item])
    return phrase

def split(illegalEnds, phrase, newPhrase=''):
    if any(x in phrase for x in illegalEnds):
        for char in phrase:
            if char in illegalEnds and not phrase.endswith(char):
                splitedPhrases = phrase.split(char, 1)
                if len(splitedPhrases) > 1:
                    newPhrase = splitedPhrases[0]
                    print("new Phrase: ", newPhrase)
                    return newPhrase + '\n' + split(illegalEnds, splitedPhrases[1])
    return phrase

def split_phrase(illegalEnds, filepath):
    filepath_temp = filepath.replace('.txt', '_temp.txt')
    f_origin = open(filepath, 'r', encoding='UTF-8', errors='ignore')
    f_temp = open(filepath_temp, 'w', encoding='UTF-8')

    string = f_origin.read()
    phrases = string.split("\n")
    # while not splitOk: 
    for phrase in phrases:
        f_temp.write(split(illegalEnds, phrase)+'\n')

    f_temp.close()
    f_origin.close()


def contain_zh(phrase):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    phrase_bytes = bytes(phrase, 'utf-8')
    phrase_bytes = phrase_bytes.decode()
    match = zh_pattern.search(phrase_bytes)
    return match

def numToTimecode(minute, second):
    params = loadConfig()
    prefix = params['prefixTC']
    suffix = params['sufixTC']
    if second > 59:
        minute += 1
        second = 0

    minute_tc = str(minute)
    second_tc = str(second)
    if minute < 10:
        minute_tc = '0' + minute_tc
    if second < 10:
        second_tc = '0' + second_tc
    timecode = prefix + minute_tc + ':' + second_tc + suffix

    return timecode, minute, second

def assemble_timecode_string(minute, second, blockLength, blockSpace):
    timecode_start, minute, second = numToTimecode(minute, second)
    second += blockLength
    timecode_end, minute, second = numToTimecode(minute, second)
    timecode = timecode_start + ' --> ' + timecode_end
    second += blockSpace
    return timecode, minute, second

def split_lang(filepath, opt_lang):
    params = loadConfig()
    # Demande for srt creating infos
    while True:
        blockLength_str = input("srt字块时长（默认" + params["blockLength"] + "秒）：")
        if not blockLength_str:
            blockLength_str = params["blockLength"]

        blockSpace_str = input("srt字块间隔（默认" + params["blockSpace"] + "秒）：")
        if not blockSpace_str:
            blockSpace_str = params["blockSpace"]

        doSplitAnwser = input("是否分割标点和长句(y-yes, n-no):")
        if doSplitAnwser == "y":
            doSplit = True
        if doSplitAnwser == "n":
            doSplit = False
        if not doSplitAnwser:
            doSplit = True

        if blockLength_str.isnumeric() and blockSpace_str.isnumeric():
            blockLength = int(blockLength_str)
            blockSpace = int(blockSpace_str)
            break

    if doSplit:
        split_phrase(params["illegalEnds"], filepath)
        filepath = filepath.replace('.txt', '_temp.txt')   
        filename_cn = filepath.replace('_temp.txt', '_cn.srt')
        filename_en = filepath.replace('_temp.txt', '_en.srt')
    else:
        filename_cn = filepath.replace('.txt', '_cn.srt')
        filename_en = filepath.replace('.txt', '_en.srt')
        

    f1 = open(filepath, 'r', encoding='UTF-8', errors='ignore')
    f_cn = open(filename_cn, 'w', encoding='UTF-8')
    f_en = open(filename_en, 'w', encoding='UTF-8')
    if opt_lang == '1':
        # init indexes
        i_cn = 1
        minute_cn = 0
        second_cn = 0
        i_en = 1
        minute_en = 0
        second_en = 0
        for s in f1.readlines():
            s = s.strip()
            if len(s) > 0:
                # check if is chinese:
                if contain_zh(s) :
                    print('cn', s)
                    s = auto_correction(s, params["illegalEnds"], params["correctionList_cn"], params["corrections_cn"])
                    minute, second = minute_cn, second_cn
                    timecode, minute, second = assemble_timecode_string(minute, second, blockLength, blockSpace)
                    srt_block = str(i_cn) + '\n' + timecode + '\n' + s + '\n\n'
                    f_cn.write(srt_block)
                    i_cn += 1
                    minute_cn = minute
                    second_cn = second
                # else it's english:
                else:
                    print('en', s[-1], s)
                    if doSplit:
                        s = auto_correction(s, params["illegalEnds"], params["correctionList_en"], params["corrections_en"])
                    minute, second = minute_en, second_en
                    timecode, minute, second = assemble_timecode_string(minute, second, blockLength, blockSpace)
                    srt_block = str(i_en) + '\n' + timecode + '\n' + s + '\n\n'
                    f_en.write(srt_block)
                    i_en += 1
                    minute_en = minute
                    second_en = second

    elif opt_lang == '2':
        pass

    f1.close()
    f_cn.close()
    f_en.close()

    # Delete f_temp
    if doSplit and os.path.exists(filepath):
        os.remove(filepath)


if __name__ == '__main__':
    while True:
        origin_file = input("原txt字幕文件:")
        origin_file = origin_file.strip('"')
        if origin_file and os.path.exists(origin_file):
            break
    
    # while True:
    #     opt_lang = input("语言分割类型(1-auto, 2-line):")
    #     if opt_lang == '1':
    #         break

    #     if opt_lang == '2':
    #         while True:
    #             first_line = input("首句为哪种语言(cn or en):")
    #             if first_line == 'cn' or first_line == 'en':
    #                 break
    opt_lang = '1'


    split_lang(origin_file, opt_lang)