# Temario práctico SMAW: de soldador a soldador de cañerías

**Objetivo:** preparar, de forma autodidacta, la prueba práctica de calificación de soldador de cañerías con **electrodo revestido (SMAW / MMA)**. Es la prueba que en Argentina se suele llamar "rendir AWS" en UOCRA, con un inspector o en un centro evaluador.

**Punto de partida:** ya sabés dar puntos y hacer cordones. Tenés soldadora de electrodo y amoladora.

**Alcance:** solamente SMAW. TIG (GTAW) y MIG/MAG (GMAW) quedan para otro capítulo.

---

## La regla de oro

> En el examen **manda la WPS** (Especificación del Procedimiento de Soldadura) **y el código que indique el evaluador**: AWS D1.1, ASME IX o API 1104.
> Este temario te prepara para los casos más comunes: caño 6G, raíz E6010 y relleno/presentación E7018.
> Los valores marcados con ⚠️ los tenés que **verificar contra la WPS o la edición vigente del código**. Las normas cambian la numeración de un año a otro, y cada empresa ajusta sus propios procedimientos.

---

## Versión para el celular

Todo el temario está armado como una sola página web, con índice, letra regulable y modo oscuro: <https://claude.ai/artifact/VkTWgc9AEDBf5sWRsUv3nQ> (privada, solo la abre el dueño de la cuenta).
Si editás los capítulos, regenerala con `python3 herramientas/generar_pagina.py salida.html` (requiere `pip install markdown==3.7`).

## Cómo usar este temario

1. **Leé primero el capítulo 00.** Ahí está qué te pueden tomar y qué preguntar antes de inscribirte.
2. **Armá tu taller** con el capítulo 04: cupones, soporte de posiciones y galgas.
3. **Seguí el plan del capítulo 09**, semana por semana. Cada módulo te manda a los capítulos de técnica.
4. **Evaluate vos mismo** con el capítulo 08: ensayo visual, doblado casero y nick-break. Practicar sin ensayar no sirve.
5. **Registrá todo** (amperaje, electrodo, posición, defecto, causa). Lo que no se mide no mejora.

## Índice

| # | Capítulo | Para qué sirve |
|---|---|---|
| 00 | [Mapa del examen](temario/00-mapa-del-examen.md) | Códigos (AWS D1.1, ASME IX, API 1104), posiciones, qué califica cada prueba, criterios de aceptación y preguntas para el evaluador |
| 01 | [Seguridad](temario/01-seguridad.md) | EPP, tonos de careta, humos, electricidad, amoladora y marco legal argentino |
| 02 | [Equipo, electrodos y parámetros](temario/02-equipo-electrodos-parametros.md) | Tu máquina, polaridad, clasificación AWS A5.1, amperajes de partida y almacenamiento del 7018 |
| 03 | [Planos, simbología y WPS](temario/03-planos-simbologia-wps.md) | Símbolos AWS A2.4, diferencias con ISO 2553, isométricos de cañería, cálculo de cortes y cómo leer una WPS |
| 04 | [Preparación de material](temario/04-preparacion-de-material.md) | Corte, biselado con amoladora, talón, luz, punteado, alineación, soporte casero y cupones |
| 05 | [Técnica en placa](temario/05-tecnica-en-placa.md) | Control de arco, filetes, ranura con respaldo 2G/3G/4G y raíz abierta en placa |
| 06 | [Técnica en caño](temario/06-tecnica-en-cano.md) | Raíz E6010 ascendente y descendente, pase caliente, relleno y presentación E7018, y técnica 2G, 5G y 6G |
| 07 | [Defectos: causas y soluciones](temario/07-defectos-causas-soluciones.md) | Diagnóstico de cada discontinuidad y cómo corregirla |
| 08 | [Inspección y autoensayos](temario/08-inspeccion-y-autoensayos.md) | Visual con galgas, corte de probetas, doblado casero, nick-break y macroataque |
| 09 | [Plan de entrenamiento](temario/09-plan-de-entrenamiento.md) | 16 semanas por fases, con criterios para avanzar, consumo estimado y planilla de registro |
| 10 | [El día del examen](temario/10-dia-del-examen.md) | Qué llevar, qué verificar y cómo administrar el tiempo y los nervios |
| 11 | [Recursos y fuentes](temario/11-recursos-y-fuentes.md) | Normas, libros, canales de YouTube, instituciones en Argentina y fuentes consultadas |
| 12 | [Glosario español-inglés](temario/12-glosario.md) | Los términos que vas a ver en videos y normas en inglés |

## Ruta resumida

```
Placa: control de arco y filetes ──► Ranura con respaldo 3G/4G (7018) ──► Raíz abierta en placa (6010)
                                                                                    │
     ┌──────────────────────────────────────────────────────────────────────────────┘
     ▼
Caño 2G ──► Caño 5G ──► Caño 6G completo ──► Simulacros con ensayo ──► EXAMEN
```

## Aviso

Este material es una guía de estudio. No reemplaza a las normas originales (AWS, ASME, API), que tienen derechos de autor y hay que consultarlas en su edición vigente, ni a la WPS del examen ni a la indicación del inspector. Las cifras sin ⚠️ son prácticas habituales del oficio o datos de fabricantes. Las marcadas con ⚠️ salen de fuentes secundarias o dependen de la edición del código.
