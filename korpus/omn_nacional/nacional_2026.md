# XXXV Olimpíada Matemática Ñandú — Certamen Nacional
> Fuente: fotos de las hojas de examen, `korpus/omn_nacional/nacional_2026_n1_dia{1,2}.jpg` (Primer Nivel) y `korpus/omn_nacional/nacional_2026_n2_dia{1,2}.jpg` (Segundo Nivel), sin PDF oficial todavía. ⚠ La hoja del Segundo Día dice «XXXIV» en el encabezado — errata de la plantilla 2025: los problemas 4–6 no coinciden con 2025 (ver `nacional_2025.md`). Respuestas: propias, verificadas por fuerza bruta (Primer Nivel 1, 3, 4, 6; Segundo Nivel 1–4, 6) y por sustitución en todos los datos (Primer Nivel 2, 5; Segundo Nivel 5, más fuerza bruta del área ABCD); no son la clave oficial. Tercer Nivel: pendiente.

## Primer Nivel

### Primer Día — Problema 1
Ariel y Catalina ponen fichas en las casillas de un tablero de 100 x 100.
Ariel pone fichas en las filas, de la siguiente manera:
- Pone una ficha en cada casilla de la primera fila.
- Deja 1 fila libre y pone una ficha en cada casilla de la fila siguiente.
- Deja 2 filas libres y pone una ficha en cada casilla de la fila siguiente.
- Deja 3 filas libres y pone una ficha en cada casilla de la fila siguiente.
Sigue así, dejando cada vez una fila libre más, hasta que se acaba el tablero.
Catalina pone fichas en las columnas, de la siguiente manera:
- Pone una ficha en cada casilla de la primera columna.
- Deja 2 columnas libres y pone una ficha en cada casilla de la columna siguiente.
Sigue de la misma manera: cada vez deja 2 columnas libres y pone una ficha en cada casilla de la columna siguiente.
Después de que Ariel y Catalina terminan de ubicar sus fichas en el tablero, ¿cuántas casillas del tablero tienen dos fichas? ¿Cuántas casillas del tablero quedan vacías?

Respuesta: 442 casillas con dos fichas (filas 1, 3, 6, …, 91 — 13 filas; columnas 1, 4, …, 100 — 34 columnas; 13 · 34); 5742 vacías (87 · 66).

### Primer Día — Problema 2
En la figura:
JEID y KBLG son cuadrados
ABCD y EFGH son rectángulos
EF = FK y FG = IH
Perímetro de ABCD = 228cm
Perímetro de EFGH = 60cm
¿Cuánto miden los lados del rectángulo ABCD?
¿Cuál es el perímetro de JEID?
¿Cuál es el perímetro de IHLC?
[Figura: rectángulo ABCD (A abajo a la izquierda, B abajo a la derecha, C arriba a la derecha, D arriba a la izquierda). J en AD, I en DC, K en AB, L en BC. Cuadrado JEID arriba a la izquierda; E y F en el segmento horizontal JF; K debajo de F; H encima de E, G encima de F, L a la altura de HG; cuadrado KBLG abajo a la derecha; rectángulo EFGH entre los dos cuadrados.]

Respuesta: AB = 72cm, BC = 42cm; perímetro de JEID = 96cm; perímetro de IHLC = 120cm.

### Primer Día — Problema 3
Fran quiere escribir un dígito del 1 al 9 en cada círculo de la figura, de modo que:
- no hay dígitos repetidos,
- las sumas de los tres dígitos escritos en los círculos de cada una de las tres líneas son todas iguales,
- de los seis dígitos de las puntas, los tres menores están en los tres círculos de la izquierda,
- los dígitos escritos en los tres círculos de la derecha están ordenados de menor a mayor.
¿De cuántas maneras distintas puede hacerlo? Explica cómo las contaste.
[Figura: estrella de 7 círculos — uno central y seis puntas, tres a la izquierda y tres a la derecha; cada una de las tres líneas rectas pasa por una punta izquierda, el centro y una punta derecha.]

Respuesta: 48 maneras (16 ternas de pares con la misma suma: suma 7, 8, 12, 13 — 1 cada una; suma 9, 10, 11 — 4 cada una; por 3 dígitos posibles en el centro).

