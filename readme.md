# Prueba técnica AB-Comercial

Este es el repositorio backend de la prueba técnica para AB-Comercial realizado con python y fastapi. 
Aquí se encuentra el paso a paso de como ejecutar el proyecto.

## Contenido

- [Tecnologías](#Tecnologías)
- [Dependencias](#Dependencias)
- [Como ejecutar](#Como-Ejecutar)
- [End Points](#End-Points)


El proyecto está realizado con:

- python 3.11.15 | versión compatible
- Fastpi
- postgreSQL
- Uvicorn

## Dependencias

Las dependencias del proyecto se encuentran ubicadas en "requirements.txt". Cada dependencia contiene su respectiva versión.

## Configuración

Para la configuración del proyecto tenemos la configuración de la base de datos. En este caso se usa postgreSQL.
En el archivo `"db\database.py"` se encuentran los parámetros de configuración deberemos ubicarlos en dicha variable. Los datos encerrados en `**` deben ser reemplazados siguiendo el ejemplo:

``` python
	DATABASE_URL="postgresql://*secretUser*:*scrtpwd1611*@*host*:*port*/*mydb*"
```

Para la configuración de CORS. Entre al archivo `"main.py"` y agregue los orígenes que necesite:


```  python
	origins=["http://localhost",
    "http://localhost:5173",
    "http://localhost:3000/",
	"http://another-host:8080/"]
```

## Como Ejecutar

Clone el repositorio

``` sh
	git clone https://github.com/FatFrogDev/ab-comercial.git
```
Entra al repositorio.
``` sh
	cd ab-comercial
```

>Nota: Debe tener instalado python 3.11.15 o una versión compatible.

Para ejecutar el proyecto, se recomienda primero crear un entorno virtual ejecutando el siguiente comando en una consola CMD:

``` sh
	python -m venv venv
```

Para activar el entorno virtual, ejecute el siguiente comando en la consola:

``` sh
	.\venv\Scripts\activate
```

> Nota: Se recomienda actualizar el instalador pip a la versión 24.2

Instale las dependencias del proyecto:

``` sh
	pip install -r requirements.txt
```

Por último, para correr el proyecto en sí, ejecute el siguiente comando:

```sh
	cd app 
```

```sh
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


Con este comando debe correr el proyecto correctamente. Tenga en cuenta que la bandera --reload hace que el servidor se mantenga en pie constantemente. Sin 
ella, ante un error considerable, el servidor se detiene.


## End-Points

Puede consultar los endpoints de forma sencilla gracias a la implementación de "docs" en fastapi. Para ello busque la ruta(URL) base en la que se ejecuta el proyecto más un "/docs".

---

Hecho con ♥ por [Deyby Ariza](https://github.com/fatfrogdev/)
