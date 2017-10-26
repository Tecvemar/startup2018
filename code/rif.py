# -*- encoding: utf-8 -*-

def calcular_rif(data):
    '''
    Toma un nro de cédula o rif y calcula el dígito validador
    data: string con número de CI o RIF sin espacios ni guiones ej.
        V12345678
        E12345678
        J123456789
    devuelve el rif con el dígito calculado
    no se validan los datos de entrada
    para validar: if data == calcular_rif(data):
    '''

    base = {'V': 4, 'E': 8, 'J': 12, 'G': 20}
    oper = [0, 3, 2, 7, 6, 5, 4, 3, 2]
    val = 0
    for i in range(len(data[:9])):
        val += base.get(data[0], 0) if i == 0 else oper[i] * int(data[i])

    digit = 11 - (val % 11)
    digit = digit if digit < 10 else 0
    return '%s%s' % (data[:9], digit)

print calcular_rif('J40425984')
