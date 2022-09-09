import datetime


def verfify_vocals(string):
    for i in range(4):
        if string[i] in ['1','2','3','4','5','6','7','8','9','0']:
            return False
    return True

def verify_middle_numbers(string):
    index = 4
    for i in string[4:10]:
        if string[index] not in ['1','2','3','4','5','6','7','8','9','0']:
            return False
        index += 1
    return True


def validate_curp(curp):
    if len(curp) == 18 and verfify_vocals(curp) and verify_middle_numbers(curp):
        return True
    return False


def validate_cp(cp):
    if len(cp) < 5 and cp[:2] == '00':
        return False
    return True


def validate_rfc(rfc):
    if len(rfc) == 13 and verfify_vocals(rfc) and verify_middle_numbers(rfc): 
        return True
    return False


def validate_telephone(telephone):
    if len(telephone) < 10:
        return False
    return True


def validate_date(date):
    try:
        obj = datetime.datetime.strptime(date, "%d-%m-%Y").date()
        return True
    except:
        return False