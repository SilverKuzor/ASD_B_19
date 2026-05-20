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


# =============================
# CLASS FAMILY MEMBER
# =============================
class FamilyMember:

    def __init__(
        self,
        member_id,
        name,
        gender,
        father_id=None,
        mother_id=None,
        spouse_id=None
    ):

        self.member_id = str(member_id)
        self.name = name
        self.gender = gender

        self.father_id = str(father_id) if father_id else None
        self.mother_id = str(mother_id) if mother_id else None

        self.spouse_id = str(spouse_id) if spouse_id else None

        self.children = []

    def to_dict(self):

        return {
            "id": self.member_id,
            "name": self.name,
            "gender": self.gender,
            "father_id": self.father_id if self.father_id else "",
            "mother_id": self.mother_id if self.mother_id else "",
            "spouse_id": self.spouse_id if self.spouse_id else ""
        }

    def __str__(self):

        father_text = self.father_id if self.father_id else "-"
        mother_text = self.mother_id if self.mother_id else "-"
        spouse_text = self.spouse_id if self.spouse_id else "-"

        return (
            f"ID: {self.member_id} | "
            f"Nama: {self.name} | "
            f"Gender: {self.gender} | "
            f"Ayah ID: {father_text} | "
            f"Ibu ID: {mother_text} | "
            f"Pasangan ID: {spouse_text}"
        )


