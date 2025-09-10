# Simulación y Modelación – Generadores y Pruebas de Números Pseudoaleatorios

Proyecto en **Python 3.10+** con GUI (estilo oscuro minimalista “cyberpunk serio”) desarrollada en **tkinter**.  
Permite generar secuencias pseudoaleatorias con **algoritmos clásicos**, visualizar los **pasos de generación**, y aplicar **pruebas estadísticas** de uniformidad.  
> Este trabajo fue realizado por *David Ronald Calle Blanco* con la ayuda de **ChatGPT (asistente de OpenAI)**.

---

## 🎯 Funcionalidades

- **Generadores** (con trazado paso a paso en la tabla):
  - **Cuadrados Medios (Mid-Square)**  
    \(Y_i=X_i^2\), tomar **D** dígitos centrales → \(X_{i+1}\), \(r_i=0.\text{(D dígitos)}\).
  - **Productos Medios (Middle Product)**  
    Parte de \(X_0,X_1\). \(Y_i=X_i\cdot X_{i+1}\), tomar D centrales → \(X_{i+2}\).
  - **Multiplicador Constante**  
    Fija una constante \(a\) de **D** dígitos. \(Y_i=a\cdot X_i\), tomar D centrales → \(X_{i+1}\).

  > **Regla de centrado:** no se rellena a \(2D\). Solo si \(|Y_i|\) tiene **longitud impar**, se antepone un **0** y luego se extraen los **D** dígitos centrales.

- **Pruebas estadísticas** (usan \(\alpha\) desde la pestaña **Variables**):
  - **Medias Z (Uniforme[0,1])**: \(Z=\sqrt{12n}(\bar u-0.5)\), bilateral (p-value).
  - **Varianza \(\chi^2\) (Uniforme[0,1])**: \(Q=\frac{(n-1)S^2}{1/12}\), bilateral + intervalo para \(S^2\) y p-value.
  - **Uniformidad \(\chi^2\) (Uniforme[0,1])**: con **m** clases; crítico derecho \(\chi^2_{1-\alpha,\,m-1}\) y p-value, tabla por intervalos.

- **Interfaz**:
  - Pestañas **Generadores**, **Pruebas**, **Variables**.
  - Campos: \(n\), semillas (y **semilla 2**/**constante a** cuando aplica).
  - **Tabla** con los pasos \(Y\), \(X\) siguiente y \(r\) por iteración.
  - **Histograma**; **Exportar CSV** (secuencia) y **Guardar PNG** (gráfico).
  - Micro-animaciones sobrias (barra de escaneo y toasts).

---

## 🧭 Pestaña **Variables** (¿para qué sirve?)

- **k (bins / m en χ²)**  
  - Controla los **bins** del **histograma**.  
  - Se usa como **m** (número de intervalos) en la **prueba de uniformidad χ²**.
- **α (significancia)**  
  - Nivel global para **todas** las pruebas: Medias Z, Varianza χ² y Uniformidad χ².

> Guarda los cambios y se aplicarán al generar y al probar.

---

## 📦 Requisitos

- **Python 3.10+**
- **tkinter** (Windows/macOS viene incluido; en Linux puede requerir paquete del sistema)
- Librerías:
  ```bash
  pip install -r requirements.txt

## requirements.txt:
```shell
  numpy>=1.24
  matplotlib>=3.7
  scipy>=1.10
```
* (Linux) si hace falta:
  ```bash
  sudo apt-get install python3-tk

## ▶️ Ejecución
  ```bash
  python main.py
```

La aplicación corre offline.

## 🛠️ Uso rápido

### 1 Generadores

* Elige algoritmo.

* Ingresa n y las semillas requeridas (en Productos Medios son 2; en Multiplicador Constante añade la constante a).

* Presiona Generar: verás la tabla de pasos y el histograma.

* Opcional: Exportar CSV o Guardar PNG.

### 2 Pruebas

* Marca una o varias: Medias Z, Varianza χ², Uniformidad χ².

* Presiona Probar. Se muestran resultados (con p-value e intervalos) y cualquier advertencia (por ej., 
𝑛
<
10
n<10 o valores fuera de 
[
0
,
1
]
[0,1]).

### 3 Variables

* Ajusta k y α y pulsa Guardar.
k se usa tanto para el histograma como para 
𝑚
m en la χ² de uniformidad.

## 📁 Estructura del proyecto
```css
.
├── core/
│   └── registry.py
├── generators/
│   ├── mid_square.py
│   ├── productos_medios.py
│   └── multiplicador_constante.py
├── tests/
│   ├── medias.py
│   ├── varianza.py
│   └── uniformidad_chi2.py
├── gui/
│   ├── main_window.py
│   ├── tab_generadores.py
│   ├── tab_pruebas.py
│   ├── tab_variables.py
│   ├── theme.py
│   └── widgets.py
├── utils/
│   ├── plotting.py
│   └── exporter.py
├── requirements.txt
└── main.py
```