### Segundo Día — Problema 4
Nati y Mía tienen, cada una, una pila de figuritas. Entre las dos tienen 381 figuritas.
Intercambian figuritas de la siguiente manera:
En el paso 1, Nati le da 1 figurita a Mía y Mía agrega esa figurita a su pila.
En el paso 2, Mía le da 2 figuritas de su pila a Nati y Nati las agrega a su pila.
En el paso 3, Nati le da 3 figuritas de su pila a Mía y Mía las agrega a su pila.
Siguen así, alternadamente, dándole una a la otra 4, 5, 6,.... figuritas.
Después de 98 pasos, Mía tiene 53 figuritas más que Nati.
¿Cuántas figuritas tenía cada una al comienzo?
Si intercambian figuritas hasta que alguna se queda sin ninguna, ¿cuántos pasos hacen?

Respuesta: Nati 115, Mía 266; 229 pasos (Nati se queda sin figuritas).

### Segundo Día — Problema 5
En la figura:
BEFD es un cuadrado
BMKJ y MNPQ son rectángulos
ABC es equilátero y ABD es isósceles
JK = JD = PN = NE
Perímetro de MNPQ = 54 cm
Perímetro de BMKJ = 66 cm
Perímetro de ABD = 88 cm
¿Cuál es el perímetro de la figura?
¿Cuál es el perímetro de BDAC?
¿Cuál es el perímetro de BNPQKJ?
¿Cuál es el perímetro de ABMKJD?
[Figura: cuadrado inclinado BEFD (B abajo, E a la derecha, F arriba, D a la izquierda) con la diagonal DE trazada. J en BD; M y N en BE; K y P en DE; Q en MK. A abajo a la izquierda en la recta de B; triángulo ABD con AD = BD (por la figura); C dentro de ABD.]

Respuesta: perímetro de la figura 154cm; BDAC 110cm; BNPQKJ 108cm; ABMKJD 100cm (BD = 33, JK = 6, AB = 22).

### Segundo Día — Problema 6
El tablero de la figura tiene una casilla central y cuatro ramas, dos de 2 casillas y dos de 3 casillas.
En cada casilla, excepto en la central, hay una lámpara.
Todas las lámparas están apagadas.
Santi quiere encender 6 lámparas de modo que en cada rama haya una o más lámparas encendidas.
¿De cuántas maneras puede elegir las 6 lámparas? Explica cómo las contaste.
[Figura: cruz — casilla central sombreada; ramas: arriba 2, abajo 2, izquierda 3, derecha 3.]

Respuesta: 141 maneras (210 − 2 · 28 − 2 · 7 + 1).

## Segundo Nivel

### Primer Día — Problema 1
Pablo escribe la lista de todos los números de 6 cifras que se forman reordenando las cifras de 345123. En la lista de Pablo, los números están ordenados de menor a mayor.
¿Cuántos números tiene la lista de Pablo?
¿Qué número está en el lugar 200 de la lista de Pablo?
¿En qué lugar de la lista de Pablo está el número 423513?

Respuesta: 360 números; en el lugar 200 está 342153; 423513 está en el lugar 260.

### Primer Día — Problema 2
En la figura,
ABCD es un cuadrado que está partido en cuatro rectángulos y un cuadrado central.
El área del rectángulo AELH es 48cm2.
El área del rectángulo JFCG es 133cm2.
Los dos rectángulos tienen lados de longitudes enteras y mayores que 1cm.
La longitud de AE es mayor que la de AH y la longitud de CF es mayor que la de GC.
¿Cuál es el área de IJKL?
¿Cuál es el área de ABCD?
¿Cuál es el perímetro de HKGD?
¿Hay una única respuesta posible?
[Figura: cuadrado ABCD (A abajo a la izquierda, B abajo a la derecha, C arriba a la derecha, D arriba a la izquierda), partido en molinete. E en AB, F en BC, G en DC, H en AD. AELH abajo a la izquierda; EBFI abajo a la derecha; JFCG arriba a la derecha; HKGD arriba a la izquierda; cuadrado central IJKL (I abajo a la izquierda, J abajo a la derecha, K arriba a la derecha, L arriba a la izquierda). E, I, L en una vertical; G, K, J en otra; H, L, K en una horizontal; I, J, F en otra.]

