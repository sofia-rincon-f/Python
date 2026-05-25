# ══════════════════════════════════════════════════════
#  FUNCIONES DE PROPAGACIÓN DE RESTRICCIONES
# ══════════════════════════════════════════════════════

def AllDif(VarsDoms, VarsList):
    """
    Técnica: Eliminación por valor único (Arc Consistency).

    Si una variable ya tiene un único valor en su dominio,
    ese valor NO puede aparecer en ninguna otra variable
    del mismo grupo (fila, columna o bloque).

    Ejemplo:
      Si A1 = {5}, entonces 5 se elimina del dominio
      de B1, C1, D1... etc.
    """
    for varSrc in VarsList:
        if len(VarsDoms[varSrc]) == 1:          # Variable ya resuelta
            for varDst in VarsList:
                if varSrc != varDst:             # No se aplica a sí misma
                    VarsDoms[varDst] = VarsDoms[varDst] - VarsDoms[varSrc]


def ExcValue(VarsDoms, VarsList):
    """
    Técnica: Valor exclusivo (Hidden Single).

    Si un valor posible de una variable NO aparece en el
    dominio de ninguna otra variable del grupo, entonces
    ESA variable es la única que puede tomar ese valor,
    y su dominio se reduce a ese único valor.

    Ejemplo:
      Si el 7 solo puede ir en E5 dentro de su bloque,
      entonces E5 = {7}, aunque antes tuviera más opciones.
    """
    for varSrc in VarsList:
        if len(VarsDoms[varSrc]) > 1:           # Solo variables no resueltas
            U = set()
            for varDst in VarsList:
                if varSrc != varDst:
                    if len(VarsDoms[varDst]) > 1:
                        U = U.union(VarsDoms[varDst])  # Unión de otros dominios
            Dif = VarsDoms[varSrc] - U          # Valores exclusivos de varSrc
            if len(Dif) == 1:                   # Si hay exactamente uno
                VarsDoms[varSrc] = Dif           # Lo asignamos


def propagar(VarsDoms, ConstraintsVarsLists):
    """
    Bucle de propagación hasta convergencia.

    Repite AllDif y ExcValue sobre todas las restricciones
    hasta que los dominios no cambien en una pasada completa.
    Esto garantiza que se aprovecha al máximo la información
    antes de recurrir a búsqueda.
    """
    cambio = True
    while cambio:
        anterior = {v: frozenset(d) for v, d in VarsDoms.items()}
        for constraint in ConstraintsVarsLists:
            AllDif(VarsDoms, constraint)
            ExcValue(VarsDoms, constraint)
        # Compara si algo cambió en esta pasada
        cambio = any(
            VarsDoms[v] != anterior[v] for v in VarsDoms
        )

print("Funciones AllDif, ExcValue y propagar definidas correctamente.")
