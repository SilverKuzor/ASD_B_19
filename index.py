
# Kelmopok 19
# Silsila
#
#
#
import csv
import os
class FamilyMember:
    def __init__(self, member_id, name, gender, parent_id=None):
        self.member_id = str(member_id)
        self.name = name
        self.gender = gender
        self.parent_id = str(parent_id) if parent_id is not None else None
        self.children = []

    def to_dict(self):
        return {
            "id": self.member_id,
            "name": self.name,
            "gender": self.gender,
            "parent_id": self.parent_id if self.parent_id is not None else ""
        }

    def __str__(self):
        parent_text = self.parent_id if self.parent_id else "-"
        return f"ID: {self.member_id} | Nama: {self.name} | Gender: {self.gender} | Parent ID: {parent_text}"


class FamilyTree:
    def __init__(self):
        self.members = {}
        self.root_ids = []

    # =========================
    # CREATE
    # =========================
    def add_member(self, member_id, name, gender, parent_id=None):
        member_id = str(member_id)
        parent_id = str(parent_id) if parent_id not in [None, ""] else None

        if member_id in self.members:
            print("Gagal: ID sudah dipakai.")
            return False

        if parent_id is not None and parent_id not in self.members:
            print("Gagal: Parent ID tidak ditemukan.")
            return False

        new_member = FamilyMember(member_id, name, gender, parent_id)
        self.members[member_id] = new_member

        if parent_id is None:
            self.root_ids.append(member_id)
        else:
            self.members[parent_id].children.append(new_member)

        print("Anggota berhasil ditambahkan.")
        return True

    # =========================
    # READ
    # =========================
    def show_all_members(self):
        if not self.members:
            print("Data keluarga kosong.")
            return

        print("\n=== DAFTAR ANGGOTA KELUARGA ===")
        for member in self.members.values():
            print(member)

    def show_member_detail(self, member_id):
        member_id = str(member_id)
        if member_id not in self.members:
            print("Anggota tidak ditemukan.")
            return

        member = self.members[member_id]
        print("\n=== DETAIL ANGGOTA ===")
        print(member)

        if member.children:
            print("Anak:")
            for child in member.children:
                print(f"- {child.name} (ID: {child.member_id})")
        else:
            print("Anak: Tidak ada")

    def show_family_tree(self):
        if not self.members:
            print("Data keluarga kosong.")
            return

        print("\n=== SILSILAH KELUARGA ===")
        for root_id in self.root_ids:
            self._print_tree(self.members[root_id], 0)

    def _print_tree(self, member, level):
        print("   " * level + f"- {member.name} (ID: {member.member_id})")
        for child in member.children:
            self._print_tree(child, level + 1)

    # =========================
    # UPDATE
    # =========================
    def update_member(self, member_id, new_name=None, new_gender=None):
        member_id = str(member_id)
        if member_id not in self.members:
            print("Gagal: anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        if new_name:
            member.name = new_name
        if new_gender:
            member.gender = new_gender

        print("Data anggota berhasil diupdate.")
        return True

    # =========================
    # DELETE
    # =========================
    def delete_member(self, member_id):
        member_id = str(member_id)
        if member_id not in self.members:
            print("Gagal: anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        if member.parent_id:
            parent = self.members[member.parent_id]
            parent.children = [child for child in parent.children if child.member_id != member_id]
        else:
            if member_id in self.root_ids:
                self.root_ids.remove(member_id)

        if member.children:
            if member.parent_id:
                parent = self.members[member.parent_id]
                for child in member.children:
                    child.parent_id = parent.member_id
                    parent.children.append(child)
            else:
                for child in member.children:
                    child.parent_id = None
                    self.root_ids.append(child.member_id)

        del self.members[member_id]
        print("Anggota berhasil dihapus.")
        return True

    # =========================
    # BANTU FILE HANDLING
    # =========================
    def get_all_data(self):
        return [member.to_dict() for member in self.members.values()]

    def build_from_rows(self, rows):
        self.members = {}
        self.root_ids = []

        for row in rows:
            member_id = str(row["id"])
            name = row["name"]
            gender = row["gender"]
            parent_id = row["parent_id"] if row["parent_id"] != "" else None

            self.members[member_id] = FamilyMember(member_id, name, gender, parent_id)

        for member in self.members.values():
            if member.parent_id is None:
                self.root_ids.append(member.member_id)
            else:
                if member.parent_id in self.members:
                    self.members[member.parent_id].children.append(member)


# =========================
# FILE HANDLING CSV
# =========================
def save_to_csv(tree, filename="keluarga.csv"):
    data = tree.get_all_data()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "gender", "parent_id"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data berhasil disimpan ke {filename}")


def load_from_csv(tree, filename="keluarga.csv"):
    if not os.path.exists(filename):
        print(f"File {filename} belum ada. Data awal kosong.")
        return

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        tree.build_from_rows(rows)
        print(f"Data berhasil dibaca dari {filename}")

    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")


# =========================
# VALIDASI INPUT
# =========================
def input_nonempty(prompt):
    while True:
        data = input(prompt).strip()
        if data:
            return data
        print("Input tidak boleh kosong.")


def input_numeric_id(prompt):
    while True:
        data = input(prompt).strip()
        if data.isdigit():
            return data
        print("ID harus berupa angka. Silakan ulangi.")


def input_gender(prompt):
    while True:
        gender = input(prompt).strip().upper()
        if gender in ["L", "P"]:
            return gender
        print("Gender harus L atau P. Silakan ulangi.")


def input_parent_id(tree, prompt):
    while True:
        data = input(prompt).strip()

        # boleh kosong
        if data == "":
            return None

        # harus angka
        if not data.isdigit():
            print("Parent ID harus berupa angka atau kosongkan saja.")
            continue

        # harus ada di data
        if data not in tree.members:
            print("Parent ID tidak ditemukan. Ulangi lagi atau kosongkan.")
            continue

        return data


def input_existing_id(tree, prompt):
    while True:
        data = input(prompt).strip()

        if not data.isdigit():
            print("ID harus berupa angka. Silakan ulangi.")
            continue

        if data not in tree.members:
            print("ID tidak ditemukan. Silakan ulangi.")
            continue

        return data


def input_new_member_id(tree, prompt):
    while True:
        data = input(prompt).strip()

        if not data.isdigit():
            print("ID harus berupa angka. Silakan ulangi.")
            continue

        if data in tree.members:
            print("ID sudah dipakai. Masukkan ID lain.")
            continue

        return data


# =========================
# PROGRAM UTAMA CLI
# =========================
def main():
    tree = FamilyTree()
    load_from_csv(tree)

    while True:
        print("\n===== MENU SILSILAH KELUARGA =====")
        print("1. Tambah anggota")
        print("2. Tampilkan semua anggota")
        print("3. Tampilkan silsilah keluarga")
        print("4. Tampilkan detail anggota")
        print("5. Update anggota")
        print("6. Hapus anggota")
        print("7. Simpan data ke CSV")
        print("0. Keluar")

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            member_id = input_new_member_id(tree, "Masukkan ID: ")
            name = input_nonempty("Masukkan nama: ")
            gender = input_gender("Masukkan gender (L/P): ")
            parent_id = input_parent_id(tree, "Masukkan Parent ID (kosongkan jika tidak ada): ")

            tree.add_member(member_id, name, gender, parent_id)

        elif choice == "2":
            tree.show_all_members()

        elif choice == "3":
            tree.show_family_tree()

        elif choice == "4":
            member_id = input_existing_id(tree, "Masukkan ID anggota: ")
            tree.show_member_detail(member_id)

        elif choice == "5":
            member_id = input_existing_id(tree, "Masukkan ID anggota yang ingin diupdate: ")
            new_name = input("Nama baru (kosongkan jika tidak diubah): ").strip()

            while True:
                new_gender = input("Gender baru (L/P, kosongkan jika tidak diubah): ").strip().upper()
                if new_gender == "":
                    new_gender = None
                    break
                elif new_gender in ["L", "P"]:
                    break
                else:
                    print("Gender tidak valid. Masukkan L, P, atau kosongkan.")

            if new_name == "":
                new_name = None

            tree.update_member(member_id, new_name, new_gender)

        elif choice == "6":
            member_id = input_existing_id(tree, "Masukkan ID anggota yang ingin dihapus: ")
            tree.delete_member(member_id)

        elif choice == "7":
            save_to_csv(tree)

        elif choice == "0":
            save_to_csv(tree)
            print("Program selesai.")
            break

        else:
            print("Menu tidak valid. Silakan pilih menu yang tersedia.")


if __name__ == "__main__":
    main()