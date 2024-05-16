#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import argparse

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Destinations (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        UNIQUE(name)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Flights (
                        id INTEGER PRIMARY KEY,
                        destination_id INTEGER NOT NULL,
                        flight_number TEXT NOT NULL,
                        plane_type TEXT NOT NULL,
                        FOREIGN KEY (destination_id) REFERENCES Destinations(id)
                    )''')
    conn.commit()

def add_destination(conn, destination):
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO Destinations (name) VALUES (?)''', (destination,))
    conn.commit()

def add_flight(conn, destination_id, flight_number, plane_type):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Flights (destination_id, flight_number, plane_type) VALUES (?, ?, ?)''',
                   (destination_id, flight_number, plane_type))
    conn.commit()

def display_flights_by_destination(conn, search_destination):
    cursor = conn.cursor()
    cursor.execute('''SELECT Flights.flight_number, Flights.plane_type
                      FROM Flights
                      JOIN Destinations ON Flights.destination_id = Destinations.id
                      WHERE Destinations.name = ?''', (search_destination,))
    flights = cursor.fetchall()

    if flights:
        print(f"Рейсы в пункт назначения '{search_destination}':")
        for flight_number, plane_type in flights:
            print(f"Номер рейса: {flight_number}, Тип самолета: {plane_type}")
    else:
        print(f"Рейсов в пункт назначения '{search_destination}' не найдено.")

def main():
    parser = argparse.ArgumentParser(description="Flight Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-d", "--destination", help="Destination to search flights for")
    args = parser.parse_args()

    conn = sqlite3.connect('flights.db')
    create_tables(conn)

    if args.add_flight:
        destination = input("Введите пункт назначения: ")
        flight_number = input("Введите номер рейса: ")
        plane_type = input("Введите тип самолета: ")

        add_destination(conn, destination)
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM Destinations WHERE name = ?''', (destination,))
        destination_id = cursor.fetchone()[0]

        add_flight(conn, destination_id, flight_number, plane_type)
        print("Информация о рейсе добавлена.")
    elif args.destination:
        display_flights_by_destination(conn, args.destination)
    else:
        print("Некорректные аргументы командной строки.")

    conn.close()

if __name__ == "__main__":
    main()
