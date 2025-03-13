## Asegurate de tener instalado GitPython
## `pip install GitPython`
## Copia este script en la carpeta del repositorio local
## Ejecuta el script con Python 3
## `python3 checkdam.py`


from git import Repo
import os

# Configuración
REPO_PATH = "../calc-kotlin-dam"  # Ruta del repositorio local

COMMIT_INITIAL_MESSAGE = "Commit inicial"
COMMIT_DIVISION_ERROR_MESSAGE = "Funcionalidad dividir con error"
COMMIT_DIVISION_MESSAGE = "Funcionalidad dividir sin error"
COMMIT_SUMA_MESSAGE = "Funcionalidad sumar"
COMMIT_RESTA_MESSAGE = "Funcionalidad restar"
COMMIT_SUMA_CONFLICTO_MESSAGE = "Conflicto suma resuelto"
COMMIT_RESTA_CONFLICTO_MESSAGE = "Conflicto resta resuelto"
PRINCIPAL_BRANCH = "main"
FEATURE_DIVISION_BRANCH = "feature/division"
FEATURE_SUMA_BRANCH = "feature/suma"
FEATURE_RESTA_BRANCH = "feature/resta"
TOTAL_SCORE = 0
COMMENTS = []



# Función para verificar ramas y origen
def check_branch_from_initial_commit(repo, branch_name, parent_branch_name, initial_commit_message):
    """
    Verifica si una rama existe y si se creó desde un commit específico.

    :param repo: Repositorio GitPython.
    :param branch_name: Nombre de la rama a verificar.
    :param parent_branch_name: Nombre de la rama de la que se parte (por ejemplo, "main").
    :param commit_message: Mensaje del commit que debe ser el punto de partida.
    :return: True si la rama existe y se creó desde el commit específico, False en caso contrario.
    """
    # Verificar si las ramas existen
    if branch_name not in [branch.name for branch in repo.branches]:
        return False
    if parent_branch_name not in [branch.name for branch in repo.branches]:
        return False

    # Obtener el commit específico
    target_commit = None
    for commit in repo.iter_commits():
        if commit.message.strip() == initial_commit_message:
            target_commit = commit
            break

    if not target_commit:
        return False  # No se encontró el commit específico

    # Obtener las ramas
    branch = repo.branches[branch_name]
    parent_branch = repo.branches[parent_branch_name]

    # Obtener el primer commit de la rama
    first_commit = None
    for commit in repo.iter_commits(branch, max_count=1):
        first_commit = commit
        break

    # Obtener el historial de la rama padre hasta el commit específico
    parent_history = list(repo.iter_commits(parent_branch, max_count=1000))  # Ajusta el límite si es necesario

    # Verificar si el commit específico está en el historial de la rama padre
    if target_commit not in parent_history:
        return False

    # Verificar que el primer commit de la rama tiene al commit específico como su único padre
    if len(first_commit.parents) == 1 and first_commit.parents[0] == target_commit:
        return True

    return False

# Función para verificar commits
def check_commit(repo, message):
    for commit in repo.iter_commits():
        if message in commit.message:
            return True
    return False

# Función para verificar ramas
def check_branch(repo, branch_name):
    return branch_name in [branch.name for branch in repo.branches]

# Función para verificar merges
def check_merge(repo, branch_name):
    for commit in repo.iter_commits():
        # Verificar si el commit es un merge (tiene más de un parent)
        if len(commit.parents) > 1:
            # Verificar si la rama está involucrada en el merge
            for parent in commit.parents:
                if branch_name in parent.name_rev:
                    return True
    return False

# Función para verificar contenido del archivo
def check_file_content(file_path, expected_content):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read()
            return expected_content in content
    return False


################################################################
###################### PROGRAMA PRINCIPAL ######################
################################################################

# Inicializar el repositorio
repo = Repo(REPO_PATH)

# obtener nombre de usuario Git
user_name = repo.config_reader().get_value("user", "name")

# Punto 1: Crear repositorio en GitHub y vincularlo
if os.path.exists(REPO_PATH):
    COMMENTS.append("✅ Repositorio local creado y vinculado.")
    TOTAL_SCORE += 5
else:
    COMMENTS.append("❌ Repositorio local no creado o no vinculado.")

# Punto 2: Commit inicial
if check_commit(repo, COMMIT_INITIAL_MESSAGE) and \
        check_file_content("Calc.kt","fun multiplica(num1: Int, num2: Int): Int"):
    COMMENTS.append("✅ Commit inicial y codigo encontrado.")
    TOTAL_SCORE += 10
else:
    COMMENTS.append("❌ Commit inicial erroneo o codigo no encontrado.")

