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

import os
from models import FamilyTree
from file_handler import save_to_csv, load_from_csv
from search_sort import search_member, sort_members


# =========================
# UTILITAS TAMPILAN
# Fungsi bantu untuk mencetak UI di terminal
# =========================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def garis(char="-", lebar=50):
    print(char * lebar)


def judul(teks, lebar=50):
    print("+" + "-" * (lebar - 2) + "+")
    print("|" + teks.center(lebar - 2) + "|")
    print("+" + "-" * (lebar - 2) + "+")


def sub_judul(teks):
    print(f"\n-- {teks} --")
    garis()


# =========================
# INPUT NONEMPTY
# Meminta input dari user dan menolak string kosong
# =========================
def input_nonempty(prompt):

    while True:

        data = input(f"  {prompt}: ").strip()

        if data:
            return data

        print("  [!] Input tidak boleh kosong.")


# =========================
# INPUT NUMERIC ID
# Meminta input ID berupa angka saja
# =========================
def input_numeric_id(prompt):

    while True:

        data = input(f"  {prompt}: ").strip()

        if data.isdigit():
            return data

        print("  [!] ID harus angka.")


# =========================
# INPUT GENDER
# Meminta input gender dan memastikan nilainya L atau P
# =========================
def input_gender(prompt):

    while True:

        data = input(f"  {prompt} (L/P): ").strip().upper()

        if data in ["L", "P"]:
            return data

        print("  [!] Gender harus L atau P.")


# =========================
# INPUT PARENT ID
# Meminta input ID orang tua, boleh kosong (opsional),
# dan memvalidasi keberadaannya di data tree
# =========================
def input_parent_id(tree, prompt):

    while True:

        data = input(
            f"  {prompt} (kosong jika tidak ada): "
        ).strip()

        if data == "":
            return None

        if not data.isdigit():
            print("  [!] ID harus angka.")
            continue

        if data not in tree.members:
            print("  [!] ID tidak ditemukan.")
            continue

        return data


# =========================
# AUTO ID
# Menghasilkan ID baru secara otomatis berdasarkan ID terbesar yang ada
# =========================
def generate_member_id(tree):

    if not tree.members:
        return "1"

    max_id = max(int(mid) for mid in tree.members)

    return str(max_id + 1)


# =========================
# BANNER
# Tampilkan judul program saat pertama jalan
# =========================
def print_banner():

    print()
    print("+================================================+")
    print("|                                                |")
    print("|        PROGRAM SILSILAH KELUARGA               |")
    print("|              Kelompok 19                       |")
    print("|                                                |")
    print("+================================================+")
    print()


# =========================
# CETAK MENU
# Cetak daftar item menu dengan format rapi
# items : list of (nomor, label)
# =========================
def cetak_menu(items):

    garis()

    for num, label in items:
        print(f"  [{num:>2}] {label}")

    garis()


