

---

## 🎯 Objetivo del proyecto

Este proyecto forma parte de la investigación titulada  
**“Uso de la Inteligencia Artificial para la resolución de incidencias en Nebrija”**.  

Su finalidad es demostrar cómo un modelo de **Procesamiento del Lenguaje Natural (PLN)** puede analizar y clasificar incidencias escritas en lenguaje natural por parte de estudiantes o personal técnico, ayudando a **optimizar la atención y gestión de soporte universitario**.

---

## ⚙️ Tecnologías utilizadas

- **Python 3.11**
- Librería [`transformers`](https://huggingface.co/docs/transformers) (modelo preentrenado `facebook/bart-large-mnli`)
- Motor de IA: [`torch`](https://pytorch.org/)
- Editor: Visual Studio Code
- Sistema operativo: Windows 11

---

## 🚀 Cómo ejecutar el asistente

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Pinguicidgon/Asistente-IA-Nebrija.git
cd Asistente-IA-Nebrija
```


### 2️⃣ Instalar dependencias

Instala las librerías necesarias ejecutando el siguiente comando:
```bash
pip install transformers torch
```
### 3️⃣ Ejecutar el programa

Una vez instaladas las dependencias, ejecuta el asistente con:
```bash
python Asistente_Nebrija.py
```
### 4️⃣ Introducir una incidencia

Cuando el programa se ejecute, te pedirá escribir una incidencia como si fueras un estudiante o usuario:

Introduce tu incidencia: No puedo acceder a Teams ni a Blackboard.


El modelo clasificará automáticamente la incidencia en la categoría más probable, por ejemplo:

🔍 Clasificación automática:
Categoría más probable: problema de acceso

### 5️⃣ Finalizar la ejecución

Cuando termines de probar el asistente, puedes cerrar el programa presionando Ctrl + C o simplemente cerrando la terminal.

## 💡 Nota importante:
Si es la primera vez que ejecutas el asistente, el modelo de lenguaje facebook/bart-large-mnli se descargará automáticamente desde la librería transformers.
Este proceso puede tardar unos minutos, pero solo ocurre la primera vez.
Después de eso, el programa funcionará de forma más rápida en tu equipo.

---

### 🧩 Descripción del funcionamiento

El asistente analiza el texto introducido por el usuario utilizando un modelo de **clasificación semántica de lenguaje natural (Zero-Shot Classification)**.  
A partir de una lista de categorías predefinidas, el modelo predice el tipo de incidencia más probable.

**Categorías posibles:**
- Problema de acceso  
- Error de matrícula  
- Cuenta bloqueada  
- Problema técnico  
- Consulta administrativa  
- Otro tipo de incidencia  

---

## 👨‍💻 Autor

**Raúl Cid González**  
📧 rcidg@alumnos.nebrija.es  
📍 Universidad Nebrija, Madrid, España  

---

## 🏁 Licencia

Este repositorio se distribuye bajo la licencia académica de uso no comercial.  
Se permite su consulta y reutilización con fines educativos citando al autor y la Universidad Nebrija.

---

# © 2025 Raúl Cid González — Universidad Nebrija

---











🧠 Asistente Inteligente Nebrija
Prototipo experimental para el análisis de incidencias mediante IA

Proyecto académico desarrollado por Raúl Cid González para la Universidad Nebrija
📚 Grado en Ingeniería Informática – Escuela Politécnica Superior
👨‍🏫 Tutor académico: Adrián Pradilla Pórtoles

🎯 Objetivo del proyecto

Este repositorio recoge el prototipo experimental desarrollado como apoyo práctico
al trabajo de investigación titulado:

“Uso de la Inteligencia Artificial para la resolución de incidencias en la Universidad Nebrija”.

El objetivo del prototipo no es desarrollar una aplicación final, sino demostrar, mediante un caso práctico, cómo las técnicas de Procesamiento del Lenguaje Natural (PLN) pueden aplicarse al análisis y clasificación de incidencias universitarias escritas en lenguaje natural.

El sistema se utiliza como herramienta de apoyo a la investigación, permitiendo:

Evaluar la capacidad de modelos preentrenados para clasificar incidencias

Analizar su comportamiento sin entrenamiento adicional

Explorar su posible utilidad en entornos universitarios

💬 Contexto académico

Este proyecto se desarrolla en el marco de la asignatura
Evaluación del Desarrollo de Capacidades en la Empresa I,
como parte del trabajo de investigación aplicado presentado en la memoria académica.

El prototipo tiene un carácter exploratorio, y su finalidad es servir como
soporte práctico a las conclusiones teóricas del trabajo, no como un sistema final listo para su implantación real.

⚙️ Tecnologías utilizadas

Python 3.11

Hugging Face – transformers

Modelo preentrenado: facebook/bart-large-mnli

Enfoque: Zero-Shot Classification

PyTorch (torch) como motor de inferencia

Pandas para evaluación experimental con datasets

Streamlit, utilizado como interfaz experimental de visualización

Visual Studio Code

Sistema operativo: Windows 11

🧠 Modelo de IA

El asistente emplea un modelo de clasificación semántica Zero-Shot, capaz de asignar una incidencia a una categoría sin necesidad de entrenamiento específico sobre datos propios.

El modelo se emplea exclusivamente con fines de investigación y demostración técnica,
sin realizar procesos de entrenamiento, ajuste fino (fine-tuning) ni despliegue en producción.

🧩 Capacidades del prototipo experimental

Las siguientes capacidades se implementan como apoyo al análisis experimental del comportamiento del modelo:

Clasificación automática de incidencias en categorías predefinidas

Estimación de prioridad a partir de reglas lingüísticas

Gestión de preguntas frecuentes (FAQ) con enlaces informativos

Registro de conversaciones y feedback del usuario

Evaluación experimental mediante datasets en formato CSV

Interfaz visual para simulación de uso real por parte de estudiantes

🧪 Evaluación del modelo

El prototipo incluye un módulo de evaluación que permite comparar las predicciones del modelo con un conjunto de incidencias simuladas almacenadas en un archivo incidencias.csv.

Los resultados obtenidos no pretenden ser concluyentes, sino orientativos, y se utilizan para apoyar la reflexión académica sobre las ventajas y limitaciones del uso de IA en la gestión de incidencias universitarias.

🚀 Cómo ejecutar el asistente
1️⃣ Clonar el repositorio
git clone https://github.com/Pinguicidgon/Asistente-IA-Nebrija.git
cd Asistente-IA-Nebrija

2️⃣ Instalar dependencias
pip install transformers torch pandas streamlit

3️⃣ Ejecutar versión consola
python Asistente_Nebrija.py

4️⃣ Ejecutar interfaz web (opcional)
streamlit run app.py


📌 Nota: la primera ejecución descargará automáticamente el modelo desde Hugging Face.
Este proceso puede tardar unos minutos y solo ocurre la primera vez.

🧩 Descripción del funcionamiento

El asistente analiza el texto introducido por el usuario utilizando técnicas de Procesamiento del Lenguaje Natural y clasifica la consulta en una de las siguientes categorías:

Problema de acceso

Error de matrícula

Cuenta bloqueada

Problema técnico

Consulta administrativa

Otro tipo de incidencia

Además, el sistema permite recoger feedback del usuario (Sí / No) sobre la utilidad de la respuesta, lo que facilita un análisis posterior del éxito percibido del asistente.

👨‍💻 Autor

Raúl Cid González
📧 rcidg@alumnos.nebrija.es

📍 Universidad Nebrija, Madrid, España

🏁 Licencia

Este repositorio se distribuye bajo una licencia académica de uso no comercial.
Se permite su consulta y reutilización con fines educativos citando al autor y a la Universidad Nebrija.

📸 Demostración
<img width="880" height="341" alt="Demostración del asistente" src="https://github.com/user-attachments/assets/8099f58c-04a2-49a3-8667-564c5d352695" />
© 2025 Raúl Cid González — Universidad Nebrija



🌐 **Repositorio oficial:** [https://github.com/Pinguicidgon/Asistente-IA-Nebrija](https://github.com/Pinguicidgon/Asistente-IA-Nebrija)

# Demostración
<img width="880" height="341" alt="Captura de pantalla 2025-11-09 200835" src="https://github.com/user-attachments/assets/8099f58c-04a2-49a3-8667-564c5d352695" />










# 🧠 Asistente Inteligente Nebrija
**Prototipo experimental para el análisis de incidencias mediante Inteligencia Artificial**

Proyecto académico desarrollado por **Raúl Cid González** para la **Universidad Nebrija**  
📚 Grado en Ingeniería Informática – Escuela Politécnica Superior  
👨‍🏫 Tutor académico: Adrián Pradilla Pórtoles

---

## 🎯 Objetivo del proyecto

Este repositorio contiene el **prototipo experimental** desarrollado como apoyo práctico al trabajo de investigación titulado:

> **“Uso de la Inteligencia Artificial para la resolución de incidencias en la Universidad Nebrija”**

El objetivo del proyecto **no es desarrollar una aplicación final**, sino **demostrar mediante un caso práctico** cómo las técnicas de **Procesamiento del Lenguaje Natural (PLN)** pueden aplicarse al análisis y clasificación de incidencias universitarias redactadas en lenguaje natural.

El sistema se utiliza como **herramienta de apoyo a la investigación**, permitiendo:

- Evaluar la capacidad de modelos preentrenados para clasificar incidencias  
- Analizar su comportamiento sin entrenamiento adicional  
- Explorar su posible utilidad en entornos universitarios  

---

## 💬 Contexto académico

Este proyecto se desarrolla en el marco de la asignatura:

**Evaluación del Desarrollo de Capacidades en la Empresa I**

Forma parte del **trabajo de investigación aplicado** presentado en la memoria académica del grado.

El prototipo tiene un **carácter exploratorio**, y su finalidad es servir como **soporte práctico a las conclusiones teóricas**, no como un sistema listo para su implantación real.

---

## ⚙️ Tecnologías utilizadas

- Python 3.11  
- Hugging Face – transformers  
- Modelo preentrenado: `facebook/bart-large-mnli`  
- Enfoque: Zero-Shot Classification  
- PyTorch (torch) como motor de inferencia  
- Pandas para evaluación experimental con datasets  
- Streamlit como interfaz experimental de visualización  
- Visual Studio Code  
- Sistema operativo: Windows 11  

---

## 🧠 Modelo de IA

El asistente emplea un **modelo de clasificación semántica Zero-Shot**, capaz de asignar una incidencia a una categoría **sin necesidad de entrenamiento específico** sobre datos propios.

El modelo se utiliza **exclusivamente con fines de investigación y demostración técnica**, sin realizar procesos de:

- Entrenamiento  
- Ajuste fino (*fine-tuning*)  
- Despliegue en producción  

---

## 🧩 Capacidades del prototipo experimental

Las siguientes funcionalidades se implementan como **apoyo al análisis experimental** del comportamiento del modelo:

- Clasificación automática de incidencias en categorías predefinidas  
- Estimación de prioridad a partir de reglas lingüísticas  
- Gestión de preguntas frecuentes (FAQ) con enlaces informativos  
- Registro de conversaciones y feedback del usuario  
- Evaluación experimental mediante datasets en formato CSV  
- Interfaz visual para simulación de uso real por parte de estudiantes  

---

## 🧪 Evaluación del modelo

El prototipo incluye un módulo de evaluación que permite comparar las predicciones del modelo con un conjunto de incidencias simuladas almacenadas en el archivo:


Los resultados obtenidos **no pretenden ser concluyentes**, sino **orientativos**, y se utilizan para apoyar la reflexión académica sobre las **ventajas y limitaciones del uso de IA** en la gestión de incidencias universitarias.

---

## 🚀 Cómo ejecutar el asistente

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Pinguicidgon/Asistente-IA-Nebrija.git
cd Asistente-IA-Nebrija
```
### 2️⃣ Instalar dependencias
pip install transformers torch pandas streamlit

### 3️⃣ Ejecutar versión consola
python Asistente_Nebrija.py

### 4️⃣ Ejecutar interfaz web (opcional)
streamlit run app.py

📌 Nota: La primera ejecución descargará automáticamente el modelo desde Hugging Face.
Este proceso puede tardar unos minutos y solo ocurre la primera vez.

---

## 🧩 Descripción del funcionamiento

El asistente analiza el texto introducido por el usuario mediante técnicas de PLN y clasifica la consulta en una de las siguientes categorías:

Problema de acceso

Error de matrícula

Cuenta bloqueada

Problema técnico

Consulta administrativa

Otro tipo de incidencia

Además, el sistema permite recoger feedback del usuario (Sí / No) sobre la utilidad de la respuesta, facilitando un análisis posterior del éxito percibido del asistente.

---

## 👨‍💻 Autor

**Raúl Cid González**  
📧 rcidg@alumnos.nebrija.es  
📍 Universidad Nebrija, Madrid, España  

---

## 🏁 Licencia

Este repositorio se distribuye bajo la licencia académica de uso no comercial.  
Se permite su consulta y reutilización con fines educativos citando al autor y la Universidad Nebrija.

---

# © 2025 Raúl Cid González — Universidad Nebrija

---
