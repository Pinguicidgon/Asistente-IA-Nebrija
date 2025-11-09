# 🧠 Asistente Inteligente Nebrija (IA + PLN)

Proyecto académico desarrollado por **Raúl Cid González** para la **Universidad Nebrija**  
📚 *Grado en Ingeniería Informática – Escuela Politécnica Superior*  
👨‍🏫 Tutor académico: Adrián Pradilla Pórtoles  

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
python asistente_nebrija.py
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
