# Insight Data Science - Find Political Donors - Challenge
# Author: Tianyi Mao, 10/27/2017

def dt_is_valid(dt_str):
    # check if a string is a valid date of format mmddyyyy
    if len(dt_str)!=8:
        return False
    else:
        try:
            month = int(dt_str[:2])
            day = int(dt_str[2:4])
            year = int(dt_str[4:])
        except:
            return False

        if (year < 2015):
            return False # the challenge assumes that all data comes from 2015 or later
        elif (month > 12) or (month < 1):
            return False
        else:
            cale = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if (year % 4 == 0) and ((year % 100 !=0) or (year % 400 == 0)):
                cale[2] = 29
            if (cale[month] < day) or (day < 1):
                return False

    return True

def quick_locate(l_sorted,l_len,new_num):
    # locate where to insert a new element new_num to a sorted list l_sorted with length l_len
    if l_len == None:
        l_len = len(l_sorted)
    front = 0
    rear = l_len-1
    while (rear >= front):
        mid = (front + rear) // 2
        if l_sorted[mid] > new_num:
            rear = mid - 1
        elif l_sorted[mid] < new_num:
            front = mid + 1
        else:
            return mid
    return front

def custom_median(l,l_len):
    # find the median of a sorted list l with given length l_len
    if l_len % 2 == 1:
        return l[l_len//2]
    else:
        return (l[l_len//2]+l[l_len//2-1])/2

class RunningCounter(object):
    def __init__(self):
        self.byzip = {}
        self.bydate = {}
        self.bydate_sorted_keys = []
        self.bydate_sorted_len = 0
        # byzip takes the form:
        # {ID: {zip:{ center:[middle 2 or 3 elements of all contributions], num, sum} }
        # bydate takes the form:
        # {ID: {date:{[list of contributions]} }
        self.input_file = './input/itcont.txt'
        self.output_file_byzip = './output/medianvals_by_zip.txt'
        self.output_file_bydate = './output/medianvals_by_date.txt'

    def update_record(self,input_str):
        l = input_str.split('|')
        # index 0,10,13,14,15 contains essential info
        cmte_id = l[0]
        zip_code = l[10]
        transaction_dt = l[13]
        transaction_amt = l[14]
        other_id = l[15]

        # only deal with a vaild entry
        if (other_id == '') and (cmte_id != '') and (transaction_amt != ''):
            d_amt = float(transaction_amt)
            # check whether entry is valid for byzip:
            if (len(zip_code) >= 5):
                zip_code = zip_code[:5]
                # add info to byzip
                try:
                    _record_dict = self.byzip[cmte_id][zip_code]
                except:
                    try:
                        _dict = self.byzip[cmte_id]
                        _dict[zip_code] = {}
                        _record_dict = _dict[zip_code]
                    except:
                        self.byzip[cmte_id]={}
                        self.byzip[cmte_id][zip_code] = {}
                        _record_dict = self.byzip[cmte_id][zip_code]
                    _record_dict['list'] = []
                    _record_dict['num'] = 0
                    _record_dict['sum'] = 0.0
                # update the dictionary with info from current line
                if _record_dict['num'] == 0:
                    _record_dict['list'].append(d_amt)
                else:
                    _loc = quick_locate(_record_dict['list'],_record_dict['num'],d_amt)
                    _record_dict['list'][_loc:_loc] = [d_amt]
                _record_dict['num'] += 1
                _record_dict['sum'] += d_amt
                # print a new line for byzip file
                byzip_line = self.print_line_byzip(cmte_id,zip_code)+"\n"
                f1.write(byzip_line)

            if dt_is_valid(transaction_dt):
                # rewrite transaction_dt as yyyymmdd
                transaction_dt = transaction_dt[4:]+transaction_dt[:4]
                # add info to bydate
                try:
                    _record_dict = self.bydate[cmte_id][transaction_dt]
                except:
                    try:
                        _dict = self.bydate[cmte_id]
                        _dict[transaction_dt] = {}
                        _record_dict = _dict[transaction_dt]
                    except:
                        self.bydate[cmte_id] = {}
                        self.bydate[cmte_id][transaction_dt] = {}
                        _record_dict = self.bydate[cmte_id][transaction_dt]
                    # add pair (cmte_id,transaction_dt) to sorted keys
                    new_pair = (cmte_id,transaction_dt)
                    _loc = quick_locate(self.bydate_sorted_keys, self.bydate_sorted_len, new_pair)
                    self.bydate_sorted_keys[_loc:_loc] = [new_pair]
                    self.bydate_sorted_len += 1
                    _record_dict['list'] = []
                    _record_dict['num'] = 0
                    _record_dict['sum'] = 0.0
                # update the dictionary with info from current line
                if _record_dict['num'] == 0:
                    _record_dict['list'].append(d_amt)
                else:
                    _loc = quick_locate(_record_dict['list'], _record_dict['num'], d_amt)
                    _record_dict['list'][_loc:_loc] = [d_amt]
                _record_dict['num'] += 1
                _record_dict['sum'] += d_amt

    def print_line_byzip(self,cmte_id,zip_code):
        l = self.byzip[cmte_id][zip_code]['list']
        count = self.byzip[cmte_id][zip_code]['num']
        median = custom_median(l,count)
        total_amt = int(round(self.byzip[cmte_id][zip_code]['sum']))
        median = int(round(median))
        output_str = '{0}|{1}|{2}|{3}|{4}'.format(cmte_id,zip_code,median,count,total_amt)
        return output_str

    def print_record_bydate(self):
        f2 = open(rc.output_file_bydate, 'w')
        for key in self.bydate_sorted_keys:
            cmte_id = key[0]
            transaction_dt = key[1]
            l = self.bydate[cmte_id][transaction_dt]['list']
            count = self.bydate[cmte_id][transaction_dt]['num']
            median = custom_median(l, count)
            total_amt = int(round(self.bydate[cmte_id][transaction_dt]['sum']))
            median = int(round(median))
            transaction_dt = transaction_dt[4:] + transaction_dt[:4]
            output_str = '{0}|{1}|{2}|{3}|{4}'.format(cmte_id, transaction_dt, median, count, total_amt)+'\n'
            f2.write(output_str)
        f2.close()

if __name__ == '__main__':
    rc = RunningCounter()
    f1 = open(rc.output_file_byzip, 'w')
    with open(rc.input_file, 'r') as f:
        for line in f:
            rc.update_record(line)

    f1.close()
    rc.print_record_bydate()
