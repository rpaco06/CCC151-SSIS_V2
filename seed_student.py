import mysql.connector
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="iLOVEmyFAMILY<3",
    database="ssis_v2"
)
cursor = conn.cursor()

firstnames = [
    "Juan", "Maria", "Jose", "Ana", "Carlos", "Rosa", "Miguel", "Sofia",
    "Luis", "Elena", "Marco", "Isabel", "Paolo", "Camille", "Andrei",
    "Bea", "Rico", "Gina", "Nathan", "Trisha", "Kevin", "Liza", "Ryan",
    "Jasmine", "Mark", "Carla", "James", "Patricia", "John", "Angela",
    "Daniel", "Hannah", "Gabriel", "Isabelle", "Jerome", "Katrina",
    "Lance", "Monica", "Noel", "Olivia", "Patrick", "Queen", "Rafael",
    "Samantha", "Tristan", "Uma", "Victor", "Wendy", "Xavier", "Yvonne",
    "Aaron", "Bianca", "Clarence", "Danielle", "Erwin", "Faith", "Gerald",
    "Hazel", "Ivan", "Jennie", "Karl", "Lovely", "Mario", "Nina", "Oscar"
]

lastnames = [
    "Santos", "Reyes", "Cruz", "Bautista", "Ocampo", "Garcia", "Torres",
    "Flores", "Villanueva", "Ramos", "Mendoza", "Dela Cruz", "Aquino",
    "Castillo", "Morales", "Gonzales", "Rivera", "Hernandez", "Lopez",
    "Perez", "Diaz", "Navarro", "Medina", "Aguilar", "Domingo", "Pascual",
    "Salazar", "Enriquez", "Soriano", "Lim", "Tan", "Go", "Sy", "Uy",
    "Dela Torre", "De Leon", "San Pedro", "Del Rosario", "De Guzman",
    "Villafuerte", "Macaraeg", "Buenaventura", "Evangelista", "Tolentino"
]

programs = [
    "BAEN", "BSPY", "BAFIL", "BAHIS", "BAPOL",
    "BSCE", "BSCER", "BSCHEM", "BSCPE", "BSECE",
    "BSEE", "BSMINE", "BSENVT", "BSME", "BSMET",
    "BSANBIO", "BSPLBIO", "BSMARBIO", "BSMICRO",
    "BSCHEM2", "BSMATH", "BSPHY", "BSSTAT",
    "BSED", "BEED",
    "BSBA", "BSHTM", "BSACCT",
    "BSIS", "BSIT", "BSCS",
    "BSN"
]

genders = ["Male", "Female"]
years   = ["1", "2", "3", "4"]

used_ids = set()
students = []

for year_prefix in range(2022, 2026):
    for _ in range(1250):
        while True:
            number = random.randint(1, 9999)
            sid    = f"{year_prefix}-{number:04d}"
            if sid not in used_ids:
                used_ids.add(sid)
                break

        yr = str(2026 - year_prefix)

        students.append((
            sid,
            random.choice(firstnames),
            random.choice(lastnames),
            random.choice(programs),
            yr,
            random.choice(genders)
        ))

cursor.executemany(
    "INSERT INTO student (id, firstname, lastname, course, year, gender) VALUES (%s, %s, %s, %s, %s, %s)",
    students
)

conn.commit()
print(f"Successfully inserted {len(students)} students!")
cursor.close()
conn.close()