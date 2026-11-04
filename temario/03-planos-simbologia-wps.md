# 03 · Lectura de planos, simbología de soldadura y WPS

En obra, el soldador de cañerías tiene que leer el **símbolo de soldadura**, interpretar un **isométrico** y seguir una **WPS**. Algunos exámenes incluyen preguntas teóricas sobre esto, y en el trabajo real te lo exigen desde el primer día.

---

## 1. Tipos de junta

```
 A tope (butt)          En T (tee)            En esquina (corner)     Solapada (lap)        De borde (edge)
 ═════╗ ╔═════              ║                 ╔══════                ══════════             ══════════
      ║ ║                   ║                 ║                         ══════════          ══════════
                       ═════╩═════            ║
```

En cañería, el 90 % de lo que vas a soldar son **juntas a tope** (caño con caño, caño con accesorio o con brida de cuello). Le siguen las **juntas en T con filete**: bridas *slip-on*, *socket weld* y derivaciones.

## 2. Partes de una junta biselada (vocabulario obligatorio)

```
                    |<----- ancho de la presentación ----->|
                     _______________________________________     ← sobremonta (refuerzo de cara) ≤ 3 mm
   ─────────────────┐            pasada de                 ┌─────────────────   superficie exterior
                     \           presentación             /
     pieza A          \     rellenos                     /          pieza B
   (pared t)           \                                /
                        \      pase caliente           /     ← cara del bisel
                         │                             │     ← talón (cara de raíz) 1,6 mm
   ──────────────────────┘          raíz               └──────────────────────   superficie interior
                          |<- luz (abertura de raíz) ->|
                                 2,4 – 3,2 mm               ▲ penetración de raíz (≤ 3 mm hacia adentro)

   Ángulo de bisel = 37,5° (en cada pieza)     Ángulo de ranura (incluido) = 75° (la suma de los dos)
   Pie del cordón = línea donde la soldadura se une con el metal base (ahí nace la socavación)
   (Dibujo NO a escala: la luz real es mucho más chica que la boca del bisel)
```

| Término | Inglés | Valor típico en caño |
|---|---|---|
| Ángulo de bisel | Bevel angle | 37,5° ± 2,5° (ASME B16.25) |
| Ángulo de ranura (incluido) | Groove angle | 75° (60° a 80°) |
| Talón / cara de raíz | Root face / land | 1,6 mm ± 0,8 mm |
| Luz / abertura de raíz | Root opening / gap | 2,4 a 3,2 mm (lo define la WPS) |
| Sobremonta | Reinforcement | ≤ 3 mm |
| Penetración de raíz | Root reinforcement / melt-through | ≤ 3 mm |

---

## 3. El símbolo de soldadura AWS A2.4

### Estructura

```
                           (OTRO LADO: lo que se dibuja ARRIBA de la línea)
                 ●  ← círculo = soldar "todo alrededor"
                 ⚑  ← bandera = soldadura "en obra" (de campo)
                 │
   ──────────────┼────────────────────────────────────  <   COLA: proceso, WPS, notas
                /│          (LADO FLECHA: lo que se dibuja ABAJO de la línea)       (ej.: SMAW · WPS-01)
               /
              ↙  FLECHA: toca la junta
```

**La regla más importante:**

- Símbolo **debajo** de la línea de referencia = soldar del **lado de la flecha**.
- Símbolo **arriba** de la línea = soldar del **otro lado**.
- Símbolo **arriba y abajo** = soldar de **ambos lados**.
- La **flecha** puede apuntar hacia arriba, hacia abajo, a la izquierda o a la derecha, y la regla **no cambia**. Lo que manda es dónde está el símbolo respecto de la **línea**.

### Símbolos básicos

