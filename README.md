# AgroClima - TechVerde Solutions S.A.

**AgroClima** es un proyecto innovador desarrollado por **TechVerde Solutions S.A.**, una empresa especializada en Nuevas Tecnologías Aplicadas al Agro. Diseñado para Mariano Correa, propietario de un campo de 20 hectáreas llamado "El Corito" en El Simbolar, Departamento Tulumba, Córdoba, Argentina, este proyecto moderniza las operaciones agrícolas en un entorno sin electricidad ni internet. El campo, dividido en un corral para vacas, cultivo de soja, un monte virgen y una casa, depende actualmente de un molino de viento y un tanque australiano para agua. Con la integración de paneles solares y una antena satelital Starlink, la aplicación permite monitoreo y control remoto de niveles de agua, bombeo, energía solar y riego automatizado.

Estructura del proyecto
weather_app/
├── .env
├── requirements.txt
├── main.py
├── models.py
├── database.py
├── templates/
│   ├── index.html
│   ├── weather.html
│   ├── sensor.html
│   ├── charts.html
├── static/
│   ├── css/
│   │   ├── styles.css
│   ├── js/
│   │   ├── chart.js

## Funcionalidades Actuales
- **Monitoreo Climático**: Registro en tiempo real de temperatura y humedad con el sensor DHT11 (vía ESP32), almacenado en una base de datos MySQL.
- **Integración con OpenWeatherMap**: Obtención de datos climáticos (temperatura, humedad, presión, viento) para cualquier ciudad, con datos históricos.
- **Visualización de Datos**: Gráficos y tablas comparativas de temperatura y humedad entre el sensor DHT11 y OpenWeatherMap.
- **Interfaz Web**: Formulario responsivo para consultar el clima, con diseño moderno y accesible desde cualquier navegador.

## Próximas Mejoras
- **Seguimiento del Campo**: Monitoreo de niveles de agua, control de bombeo, gestión de energía solar y riego automatizado.
- **Nuevos Sensores**: 
  - Sensor LDR para detectar baja luz ambiental.
  - Ventilador automático en el depósito de fertilizantes/herramientas (activado por temperatura alta).
  - Higrómetro de suelo para optimizar el riego en la huerta.
- **Conectividad y Control**: Integración con Starlink para datos en tiempo real y panel de control remoto.
- **Alertas y Reportes**: Notificaciones push para condiciones críticas y informes periódicos.

## Instalación
1. Clona el repositorio: `git clone https://github.com/fabi-57-ana/weather_app.git`
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno: 
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instala dependencias: `pip install -r requirements.txt`
5. Configura las variables de entorno en un archivo `.env`.
   -OPENWEATHER_API_KEY=tu_clave_api
   -DB_HOST=localhost
   -DB_USER=root
   -DB_PASSWORD=tu_contraseña
   -DB_NAME=agroclima

6. Instala MySQL y crea una base de datos:CREATE DATABASE agroclima;

7. Inicia el servidor: `python main.py`

## Uso
- Accede a `http://192.168.0.227:8000` desde un navegador.
- Usa el formulario para consultar el clima de cualquier ciudad.
- Revisa los datos del sensor en `/sensor/last` y los gráficos en `/charts`.

## Tecnologías Utilizadas
- **Backend**: FastAPI, Uvicorn
- **Base de Datos**: MySQL
- **Sensores**: DHT11 (vía ESP32)
- **API**: OpenWeatherMap
- **Frontend**: HTML, CSS, Chart.js

## Contribución
¡Colaboraciones y sugerencias son bienvenidas! Contacta al equipo de TechVerde Solutions S.A. para unirte al desarrollo.

## Estado del Proyecto
- **Estado**: En desarrollo activo con planes de expansión.



