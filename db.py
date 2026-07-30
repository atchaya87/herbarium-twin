import sqlite3
from datetime import datetime

DB_NAME = "herbarium_database.db"


def get_connection():
    """
    Create a database connection.
    """
    return sqlite3.connect(DB_NAME)


def db_init():
    """
    Create tables if they do not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boxes (
            box_id TEXT PRIMARY KEY,

            current_location TEXT,
            collection_area TEXT,
            material_type TEXT,

            estimated_packet_count TEXT,

            taxonomic_clues TEXT,
            geographic_clues TEXT,
            collector_clues TEXT,

            condition TEXT,
            processing_status TEXT,
            priority TEXT,

            human_notes TEXT,

            ai_summary TEXT,
            ai_confidence_notes TEXT,

            image_paths TEXT,

            date_inventoried TEXT,
            inventoried_by TEXT
        )
    """)

    conn.commit()
    conn.close()



def get_next_box_id():
    """
    Generates the next box ID.
    Example:
    HB001
    HB002
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT box_id 
        FROM boxes
        ORDER BY box_id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return "HB001"

    last_id = result[0]

    try:
        number = int(last_id.replace("HB", ""))
        return f"HB{number + 1:03d}"

    except:
        return "HB001"



def box_id_exists(box_id):
    """
    Check whether a box already exists.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1 
        FROM boxes 
        WHERE box_id = ?
        """,
        (box_id,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists



def save_box(data):
    """
    Save a completed herbarium box record.

    data should be a dictionary.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO boxes (
            box_id,
            current_location,
            collection_area,
            material_type,
            estimated_packet_count,
            taxonomic_clues,
            geographic_clues,
            collector_clues,
            condition,
            processing_status,
            priority,
            human_notes,
            ai_summary,
            ai_confidence_notes,
            image_paths,
            date_inventoried,
            inventoried_by
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["box_id"],
        data["current_location"],
        data["collection_area"],
        data["material_type"],
        data["estimated_packet_count"],
        data["taxonomic_clues"],
        data["geographic_clues"],
        data["collector_clues"],
        data["condition"],
        data["processing_status"],
        data["priority"],
        data["human_notes"],
        data["ai_summary"],
        data["ai_confidence_notes"],
        data["image_paths"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data["inventoried_by"]

    ))

    conn.commit()
    conn.close()



def get_all_boxes():
    """
    Retrieve all inventory records.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM boxes
        ORDER BY date_inventoried DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



def get_box(box_id):
    """
    Retrieve one box.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM boxes
        WHERE box_id = ?
    """, (box_id,))

    row = cursor.fetchone()

    conn.close()

    return row