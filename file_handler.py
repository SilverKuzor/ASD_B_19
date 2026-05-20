# =============================
# file_handler.py
# Berisi fungsi untuk menyimpan dan memuat data
# pohon keluarga dari file CSV.
# =============================

import csv
import os

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keluarga.csv")


# =========================
# SAVE CSV
# Menyimpan seluruh data pohon keluarga ke file CSV
# =========================
def save_to_csv(tree):

    try:

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "name",
                    "gender",
                    "father_id",
                    "mother_id",
                    "spouse_id"
                ]
            )

            writer.writeheader()
            writer.writerows(tree.get_all_data())

        print("Data berhasil disimpan.")

    except Exception as e:

        print(f"Gagal menyimpan: {e}")


# =========================
# LOAD CSV
# Memuat data pohon keluarga dari file CSV ke dalam objek tree
# =========================
def load_from_csv(tree):

    if not os.path.exists(CSV_FILE):
        return

    try:

        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            rows = list(reader)

        tree.build_from_rows(rows)

        print("Data berhasil dimuat.")

    except Exception as e:

        print(f"Gagal membaca CSV: {e}")
