
# Kelmopok 19
# Silsila
#
#
#
import csv
import os
from datetime import datetime
from collections import deque

# =============================
#
# PROGRAM SILSILAH KELUARGA
#
# =============================
# KELOMPOK 19
# J0403251020 - Bunga Auppa Anpal
# J0403251054 - Rieska Riza
# J0403251137 - Muhammad Faqih Husnan
# =============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "keluarga.csv")
LOG_FILE = os.path.join(BASE_DIR, "log_perubahan.txt") 

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

        log_change("TAMBAH", f"ID={member_id} | Nama={name} | Gender={gender} | Parent ID={parent_id if parent_id else '-'}")
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

        generation = self.get_generation(member_id)
        print(f"Generasi ke-{generation}")

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

        print("\n=========== SILSILAH KELUARGA ===========")

        for i, root_id in enumerate(self.root_ids):
            is_last = i == len(self.root_ids) - 1
            self._print_tree(self.members[root_id], "", is_last)

    def _print_tree(self, member, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "

        gender = "♂" if member.gender == "L" else "♀"

        generation = self.get_generation(member.member_id)

        print(
            prefix +
            connector +
            f"{member.name} {gender} "
            f"[Gen {generation}] "
            f"(ID:{member.member_id})"
        )

        prefix += "    " if is_last else "│   "

        for i, child in enumerate(member.children):
            is_child_last = i == len(member.children) - 1
            self._print_tree(child, prefix, is_child_last)

    # =========================
    # GENERASI
    # =========================
    def get_generation(self, member_id):
        member_id = str(member_id)

        if member_id not in self.members:
            return None

        level = 1
        current = self.members[member_id]

        while current.parent_id:
            level += 1
            current = self.members[current.parent_id]

        return level

    # =========================
    # CARI JALUR HUBUNGAN
    # =========================
    def find_relationship_path(self, id1, id2):
        id1 = str(id1)
        id2 = str(id2)

        if id1 not in self.members or id2 not in self.members:
            return "Anggota tidak ditemukan."

        if id1 == id2:
            return "Orang yang sama."

        queue = deque()
        visited = set()

        queue.append((id1, [id1]))

        while queue:
            current_id, path = queue.popleft()

            if current_id == id2:
                return self.translate_relationship_path(path)

            visited.add(current_id)

            current = self.members[current_id]

            neighbors = []

            # parent
            if current.parent_id:
                neighbors.append(current.parent_id)

            # children
            for child in current.children:
                neighbors.append(child.member_id)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return "Hubungan tidak ditemukan."

    def translate_relationship_path(self, path):
        relation_text = []

        for i in range(len(path) - 1):
            current = self.members[path[i]]
            nxt = self.members[path[i + 1]]

            # parent
            if nxt.member_id == current.parent_id:
                relation = "Orang Tua"

            # child
            elif nxt.parent_id == current.member_id:
                relation = "Anak"

            # sibling
            elif (
                current.parent_id is not None and
                current.parent_id == nxt.parent_id
            ):
                relation = "Saudara"

            else:
                relation = "Kerabat"

            relation_text.append(
                f"{current.name} --[{relation}]--> {nxt.name}"
            )

        return "\n".join(relation_text)

    # =========================
    # UPDATE
    # =========================
    def update_member(self, member_id, new_name=None, new_gender=None):
        member_id = str(member_id)
        if member_id not in self.members:
            print("Gagal: anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        old_name = member.name
        old_gender = member.gender

        if new_name:
            member.name = new_name
        if new_gender:
            member.gender = new_gender

        print("Data anggota berhasil diupdate.")

        log_change("UPDATE", f"ID={member_id} | Nama: {old_name} → {member.name} | Gender: {old_gender} → {member.gender}")
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

        deleted_info = f"ID={member.member_id} | Nama={member.name} | Gender={member.gender} | Parent ID={member.parent_id if member.parent_id else '-'}"

        # hapus dari parent
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
        log_change("HAPUS", deleted_info)
        return True
    
    # =========================
    # SEARCH
    # =========================
    def search_member(self, keyword):
        keyword = keyword.lower()
        results = []
        for member in self.members.values():
            if keyword in member.name.lower() or keyword == member.member_id:
                results.append(member)
                
        if not results:
            print("Anggota tidak ditemukan.")
            return
        
        print("\n=== HASIL PENCARIAN ===")
        for member in results:
            print(member)


    # =========================
    # SORTING
    # =========================
    def sort_members(self, by="name", reverse=False):
        if not self.members:
            print("Data keluarga kosong.")
            return
        
        if by == "name":
            sorted_members = sorted(self.members.values(), key=lambda m: m.name.lower(), reverse=reverse)
        elif by == "id":
            sorted_members = sorted(self.members.values(), key=lambda m: int(m.member_id), reverse=reverse)
        elif by == "generation":
            sorted_members = sorted(self.members.values(), key=lambda m: self.get_generation(m.member_id), reverse=reverse)
        elif by == "gender":
            sorted_members = sorted(self.members.values(), key=lambda m: m.gender, reverse=reverse)
        elif by == "parent_id":
            sorted_members = sorted(self.members.values(), key=lambda m: m.parent_id if m.parent_id else "", reverse=reverse)
        else:
            print("Kriteria sorting tidak valid.")
            return
        
        order_text = "Menurun" if reverse else "Naik"
        print(f"\n=== ANGGOTA KELUARGA TERURUT BERDASARKAN {by.upper()} ({order_text}) ===")
        for member in sorted_members:
            if by == "generation":
                gen = self.get_generation(member.member_id)
                print(f"{member} | Generasi: {gen}")
            elif by == "parent_id":
                parent_text = f"Parent: {member.parent_id}" if member.parent_id else "Parent: -"
                print(f"{member} | {parent_text}")
            else:
                print(member)


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
#  FUNGSI LOG PERUBAHAN DATA
# =========================
def log_change(action, detail, filename=LOG_FILE):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{action}] {detail}\n"
    try:
        with open(filename, mode="a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Gagal menulis log: {e}")


# =========================
# FILE HANDLING CSV
# =========================
def save_to_csv(tree, filename=CSV_FILE):
    data = tree.get_all_data()

    file_exists = os.path.exists(filename)

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "name", "gender", "parent_id"]
            )

            writer.writeheader()
            writer.writerows(data)

        if file_exists:
            print(f"Data berhasil diperbarui ke file {filename}")
        else:
            print(f"File {filename} berhasil dibuat dan data disimpan.")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan file: {e}")