| Soldadura | Cómo se dibuja | Notas |
|---|---|---|
| Filete | Triángulo rectángulo. **El cateto vertical siempre a la izquierda** | La medida a la izquierda es el **tamaño de pierna (cateto)** |
| Ranura recta (sin bisel) | Dos líneas paralelas `‖` | Chapa fina, bordes rectos |
| Ranura en V | `V` | Las dos piezas biseladas. **La típica de caño** |
| Ranura en bisel (½ V) | `|/`, con el lado recto a la izquierda | Solo una pieza biselada. La flecha "quebrada" apunta a la pieza que se bisela |
| Ranura en U | `U` | Espesores grandes |
| Ranura en J | `|)`, con el lado recto a la izquierda | Como la U, pero en una sola pieza |
| Abocinada en V / en bisel | `)(` / `|(` | Uniones de caños con perfiles redondos o chapas plegadas |
| Tapón / ojal | Rectángulo | Soldadura en agujero |

### Símbolos suplementarios

| Símbolo | Significado |
|---|---|
| ● Círculo en el quiebre de la flecha | Soldar **todo alrededor** (por ejemplo, un caño soldado a una placa) |
| ⚑ Bandera | Soldadura **en obra (de campo)**, no en taller |
| ◗ Semicírculo relleno del lado opuesto | **Penetración completa visible** (*melt-through*). Típico de la raíz abierta de caño |
| ▭ Rectángulo del lado opuesto | **Respaldo** (con "R" adentro si se quita después) |
| ▭ Rectángulo cruzando la línea | **Separador** (*spacer*) |
| ─ / ⌒ / ‿ sobre el símbolo | **Contorno**: al ras, convexo o cóncavo |
| Letra junto al contorno | **Terminación**: G = amolado, M = mecanizado, C = cincelado, H = martillado, R = laminado, P = planchado, U = sin especificar |

### Dónde va cada dimensión

```
 FILETE:          tamaño  ◺  largo – paso                      Ej.:  6 ◺ 50-150
                                                                    = filete de 6 mm de cateto,
                                                                      tramos de 50 mm cada 150 mm entre centros

 RANURA:   profundidad(garganta)  V  ← la luz va DENTRO del símbolo, el ángulo AFUERA del símbolo
                                                                Ej.:  10 (10)  con 75° y luz 3 adentro de la V
                                                                    = bisel de 10 mm de profundidad,
                                                                      garganta efectiva 10 mm, ranura de 75°, luz 3 mm
```

- **Profundidad del bisel (S)** a la izquierda. La **garganta efectiva (E)** va entre paréntesis: `S (E)`.
- Si una ranura simple **no tiene medida de profundidad**, se entiende **penetración completa (CJP)**. A menudo igual se escribe "CJP" en la cola.
- **Varias líneas de referencia:** indican una **secuencia de operaciones**. La línea más cercana a la flecha es la primera operación.
- **Cola:** proceso (SMAW, GTAW, etc.), número de WPS y otras notas. Si no hay referencias, la cola se omite.

### Diferencias con ISO 2553 (te lo podés cruzar en planos europeos o de empresas multinacionales)

| Aspecto | AWS A2.4 | ISO 2553 (sistema A) |
|---|---|---|
| Línea de referencia | Una línea continua | **Doble**: continua + línea de trazos |
| Lado flecha / otro lado | Abajo / arriba de la línea | Sobre la **línea continua** = lado flecha. Sobre la **de trazos** = otro lado |
| Medida del filete | Número = **cateto (pierna)** | **"a5"** = garganta de 5 mm · **"z7"** = cateto de 7 mm. ¡No es lo mismo! |
| Proceso | Sigla (SMAW) | Número: **111 = electrodo revestido**, 141 = TIG, 135 = MAG |

> ⚠️ **Trampa clásica:** un filete "a5" en ISO tiene unos **7 mm de cateto** (cateto ≈ garganta × 1,41). Si lo hacés de 5 mm de pierna, queda chico y lo rechazan.

---

## 4. Ejercicios de simbología (tapá las respuestas)

1. Triángulo **debajo** de la línea, "8" a la izquierda, sin nada a la derecha, círculo en el quiebre.
2. Una "V" **arriba** de la línea, "60°" afuera del símbolo, "3" adentro, y un semicírculo relleno **debajo**.
3. Triángulos **arriba y abajo**, desfasados, con "6" y "50-200" en cada uno.
4. Bisel (½ V) debajo de la línea, la flecha quebrada apuntando a la pieza de la izquierda, bandera en el quiebre, cola "SMAW WPS-12".
5. En un plano ISO: línea continua + línea de trazos, triángulo sobre la de trazos, "a4".

