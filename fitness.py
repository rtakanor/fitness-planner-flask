class UserProfile:
    def __init__(self, edad, peso, altura, genero):
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.genero = genero.lower()

def calcular_bmr(user):
    if user.genero == "hombre":
        return 88.362 + (13.397 * user.peso) + (4.799 * user.altura) - (5.677 * user.edad)
    elif user.genero == "mujer":
        return 447.593 + (9.247 * user.peso) + (3.098 * user.altura) - (4.330 * user.edad)
    return 0

def calcular_tmr(user, actividad):
    if user.genero == "hombre":
        tmr = 10 * user.peso + 6.25 * user.altura - 5 * user.edad + 5
    elif user.genero == "mujer":
        tmr = 10 * user.peso + 6.25 * user.altura - 5 * user.edad - 161
    else:
        return 0

    factores = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
    return tmr * factores.get(actividad, 0)

rutinas = {
    "volumen": [
        "Pecho Pesado", "Espalda y Trapecio", "Piernas Cuadriceps",
        "Hombros y Abs", "Brazos", "Full Body Carga", "Descanso o Caminata"
    ],
    "definicion": [
        "HIIT + Abs", "Cardio y Piernas", "Full Body Circuit",
        "Boxeo o Funcional", "Cardio Largo", "Ligero + Core", "Descanso Activo"
    ],
    "dias": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
}
