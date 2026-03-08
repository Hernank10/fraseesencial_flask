import json
import random

temas = ['académico', 'profesional', 'cotidiano', 'científico', 'literario', 'periodístico']
verbos = ['explica', 'desarrolla', 'presenta', 'analiza', 'describe', 'propone', 'investiga', 'publica', 'escribe', 'estudia']
sujetos = ['El profesor', 'La empresa', 'El investigador', 'El equipo', 'La organización', 'El autor', 'El científico']
objetos = ['un estudio', 'un informe', 'una propuesta', 'un análisis', 'una investigación', 'un artículo']
complementos = ['a los estudiantes', 'para los clientes', 'a la comunidad', 'al público', 'a los lectores']

ejercicios = []

for i in range(1, 101):
    dificultad = random.choices(['fácil', 'medio', 'difícil'], weights=[50, 30, 20])[0]
    tema = random.choice(temas)
    
    # Estructura básica
    quien = random.choice(sujetos)
    verbo = random.choice(verbos)
    que = random.choice(objetos)
    a_quien = random.choice(complementos)
    
    elementos = [
        f"QUIÉN: {quien}",
        f"VERBO: {verbo}",
        f"QUÉ: {que}",
        f"A QUIÉN: {a_quien}"
    ]
    
    orden_correcto = ["QUIÉN", "VERBO", "QUÉ", "A QUIÉN"]
    
    if dificultad == 'difícil':
        # Añadir complementos accidentales
        elementos.append("DÓNDE: en el laboratorio")
        elementos.append("CUÁNDO: el año pasado")
        orden_correcto.extend(["DÓNDE", "CUÁNDO"])
    
    ejercicio = {
        "id": i,
        "tipo": "esencial" if dificultad != 'difícil' else "accidental",
        "dificultad": dificultad,
        "tema": tema,
        "frase_completa": f"{quien} {verbo} {que} {a_quien}.",
        "elementos": elementos,
        "orden_correcto": orden_correcto,
        "explicacion": f"Ejercicio de práctica nivel {dificultad} sobre tema {tema}.",
        "pista": "Recuerda: primero el sujeto, luego el verbo, después el objeto directo."
    }
    ejercicios.append(ejercicio)

# Guardar archivo
with open('app/static/data/ejercicios.json', 'w', encoding='utf-8') as f:
    json.dump(ejercicios, f, ensure_ascii=False, indent=2)

print(f"✅ Generados {len(ejercicios)} ejercicios")
