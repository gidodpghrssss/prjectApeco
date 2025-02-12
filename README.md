# AI Real Estate Platform

An intelligent real estate platform powered by AI, featuring property listings, user preferences, and an AI chat assistant.

## Features

- User authentication and authorization
- Property listing and management
- AI-powered chat assistant for property inquiries
- Blog system with AI-generated content
- User preference tracking and analysis
- Admin dashboard for property and user management

## Prerequisites

- Python 3.8+
- MySQL
- Nebius API key

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd ai-real-estate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
SECRET_KEY=your-secret-key
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
MYSQL_HOST=localhost
MYSQL_DATABASE=ai_real_estate
NEBIUS_API_KEY=your-nebius-api-key
```

5. Initialize the database:
```bash
python init_db.py
```

## Running the Application

1. Start the development server:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

## Testing

Run the test suite:
```bash
python -m unittest test_app.py
```

## Project Structure

- `/admin` - Admin interface routes and views
- `/api` - API endpoints
- `/models` - Database models
- `/routes` - Application routes
- `/services` - Business logic and AI services
- `/static` - Static files (CSS, JS, images)
- `/templates` - HTML templates

---

# User Guide (English)

## Getting Started

1. **Registration and Login**
   - Click "Register" in the navigation bar
   - Fill in your details and create an account
   - Login with your email and password

2. **Property Search**
   - Use the search bar to find properties
   - Apply filters for price, location, and property type
   - Click on properties to view details
   - Save properties to your favorites

3. **AI Assistant**
   - Click the chat bubble in the bottom right
   - Ask questions about properties
   - Get personalized recommendations
   - Inquire about market trends

4. **Blog and News**
   - Browse the latest real estate news
   - Read AI-generated market analysis
   - Filter articles by topic
   - Share interesting posts

5. **User Profile**
   - Update your preferences
   - View saved properties
   - Track your inquiries
   - Manage notifications

---

# Guía del Usuario (Español)

## Comenzando

1. **Registro e Inicio de Sesión**
   - Haga clic en "Registrarse" en la barra de navegación
   - Complete sus datos y cree una cuenta
   - Inicie sesión con su correo electrónico y contraseña

2. **Búsqueda de Propiedades**
   - Use la barra de búsqueda para encontrar propiedades
   - Aplique filtros de precio, ubicación y tipo de propiedad
   - Haga clic en las propiedades para ver detalles
   - Guarde propiedades en favoritos

3. **Asistente de IA**
   - Haga clic en el botón de chat en la esquina inferior derecha
   - Haga preguntas sobre propiedades
   - Obtenga recomendaciones personalizadas
   - Consulte sobre tendencias del mercado

4. **Blog y Noticias**
   - Explore las últimas noticias inmobiliarias
   - Lea análisis de mercado generados por IA
   - Filtre artículos por tema
   - Comparta publicaciones interesantes

5. **Perfil de Usuario**
   - Actualice sus preferencias
   - Vea propiedades guardadas
   - Realice seguimiento de sus consultas
   - Administre notificaciones

---

# Guide d'Utilisation (Français)

## Pour Commencer

1. **Inscription et Connexion**
   - Cliquez sur "S'inscrire" dans la barre de navigation
   - Remplissez vos informations et créez un compte
   - Connectez-vous avec votre email et mot de passe

2. **Recherche de Propriétés**
   - Utilisez la barre de recherche pour trouver des propriétés
   - Appliquez des filtres de prix, lieu et type de propriété
   - Cliquez sur les propriétés pour voir les détails
   - Sauvegardez vos propriétés favorites

3. **Assistant IA**
   - Cliquez sur la bulle de chat en bas à droite
   - Posez des questions sur les propriétés
   - Obtenez des recommandations personnalisées
   - Renseignez-vous sur les tendances du marché

4. **Blog et Actualités**
   - Parcourez les dernières actualités immobilières
   - Lisez les analyses de marché générées par l'IA
   - Filtrez les articles par thème
   - Partagez les publications intéressantes

5. **Profil Utilisateur**
   - Mettez à jour vos préférences
   - Consultez vos propriétés sauvegardées
   - Suivez vos demandes
   - Gérez vos notifications

---

## API Endpoints

- `/api/properties` - Property management
- `/api/chat` - AI chat interface
- `/api/blog` - Blog management
- `/api/user` - User preference management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
