import datetime
from rest_framework.response import Response
from rest_framework import status

class DataValidationSuite():

    def __init__(self, request_data):

        self.request_data = request_data

    def execute_validation(self):
        ret = []
        
        if 'curp' in self.request_data: ret.append(self.validate_curp(self.request_data['curp']))
        if 'cp' in self.request_data: ret.append(self.validate_cp(self.request_data['cp']))
        if 'date' in self.request_data: ret.append(self.validate_date(self.request_data['date']))
        if 'telephone' in self.request_data: ret.append(self.validate_telephone(self.request_data['telephone']))
        if 'rfc' in self.request_data: ret.append(self.validate_rfc(self.request_data['rfc']))

        return ret

    def verfify_vocals(self, string):
        for i in range(4):
            if string[i] in ['1','2','3','4','5','6','7','8','9','0']:
                return False
        return True

    def verify_middle_numbers(self, string):
        index = 4
        for i in string[4:10]:
            if string[index] not in ['1','2','3','4','5','6','7','8','9','0']:
                return False
            index += 1
        return True

    def validate_curp(self, curp):
        if len(curp) == 18 and self.verfify_vocals(curp) and self.verify_middle_numbers(curp):
            return True
        return Response(data={'dato_invalido':'El curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def validate_cp(self, cp):
        if len(cp) == 5 and cp[:2] != '00':
            return True
        return Response(data={'dato_invalido':'El cp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def validate_rfc(self, rfc):
        if len(rfc) == 13 and self.verfify_vocals(rfc) and self.verify_middle_numbers(rfc) : 
            return True
        return Response(data={'dato_invalido':'El rfc ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def validate_telephone(self, telephone):
        if len(telephone) == 10:
            return True
        return Response(data={'dato_invalido':'El telefono ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def validate_date(self, date):
        try:
            datetime.datetime.strptime(date, "%d-%m-%Y").date()
        except:
            return Response(data={'dato_invalido':'La fecha ingresada no respeta el formato requerido "dd-mm-aaaa"'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return True