# Punto 3: Crear rama feature/division y añadir división sin control de errores
if check_branch(repo, FEATURE_DIVISION_BRANCH):
    COMMENTS.append("✅ Rama 'feature/division' encontrada.")
    TOTAL_SCORE += 5
else:
    COMMENTS.append("❌ Rama 'feature/division' no encontrada.")


# Punto 5: Revocar merge y commit de división sin control de errores
if check_branch(repo, FEATURE_DIVISION_BRANCH) and \
        not check_commit(repo, COMMIT_DIVISION_ERROR_MESSAGE) and \
        not check_file_content("Calc.kt", "fun divideE(num1: Int, num2: Int): Int"):
    COMMENTS.append("✅ Revocación de merge y commit.")
    TOTAL_SCORE += 15
else:
    COMMENTS.append("❌ Revocación de merge y commit erronea.")


# Punto 6: Corregir división y realizar commit
if check_file_content("Calc.kt", "if (num2 == 0)") and \
        check_file_content("Calc.kt", '"divide" -> divide(num1, num2)'):
    COMMENTS.append("✅ División corregida con control de errores.")
    TOTAL_SCORE += 10
else:
    COMMENTS.append("❌ División no corregida o código incorrecto.")

# Punto 4 y 7: Merge final de feature/division en main
if check_merge(repo, FEATURE_DIVISION_BRANCH) and \
        check_commit(repo, COMMIT_DIVISION_MESSAGE):
    COMMENTS.append("✅ Merge final de 'feature/division' encontrado.")
    TOTAL_SCORE += 10
else:
    COMMENTS.append("❌ Merge final de 'feature/division' no encontrado.")

# Punto 8: Crear ramas feature/suma y feature/resta desde commit inicial
if check_branch_from_initial_commit(repo, FEATURE_SUMA_BRANCH, PRINCIPAL_BRANCH, COMMIT_INITIAL_MESSAGE):
    COMMENTS.append("✅ Rama 'feature/suma' encontrada.")
    TOTAL_SCORE += 5
else:
    COMMENTS.append("❌ Rama 'feature/suma' no encontrada o con origen erroneo.")

if check_branch_from_initial_commit(repo, FEATURE_RESTA_BRANCH, PRINCIPAL_BRANCH, COMMIT_INITIAL_MESSAGE) :
    COMMENTS.append("✅ Rama 'feature/resta' encontrada.")
    TOTAL_SCORE += 5
else:
    COMMENTS.append("❌ Rama 'feature/resta' no encontrada o con origen erroneo.")

# Punto 9: Añadir funcionalidad de suma en feature/suma
if check_file_content("Calc.kt", "fun suma(num1: Int, num2: Int): Int") and \
        check_file_content("Calc.kt", '"suma" -> suma(num1, num2)') and \
        check_commit(repo, COMMIT_SUMA_MESSAGE):
    COMMENTS.append("✅ Función de suma añadida.")
    TOTAL_SCORE += 10
else:
    COMMENTS.append("❌ Función de suma no añadida o código incorrecto.")

# Punto 10: Añadir funcionalidad de resta en feature/resta
if check_file_content("Calc.kt", "fun resta(num1: Int, num2: Int): Int") and \
        check_file_content("Calc.kt", '"resta" -> resta(num1, num2)') and \
        check_commit(repo, COMMIT_RESTA_MESSAGE):
    COMMENTS.append("✅ Función de resta añadida.")
    TOTAL_SCORE += 10
else:
    COMMENTS.append("❌ Función de resta no añadida o código incorrecto.")

# Punto 11: Merge de feature/suma y feature/resta con resolución de conflictos
if check_merge(repo, FEATURE_SUMA_BRANCH) and \
        check_commit(repo, COMMIT_SUMA_CONFLICTO_MESSAGE):
    COMMENTS.append("✅ Merge de 'feature/suma' y conflicto resuelto encontrado.")
    TOTAL_SCORE += 7
else:
    COMMENTS.append("❌ Merge de 'feature/suma' o conflicto resuelto no encontrado.")

if check_merge(repo, FEATURE_RESTA_BRANCH) and \
        check_commit(repo, COMMIT_RESTA_CONFLICTO_MESSAGE):
    COMMENTS.append("✅ Merge de 'feature/resta' y conflicto resuelto encontrado.")
    TOTAL_SCORE += 8
else:
    COMMENTS.append("❌ Merge de 'feature/resta' o conflicto resuelto no encontrado.")

# Mostrar informe
print("📝 Informe de Evaluación:")
for comment in COMMENTS:
    print(comment)
print(f"📊 Puntuación final {user_name}: {TOTAL_SCORE}/100")