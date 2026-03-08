#!/usr/bin/env python3
"""
Script de inicialización de base de datos para Fraseesencial
"""
import sys
import os
import json

# Asegurar que podemos importar desde el directorio actual
sys.path.insert(0, os.getcwd())

print("🔄 Inicializando sistema Fraseesencial...")

try:
    # Importar la función create_app directamente
    from app import create_app, db
    from app.models.user import User
    from app.models.progress import Progress
    from app.models.example import Example
    from app.models.writing import Writing
    from app.models.exercise_progress import ExerciseProgress
    
    # Crear la aplicación
    app = create_app()
    
    with app.app_context():
        print("📊 Conectando a base de datos...")
        
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas/verificadas")
        
        # Crear usuario de prueba
        if not User.query.filter_by(username='test').first():
            user = User(username='test', email='test@test.com')
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()
            print("✅ Usuario test creado (test/test123)")
            
            # Crear progreso
            progress = Progress(user_id=user.id)
            db.session.add(progress)
            db.session.commit()
            print("✅ Progreso inicial creado")
        else:
            print("✅ Usuario test ya existe")
        
        # Crear ejercicios si no existen
        json_path = os.path.join('app', 'static', 'data', 'ejercicios.json')
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        
        if not os.path.exists(json_path):
            ejercicios = [
                {
                    "id": 1,
                    "tipo": "esencial",
                    "dificultad": "fácil",
                    "tema": "académico",
                    "frase_completa": "El profesor explica la lección a los estudiantes.",
                    "elementos": [
                        "QUIÉN: El profesor",
                        "VERBO: explica",
                        "QUÉ: la lección",
                        "A QUIÉN: a los estudiantes"
                    ],
                    "orden_correcto": ["QUIÉN", "VERBO", "QUÉ", "A QUIÉN"],
                    "explicacion": "Estructura básica de una oración.",
                    "pista": "Primero identifica quién realiza la acción."
                },
                {
                    "id": 2,
                    "tipo": "esencial",
                    "dificultad": "fácil",
                    "tema": "cotidiano",
                    "frase_completa": "María compró flores para su madre.",
                    "elementos": [
                        "QUIÉN: María",
                        "VERBO: compró",
                        "QUÉ: flores",
                        "PARA QUIÉN: para su madre"
                    ],
                    "orden_correcto": ["QUIÉN", "VERBO", "QUÉ", "PARA QUIÉN"],
                    "explicacion": "El complemento indirecto indica el destinatario.",
                    "pista": "¿Quién compró algo y para quién?"
                }
            ]
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(ejercicios, f, ensure_ascii=False, indent=2)
            print(f"✅ Archivo de ejercicios creado con {len(ejercicios)} ejercicios")
        else:
            with open(json_path, 'r', encoding='utf-8') as f:
                ejercicios = json.load(f)
            print(f"✅ Archivo de ejercicios existe: {len(ejercicios)} ejercicios")
        
        # Mostrar resumen
        print("\n📊 RESUMEN:")
        print(f"   Usuarios: {User.query.count()}")
        print(f"   Progresos: {Progress.query.count()}")
        print(f"   Ejemplos: {Example.query.count()}")
        print(f"   Redacciones: {Writing.query.count()}")
        print(f"   Progreso ejercicios: {ExerciseProgress.query.count()}")
        
        print("\n🎉 ¡Base de datos inicializada correctamente!")
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("\n💡 Verifica que:")
    print("   1. Estás en el directorio correcto")
    print("   2. Los archivos existen en app/models/")
    print("   3. Ejecuta: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    sys.exit(1)