def load_from_csv(tree, filename=CSV_FILE):
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
        print("2. Tampilkan")
        print("3. Update anggota")
        print("4. Hapus anggota")
        print("5. Simpan data ke CSV")
        print("6. Cari")
        print("7. Urutkan")
        print("0. Keluar")

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            member_id = input_new_member_id(tree, "Masukkan ID: ")
            name = input_nonempty("Masukkan nama: ")
            gender = input_gender("Masukkan gender (L/P): ")

            parent_id = input_optional_parent(
                "Masukkan Parent ID (kosongkan jika tidak ada): "
            )

            tree.add_member(
                member_id,
                name,
                gender,
                parent_id
            )

        elif choice == "2":
            print("\n=== MENU TAMPILKAN ===")
            print("1. Tampilkan semua anggota")
            print("2. Tampilkan silsilah keluarga")
            print("3. Tampilkan detail anggota")
            
            display_choice = input("Pilih opsi tampilkan: ").strip()
            
            if display_choice == "1":
                tree.show_all_members()
                
            elif display_choice == "2":
                tree.show_family_tree()
                
            elif display_choice == "3":
                member_id = input_numeric_id("Masukkan ID anggota: ")
                tree.show_member_detail(member_id)
                
            else:
                print("Opsi tampilkan tidak valid.")

        elif choice == "3":
            member_id = input_numeric_id(
                "Masukkan ID anggota yang ingin diupdate: "
            )

            new_name = input(
                "Nama baru (kosongkan jika tidak diubah): "
            ).strip()

            new_gender = input(
                "Gender baru (L/P, kosongkan jika tidak diubah): "
            ).strip().upper()

            if new_name == "":
                new_name = None

            if new_gender == "":
                new_gender = None

            elif new_gender not in ["L", "P"]:
                print("Gender tidak valid.")
                continue

            tree.update_member(
                member_id,
                new_name,
                new_gender
            )

        elif choice == "4":
            member_id = input_numeric_id(
                "Masukkan ID anggota yang ingin dihapus: "
            )

            tree.delete_member(member_id)

        elif choice == "5":
            save_to_csv(tree)

        elif choice == "6":
            print("\n=== MENU CARI ===")
            print("1. Cari anggota")
            print("2. Cari jalur hubungan keluarga")
            
            search_choice = input("Pilih opsi cari: ").strip()
            
            if search_choice == "1":
                keyword = input_nonempty(
                    "Masukkan nama atau ID yang ingin dicari: "
                ).lower()

                tree.search_member(keyword)
                
            elif search_choice == "2":
                id1 = input_numeric_id(
                    "Masukkan ID orang pertama: "
                )

                id2 = input_numeric_id(
                    "Masukkan ID orang kedua: "
                )

                result = tree.find_relationship_path(id1, id2)

                print("\n=== JALUR HUBUNGAN ===")
                print(result)
                
            else:
                print("Opsi cari tidak valid.")

        elif choice == "7":
            print("\n=== MENU URUTKAN ===")
            print("Pilih kriteria untuk mengurutkan anggota:")
            print("1. Nama")
            print("2. ID")
            print("3. Generasi")
            print("4. Gender")
            print("5. Parent ID")

            sort_choice = input(
                "Pilih kriteria untuk mengurutkan anggota: "
            ).strip()

            sort_by = None
            
            if sort_choice == "1":
                sort_by = "name"
            elif sort_choice == "2":
                sort_by = "id"
            elif sort_choice == "3":
                sort_by = "generation"
            elif sort_choice == "4":
                sort_by = "gender"
            elif sort_choice == "5":
                sort_by = "parent_id"
            else:
                print("Kriteria urut tidak valid.")
                continue

            print("\nPilih urutan:")
            print("1. Naik (A-Z, 0-9)")
            print("2. Menurun (Z-A, 9-0)")
            
            order_choice = input(
                "Pilih urutan: "
            ).strip()

            reverse = False
            if order_choice == "2":
                reverse = True
            elif order_choice != "1":
                print("Urutan tidak valid.")
                continue

            tree.sort_members(by=sort_by, reverse=reverse)

        elif choice == "0":
            save_to_csv(tree)

            print("Program selesai, Terima kasih telah menggunakan program ini!")

            break

        else:
            print("Menu tidak valid. Silakan pilih menu yang tersedia.")


if __name__ == "__main__":
    main()