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

def assemble_timecode_string(minute, second):
    timecode_start, minute, second = numToTimecode(minute, second)
    second += 3
    timecode_end, minute, second = numToTimecode(minute, second)
    timecode = timecode_start + ' --> ' + timecode_end
    return timecode, minute, second

def split_lang(filepath, opt_lang):
    f1 = open(filepath, 'r', encoding='UTF-8', errors='ignore')
    filename_cn = filepath.replace('.txt', '_cn.srt')
    filename_en = filepath.replace('.txt', '_en.srt')
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
                # check if is english:
                if not '\u4e00' <= s[0] <= '\u9fa5' and not '\u4e00' <= s[-1] <= '\u9fa5' :
                    print('en', s[-1], s)
                    minute, second = minute_en, second_en
                    timecode, minute, second = assemble_timecode_string(minute, second)
                    srt_block = str(i_en) + '\n' + timecode + '\n' + s + '\n\n'
                    f_en.write(srt_block)
                    i_en += 1
                    minute_en = minute
                    second_en = second
                # else it's chinese:
                else:
                    print('cn', s)
                    minute, second = minute_cn, second_cn
                    timecode, minute, second = assemble_timecode_string(minute, second)
                    srt_block = str(i_cn) + '\n' + timecode + '\n' + s + '\n\n'
                    f_cn.write(srt_block)
                    i_cn += 1
                    minute_cn = minute
                    second_cn = second
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
            while True:
                first_line = input("首句为哪种语言(cn or en):")
                if first_line == 'cn' or first_line == 'en':
                    break

    split_lang(origin_file, opt_lang)