# =============================
# CLASS FAMILY TREE
# =============================
class FamilyTree:

    def __init__(self):

        self.members = {}
        self.root_ids = []

    # =========================
    # CEK KETURUNAN
    # =========================
    def is_descendant(self, ancestor_id, descendant_id):

        ancestor_id = str(ancestor_id)
        descendant_id = str(descendant_id)

        if ancestor_id not in self.members:
            return False

        queue = deque([self.members[ancestor_id]])

        visited = set()

        while queue:

            current = queue.popleft()

            if current.member_id in visited:
                continue

            visited.add(current.member_id)

            for child in current.children:

                if child.member_id == descendant_id:
                    return True

                queue.append(child)

        return False

    # =========================
    # VALIDASI INCEST
    # =========================
    def is_incest(self, member_id, spouse_id):

        member_id = str(member_id)
        spouse_id = str(spouse_id)

        if member_id == spouse_id:
            return True

        if member_id not in self.members:
            return False

        if spouse_id not in self.members:
            return False

        member = self.members[member_id]
        spouse = self.members[spouse_id]

        # orang tua kandung
        if (
            spouse_id == member.father_id
            or spouse_id == member.mother_id
        ):
            return True

        # anak kandung
        if self.is_descendant(member_id, spouse_id):
            return True

        # sebaliknya
        if self.is_descendant(spouse_id, member_id):
            return True

        # saudara kandung
        same_father = (
            member.father_id
            and member.father_id == spouse.father_id
        )

        same_mother = (
            member.mother_id
            and member.mother_id == spouse.mother_id
        )

        if same_father or same_mother:
            return True

        return False

    # =========================
    # CREATE
    # =========================
    def add_member(
        self,
        member_id,
        name,
        gender,
        father_id=None,
        mother_id=None,
        spouse_id=None
    ):

        member_id = str(member_id)

        father_id = str(father_id) if father_id else None
        mother_id = str(mother_id) if mother_id else None
        spouse_id = str(spouse_id) if spouse_id else None

        # =========================
        # VALIDASI ID
        # =========================
        if member_id in self.members:

            print("Gagal: ID sudah dipakai.")
            return False

        # =========================
        # VALIDASI GENDER
        # =========================
        if gender not in ["L", "P"]:

            print("Gagal: Gender harus L atau P.")
            return False

        # =========================
        # VALIDASI AYAH
        # =========================
        if father_id:

            if father_id not in self.members:

                print("Gagal: Ayah tidak ditemukan.")
                return False

            if self.members[father_id].gender != "L":

                print("Gagal: Ayah harus gender L.")
                return False

        # =========================
        # VALIDASI IBU
        # =========================
        if mother_id:

            if mother_id not in self.members:

                print("Gagal: Ibu tidak ditemukan.")
                return False

            if self.members[mother_id].gender != "P":

                print("Gagal: Ibu harus gender P.")
                return False

        # =========================
        # AUTO ISI ORTU
        # =========================
        if father_id and not mother_id:

            father = self.members[father_id]

            if father.spouse_id:
                mother_id = father.spouse_id

        if mother_id and not father_id:

            mother = self.members[mother_id]

            if mother.spouse_id:
                father_id = mother.spouse_id

        # =========================
        # VALIDASI ORTU
        # =========================
        if father_id and mother_id:

            if father_id == mother_id:

                print("Gagal: Ayah dan ibu tidak boleh sama.")
                return False

        # =========================
        # VALIDASI PASANGAN
        # =========================
        if spouse_id:

            if spouse_id not in self.members:

                print("Gagal: Pasangan tidak ditemukan.")
                return False

            spouse = self.members[spouse_id]

            if spouse_id == member_id:

                print("Gagal: Tidak bisa menikah dengan diri sendiri.")
                return False

            if spouse.gender == gender:

                print("Gagal: Pasangan tidak boleh gender sama.")
                return False

            if spouse.spouse_id is not None:

                print("Gagal: Orang tersebut sudah memiliki pasangan.")
                return False

            # validasi incest
            if self.is_incest(spouse_id, member_id):

                print("Gagal: Tidak boleh incest dalam keluarga.")
                return False

        # =========================
        # BUAT MEMBER
        # =========================
        new_member = FamilyMember(
            member_id,
            name,
            gender,
            father_id,
            mother_id,
            spouse_id
        )

        self.members[member_id] = new_member

        # =========================
        # HUBUNGKAN PASANGAN
        # =========================
        if spouse_id:

            self.members[spouse_id].spouse_id = member_id

        # =========================
        # ROOT
        # =========================
        if not father_id and not mother_id:

            self.root_ids.append(member_id)

        # =========================
        # HUBUNGKAN KE AYAH
        # =========================
        if father_id:

            self.members[father_id].children.append(new_member)

        # =========================
        # HUBUNGKAN KE IBU
        # =========================
        if mother_id:

            self.members[mother_id].children.append(new_member)

        print("Anggota berhasil ditambahkan.")

        log_change(
            "TAMBAH",
            (
                f"ID={member_id} | "
                f"Nama={name} | "
                f"Gender={gender}"
            )
        )

        return True

    # =========================
    # GENERASI
    # =========================
    def get_generation(self, member_id):

        member_id = str(member_id)

        if member_id not in self.members:
            return None

        level = 1

        current = self.members[member_id]

        while current.father_id:

            level += 1
            current = self.members[current.father_id]

        return level

    # =========================
    # SHOW ALL
    # =========================
    def show_all_members(self):

        if not self.members:

            print("Data keluarga kosong.")
            return

        print("\n=== DAFTAR ANGGOTA ===")

        for member in self.members.values():
            print(member)

    # =========================
    # DETAIL
    # =========================
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

        if member.spouse_id:

            spouse = self.members[member.spouse_id]

            print(f"Pasangan: {spouse.name}")

        if member.children:

            print("Anak:")

            unique_children = []
            already = set()

            for child in member.children:

                if child.member_id not in already:

                    unique_children.append(child)
                    already.add(child.member_id)

            for child in unique_children:
                print(f"- {child.name}")

        else:

            print("Anak: Tidak ada")

    # =========================
    # TREE
    # =========================
    def show_family_tree(self):

        if not self.members:

            print("Data keluarga kosong.")
            return

        print("\n")
        print("╔══════════════════════════════════════╗")
        print("║         SILSILAH KELUARGA           ║")
        print("╚══════════════════════════════════════╝")
        print()

        visited = set()
        printed_roots = set()

        for i, root_id in enumerate(self.root_ids):

            if root_id in printed_roots:
                continue

            root = self.members[root_id]

            printed_roots.add(root_id)

            if root.spouse_id:
                printed_roots.add(root.spouse_id)

            is_last = (i == len(self.root_ids) - 1)

            self._print_tree_ui(
                root,
                "",
                is_last,
                visited
            )

    # =========================
    # PRINT TREE
    # =========================
    def _print_tree_ui(
        self,
        member,
        prefix="",
        is_last=True,
        visited=None
    ):

        if visited is None:
            visited = set()

        if member.member_id in visited:
            return

        visited.add(member.member_id)

        connector = "└── " if is_last else "├── "

        gender_icon = (
            "♂"
            if member.gender == "L"
            else "♀"
        )

        spouse_text = ""

        if member.spouse_id:

            spouse = self.members[member.spouse_id]

            spouse_gender = (
                "♂"
                if spouse.gender == "L"
                else "♀"
            )

            spouse_text = (
                f" ══ ♥ ══ "
                f"{spouse.name} {spouse_gender}"
            )

        generation = self.get_generation(member.member_id)

        print(
            prefix +
            connector +
            f"[{member.name} {gender_icon}]"
            +
            spouse_text
            +
            f"  (Gen {generation})"
        )

        if is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "

        unique_children = []
        already = set()

        for child in member.children:

            if child.member_id not in already:

                unique_children.append(child)
                already.add(child.member_id)

        for index, child in enumerate(unique_children):

            child_is_last = (
                index == len(unique_children) - 1
            )

            self._print_tree_ui(
                child,
                new_prefix,
                child_is_last,
                visited
            )

    # =========================
    # UPDATE
    # =========================
    def update_member(
        self,
        member_id,
        new_name=None,
        new_gender=None
    ):

        member_id = str(member_id)

        if member_id not in self.members:

            print("Gagal: anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        old_name = member.name
        old_gender = member.gender

        if new_gender:

            if new_gender not in ["L", "P"]:

                print("Gagal: Gender harus L atau P.")
                return False

            if member.spouse_id:

                spouse = self.members[member.spouse_id]

                if spouse.gender == new_gender:

                    print(
                        "Gagal: pasangan sesama gender."
                    )

                    return False

        if new_name:
            member.name = new_name

        if new_gender:
            member.gender = new_gender

        print("Data anggota berhasil diupdate.")

        log_change(
            "UPDATE",
            (
                f"ID={member_id} | "
                f"Nama: {old_name} -> {member.name}"
            )
        )

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

        if member.spouse_id:

            spouse = self.members[member.spouse_id]

            spouse.spouse_id = None

        if member.father_id:

            father = self.members[member.father_id]

            father.children = [
                child
                for child in father.children
                if child.member_id != member_id
            ]

        if member.mother_id:

            mother = self.members[member.mother_id]

            mother.children = [
                child
                for child in mother.children
                if child.member_id != member_id
            ]

        if member_id in self.root_ids:
            self.root_ids.remove(member_id)

        for child in member.children:

            if child.father_id == member_id:
                child.father_id = None

            if child.mother_id == member_id:
                child.mother_id = None

            if (
                not child.father_id
                and not child.mother_id
            ):

                if child.member_id not in self.root_ids:
                    self.root_ids.append(child.member_id)

        del self.members[member_id]

        print("Anggota berhasil dihapus.")

        return True

    # =========================
    # SEARCH
    # =========================
    def search_member(self, keyword):

        keyword = keyword.lower()

        results = []

        for member in self.members.values():

            if (
                keyword in member.name.lower()
                or keyword == member.member_id
            ):

                results.append(member)

        if not results:

            print("Anggota tidak ditemukan.")
            return

        print("\n=== HASIL PENCARIAN ===")

        for member in results:
            print(member)
            
    # =========================
    # AMBIL SAUDARA
    # =========================
    def get_siblings(self, member_id):

        member = self.members[member_id]

        siblings = []

        for other in self.members.values():

            if other.member_id == member_id:
                continue

            same_father = (
                member.father_id
                and member.father_id == other.father_id
            )

            same_mother = (
                member.mother_id
                and member.mother_id == other.mother_id
            )

            if (
                same_father
                or same_mother
            ):
                siblings.append(other)

        return siblings

    # =========================
    # AMBIL SAUDARA TIRI
    # =========================
    def get_half_siblings(self, member_id):

        member = self.members[member_id]

        results = []

        for other in self.members.values():

            if other.member_id == member_id:
                continue

            same_father = (
                member.father_id
                and member.father_id == other.father_id
            )

            same_mother = (
                member.mother_id
                and member.mother_id == other.mother_id
            )

            # hanya salah satu yang sama
            if (
                (same_father and not same_mother)
                or
                (same_mother and not same_father)
            ):
                results.append(other)

        return results

    # =========================
    # AMBIL PAMAN & BIBI
    # =========================
    def get_uncles_aunts(self, member_id):

        member = self.members[member_id]

        results = []

        parent_ids = []

        if member.father_id:
            parent_ids.append(member.father_id)

        if member.mother_id:
            parent_ids.append(member.mother_id)

        for parent_id in parent_ids:

            siblings = self.get_siblings(parent_id)

            for sibling in siblings:

                if sibling not in results:
                    results.append(sibling)

        return results

    # =========================
    # AMBIL KEPONAKAN
    # =========================
    def get_nephews_nieces(self, member_id):

        siblings = self.get_siblings(member_id)

        results = []

        for sibling in siblings:

            for child in sibling.children:

                if child not in results:
                    results.append(child)

        return results

    # =========================
    # AMBIL SEPUPU
    # =========================
    def get_cousins(self, member_id):

        uncles_aunts = self.get_uncles_aunts(member_id)

        results = []

        for person in uncles_aunts:

            for child in person.children:

                if child not in results:
                    results.append(child)

        return results

    # =========================
    # TAMPILKAN RELASI LENGKAP
    # =========================
    def show_relationships(self, member_id):

        member_id = str(member_id)

        if member_id not in self.members:

            print("Anggota tidak ditemukan.")
            return

        member = self.members[member_id]

        print("\n=== RELASI KELUARGA ===")
        print(f"Nama : {member.name}")
                # pasangan
        if member.spouse_id:

            spouse = self.members[member.spouse_id]

            if spouse.gender == "L":
                print(f"Suami : {spouse.name}")
            else:
                print(f"Istri : {spouse.name}")

        else:
            print("Pasangan : -")

        # anak
        if member.children:

            unique_children = []
            already = set()

            for child in member.children:

                if child.member_id not in already:

                    unique_children.append(child)
                    already.add(child.member_id)

            print(
                "Anak : "
                +
                ", ".join(
                    child.name
                    for child in unique_children
                )
            )

        else:
            print("Anak : -")

        # bapak
        if member.father_id:

            father = self.members[member.father_id]

            print(f"Bapak : {father.name}")

        else:
            print("Bapak : -")

        # ibu
        if member.mother_id:

            mother = self.members[member.mother_id]

            print(f"Ibu : {mother.name}")

        else:
            print("Ibu : -")

        # kakek nenek ayah
        if member.father_id:

            father = self.members[member.father_id]

            kakek1 = (
                self.members[father.father_id].name
                if father.father_id
                else "-"
            )

            nenek1 = (
                self.members[father.mother_id].name
                if father.mother_id
                else "-"
            )

            print(f"Kakek (Ayah) : {kakek1}")
            print(f"Nenek (Ayah) : {nenek1}")

        # kakek nenek ibu
        if member.mother_id:

            mother = self.members[member.mother_id]

            kakek2 = (
                self.members[mother.father_id].name
                if mother.father_id
                else "-"
            )

            nenek2 = (
                self.members[mother.mother_id].name
                if mother.mother_id
                else "-"
            )

            print(f"Kakek (Ibu) : {kakek2}")
            print(f"Nenek (Ibu) : {nenek2}")

        # saudara kandung
        siblings = self.get_siblings(member_id)

        if siblings:

            print(
                "Saudara : "
                +
                ", ".join(
                    s.name for s in siblings
                )
            )

        else:
            print("Saudara : -")

        # saudara tiri
        half_siblings = self.get_half_siblings(member_id)

        if half_siblings:

            print(
                "Saudara Tiri : "
                +
                ", ".join(
                    s.name for s in half_siblings
                )
            )

        else:
            print("Saudara Tiri : -")

        # paman
        uncles = []

        # bibi
        aunts = []

        for person in self.get_uncles_aunts(member_id):

            if person.gender == "L":
                uncles.append(person.name)
            else:
                aunts.append(person.name)

        print(
            "Paman : "
            +
            (
                ", ".join(uncles)
                if uncles
                else "-"
            )
        )

        print(
            "Bibi : "
            +
            (
                ", ".join(aunts)
                if aunts
                else "-"
            )
        )

        # keponakan
        nephews = self.get_nephews_nieces(member_id)

        if nephews:

            print(
                "Keponakan : "
                +
                ", ".join(
                    n.name for n in nephews
                )
            )

        else:
            print("Keponakan : -")

        # sepupu
        cousins = self.get_cousins(member_id)

        if cousins:

            print(
                "Sepupu : "
                +
                ", ".join(
                    c.name for c in cousins
                )
            )

        else:
            print("Sepupu : -")

    # =========================
    # CEK STATUS RELASI
    # =========================
    def get_relationship_status(self, id1, id2):

        id1 = str(id1)
        id2 = str(id2)

        if (
            id1 not in self.members
            or
            id2 not in self.members
        ):

            return "Anggota tidak ditemukan"

        person1 = self.members[id1]
        person2 = self.members[id2]

        # suami istri
        if person1.spouse_id == id2:
            return "SUAMI ISTRI"

        # ayah anak
        if person2.father_id == id1:
            return "AYAH ANAK"

        if person1.father_id == id2:
            return "ANAK AYAH"

        # ibu anak
        if person2.mother_id == id1:
            return "IBU ANAK"

        if person1.mother_id == id2:
            return "ANAK IBU"

        # saudara kandung
        siblings = self.get_siblings(id1)

        for s in siblings:

            if s.member_id == id2:
                return "SAUDARA"

        # saudara tiri
        half = self.get_half_siblings(id1)

        for s in half:

            if s.member_id == id2:
                return "SAUDARA TIRI"

        # paman/bibi
        uncles_aunts = self.get_uncles_aunts(id2)

        for p in uncles_aunts:

            if p.member_id == id1:

                if person1.gender == "L":
                    return "PAMAN"

                return "BIBI"

        # keponakan
        nephews = self.get_nephews_nieces(id1)

        for n in nephews:

            if n.member_id == id2:
                return "KEPONAKAN"

        # sepupu
        cousins = self.get_cousins(id1)

        for c in cousins:

            if c.member_id == id2:
                return "SEPUPU"

        return "TIDAK ADA RELASI"

    # =========================
    # FILE HANDLING
    # =========================
    def get_all_data(self):

        return [
            member.to_dict()
            for member in self.members.values()
        ]

    def build_from_rows(self, rows):

        self.members = {}
        self.root_ids = []

        # load member
        for row in rows:

            member_id = str(row["id"])

            name = row["name"]

            gender = row["gender"]

            father_id = (
                row["father_id"]
                if row["father_id"] != ""
                else None
            )

            mother_id = (
                row["mother_id"]
                if row["mother_id"] != ""
                else None
            )

            spouse_id = (
                row["spouse_id"]
                if row["spouse_id"] != ""
                else None
            )

            self.members[member_id] = FamilyMember(
                member_id,
                name,
                gender,
                father_id,
                mother_id,
                spouse_id
            )

        # bangun tree
        for member in self.members.values():

            if (
                not member.father_id
                and not member.mother_id
            ):

                self.root_ids.append(
                    member.member_id
                )

            if member.father_id:

                self.members[
                    member.father_id
                ].children.append(member)

            if member.mother_id:

                self.members[
                    member.mother_id
                ].children.append(member)


# =========================
# LOG
# =========================
def log_change(action, detail, filename=LOG_FILE):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    entry = f"[{timestamp}] [{action}] {detail}\n"

    try:

        with open(
            filename,
            mode="a",
            encoding="utf-8"
        ) as f:

            f.write(entry)

    except Exception as e:

        print(f"Gagal menulis log: {e}")


# =========================
# SAVE CSV
# =========================
def save_to_csv(tree, filename=CSV_FILE):

    data = tree.get_all_data()

    try:

        with open(
            filename,
            mode="w",
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
            writer.writerows(data)

        print(
            f"Data berhasil disimpan ke {filename}"
        )

    except Exception as e:

        print(
            f"Terjadi kesalahan saat menyimpan: {e}"
        )


# =========================
# LOAD CSV
# =========================
def load_from_csv(tree, filename=CSV_FILE):

    if not os.path.exists(filename):

        print(f"File {filename} belum ada.")
        return

    try:

        with open(
            filename,
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            rows = list(reader)

        tree.build_from_rows(rows)

        print(
            f"Data berhasil dibaca dari {filename}"
        )

    except Exception as e:

        print(
            f"Terjadi kesalahan saat membaca file: {e}"
        )


# =========================
# INPUT
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

        print("ID harus berupa angka.")


def input_gender(prompt):

    while True:

        gender = input(prompt).strip().upper()

        if gender in ["L", "P"]:
            return gender

        print("Gender harus L atau P.")


def input_parent_id(tree, prompt):

    while True:

        data = input(prompt).strip()

        if data == "":
            return None

        if not data.isdigit():

            print("ID harus berupa angka.")
            continue

        if data not in tree.members:

            print("ID tidak ditemukan.")
            continue

        return data


# =========================
# AUTO ID
# =========================
def generate_member_id(tree):

    if not tree.members:
        return "1"

    max_id = max(
        int(member_id)
        for member_id in tree.members.keys()
    )

    return str(max_id + 1)


# =========================
# MAIN
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
        print("9. Relasi keluarga")
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
                "Masukkan ID Ayah (kosongkan jika tidak ada): "
            )

            mother_id = None

            # hanya minta ibu jika ayah kosong
            if not father_id:

                mother_id = input_parent_id(
                    tree,
                    "Masukkan ID Ibu (kosongkan jika tidak ada): "
                )

            spouse_id = input_parent_id(
                tree,
                "Masukkan ID Pasangan (kosongkan jika tidak ada): "
            )

            tree.add_member(
                member_id,
                name,
                gender,
                father_id,
                mother_id,
                spouse_id
            )

        # tampilkan
        elif choice == "2":

            tree.show_all_members()

        # detail
        elif choice == "3":

            member_id = input_numeric_id(
                "Masukkan ID anggota: "
            )

            tree.show_member_detail(member_id)

        # update
        elif choice == "4":

            member_id = input_numeric_id(
                "Masukkan ID anggota: "
            )

            new_name = input(
                "Nama baru (kosongkan jika tidak diubah): "
            ).strip()

            new_gender = input(
                "Gender baru (L/P): "
            ).strip().upper()

            if new_name == "":
                new_name = None

            if new_gender == "":
                new_gender = None

            tree.update_member(
                member_id,
                new_name,
                new_gender
            )

        # delete
        elif choice == "5":

            member_id = input_numeric_id(
                "Masukkan ID anggota: "
            )

            tree.delete_member(member_id)

        # search
        elif choice == "6":

            keyword = input_nonempty(
                "Masukkan nama atau ID: "
            )

            tree.search_member(keyword)

        # tree
        elif choice == "7":

            tree.show_family_tree()

        # save
        elif choice == "8":

            save_to_csv(tree)
        
                # =========================
                # RELASI KELUARGA
                # =========================
        elif choice == "9":

                    print("\n=== MENU RELASI ===")
                    print("1. Lihat relasi lengkap")
                    print("2. Cek hubungan dua orang")

                    sub = input("Pilih: ").strip()

                    # relasi lengkap
                    if sub == "1":

                        member_id = input_numeric_id(
                            "Masukkan ID anggota: "
                        )

                        tree.show_relationships(member_id)

                    # hubungan dua orang
                    elif sub == "2":

                        id1 = input_numeric_id(
                            "Masukkan ID orang pertama: "
                        )

                        id2 = input_numeric_id(
                            "Masukkan ID orang kedua: "
                        )

                        result = tree.get_relationship_status(
                            id1,
                            id2
                        )

                        print(
                            f"\nStatus Relasi: {result}"
                        )

                    else:

                        print("Pilihan tidak valid.")

        # exit
        elif choice == "0":

            save_to_csv(tree)

            print("Program selesai.")

            break

        else:

            print("Menu tidak valid.")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()