# =========================
# MAIN
# Fungsi utama yang menjalankan loop menu program
# =========================
def main():

    tree = FamilyTree()

    print_banner()

    load_from_csv(tree)

    while True:

        judul("MENU UTAMA")

        cetak_menu([
            ("1",  "Tambah anggota"),
            ("2",  "Tampilkan semua"),
            ("3",  "Detail anggota"),
            ("4",  "Update anggota"),
            ("5",  "Hapus anggota"),
            ("6",  "Cari anggota"),
            ("7",  "Tampilkan silsilah"),
            ("8",  "Simpan CSV"),
            ("9",  "Cek hubungan"),
            ("10", "Urutkan anggota"),
            ("0",  "Keluar"),
        ])

        choice = input("  Pilih menu: ").strip()

        # ── tambah ──
        if choice == "1":

            sub_judul("TAMBAH ANGGOTA")

            member_id = generate_member_id(tree)

            print(f"  ID otomatis : {member_id}\n")

            name      = input_nonempty("Nama")
            gender    = input_gender("Gender")
            father_id = input_parent_id(tree, "ID Ayah")

            # jika ayah diisi dan ayah punya pasangan,
            # ibu otomatis dari pasangan ayah — tidak perlu ditanya
            if father_id and tree.members[father_id].spouse_id:

                ibu = tree.members[
                    tree.members[father_id].spouse_id
                ]

                mother_id = ibu.member_id

                print(
                    f"  Ibu otomatis : "
                    f"{ibu.name} (ID {ibu.member_id})"
                )

            else:

                # ayah tidak ada / ayah jomblo → tanya ibu manual
                mother_id = input_parent_id(tree, "ID Ibu")

                # jika ibu diisi dan ibu punya pasangan,
                # ayah otomatis dari pasangan ibu — tidak perlu ditanya
                if (
                    mother_id
                    and not father_id
                    and tree.members[mother_id].spouse_id
                ):

                    ayah = tree.members[
                        tree.members[mother_id].spouse_id
                    ]

                    father_id = ayah.member_id

                    print(
                        f"  Ayah otomatis : "
                        f"{ayah.name} (ID {ayah.member_id})"
                    )

            spouse_id = input_parent_id(tree, "ID Pasangan")

            tree.add_member(
                member_id, name, gender,
                father_id, mother_id, spouse_id
            )

        # ── tampil semua ──
        elif choice == "2":

            sub_judul("DAFTAR ANGGOTA")

            tree.show_all_members()

        # ── detail ──
        elif choice == "3":

            sub_judul("DETAIL ANGGOTA")

            member_id = input_numeric_id("ID anggota")

            tree.show_member_detail(member_id)

        # ── update ──
        elif choice == "4":

            sub_judul("UPDATE ANGGOTA")

            member_id = input_numeric_id("ID anggota")

            if member_id not in tree.members:
                print("  [!] Anggota tidak ditemukan.")
                continue

            print(f"  Data saat ini: {tree.members[member_id]}\n")

            new_name = input(
                "  Nama baru (kosong = tidak diubah): "
            ).strip()

            new_gender = ""

            new_spouse_raw = input(
                "  ID pasangan baru"
                " (kosong = tidak diubah, '-' = cerai): "
            ).strip()

            new_name   = new_name or None
            new_gender = new_gender if new_gender in ["L", "P"] else None

            if new_spouse_raw == "":
                new_spouse_id = None
            elif new_spouse_raw == "-":
                new_spouse_id = ""
            else:
                new_spouse_id = new_spouse_raw

            tree.update_member(
                member_id, new_name, new_gender, new_spouse_id
            )

        # ── hapus ──
        elif choice == "5":

            sub_judul("HAPUS ANGGOTA")

            member_id = input_numeric_id("ID anggota")

            if member_id not in tree.members:
                print("  [!] Anggota tidak ditemukan.")
                continue

            m = tree.members[member_id]

            print(f"  Akan menghapus : {m.name} (ID {member_id})")

            konfirm = input(
                "  Ketik 'ya' untuk konfirmasi: "
            ).strip().lower()

            if konfirm != "ya":
                print("  Penghapusan dibatalkan.")
                continue

            tree.delete_member(member_id)

        # ── cari ──
        elif choice == "6":

            sub_judul("CARI ANGGOTA")

            keyword = input_nonempty("Nama atau ID")

            search_member(tree, keyword)

        # ── silsilah ──
        elif choice == "7":

            tree.show_family_tree()

        # ── simpan ──
        elif choice == "8":

            save_to_csv(tree)

        # ── hubungan ──
        elif choice == "9":

            while True:

                judul("CEK HUBUNGAN")

                cetak_menu([
                    ("1", "Cek hubungan 2 arah"),
                    ("2", "Cek relasi lengkap"),
                    ("0", "Kembali"),
                ])

                sub = input("  Pilih menu: ").strip()

                if sub == "0":
                    break

                elif sub == "1":

                    sub_judul("HUBUNGAN 2 ARAH")

                    id1 = input_numeric_id("ID orang pertama")
                    id2 = input_numeric_id("ID orang kedua")

                    if (
                        id1 not in tree.members
                        or id2 not in tree.members
                    ):
                        print("  [!] Anggota tidak ditemukan.")
                        continue

                    p1  = tree.members[id1]
                    p2  = tree.members[id2]
                    r12 = tree.get_relationship_status(id1, id2)
                    r21 = tree.get_relationship_status(id2, id1)

                    print()
                    garis()
                    print(
                        f"  {p1.name:<20} terhadap"
                        f" {p2.name:<20} : {r12}"
                    )
                    print(
                        f"  {p2.name:<20} terhadap"
                        f" {p1.name:<20} : {r21}"
                    )
                    garis()

                elif sub == "2":

                    sub_judul("RELASI LENGKAP")

                    id1 = input_numeric_id("ID anggota")

                    if id1 not in tree.members:
                        print("  [!] Anggota tidak ditemukan.")
                        continue

                    p1  = tree.members[id1]
                    ada = False

                    print()
                    garis()
                    print(f"  Relasi milik : {p1.name}")
                    garis()

                    for id2 in tree.members:

                        if id2 == id1:
                            continue

                        rels = tree.get_all_relations(id1, id2)

                        if not rels:
                            continue

                        for label, value in rels.items():
                            print(f"  {label:<25}: {value}")
                            ada = True

                    if not ada:
                        print(
                            f"  {p1.name} tidak memiliki"
                            f" relasi yang tercatat."
                        )

                    garis()

                else:
                    print("  [!] Menu tidak valid.")

        # ── urutkan ──
        elif choice == "10":

            judul("URUTKAN ANGGOTA")

            cetak_menu([
                ("1", "Nama"),
                ("2", "ID"),
                ("3", "Generasi"),
                ("4", "Gender"),
                ("5", "Ayah ID"),
                ("6", "Ibu ID"),
            ])

            sort_choice = input("  Pilih kriteria: ").strip()

            sort_map = {
                "1": "name",      "2": "id",
                "3": "generation","4": "gender",
                "5": "father_id", "6": "mother_id",
            }

            if sort_choice not in sort_map:
                print("  [!] Kriteria tidak valid.")
                continue

            sort_by = sort_map[sort_choice]

            print()
            print("  [1] Naik  (A-Z / 0-9)")
            print("  [2] Turun (Z-A / 9-0)")
            print()

            order = input("  Pilih urutan: ").strip()

            if order == "1":
                reverse = False
            elif order == "2":
                reverse = True
            else:
                print("  [!] Urutan tidak valid.")
                continue

            sort_members(tree, by=sort_by, reverse=reverse)

        # ── keluar ──
        elif choice == "0":

            save_to_csv(tree)
            print()
            garis()
            print("  Data tersimpan. Program selesai.")
            garis()
            print()
            break

        else:

            print("  [!] Menu tidak valid.")


# =========================
# RUN
# Titik masuk eksekusi program
# =========================
if __name__ == "__main__":
    main()