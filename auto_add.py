import os

def numToTimecode(minute, second):
    prefix = '01:'
    suffix = ',000'
    if second > 59:
        minute += 1
        second = 0

    minute_tc = str(minute)
    second_tc = str(second)
    if minute < 10:
        minute_tc = '0'+minute_tc
    if second < 10:
        second_tc = '0'+second_tc
    timecode = prefix + minute_tc + ':' + second_tc + suffix

    return timecode, minute, second

def split_lang(filepath, opt_lang):
    f1 = open(filepath, 'r', encoding='UTF-8', errors='ignore')
    filename_cn = filepath.replace('.txt', '_cn.srt')
    filename_en = filepath.replace('.txt', '_en.srt')
    f_cn = open(filename_cn, 'w', encoding='UTF-8')
    f_en = open(filename_en, 'w', encoding='UTF-8')
    if opt_lang == '1':
        i = 1
        minute_sum = 0
        second_sum = 0
        for s in f1.readlines():
            s = s.strip()
            if len(s) > 0 and not '\u4e00' <= s[0] <= '\u9fa5' and not '\u4e00' <= s[-2] <= '\u9fa5' :
                print('en', s[-1], s)
                minute, second = minute_sum, second_sum
                tc_start, minute, second = numToTimecode(minute, second)
                second += 3
                tc_end, minute, second = numToTimecode(minute, second)
                srt_block = str(i) + '\n' + tc_start + ' --> ' + tc_end + '\n' + s + '\n\n'
                f_en.write(srt_block)
                i += 1
                minute_sum = minute
                second_sum = second
        f1.close()
        
        f1 = open(filepath, 'r', encoding='UTF-8', errors='ignore')
        i = 1
        minute_sum = 0
        second_sum = 0
        for s in f1.readlines():
            s = s.strip()
            if len(s) > 0 and ('\u4e00' <= s[0] <= '\u9fa5' or  '\u4e00' <= s[-2] <= '\u9fa5') :
                print('cn', s)
                minute, second = minute_sum, second_sum
                tc_start, minute, second = numToTimecode(minute, second)
                second += 3
                tc_end, minute, second = numToTimecode(minute, second)
                srt_block = str(i) + '\n' + tc_start + ' --> ' + tc_end + '\n' + s + '\n\n'
                f_cn.write(srt_block)
                i += 1
                minute_sum = minute
                second_sum = second

    elif opt_lang == '2':
        pass

    f1.close()
    f_cn.close()
    f_en.close()


if __name__ == '__main__':
    while True:
        origin_file = input("原txt字幕文件:")
        origin_file = origin_file.strip('"')
        if origin_file and os.path.exists(origin_file):
            break
    
    while True:
        opt_lang = input("语言分割类型(1-auto, 2-line):")
        if opt_lang == '1':
            break

        if opt_lang == '2':
            cn_line = input("中文首句在第几行(1 or 2):")

    split_lang(origin_file, opt_lang)