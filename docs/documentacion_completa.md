# Bienes Raíces con IA
## Documentación Completa

---

# Índice General

1. [README](#readme)
2. [Documentación Técnica](#documentación-técnica)
3. [Guía de Usuario](#guía-de-usuario)

---

# README

## Bienes Raíces con IA

Sistema integral de gestión inmobiliaria potenciado por Inteligencia Artificial, diseñado para revolucionar el sector inmobiliario mediante la implementación de tecnologías avanzadas y automatización inteligente.

### Características Principales

- **Asistente Virtual IA 24/7**
- **Búsqueda Inteligente de Propiedades**
- **Sistema de Gestión de Contenidos**
- **Analytics Avanzados**
- **Panel de Administración Completo**

### Requisitos del Sistema

- Python 3.8+
- MySQL 8.0+
- Node.js 14+

### Dependencias Principales

```
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.2
mysql-connector-python==8.1.0
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.0.0
openai==1.12.0
python-jose==3.3.0
bcrypt==4.0.1
```

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/ai-real-estate.git
cd ai-real-estate
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Inicializar la base de datos:
```bash
python init_db.py
```

6. Ejecutar la aplicación:
```bash
python app.py
```

### Estructura del Proyecto

```
ai-real-estate/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   └── ...
├── routes/
│   ├── main.py
│   ├── auth.py
│   └── api.py
├── models/
│   └── database.py
├── services/
│   └── ai_service.py
└── tests/
    └── test_app.py
```

### Configuración

Crear archivo `.env` con:

```env
SECRET_KEY=your-secret-key
MYSQL_USER=your-db-user
MYSQL_PASSWORD=your-db-password
MYSQL_HOST=localhost
MYSQL_DATABASE=airealestate
NEBIUS_API_KEY=your-api-key
```

### Uso

1. Acceder a http://localhost:5000
2. Registrarse o iniciar sesión
3. Explorar propiedades o gestionar listados

### Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

### Contacto

Email: info@airealestate.com
Website: https://www.airealestate.com

---

[Contenido de documentacion_tecnica.md]

---

[Contenido de guia_usuario.md]
