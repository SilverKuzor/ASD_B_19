# =============================
# main.py
# Entry point program Silsilah Keluarga.
# Menangani menu utama dan interaksi dengan pengguna.
# =============================
#
# KELOMPOK 19
# J0403251020 - Bunga Auppa Anpal
# J0403251054 - Rieska Riza
# J0403251137 - Muhammad Faqih Husnan
# =============================

from models import FamilyTree
from file_handler import save_to_csv, load_from_csv
from search_sort import search_member, sort_members


# =========================
# INPUT NONEMPTY
# Meminta input dari user dan menolak string kosong
# =========================
def input_nonempty(prompt):

    while True:

        data = input(prompt).strip()

        if data:
            return data

        print("Input tidak boleh kosong.")


# =========================
# INPUT NUMERIC ID
# Meminta input ID berupa angka saja
# =========================
def input_numeric_id(prompt):

    while True:

        data = input(prompt).strip()

        if data.isdigit():
            return data

        print("ID harus angka.")


# =========================
# INPUT GENDER
# Meminta input gender dan memastikan nilainya L atau P
# =========================
def input_gender(prompt):

    while True:

        gender = input(prompt).strip().upper()

        if gender in ["L", "P"]:
            return gender

        print("Gender harus L/P.")


# =========================
# INPUT PARENT ID
# Meminta input ID orang tua, boleh kosong (opsional),
# dan memvalidasi keberadaannya di data tree
# =========================
def input_parent_id(tree, prompt):

    while True:

        data = input(prompt).strip()

        if data == "":
            return None

        if not data.isdigit():

            print("ID harus angka.")
            continue

        if data not in tree.members:

            print("ID tidak ditemukan.")
            continue

        return data


# =========================
# AUTO ID
# Menghasilkan ID baru secara otomatis berdasarkan ID terbesar yang ada
# =========================
def generate_member_id(tree):

    if not tree.members:
        return "1"

    max_id = max(
        int(member_id)
        for member_id in tree.members
    )

    return str(max_id + 1)


