import hashlib
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ENTRADA = BASE / "datos" / "telemetria_envios.csv"
SALIDA = BASE / "datos" / "telemetria_limpia.csv"

ESTADOS_VALIDOS = {"ENTREGADO", "EN_TRANSITO", "EN_REPARTO", "INCIDENCIA_REPARTO"}
CLAVE_NULOS = ["destino", "peso_kg", "temp_celsius"]

def sha256_fichero(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            h.update(bloque)
    return h.hexdigest()

def main():
    print(f"SHA-256 ORIGINAL: {sha256_fichero(ENTRADA)}")
    df = pd.read_csv(ENTRADA, encoding="utf-8")
    n0 = len(df); print(f"Filas iniciales: {n0}")

    df = df.drop_duplicates();                         n1 = len(df); print(f"- Duplicados eliminados: {n0-n1}")
    df = df.dropna(subset=CLAVE_NULOS);                n2 = len(df); print(f"- Filas con nulos eliminadas: {n1-n2}")
    df = df[df["peso_kg"] > 0];                        n3 = len(df); print(f"- Pesos no positivos eliminados: {n2-n3}")
    df = df[df["temp_celsius"].between(-30, 30)];      n4 = len(df); print(f"- Temperaturas fuera de rango: {n3-n4}")
    df = df[df["estado_envio"].isin(ESTADOS_VALIDOS)]; n5 = len(df); print(f"- Estados no catalogados: {n4-n5}")

    df.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"Filas finales: {n5}")
    print(f"SHA-256 LIMPIO:   {sha256_fichero(SALIDA)}")

if __name__ == "__main__":
    main()