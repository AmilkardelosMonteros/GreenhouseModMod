MODELO_FOTOSINTESIS = {'Surrogate':    False,
                      'Simplificado': False,
                      'EstomataVar':  True
                    }

if sum(MODELO_FOTOSINTESIS.values()) != 1:
    raise SystemExit('Revisa tus parametros de Fotosisntesis, Adios')