Respuesta: dos posibilidades, no es única. AE = 8, AH = 6, GC = 7, CF = 19: IJKL = 25cm2, ABCD = 400cm2, perímetro de HKGD = 54cm. AE = 12, AH = 4, GC = 7, CF = 19: IJKL = 4cm2, ABCD = 441cm2, perímetro de HKGD = 62cm. (AE = 16 o 24 dan lado negativo del cuadrado central.)

### Primer Día — Problema 3
La figura muestra una cuadrícula de 6x7 en la que se dibujó un segmento oblicuo.
Seba cuenta rectángulos con todos sus lados en las líneas de la cuadrícula.
¿Cuántos de estos rectángulos no tienen ningún punto en común con el segmento oblicuo dibujado?
Explica cómo los contaste.
Aclaración: No te olvides de contar los cuadrados (también son rectángulos).
[Figura: cuadrícula de 7 columnas y 6 filas de cuadrados iguales. El segmento va desde el vértice inferior izquierdo hasta el punto de la línea superior que está a 6 cuadrados del borde izquierdo: es la diagonal de los 6 cuadrados de la izquierda en cada fila hacia arriba, y pasa por los nodos (k, k), k = 0…6.]

Respuesta: 105 rectángulos (de 588 en total).

### Segundo Día — Problema 4
ABC es un número de tres cifras y ADBC es un número de cuatro cifras.
Hallar los dígitos A, B, C y D que verifican:
ABC x 9 = ADBC
Dar todas las posibilidades.

Respuesta: 12 posibilidades si letras distintas pueden ser el mismo dígito — ABC = 125, 150, 175, 225, 250, 275, 350, 375, 450, 475, 575, 675 (1125, 1350, 1575, 2025, 2250, 2475, 3150, 3375, 4050, 4275, 5175, 6075). Si letras distintas deben ser dígitos distintos: 5 — 150, 275, 350, 475, 675.

### Segundo Día — Problema 5
En la figura, un cuadrado grande está partido en 5 octógonos iguales, 4 trapecios isósceles iguales, 4 triángulos isósceles iguales y 4 cuadraditos iguales.
En cada trapecio, la longitud de la base mayor es el triple de la longitud de la base menor.
El área de cada octógono es 252 cm2.
¿Cuánto mide el lado de cada cuadradito?
¿Cuál es el área de la parte sombreada? ¿Cuál es el área del cuadrilátero ABCD?
[Figura (dos copias del mismo cuadrado): un octógono en el centro y uno en cada esquina; un cuadradito pegado a cada lado del octógono central; en el medio de cada lado del cuadrado grande, un trapecio con la base menor pegada al cuadradito y la base mayor sobre el lado del cuadrado; en cada esquina, un triángulo rectángulo isósceles. Sombreado: octógono central, 4 cuadraditos y 4 trapecios. A en el lado izquierdo, extremo superior de la base mayor del trapecio izquierdo; B en el lado inferior, vértice del triángulo de la esquina inferior izquierda; C en el lado derecho, extremo inferior de la base mayor del trapecio derecho; D vértice superior derecho del cuadradito de arriba.]

Respuesta: lado del cuadradito 6cm (lado del cuadrado grande 42cm); parte sombreada 684cm2; área de ABCD 918cm2.

### Segundo Día — Problema 6
Martín tiene 36 fichas: 18 rojas y 18 azules.
Quiere ubicarlas formando una hilera de modo que se cumplan estas condiciones:
- hay 4 bloques de fichas rojas y 4 bloques de fichas azules, con los colores intercalados, empezando con rojo,
- los bloques de fichas de un mismo color tienen distintas cantidades de fichas,
- la cantidad de fichas de los bloques de un mismo color va siempre en aumento.
¿De cuántas maneras puede hacerlo? Explica cómo las contaste.
¿En cuántos casos los 8 bloques tienen distintas cantidades de fichas?

Respuesta: 225 maneras (15 formas de escribir 18 como suma de 4 números distintos, para cada color: 15 · 15); 8 casos con los 8 bloques distintos (los bloques son 1, 2, …, 8).
