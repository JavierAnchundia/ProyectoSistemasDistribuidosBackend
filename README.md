# MapaVirtual Backend
Pasos a seguir:

# Crear en mysql el schema para la base de datos
```bash
CREATE SCHEMA `MapaVirtual`;
```

# Instalar requerimientos en sus entornos
Usar el siguiente comando sobre la carpeta raíz -> proyecto ServidorMapaVirtual
```bash
pip install -r requirements.txt
```

# Generar archivo requirements.txt
Usar el siguiente comando sobre la carpeta raíz -> proyecto ServidorMapaVirtual para generar archivo
```bash
pip freeze > requirements.txt
```

# Migrar el modelo creado en Django a la base de datos Mysql
Seguir los siguientes comandos, el 0001 es un ejemplo y dependera del valor que salga con el comando makemigrations.
```bash
python manage.py makemigrations
python manage.py sqlmigrate serviciosBackend 0001
python manage.py migrate serviciosBackend
python manage.py migrate admin
python manage.py migrate sessions
python manage.py migrate
```
# Crear el admin el django
Se realiza con el siguiente comando
```bash
python manage.py createsuperuser
```

# Correr django con la ip del equipo
Se realiza con el siguiente comando
```bash
python manage.py runserver ip:8100
```