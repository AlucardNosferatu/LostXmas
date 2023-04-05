import os

from ocr_config import text_dir, std_full_len
from ocr_util import ends_with_strs


def manual_filter(tgt_txt, tag_missing=False):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if tag_missing:
        i = 0
        while i != len(lines):
            if i + 1 < len(lines):
                this_tag = lines[i].split('\t')[0]
                next_tag = lines[i + 1].split('\t')[0]
                if this_tag == 'q' and this_tag == next_tag:
                    insert_tag_missing = ''
                    while insert_tag_missing not in ['y', 'n']:
                        print('Current txt:', tgt_txt)
                        print('prev line:', lines[i].strip('\n'))
                        print('next line:', lines[i + 1].strip('\n'))
                        insert_tag_missing = input('y for tagging missing sentences\nn for pass')
                    if insert_tag_missing == 'y':
                        lines.insert(i + 1, 'm\t\n')
                i += 1
            else:
                break
    else:
        i = len(lines)
        while i != 0:
            i -= 1
            # do not check concatenated sentences
            if len(lines[i]) < std_full_len:
                drop_this_line = ''
                while drop_this_line not in ['y', 'n']:
                    print('Current txt:', tgt_txt)
                    if i - 1 >= 0:
                        print(lines[i - 1], lines[i])
                    else:
                        print(lines[i])
                    drop_this_line = input('y for drop\nn for pass')
                if drop_this_line == 'y':
                    lines.pop(i)

    with open(tgt_txt.replace('.txt', '_man.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def delete_redundant_version(txt_in_dir):
    for txt in txt_in_dir:
        old_txt = txt
        txt = txt.replace('.txt', '')
        txt = txt.split('_')
        last_mod = txt[-1]
        if txt.count(last_mod) > 1:
            rollback_ver = txt.index(last_mod)
            while len(txt) > rollback_ver + 1:
                txt.pop(-1)
            txt = '_'.join(txt)
            txt += '.txt'
            if os.path.exists(os.path.join(text_dir, txt)):
                os.remove(os.path.join(text_dir, txt))
            if os.path.exists(os.path.join(text_dir, old_txt)):
                os.rename(os.path.join(text_dir, old_txt), os.path.join(text_dir, txt))


def match_with_stacks(tgt_txt, eager_mode=False):
    def isint(str_cmd):
        # noinspection PyBroadException
        try:
            _ = int(str_cmd)
            return True
        except Exception as e:
            _ = repr(e)
            return False

    def select_partner(this_line, wait_partner, paired, wait_rivals):
        halt_ctrl = False
        if len(wait_partner) <= 1:
            if len(wait_partner) < 1:
                wait_rivals.append(this_line)
                return wait_partner, paired, wait_rivals, halt_ctrl
            elif eager_mode:
                selected_partner = wait_partner.pop(0)
                tag_this_line = this_line.split('\t')[0]
                tag_selected_partner = selected_partner.split('\t')[0]
                paired_dict = {
                    tag_this_line: this_line,
                    tag_selected_partner: selected_partner
                }
                paired.append(paired_dict)
                return wait_partner, paired, wait_rivals, halt_ctrl
        else:
            select_cmd = ''
            while not isint(select_cmd) or int(select_cmd) not in list(range(-3, len(wait_partner))):
                print('>>>Current line:')
                print(this_line.strip('\n'))
                print('>>>Potential partner:')
                for i, potential_partner in enumerate(wait_partner):
                    print(i, potential_partner.strip('\n'))
                select_cmd = input('>>>Input partner index:')
            select_cmd = int(select_cmd)
            if select_cmd < 0:
                wait_rivals.append(this_line)
                if select_cmd < -1:
                    if select_cmd < -2:
                        purge_partner = ''
                        while purge_partner not in ['y', 'n']:
                            purge_partner = input('>>>Are you sure to purge waiting partners? [y/n]:')
                        if purge_partner == 'y':
                            wait_partner.clear()
                            print('>>>Waiting partners have been purged.')
                        else:
                            print('>>>Abort purging, waiting partners remain intact.')
                    else:
                        halt_ctrl = True
                return wait_partner, paired, wait_rivals, halt_ctrl
            else:
                selected_partner = wait_partner.pop(select_cmd)
                tag_this_line = this_line.split('\t')[0]
                tag_selected_partner = selected_partner.split('\t')[0]
                paired_dict = {
                    tag_this_line: this_line,
                    tag_selected_partner: selected_partner
                }
                paired.append(paired_dict)
                return wait_partner, paired, wait_rivals, halt_ctrl

    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    p_list = []
    w_que = []
    w_ans = []
    halt = False
    while len(lines) > 0 and not halt:
        print('Current txt:', tgt_txt)
        tl = lines.pop(0)
        tag = tl.split('\t')[0]
        if tag == 'q':
            w_ans, p_list, w_que, halt = select_partner(tl, w_ans, p_list, w_que)
        elif tag == 'a':
            w_que, p_list, w_ans, halt = select_partner(tl, w_que, p_list, w_ans)
        else:
            raise ValueError('Unexpected tag alphabet.')
    halt = False
    while (len(w_ans) > 0 and len(w_que) > 0) and not halt:
        tl = w_que.pop(0)
        w_ans, p_list, w_que, halt = select_partner(tl, w_ans, p_list, w_que)
    while len(p_list) > 0:
        pair_dict = p_list.pop(0)
        pair_q = pair_dict['q']
        pair_a = pair_dict['a']
        lines.append(pair_q)
        lines.append(pair_a)
    if eager_mode:
        with open(tgt_txt.replace('.txt', '_eag_mat.txt'), 'w', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        with open(tgt_txt.replace('.txt', '_mat.txt'), 'w', encoding='utf-8') as f:
            f.writelines(lines)


if __name__ == '__main__':
    file_type_postfixes = [
        '_mat.txt'
    ]
    skipped = [
        'xiaoice_island (1).txt'
        # 'xiaoice_island (2).txt',
        # 'xiaoice_island (3).txt',
        # 'xiaoice_island (4).txt',
        # 'xiaoice_island (5).txt',
        # 'xiaoice_island (6).txt',
        # 'xiaoice_island (7).txt',
        # 'xiaoice_island (8).txt',
        # 'xiaoice_island (9).txt',
        # 'xiaoice_island (10).txt',
        # 'xiaoice_island (11).txt',
        # 'xiaoice_island (12).txt',
        # 'xiaoice_island (13).txt',
        # 'xiaoice_island (14).txt',
        # 'xiaoice_island (15).txt',
        # 'xiaoice_island (16).txt',
        # 'xiaoice_island (17).txt',
    ]
    files = os.listdir(text_dir)
    delete_redundant_version(files)

    # # full-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         filter_by_prefix(os.path.join(text_dir, file))

    # # semi-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         concatenate_by_length_and_tag(os.path.join(text_dir, file))

    # # manual
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('_fin.txt') and file not in skipped:
    #         sort_by_batch(os.path.join(text_dir, file))

    # # full-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         correct_wrong_word(os.path.join(text_dir, file))

    # # semi-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('_cor.txt') and file not in skipped:
    #         manual_filter(os.path.join(text_dir, file), tag_missing=False)

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
            match_with_stacks(os.path.join(text_dir, file))

    # # semi-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         manual_filter(os.path.join(text_dir, file), tag_missing=True)

    files = os.listdir(text_dir)
    delete_redundant_version(files)
    print('Done')
