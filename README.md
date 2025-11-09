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

## 💬 Contexto académico

Este proyecto forma parte del **capítulo 6 (Proyecto)** de la memoria presentada en la asignatura *Evaluación de Capacidades en la Empresa I*.  
Corresponde a la parte práctica del trabajo de investigación sobre la aplicación de IA en la **gestión de incidencias universitarias**.  

El prototipo se desarrolló con un enfoque **de investigación aplicada**, y su propósito es servir como **demostración conceptual** de la viabilidad técnica del uso de IA y PLN en instituciones académicas.

---

## 📚 Referencias principales

- UNESCO. (2021). *AI and Education: Guidance for Policy-Makers.*  
  [https://unesdoc.unesco.org/ark:/48223/pf0000376709](https://unesdoc.unesco.org/ark:/48223/pf0000376709)  

- OECD. (2020). *Trustworthy artificial intelligence (AI) in education.*  
  [[https://www.oecd.org/education/opportunities-guidelines-and-guardrails-for-effective-and-equitable-use-of-ai-in-education.pdf](https://www.oecd.org/education/opportunities-guidelines-and-guardrails-for-effective-and-equitable-use-of-ai-in-education.pdf](https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/04/trustworthy-artificial-intelligence-ai-in-education_f1a7c415/a6c90fa9-en.pdf))

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

🌐 **Repositorio oficial:** [https://github.com/Pinguicidgon/Asistente-IA-Nebrija](https://github.com/Pinguicidgon/Asistente-IA-Nebrija)