<details>
<summary><b>Respuestas</b></summary>

1. Filete de 8 mm de cateto del lado de la flecha, **todo alrededor**.
2. Ranura en V del **otro lado**, con 60° de ángulo incluido y 3 mm de luz, y **penetración completa visible del lado de la flecha** (melt-through).
3. Filetes de 6 mm **en ambos lados, intermitentes y alternados** (en zigzag): tramos de 50 mm cada 200 mm entre centros.
4. Bisel en ½ V del lado de la flecha, biselando **solo la pieza indicada por la flecha quebrada**, soldado **en obra**, con proceso SMAW según la **WPS-12**.
5. Filete del **otro lado** (porque está sobre la línea de trazos), con **garganta de 4 mm** (cateto ≈ 5,7 mm).

</details>

---

## 5. Isométricos y planos de cañería

### Qué es un isométrico

Es un dibujo de una **sola línea** (el eje del caño) en perspectiva a 30°. No está a escala. Las medidas van **de eje a eje** o de eje a cara de brida.

Elementos que tenés que reconocer:

- **Soldadura de taller:** punto `•` en la unión.
- **Soldadura de campo:** `FW` (*field weld*) o el símbolo de bandera. A menudo cada soldadura va numerada (W1, W2…) para trazabilidad: quién la soldó, con qué WPS y si se inspeccionó.
- **Bridas** `‖`, **válvulas** `⋈`, **reducciones** (trapecio), **codos** (curva o vértice) y **tees**.
- **Flecha de Norte** de planta, **cotas** de eje (EL +3.500) y **número de línea** (diámetro, servicio, especificación del material, por ejemplo `6"-P-1001-A1A`).
- **Lista de materiales (BOM):** diámetro, schedule, norma del caño (A106 Gr. B) y de los accesorios (A234 WPB).

### Dimensiones de caños que vas a usar (ASME B36.10)

| NPS | Diámetro exterior | Sch 40 | Sch 80 | Sch 120 |
|---|---|---|---|---|
| 2" | 60,3 mm | 3,91 mm | 5,54 mm | – |
| 3" | 88,9 mm | 5,49 mm | 7,62 mm | – |
| 4" | 114,3 mm | 6,02 mm | 8,56 mm | 11,13 mm |
| 6" | 168,3 mm | 7,11 mm | 10,97 mm | 14,27 mm |
| 8" | 219,1 mm | 8,18 mm | 12,70 mm | 18,26 mm |

> Recordá: el **NPS** (diámetro nominal) **no es** ni el diámetro exterior ni el interior. A partir de 14", el NPS coincide con el diámetro exterior.

### "Take-off": cuánto ocupa cada accesorio (ASME B16.9, soldadura a tope)

| Accesorio | Fórmula práctica | 2" | 4" | 6" | 8" |
|---|---|---|---|---|---|
| Codo 90° radio largo (LR), centro a cara | **1,5 × NPS** (en pulgadas) | 76 mm | 152 mm | 229 mm | 305 mm |
| Codo 90° radio corto (SR) | **1,0 × NPS** | 51 mm | 102 mm | 152 mm | 203 mm |
| Codo 45° LR | ≈ 0,625 × NPS | 35 mm | 64 mm | 95 mm | 127 mm |
| Tee recta, centro a cara | (tabla) | 64 mm | 105 mm | 143 mm | 178 mm |

### Cálculo de largo de corte

```
  Largo de corte = medida eje a eje − take-off de cada accesorio − luz de cada soldadura
```

**Ejemplo 1.** Dos codos 90° LR de 4", con 1000 mm de eje a eje y luz de 3 mm en cada soldadura:
`1000 − 152,4 − 152,4 − 3 − 3 =` **689,2 mm**

**Ejemplo 2 (desvío a 45°).** Un desvío (*offset*) de 300 mm con dos codos de 45° de 4":

- Recorrido (*travel*) = desvío × 1,414 = 424,3 mm
- Corte = 424,3 − 2 × 63,5 − 2 × 3 = **291,3 mm**

