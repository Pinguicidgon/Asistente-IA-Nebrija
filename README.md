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
```bash
pip install transformers torch pandas
python -m pip install streamlit

```

### 3️⃣ Ejecutar versión consola
```bash
python Asistente_Nebrija.py

```

### 4️⃣ Ejecutar interfaz web (recomendada)
```bash
python -m streamlit run app.py

```
<img width="2946" height="1595" alt="Captura de pantalla 2026-01-06 225618" src="https://github.com/user-attachments/assets/312f1b7c-7f1e-4619-b1f6-83705f99bc21" />


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
