import sqlite3
import os


def create_database():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))


    # Path for the database file
    db_path = os.path.join('school.db')

    try:
        # Connect to the database (creates file if it doesn't exist)
        print(f"Creating database at: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if school_queries.sql exists in the same directory as this script
        sql_file_path = os.path.join(current_dir, 'school_queries.sql')

        if not os.path.exists(sql_file_path):
            # If not found, try to find it in the current directory
            print(f"SQL file not found at: {sql_file_path}")
            sql_file_path = 'school_queries.sql'

            if not os.path.exists(sql_file_path):
                print(" Error: school_queries.sql file not found")
                print("   Please make sure school_queries.sql is in the same directory as this script")
                return

        # Read the SQL script file
        print("Reading SQL script...")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Execute the entire SQL script
        print("Executing SQL script...")
        cursor.executescript(sql_script)

        # Commit all changes
        conn.commit()
        print(" Database successfully created:", db_path)
        print(" Tables created and populated with data")
        print(" Indexes created for query optimization")

        # Show database statistics
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM grades")
        grade_count = cursor.fetchone()[0]

        print("\n Database Statistics:")
        print(f"   Students: {student_count}")
        print(f"   Grades: {grade_count}")

        # Show table structure
        print("\n Table Structure:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   Table: {table[0]}")

        # Test one of the queries
        print("\n Testing Query 7 (Top 3 students):")
        cursor.execute("""
            SELECT 
                s.full_name,
                ROUND(AVG(g.grade), 2) as average_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name
            ORDER BY average_grade DESC
            LIMIT 3;
        """)

        top_students = cursor.fetchall()
        for i, student in enumerate(top_students, 1):
            print(f"   {i}. {student[0]}: {student[1]}")

    except sqlite3.Error as e:
        print(f" SQL Error: {e}")
        print(f"   Database path: {db_path}")
        print(f"   Current directory: {current_dir}")
    except Exception as e:
        print(f" Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the database connection
        if 'conn' in locals():
            conn.close()
            print("\n Database connection closed")


# Create the database
create_database()