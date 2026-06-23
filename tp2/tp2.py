def principal():
    m=open("tratamientos.txt")
    suma_total_general = 0
    cont_total_general = 0
    montoAL = montoMZ = montoU = 0
    r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = r10 = 0
    suma_prom = cont_prom = 0
    promedio_final = 0
    paciente_mayor_importe = ""
    mayor_importe = 0
    cont_alta_complejidad = 0
    cont_alta_complejidad_supera_promedio = 0
    for linea in m:
        if linea[0] == "#":
            montoAL=int(linea[2:8])
            montoMZ=int(linea[8:14])
            montoU=int(linea[14:20])
        else:
            r1+=1
            paciente=linea[0:25].strip()
            ICD10=linea[25:31].strip()
            monto_base=int(linea[31:39].strip())
            if linea[39:40]=="X":
                complejidad = linea[39]
            else:
                complejidad = "N"
            porcentaje = encontrar_porcentaje(ICD10)
            monto_total=calcular_monto(ICD10,monto_base,montoAL,montoU,montoMZ,porcentaje,complejidad)
            suma_total_general+=monto_total
    if r1 != 0:
        promedio_general=suma_total_general/r1
    else:
        promedio_general=0

    m.seek(0)

    for linea in m:
        if linea[0] == "#":
            montoAL=int(linea[2:8])
            montoMZ=int(linea[8:14])
            montoU=int(linea[14:20])
        else:
            paciente=linea[0:25].strip()
            ICD10=linea[25:31].strip()
            monto_base=int(linea[31:39].strip())
            if linea[39:40]=="X":
                complejidad = linea[39]
            else:
                complejidad = "N"
            porcentaje = encontrar_porcentaje(ICD10)
            monto_total = calcular_monto(ICD10, monto_base, montoAL, montoU, montoMZ, porcentaje, complejidad)
            if ICD10[0] == "A":
                r2 += 1
            elif ICD10[0] == "B":
                r3 += 1
            elif ICD10[0] == "C":
                r4 += 1
            elif ICD10[0] == "E":
                r5 += 1
            elif ICD10[0] == "P":
                r6 += 1

            if ICD10[0] == "S" or ICD10[0] == "T":
                suma_prom+=monto_total
                cont_prom+=1
            if mayor_importe<monto_total and ICD10[0]!="U":
                mayor_importe=monto_total
                paciente_mayor_importe=paciente
            if complejidad=="X":
                cont_alta_complejidad+=1
                if monto_total>promedio_general:
                    cont_alta_complejidad_supera_promedio+=1
    r8=paciente_mayor_importe
    r7=round(suma_prom/cont_prom,2)
    r9=round(mayor_importe,2)
    r10=cont_alta_complejidad_supera_promedio*100//cont_alta_complejidad
    resultados(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10)

def resultados(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10):
    print('(r1) Cantidad de tratamientos cargados:', r1)
    print('(r2) Cantidad de tratamientos "A":', r2)
    print('(r3) Cantidad de tratamientos "B":', r3)
    print('(r4) Cantidad de tratamientos "C":', r4)
    print('(r5) Cantidad de tratamientos "E":', r5)
    print('(r6) Cantidad de tratamientos "P":', r6)
    print('(r7) Importe final promedio (capitulo 19):', r7)
    print('(r8) Paciente (no tipo "U") que pago el mayor importe final:', r8)
    print('(r9) Mayor importe pagado por ese paciente:', r9)
    print('(r10) Porcentaje de tratamientos de alta complejidad con coste mayor al promedio:', r10)

def encontrar_porcentaje(ICD10):
    punto = ICD10.find(".")
    decimal = ICD10[punto + 1:]
    porcentaje = int(decimal)
    return porcentaje

def calcular_monto(ICD10,monto_base,montoAL,montoU,montoMZ,porcentaje,complejidad):
    monto_total=0
    if "A" <= ICD10[0] <= "L":
        monto_total = (monto_base + montoAL) + (monto_base + montoAL) * porcentaje / 100
    elif "M" <= ICD10[0] <= "Z" and ICD10[0] != "U":
        monto_total = (monto_base + montoMZ) + (monto_base + montoMZ) * porcentaje / 100
    elif ICD10[0] == "U":
        monto_total = (monto_base + montoU) + (monto_base + montoU) * porcentaje / 100
    if complejidad == "X":
        monto_total += (monto_total * 0.05)
    return monto_total
def mayor_importe(ICD10,mayor_importe,monto_total,paciente):
    if mayor_importe < monto_total and ICD10[0] != "U":
        mayor_importe = monto_total
        paciente_mayor_importe = paciente
        return mayor_importe,paciente_mayor_importe
principal()