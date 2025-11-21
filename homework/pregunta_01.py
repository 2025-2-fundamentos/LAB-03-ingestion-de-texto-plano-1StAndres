"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd
    import re

    path = 'files/input/clusters_report.txt'

    with open(path, encoding='utf-8') as fh:
      lines = fh.readlines()

    # localizar inicio de datos (linea de guiones)
    start = 0
    for idx, ln in enumerate(lines):
      if ln.strip() and set(ln.strip()) == set('-'):
        start = idx + 1
        break

    pattern = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$")

    records = []
    i = start
    while i < len(lines):
      line = lines[i].rstrip('\n')
      if not line.strip():
        i += 1
        continue

      m = pattern.match(line)
      if not m:
        i += 1
        continue

      cluster = int(m.group(1))
      cantidad = int(m.group(2))
      porcentaje = float(m.group(3).replace(',', '.'))
      principales = m.group(4).strip()

      # capturar líneas de continuación hasta la siguiente entrada o línea en blanco
      j = i + 1
      while j < len(lines):
        nxt = lines[j].rstrip('\n')
        if not nxt.strip():
          j += 1
          break
        if pattern.match(nxt):
          break
        principales += ' ' + nxt.strip()
        j += 1

      # Normalizaciones: colapsar espacios, remover punto final, normalizar comas
      principales = re.sub(r"\s+", ' ', principales).strip()
      if principales.endswith('.'):
        principales = principales[:-1]
      principales = re.sub(r"\s*,\s*", ', ', principales)

      records.append(
        {
          'cluster': cluster,
          'cantidad_de_palabras_clave': cantidad,
          'porcentaje_de_palabras_clave': porcentaje,
          'principales_palabras_clave': principales,
        }
      )

      i = j

    df = pd.DataFrame(records)
    df = df.sort_values('cluster').reset_index(drop=True)

    # asegurar nombres de columnas en minusculas y con guiones bajos (ya están)
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    return df
