// Configuración de variables de entorno para el frontend

const env = {
  // URL del servidor API (backend)
  API_SERVER_URL: import.meta.env.VITE_API_SERVER_URL || 'http://localhost:8000',
  
  // Configuraciones adicionales
  API_TIMEOUT: import.meta.env.VITE_API_TIMEOUT || 30000,
  
  // Configuración de desarrollo
  isDevelopment: import.meta.env.DEV,
  
  // Versión de la aplicación
  APP_VERSION: import.meta.env.VITE_APP_VERSION || '1.0.0'
};

export default env;