# =========================
# MAIN
# Fungsi utama yang menjalankan loop menu program
# =========================
def main():

    tree = FamilyTree()

    load_from_csv(tree)

    while True:

        print("\n===== MENU =====")
        print("1. Tambah anggota")
        print("2. Tampilkan semua")
        print("3. Detail anggota")
        print("4. Update anggota")
        print("5. Hapus anggota")
        print("6. Cari anggota")
        print("7. Tampilkan tree")
        print("8. Simpan CSV")
        print("9. Cek hubungan")
        print("10. Urutkan anggota")
        print("0. Keluar")

        choice = input("Pilih menu: ").strip()

        # tambah
        if choice == "1":

            member_id = generate_member_id(tree)

            print(f"ID otomatis: {member_id}")

            name = input_nonempty(
                "Masukkan nama: "
            )

            gender = input_gender(
                "Masukkan gender (L/P): "
            )

            father_id = input_parent_id(
                tree,
                "ID Ayah (kosong jika tidak ada): "
            )

            mother_id = input_parent_id(
                tree,
                "ID Ibu (kosong jika tidak ada): "
            )

            spouse_id = input_parent_id(
                tree,
                "ID Pasangan (kosong jika tidak ada): "
            )

            tree.add_member(
                member_id,
                name,
                gender,
                father_id,
                mother_id,
                spouse_id
            )

        # tampil semua
        elif choice == "2":

            tree.show_all_members()

                # detail
        elif choice == "3":

            while True:

                print("\n=== MENU DETAIL ===")
                print("1. Lihat detail anggota")
                print("0. Kembali")

                sub = input(
                    "Pilih menu: "
                ).strip()

                # detail anggota
                if sub == "1":

                    member_id = input_numeric_id(
                        "Masukkan ID anggota: "
                    )

                    tree.show_member_detail(
                        member_id
                    )

                # kembali
                elif sub == "0":

                    break

                else:

                    print("Menu tidak valid.")

        # update
        elif choice == "4":

            while True:

                print("\n=== MENU UPDATE ===")
                print("1. Update anggota")
                print("0. Kembali")

                sub = input(
                    "Pilih menu: "
                ).strip()

                # update anggota
                if sub == "1":

                    member_id = input_numeric_id(
                        "Masukkan ID anggota: "
                    )

                    new_name = input(
                        "Nama baru "
                        "(kosong jika tidak diubah): "
                    ).strip()

                    new_gender = input(
                        "Gender baru L/P "
                        "(kosong jika tidak diubah): "
                    ).strip().upper()

                    new_spouse_id = input(
                        "ID pasangan baru "
                        "(kosong = tidak diubah, "
                        "'-' = cerai): "
                    ).strip()

                    if new_name == "":
                        new_name = None

                    if new_gender == "":
                        new_gender = None

                    if new_spouse_id == "":
                        new_spouse_id = None

                    elif new_spouse_id == "-":
                        new_spouse_id = ""

                    tree.update_member(
                        member_id,
                        new_name,
                        new_gender,
                        new_spouse_id
                    )

                # kembali
                elif sub == "0":

                    break

                else:

                    print("Menu tidak valid.")

        # hapus
        elif choice == "5":

            while True:

                print("\n=== MENU HAPUS ===")
                print("1. Hapus anggota")
                print("0. Kembali")

                sub = input(
                    "Pilih menu: "
                ).strip()

                # hapus anggota
                if sub == "1":

                    member_id = input_numeric_id(
                        "Masukkan ID anggota: "
                    )

                    tree.delete_member(
                        member_id
                    )

                # kembali
                elif sub == "0":

                    break

                else:

                    print("Menu tidak valid.")

        # cari
        elif choice == "6":

            while True:

                print("\n=== MENU CARI ===")
                print("1. Cari anggota")
                print("0. Kembali")

                sub = input(
                    "Pilih menu: "
                ).strip()

                # cari anggota
                if sub == "1":

                    keyword = input_nonempty(
                        "Masukkan nama / ID: "
                    )

                    search_member(
                        tree,
                        keyword
                    )

                # kembali
                elif sub == "0":

                    break

                else:

                    print("Menu tidak valid.")

        # tree
        elif choice == "7":

            tree.show_family_tree()

        # save
        elif choice == "8":

            save_to_csv(tree)

        # relasi
        elif choice == "9":

                    id1 = input_numeric_id(
                        "ID orang pertama: "
                    )

                    id2 = input_numeric_id(
                        "ID orang kedua: "
                    )

                    if (
                        id1 not in tree.members
                        or id2 not in tree.members
                    ):

                        print("Anggota tidak ditemukan.")
                        continue

                    person1 = tree.members[id1]
                    person2 = tree.members[id2]

                    result = tree.get_relationship_status(
                        id1,
                        id2
                    )

                    print("\n=== HASIL RELASI ===")

                    print(
                        f"{person1.name} "
                        f"<-> "
                        f"{person2.name}"
                    )

                    print(f"Relasi : {result}")
                    continue


        # urutkan
        elif choice == "10":

            while True:

                print("\n=== MENU URUTKAN ===")
                print("1. Nama")
                print("2. ID")
                print("3. Generasi")
                print("4. Gender")
                print("0. Kembali")

                sort_choice = input(
                    "Pilih kriteria: "
                ).strip()

                # kembali
                if sort_choice == "0":

                    break

                sort_by = None

                if sort_choice == "1":

                    sort_by = "name"

                elif sort_choice == "2":

                    sort_by = "id"

                elif sort_choice == "3":

                    sort_by = "generation"

                elif sort_choice == "4":

                    sort_by = "gender"

                else:

                    print(
                        "Kriteria urut tidak valid."
                    )

                    continue

                print("\n=== MENU URUTAN ===")
                print("1. Naik")
                print("2. Menurun")

                order_choice = input(
                    "Pilih urutan: "
                ).strip()

                if order_choice == "1":

                    reverse = False

                elif order_choice == "2":

                    reverse = True

                else:

                    print("Urutan tidak valid.")

                    continue

                sort_members(
                    tree,
                    by=sort_by,
                    reverse=reverse
                )

        # keluar
        elif choice == "0":

            save_to_csv(tree)

            print("Program selesai.")
            break

        else:

            print("Menu tidak valid.")


# =========================
# RUN
# Titik masuk eksekusi program
# =========================
if __name__ == "__main__":
    main()