---

## 6. Cómo leer una WPS

La **WPS** (*Welding Procedure Specification*) es la "receta" calificada que tenés que seguir. Está respaldada por un **PQR** (*Procedure Qualification Record*), que es el registro del ensayo que demostró que la receta funciona.

### Campos principales (formato ASME QW-482 y similares en AWS B2.1 / D1.1)

| Bloque | Qué dice | Qué te importa a vos |
|---|---|---|
| **Juntas** (QW-402) | Diseño de junta, ángulo, talón, luz, respaldo sí o no | Cómo preparás y armás |
| **Metal base** (QW-403) | P-Number, rango de espesores y diámetros | El caño que soldás está dentro del rango |
| **Metal de aporte** (QW-404) | Especificación (SFA 5.1), clase AWS (E6010/E7018), F-No., A-No. y diámetro | Qué electrodo usás en cada pasada |
| **Posición** (QW-405) | Posiciones y **progresión** (ascendente o descendente) | ¿Ascendente? ¿Descendente? No se negocia |
| **Precalentamiento** (QW-406) | Temperatura mínima de precalentamiento y **máxima entre pasadas** | Si hace frío, precalentar. No superar el máximo entre pasadas |
| **Tratamiento térmico** (QW-407) | Si lleva alivio de tensiones después de soldar | Normalmente no, en cupones de examen |
| **Características eléctricas** (QW-409) | Tipo de corriente, polaridad, **rango de amperaje** y voltaje | **Tenés que estar dentro del rango** |
| **Técnica** (QW-410) | Cordón recto o tejido, limpieza entre pasadas, una o varias pasadas, velocidad | Si dice "cordón recto", no tejas |

### Ejemplo didáctico de WPS

> ⚠️ **EJEMPLO DIDÁCTICO** para entender el formato. **No es una WPS calificada.** No lo uses en obra.

```
 WPS N°: PRACT-SMAW-01            Proceso: SMAW (111)  Manual
 JUNTA:  A tope, V simple · bisel 37,5° ± 2,5° · talón 1,6 ± 0,8 mm · luz 2,4–3,2 mm · SIN respaldo
 METAL BASE: P-No. 1 (ASTM A106 Gr. B) · espesor calificado 5–22 mm · diámetro ≥ 73 mm
 APORTE: SFA 5.1 · raíz E6010 (F3) · relleno/presentación E7018 (F4, A1)
 POSICIÓN: Todas · progresión ASCENDENTE
 PRECALENTAMIENTO: mínimo 10 °C (si hay humedad o frío, secar/calentar) · ENTRE PASADAS: máximo 250 °C
 CORRIENTE: DC, electrodo positivo (DCEP)
 TÉCNICA: limpieza con cepillo y amoladora entre pasadas · raíz con cordón recto o latigueo · relleno con tejido
          ancho máximo del tejido: 3 × Ø del electrodo · empalmes amolados

 PASADA        ELECTRODO   Ø (mm)   CORRIENTE   AMPERAJE   PROGRESIÓN
 Raíz          E6010       3,2      DCEP        75–95 A    Ascendente
 Pase caliente E6010       3,2      DCEP        95–115 A   Ascendente
 Relleno       E7018       3,2      DCEP        100–120 A  Ascendente
 Presentación  E7018       2,5      DCEP        75–90 A    Ascendente
```

### Ejercicio

Con esa WPS:

1. ¿Podés soldar la raíz con 7018?
2. ¿Podés hacer la raíz descendente?
3. El caño está a 5 °C y húmedo. ¿Qué hacés?
4. ¿Podés tejer la presentación con un tejido de 15 mm de ancho usando un 7018 de 2,5 mm?

<details>
<summary><b>Respuestas</b></summary>

1. **No.** La WPS dice E6010 para la raíz.
2. **No.** La progresión es ascendente. Cambiarla es una variable esencial.
3. **Precalentar y secar** con soplete hasta superar el mínimo (y quitar la humedad) antes de puntear y soldar.
4. **No.** El ancho máximo es 3 × 2,5 = 7,5 mm. Hacé dos cordones o un tejido más angosto.

</details>
