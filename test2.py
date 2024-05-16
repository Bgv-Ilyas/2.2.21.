import psycopg2

# Функция для подключения к базе данных PostgreSQL
def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname="flight_management",
            user="postgres",
            password="123",
            host="localhost"
        )
        return connection
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)

# Функция для добавления нового пункта назначения
def add_destination(connection, destination_name):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO destinations (destination_name)
        VALUES (%s)
        RETURNING destination_id
    """, (destination_name,))
    destination_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return destination_id

# Функция для добавления нового рейса
def add_flight(connection, destination_id, flight_number, plane_type):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO flights (destination_id, flight_number, plane_type)
        VALUES (%s, %s, %s)
    """, (destination_id, flight_number, plane_type))
    connection.commit()
    cursor.close()
    print("Информация о рейсе добавлена.")

# Функция для вывода рейсов по пункту назначения
def display_flights_by_destination(connection, search_destination):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT f.flight_number, f.plane_type
        FROM flights f
        JOIN destinations d ON f.destination_id = d.destination_id
        WHERE d.destination_name = %s
    """, (search_destination,))
    matching_flights = cursor.fetchall()
    cursor.close()

    if matching_flights:
        print(f"Рейсы в пункт назначения '{search_destination}':")
        for flight_number, plane_type in matching_flights:
            print(f"Номер рейса: {flight_number}, Тип самолета: {plane_type}")
    else:
        print(f"Рейсов в пункт назначения '{search_destination}' не найдено.")

# Подключение к базе данных
connection = connect_to_database()

# Добавление пункта назначения "Москва"
moscow_destination_id = add_destination(connection, "Москва")

# Добавление рейса в Москву
add_flight(connection, moscow_destination_id, "SU123", "Boeing 737")

# Поиск рейсов в Москву
display_flights_by_destination(connection, "Москва")

# Закрытие соединения с базой данных
connection.close()
