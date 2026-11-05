from collections import deque

LIMITE = 20
LIMITE_MATRIZ = 10


# ----------------------------------------------------------------------
# Utilidades de entrada y validación
# ----------------------------------------------------------------------
def leer_entero(mensaje):
    """Pide un entero y repite hasta que sea válido."""
    while True:
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            print("  [Error] Debe ingresar un número entero. Intente de nuevo.")


def leer_cantidad(mensaje, limite=LIMITE):
    """Pide un entero positivo menor o igual al límite."""
    while True:
        n = leer_entero(mensaje)
        if n <= 0:
            print("  [Error] La cantidad debe ser un entero positivo (mayor que 0).")
        elif n > limite:
            print(f"  [Error] La cantidad máxima permitida es {limite}.")
        else:
            return n


def leer_indice(mensaje, tamano):
    """Pide un índice entre 0 y tamano-1."""
    while True:
        i = leer_entero(mensaje)
        if 0 <= i < tamano:
            return i
        print(f"  [Error] Índice fuera de rango. Valores válidos: 0 a {tamano - 1}.")


def leer_id_vertice(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto and " " not in texto:
            return texto
        print("  [Error] El identificador no puede estar vacío ni contener espacios.")


def menu(titulo, opciones):
    """Muestra un submenú numerado; 0 siempre es volver. Devuelve la opción."""
    print(f"\n--- {titulo} ---")
    for i, texto in enumerate(opciones, start=1):
        print(f"  {i}. {texto}")
    print("  0. Volver al menú principal")
    while True:
        op = leer_entero("Seleccione una opción: ")
        if 0 <= op <= len(opciones):
            return op
        print("  [Error] Opción no válida.")


# ----------------------------------------------------------------------
# 1. ARREGLO UNIDIMENSIONAL
# ----------------------------------------------------------------------
def mostrar_arreglo(datos):
    anchos = [max(len(str(i)), len(str(v))) for i, v in enumerate(datos)]
    print("\n  Índice : " + " | ".join(str(i).rjust(w) for i, w in enumerate(anchos)))
    print("  Valor  : " + " | ".join(str(v).rjust(w) for v, w in zip(datos, anchos)))


def arreglo():
    print("\n=== ARREGLO UNIDIMENSIONAL ===")
    n = leer_cantidad(f"¿Cuántos elementos va a ingresar? (1-{LIMITE}): ")
    datos = [leer_entero(f"  Elemento en la posición [{i}]: ") for i in range(n)]
    mostrar_arreglo(datos)
    while True:
        op = menu("Operaciones del arreglo",
                  ["Consultar por índice", "Modificar por índice",
                   "Recorrer elementos", "Mostrar arreglo"])
        if op == 0:
            return
        if op == 1:
            i = leer_indice(f"  Índice a consultar (0-{n - 1}): ", n)
            print(f"  El valor en la posición [{i}] es {datos[i]}")
        elif op == 2:
            i = leer_indice(f"  Índice a modificar (0-{n - 1}): ", n)
            anterior = datos[i]
            datos[i] = leer_entero("  Nuevo valor: ")
            print(f"  Posición [{i}]: {anterior} -> {datos[i]}")
            mostrar_arreglo(datos)
        elif op == 3:
            print("  Recorrido:")
            for i, v in enumerate(datos):
                print(f"    datos[{i}] = {v}")
        else:
            mostrar_arreglo(datos)


# ----------------------------------------------------------------------
# 2. MATRIZ
# ----------------------------------------------------------------------
def mostrar_matriz(m):
    filas, cols = len(m), len(m[0])
    w = max(len(str(v)) for fila in m for v in fila)
    w = max(w, len(str(cols - 1)))
    print("\n  " + " " * 4 + " ".join(f"C{j}".rjust(w + 1) for j in range(cols)))
    for i, fila in enumerate(m):
        print(f"  F{i}".ljust(6) + " ".join(str(v).rjust(w + 1) for v in fila))


def matriz():
    print("\n=== MATRIZ ===")
    filas = leer_cantidad(f"Número de filas (1-{LIMITE_MATRIZ}): ", LIMITE_MATRIZ)
    cols = leer_cantidad(f"Número de columnas (1-{LIMITE_MATRIZ}): ", LIMITE_MATRIZ)
    print(f"Total de elementos a ingresar: {filas * cols}")
    m = [[leer_entero(f"  Valor para fila {i}, columna {j}: ") for j in range(cols)]
         for i in range(filas)]
    mostrar_matriz(m)
    while True:
        op = menu("Operaciones de la matriz",
                  ["Consultar por fila y columna", "Modificar por fila y columna",
                   "Recorrer elementos (por filas)", "Mostrar matriz"])
        if op == 0:
            return
        if op in (1, 2):
            i = leer_indice(f"  Fila (0-{filas - 1}): ", filas)
            j = leer_indice(f"  Columna (0-{cols - 1}): ", cols)
            if op == 1:
                print(f"  m[{i}][{j}] = {m[i][j]}")
            else:
                anterior = m[i][j]
                m[i][j] = leer_entero("  Nuevo valor: ")
                print(f"  m[{i}][{j}]: {anterior} -> {m[i][j]}")
                mostrar_matriz(m)
        elif op == 3:
            print("  Recorrido por filas:")
            for i in range(filas):
                for j in range(cols):
                    print(f"    m[{i}][{j}] = {m[i][j]}")
        else:
            mostrar_matriz(m)


# ----------------------------------------------------------------------
# 3. LISTA ENLAZADA SIMPLE
# ----------------------------------------------------------------------
class NodoLista:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def insertar(self, valor, pos):
        """Inserta en la posición pos (0 = inicio, tamano = final)."""
        nuevo = NodoLista(valor)
        if pos == 0:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            for _ in range(pos - 1):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        self.tamano += 1

    def buscar(self, valor):
        actual, pos = self.cabeza, 0
        while actual:
            if actual.valor == valor:
                return pos
            actual, pos = actual.siguiente, pos + 1
        return -1

    def eliminar(self, valor):
        """Elimina la primera aparición. Devuelve True si existía."""
        previo, actual = None, self.cabeza
        while actual:
            if actual.valor == valor:
                if previo is None:
                    self.cabeza = actual.siguiente
                else:
                    previo.siguiente = actual.siguiente
                self.tamano -= 1
                return True
            previo, actual = actual, actual.siguiente
        return False

    def a_lista(self):
        datos, actual = [], self.cabeza
        while actual:
            datos.append(actual.valor)
            actual = actual.siguiente
        return datos

    def mostrar(self):
        datos = self.a_lista()
        if not datos:
            print("  Lista vacía: cabeza -> None")
            return
        print("  cabeza -> " + " -> ".join(f"[{v}]" for v in datos) + " -> None")
        print("  posición:  " + "    ".join(str(i).center(len(str(v)) + 2)
                                            for i, v in enumerate(datos)))


def lista():
    print("\n=== LISTA ENLAZADA ===")
    n = leer_cantidad(f"¿Cuántos elementos va a ingresar? (1-{LIMITE}): ")
    lst = ListaEnlazada()
    for i in range(n):
        lst.insertar(leer_entero(f"  Elemento #{i + 1} (se agrega al final): "), lst.tamano)
    lst.mostrar()
    while True:
        op = menu("Operaciones de la lista",
                  ["Insertar (inicio, final o posición)", "Buscar un valor",
                   "Eliminar un valor", "Recorrer", "Mostrar lista"])
        if op == 0:
            return
        if op == 1:
            if lst.tamano >= LIMITE:
                print(f"  [Error] La lista alcanzó el límite de {LIMITE} elementos.")
                continue
            valor = leer_entero("  Valor a insertar: ")
            pos = leer_indice_insercion(lst.tamano)
            print("  Antes:  " + str(lst.a_lista()))
            lst.insertar(valor, pos)
            print("  Después: " + str(lst.a_lista()))
            lst.mostrar()
        elif op == 2:
            pos = lst.buscar(leer_entero("  Valor a buscar: "))
            print(f"  Encontrado en la posición {pos}." if pos >= 0
                  else "  El dato NO existe en la lista.")
        elif op == 3:
            valor = leer_entero("  Valor a eliminar: ")
            print("  Antes:  " + str(lst.a_lista()))
            if lst.eliminar(valor):
                print("  Después: " + str(lst.a_lista()))
                lst.mostrar()
            else:
                print("  [Aviso] El dato no existe; la lista no cambió.")
        elif op == 4:
            print("  Recorrido: " + " -> ".join(str(v) for v in lst.a_lista()) if lst.tamano
                  else "  La lista está vacía.")
        else:
            lst.mostrar()


def leer_indice_insercion(tamano):
    while True:
        p = leer_entero(f"  Posición de inserción (0 = inicio, {tamano} = final): ")
        if 0 <= p <= tamano:
            return p
        print(f"  [Error] Posición válida: 0 a {tamano}.")


# ----------------------------------------------------------------------
# 4. PILA (LIFO)
# ----------------------------------------------------------------------
def mostrar_pila(pila):
    if not pila:
        print("  Pila vacía.")
        return
    ancho = max(len(str(v)) for v in pila) + 4
    print("  +" + "-" * ancho + "+")
    for k in range(len(pila) - 1, -1, -1):
        marca = "  <- CIMA" if k == len(pila) - 1 else ("  <- BASE" if k == 0 else "")
        print("  |" + str(pila[k]).center(ancho) + "|" + marca)
    print("  +" + "-" * ancho + "+")


def pila():
    print("\n=== PILA (LIFO: último en entrar, primero en salir) ===")
    n = leer_cantidad(f"¿Cuántos elementos va a apilar? (1-{LIMITE}): ")
    p = []
    for i in range(n):
        v = leer_entero(f"  Elemento #{i + 1} a apilar: ")
        p.append(v)
        print(f"  Apilado {v}. La cima ahora es {p[-1]}.")
    mostrar_pila(p)
    while True:
        op = menu("Operaciones de la pila",
                  ["Apilar (push)", "Desapilar (pop)", "Ver elemento superior (peek)",
                   "Mostrar pila"])
        if op == 0:
            return
        if op == 1:
            if len(p) >= LIMITE:
                print(f"  [Error] Pila llena (límite {LIMITE}).")
                continue
            p.append(leer_entero("  Valor a apilar: "))
            mostrar_pila(p)
        elif op == 2:
            if not p:
                print("  [Error] La pila está vacía: no hay elemento que retirar.")
            else:
                print(f"  Se retiró: {p.pop()}")
                mostrar_pila(p)
        elif op == 3:
            print(f"  Elemento superior (cima): {p[-1]}" if p
                  else "  [Error] La pila está vacía.")
        else:
            mostrar_pila(p)


# ----------------------------------------------------------------------
# 5. COLA (FIFO)
# ----------------------------------------------------------------------
def mostrar_cola(cola):
    if not cola:
        print("  Cola vacía.")
        return
    print("  SALE <- FRENTE [ " + " | ".join(str(v) for v in cola) + " ] FINAL <- ENTRA")
    print("  Orden de salida: " + " , ".join(str(v) for v in cola))


def cola():
    print("\n=== COLA (FIFO: primero en entrar, primero en salir) ===")
    n = leer_cantidad(f"¿Cuántos elementos va a encolar? (1-{LIMITE}): ")
    c = deque()
    for i in range(n):
        v = leer_entero(f"  Elemento #{i + 1} a encolar: ")
        c.append(v)
        print(f"  Encolado {v}. Frente: {c[0]} | Final: {c[-1]}")
    mostrar_cola(c)
    while True:
        op = menu("Operaciones de la cola",
                  ["Encolar (enqueue)", "Desencolar (dequeue)",
                   "Ver primer elemento (frente)", "Mostrar cola"])
        if op == 0:
            return
        if op == 1:
            if len(c) >= LIMITE:
                print(f"  [Error] Cola llena (límite {LIMITE}).")
                continue
            c.append(leer_entero("  Valor a encolar: "))
            mostrar_cola(c)
        elif op == 2:
            if not c:
                print("  [Error] La cola está vacía: no hay elemento que retirar.")
            else:
                print(f"  Se retiró: {c.popleft()}")
                mostrar_cola(c)
        elif op == 3:
            print(f"  Primer elemento (frente): {c[0]}" if c
                  else "  [Error] La cola está vacía.")
        else:
            mostrar_cola(c)


def comparar_pila_cola():
    """Misma secuencia de entrada en pila y cola; muestra el orden de salida."""
    print("\n=== COMPARACIÓN PILA vs COLA ===")
    n = leer_cantidad(f"¿Cuántos elementos tendrá la secuencia? (1-{LIMITE}): ")
    secuencia = [leer_entero(f"  Elemento #{i + 1}: ") for i in range(n)]
    p, c = list(secuencia), deque(secuencia)
    salida_pila = [p.pop() for _ in range(len(p))]
    salida_cola = [c.popleft() for _ in range(len(c))]
    print(f"\n  Entrada (en este orden): {secuencia}")
    print(f"  Salida de la PILA (LIFO): {salida_pila}")
    print(f"  Salida de la COLA (FIFO): {salida_cola}")
    print("  La pila retira primero el último que entró (cima); la cola retira\n"
          "  primero el que lleva más tiempo esperando (frente).")


# ----------------------------------------------------------------------
# 6. ÁRBOL BINARIO DE BÚSQUEDA
# ----------------------------------------------------------------------
class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        """Devuelve False si el valor ya existe (duplicados rechazados)."""
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
            return True
        actual = self.raiz
        while True:
            if valor == actual.valor:
                return False
            lado = "izq" if valor < actual.valor else "der"
            siguiente = getattr(actual, lado)
            if siguiente is None:
                setattr(actual, lado, NodoArbol(valor))
                return True
            actual = siguiente

    def buscar(self, valor):
        actual, camino = self.raiz, []
        while actual:
            camino.append(actual.valor)
            if valor == actual.valor:
                return True, camino
            actual = actual.izq if valor < actual.valor else actual.der
        return False, camino

    def inorden(self, n, r):
        if n:
            self.inorden(n.izq, r); r.append(n.valor); self.inorden(n.der, r)

    def preorden(self, n, r):
        if n:
            r.append(n.valor); self.preorden(n.izq, r); self.preorden(n.der, r)

    def postorden(self, n, r):
        if n:
            self.postorden(n.izq, r); self.postorden(n.der, r); r.append(n.valor)

    def mostrar(self):
        if not self.raiz:
            print("  Árbol vacío.")
            return
        print(f"  Raíz: {self.raiz.valor}")
        hijos = [(h, e) for h, e in ((self.raiz.izq, "I"), (self.raiz.der, "D")) if h]
        for k, (h, e) in enumerate(hijos):
            self._dibujar(h, "  ", e, k == len(hijos) - 1)
        print("  Relaciones padre -> hijos:")
        self._relaciones(self.raiz)

    def _dibujar(self, nodo, prefijo, etiqueta, ultimo):
        print(prefijo + ("└── " if ultimo else "├── ") + f"{etiqueta}: {nodo.valor}")
        nuevo = prefijo + ("    " if ultimo else "│   ")
        hijos = [(h, e) for h, e in ((nodo.izq, "I"), (nodo.der, "D")) if h]
        for k, (h, e) in enumerate(hijos):
            self._dibujar(h, nuevo, e, k == len(hijos) - 1)

    def _relaciones(self, n):
        if not n:
            return
        izq = n.izq.valor if n.izq else "-"
        der = n.der.valor if n.der else "-"
        print(f"    {n.valor}: izquierdo={izq}, derecho={der}")
        self._relaciones(n.izq)
        self._relaciones(n.der)


def arbol():
    print("\n=== ÁRBOL BINARIO DE BÚSQUEDA ===")
    print("(Menores a la izquierda, mayores a la derecha; duplicados rechazados)")
    n = leer_cantidad(f"¿Cuántos valores va a insertar? (1-{LIMITE}): ")
    t = ABB()
    insertados = 0
    while insertados < n:
        v = leer_entero(f"  Valor #{insertados + 1} a insertar: ")
        if t.insertar(v):
            insertados += 1
        else:
            print(f"  [Error] El valor {v} ya existe en el árbol. Ingrese otro.")
    t.mostrar()
    total = n
    while True:
        op = menu("Operaciones del árbol",
                  ["Insertar valor", "Buscar valor", "Recorrido inorden",
                   "Recorrido preorden", "Recorrido postorden", "Mostrar árbol"])
        if op == 0:
            return
        if op == 1:
            if total >= LIMITE:
                print(f"  [Error] Se alcanzó el límite de {LIMITE} nodos.")
            elif t.insertar(leer_entero("  Valor a insertar: ")):
                total += 1
                t.mostrar()
            else:
                print("  [Error] El valor ya existe; el árbol no cambió.")
        elif op == 2:
            v = leer_entero("  Valor a buscar: ")
            ok, camino = t.buscar(v)
            print(f"  Camino recorrido: {camino}")
            print("  ¡Encontrado!" if ok else "  El dato NO existe en el árbol.")
        elif op in (3, 4, 5):
            r = []
            nombre = {3: "inorden (I-R-D)", 4: "preorden (R-I-D)", 5: "postorden (I-D-R)"}[op]
            {3: t.inorden, 4: t.preorden, 5: t.postorden}[op](t.raiz, r)
            print(f"  {nombre}: {r}")
        else:
            t.mostrar()


# ----------------------------------------------------------------------
# 7. GRAFO NO DIRIGIDO (lista de adyacencia)
# ----------------------------------------------------------------------
class Grafo:
    def __init__(self):
        self.ady = {}

    def agregar_vertice(self, v):
        if v in self.ady:
            return False
        self.ady[v] = []
        return True

    def agregar_arista(self, a, b):
        """Devuelve None si es válida o un mensaje de error."""
        if a not in self.ady or b not in self.ady:
            return "Uno o ambos vértices no existen."
        if a == b:
            return "No se permiten aristas de un vértice consigo mismo."
        if b in self.ady[a]:
            return "Esa arista ya existe."
        self.ady[a].append(b)
        self.ady[b].append(a)
        return None

    def bfs(self, inicio):
        visitados, orden, cola_ = {inicio}, [], deque([inicio])
        while cola_:
            v = cola_.popleft()
            orden.append(v)
            for w in self.ady[v]:
                if w not in visitados:
                    visitados.add(w)
                    cola_.append(w)
        return orden

    def dfs(self, inicio):
        visitados, orden, pila_ = set(), [], [inicio]
        while pila_:
            v = pila_.pop()
            if v in visitados:
                continue
            visitados.add(v)
            orden.append(v)
            for w in reversed(self.ady[v]):
                if w not in visitados:
                    pila_.append(w)
        return orden

    def mostrar(self):
        print("  Lista de adyacencia:")
        for v, vecinos in self.ady.items():
            print(f"    {v} -> {vecinos if vecinos else 'sin conexiones'}")
        aristas = {tuple(sorted((a, b))) for a in self.ady for b in self.ady[a]}
        print(f"  Vértices: {len(self.ady)} | Aristas: {len(aristas)}")


def grafo():
    print("\n=== GRAFO (no dirigido, sin lazos) ===")
    g = Grafo()
    n = leer_cantidad(f"¿Cuántos vértices tendrá el grafo? (1-{LIMITE}): ")
    while len(g.ady) < n:
        v = leer_id_vertice(f"  Identificador del vértice #{len(g.ady) + 1}: ")
        if not g.agregar_vertice(v):
            print(f"  [Error] El identificador '{v}' ya existe. Debe ser único.")
    maximo = n * (n - 1) // 2
    if maximo == 0:
        print("  Con un solo vértice no hay aristas posibles.")
        m = 0
    else:
        while True:
            m = leer_entero(f"¿Cuántas aristas va a ingresar? (0-{maximo}): ")
            if 0 <= m <= maximo:
                break
            print(f"  [Error] Debe estar entre 0 y {maximo}.")
    creadas = 0
    while creadas < m:
        print(f"  Arista #{creadas + 1}:")
        a = leer_id_vertice("    Vértice origen: ")
        b = leer_id_vertice("    Vértice destino: ")
        error = g.agregar_arista(a, b)
        if error:
            print(f"  [Error] {error} Intente de nuevo.")
        else:
            creadas += 1
    g.mostrar()
    while True:
        op = menu("Operaciones del grafo",
                  ["Agregar vértice", "Agregar arista", "Consultar vecinos",
                   "Recorrido en anchura (BFS)", "Recorrido en profundidad (DFS)",
                   "Mostrar grafo"])
        if op == 0:
            return
        if op == 1:
            if len(g.ady) >= LIMITE:
                print(f"  [Error] Límite de {LIMITE} vértices alcanzado.")
                continue
            v = leer_id_vertice("  Identificador del nuevo vértice: ")
            print("  Vértice agregado." if g.agregar_vertice(v)
                  else f"  [Error] El identificador '{v}' ya existe.")
        elif op == 2:
            a = leer_id_vertice("  Vértice origen: ")
            b = leer_id_vertice("  Vértice destino: ")
            error = g.agregar_arista(a, b)
            print(f"  [Error] {error}" if error else f"  Arista {a} -- {b} agregada.")
        elif op == 3:
            v = leer_id_vertice("  Vértice a consultar: ")
            if v not in g.ady:
                print("  [Error] Ese vértice no existe.")
            else:
                print(f"  Vecinos de {v}: {g.ady[v] if g.ady[v] else 'ninguno'}")
        elif op in (4, 5):
            inicio = leer_id_vertice("  Vértice inicial del recorrido: ")
            if inicio not in g.ady:
                print("  [Error] Ese vértice no existe.")
                continue
            orden = g.bfs(inicio) if op == 4 else g.dfs(inicio)
            print(f"  Recorrido desde {inicio}: {' -> '.join(orden)}")
            no_alcanzados = [v for v in g.ady if v not in orden]
            if no_alcanzados:
                print(f"  No alcanzables desde {inicio}: {no_alcanzados}")
            else:
                print("  Todos los vértices fueron alcanzados.")
        else:
            g.mostrar()


# ----------------------------------------------------------------------
# MENÚ PRINCIPAL
# ----------------------------------------------------------------------
def main():
    acciones = {1: arreglo, 2: matriz, 3: lista, 4: pila, 5: cola,
                6: arbol, 7: grafo, 8: comparar_pila_cola}
    while True:
        print("\n" + "=" * 44)
        print("   ESTRUCTURAS DE DATOS - MENÚ PRINCIPAL")
        print("=" * 44)
        for k, nombre in enumerate(["Arreglo unidimensional", "Matriz", "Lista",
                                    "Pila", "Cola", "Árbol binario de búsqueda",
                                    "Grafo", "Comparar pila y cola"], start=1):
            print(f"  {k}. {nombre}")
        print("  0. Salir")
        op = leer_entero("Seleccione una estructura: ")
        if op == 0:
            print("¡Hasta pronto!")
            break
        if op in acciones:
            acciones[op]()
        else:
            print("  [Error] Opción no válida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado por el usuario.")
