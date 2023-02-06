def format_acc(acc):
    new_acc = {}
    new_acc['acc_no'] = format_acc_no(acc['acc_no'])
    new_acc['bal'] = format_money(acc['bal'])
    new_acc['min_bal'] = format_money(acc['min_bal'])
    new_acc['interest_rate'] = format_ir(acc['interest_rate'])
    new_acc['acc_type'] = acc['acc_type']

    return new_acc

def format_acc_no(num):
    return str(num).zfill(8)

def format_money(num):
    return '%.2f' % num

def format_ir(num):
    return '%.2f' % num
