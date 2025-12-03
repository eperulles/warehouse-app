# 📱 Guía Paso a Paso: Crear APK con GitHub

Esta es la forma **más segura y exitosa** de crear tu aplicación Android. Usaremos los servidores de GitHub para construir el APK, evitando todos los errores de tu computadora.

## Paso 1: Crear Cuenta en GitHub (Gratis)

1. Ve a [github.com/signup](https://github.com/signup)
2. Ingresa tu correo, crea una contraseña y un nombre de usuario.
3. Resuelve el captcha y verifica tu correo electrónico.
4. **¡Listo!** Ya tienes cuenta.

## Paso 2: Instalar Git (Si no lo tienes)

1. Descarga Git aquí: [git-scm.com/download/win](https://git-scm.com/download/win)
2. Descarga la versión **"64-bit Git for Windows Setup"**.
3. Instálalo dando "Next" a todo (la configuración por defecto está bien).
4. Al finalizar, abre una nueva terminal (PowerShell) y escribe `git --version` para verificar.

## Paso 3: Crear tu Repositorio

1. Ve a [github.com/new](https://github.com/new) (estando logueado).
2. En **"Repository name"** escribe: `warehouse-app`
3. Asegúrate que esté seleccionado **"Public"** (es más fácil) o "Private" (si prefieres privacidad).
4. **NO** marques ninguna otra casilla (ni README, ni .gitignore).
5. Dale al botón verde **"Create repository"**.

## Paso 4: Subir tu Código

Abre **PowerShell** en la carpeta de tu proyecto (`warehouse_flet_app`) y ejecuta estos comandos uno por uno:

```powershell
# 1. Inicializar Git
git init

# 2. Configurar tu usuario (cambia los datos por los tuyos)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# 3. Preparar los archivos
git add .

# 4. Guardar los cambios
git commit -m "Primera versión de la app"

# 5. Conectar con GitHub (¡IMPORTANTE!)
# Copia el comando que te dio GitHub en la página del repositorio.
# Se verá algo así (REEMPLAZA CON TU URL):
git remote add origin https://github.com/TU_USUARIO/warehouse-app.git

# 6. Subir el código
git branch -M main
git push -u origin main
```

*Nota: Al hacer el último paso, te pedirá iniciar sesión. Usa la opción "Sign in with your browser" si aparece.*

## Paso 5: Descargar tu APK 🎉

Una vez que el código suba:

1. Ve a la página de tu repositorio en GitHub.
2. Haz clic en la pestaña **"Actions"** (arriba, al centro).
3. Verás un proceso llamado **"Build APK"** con un círculo amarillo (en progreso) o verde (terminado).
4. Haz clic en **"Build APK"**.
5. Espera a que termine (3-5 minutos).
6. Cuando termine (círculo verde ✅), baja hasta la sección **"Artifacts"**.
7. Haz clic en **"warehouse-app-release"**.
8. Se descargará un archivo `.zip`. **Descomprímelo y ahí estará tu APK.**

¡Instálalo en tu celular y listo! 🚀
