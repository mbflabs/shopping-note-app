import mysql.connector
from mysql.connector import Error

# Koneksi ke database (ubah sesuai setting MySQL kamu)
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='belanja_db',
            user='root',
            password=''  # isi password MySQL kamu
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Buat tabel jika belum ada
def setup_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catatan_belanja (
            id INT AUTO_INCREMENT PRIMARY KEY,
            barang VARCHAR(100) NOT NULL,
            jumlah INT NOT NULL
        )
    ''')
    conn.commit()

# Tambah barang
def tambah_barang(conn, barang, jumlah):
    cursor = conn.cursor()
    sql = "INSERT INTO catatan_belanja (barang, jumlah) VALUES (%s, %s)"
    cursor.execute(sql, (barang, jumlah))
    conn.commit()
    print(f"Berhasil tambah: {barang} ({jumlah})")

# Lihat semua barang
def lihat_semua(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catatan_belanja")
    hasil = cursor.fetchall()
    if not hasil:
        print("Belum ada data.")
    else:
        for row in hasil:
            print(f"ID: {row[0]}, Barang: {row[1]}, Jumlah: {row[2]}")

# Update barang
def update_barang(conn, id_barang, barang_baru, jumlah_baru):
    cursor = conn.cursor()
    sql = "UPDATE catatan_belanja SET barang=%s, jumlah=%s WHERE id=%s"
    cursor.execute(sql, (barang_baru, jumlah_baru, id_barang))
    conn.commit()
    print(f"ID {id_barang} berhasil diupdate.")

# Hapus barang
def hapus_barang(conn, id_barang):
    cursor = conn.cursor()
    sql = "DELETE FROM catatan_belanja WHERE id=%s"
    cursor.execute(sql, (id_barang,))
    conn.commit()
    print(f"ID {id_barang} berhasil dihapus.")

# Menu utama
def menu():
    conn = create_connection()
    if conn is None:
        return
    setup_table(conn)

    while True:
        print("\n=== APLIKASI CATATAN BELANJA ===")
        print("1. Tambah barang")
        print("2. Lihat semua barang")
        print("3. Update barang")
        print("4. Hapus barang")
        print("5. Keluar")
        pilih = input("Pilih menu: ")

        if pilih == '1':
            barang = input("Nama barang: ")
            jumlah = int(input("Jumlah: "))
            tambah_barang(conn, barang, jumlah)
        elif pilih == '2':
            lihat_semua(conn)
        elif pilih == '3':
            id_barang = int(input("ID barang yang akan diupdate: "))
            barang_baru = input("Nama baru: ")
            jumlah_baru = int(input("Jumlah baru: "))
            update_barang(conn, id_barang, barang_baru, jumlah_baru)
        elif pilih == '4':
            id_barang = int(input("ID barang yang akan dihapus: "))
            hapus_barang(conn, id_barang)
        elif pilih == '5':
            print("Terima kasih!")
            break
        else:
            print("Menu tidak valid.")

    conn.close()

if __name__ == "__main__":
    menu()
