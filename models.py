# =============================
# models.py
# Berisi definisi class FamilyMember dan FamilyTree
# beserta seluruh logika relasi, validasi, dan operasi CRUD.
# =============================

from collections import deque
from datetime import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_perubahan.txt")


# =============================
# CLASS FAMILY MEMBER
# Representasi satu anggota keluarga
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
        self.name = name.strip()
        self.gender = gender.upper()

        self.father_id = str(father_id) if father_id else None
        self.mother_id = str(mother_id) if mother_id else None
        self.spouse_id = str(spouse_id) if spouse_id else None

        self.children = []

    # Konversi data member ke dictionary untuk disimpan ke CSV
    def to_dict(self):

        return {
            "id": self.member_id,
            "name": self.name,
            "gender": self.gender,
            "father_id": self.father_id or "",
            "mother_id": self.mother_id or "",
            "spouse_id": self.spouse_id or ""
        }

    # Representasi string untuk ditampilkan ke layar
    def __str__(self):

        return (
            f"ID: {self.member_id} | "
            f"Nama: {self.name} | "
            f"Gender: {self.gender} | "
            f"Ayah ID: {self.father_id or '-'} | "
            f"Ibu ID: {self.mother_id or '-'} | "
            f"Pasangan ID: {self.spouse_id or '-'}"
        )


# =============================
# CLASS FAMILY TREE
# Struktur pohon keluarga dengan seluruh operasi CRUD dan relasi
# =============================
class FamilyTree:

    def __init__(self):

        self.members = {}
        self.root_ids = []

    # =========================
    # CEK KETURUNAN
    # Mengecek apakah descendant_id adalah keturunan dari ancestor_id
    # menggunakan BFS (Breadth-First Search)
    # =========================
    def is_descendant(self, ancestor_id, descendant_id):

        ancestor_id = str(ancestor_id)
        descendant_id = str(descendant_id)

        if ancestor_id not in self.members:
            return False

        queue = deque([ancestor_id])
        visited = set()

        while queue:

            current_id = queue.popleft()

            if current_id in visited:
                continue

            visited.add(current_id)

            current = self.members[current_id]

            for child in current.children:

                if child.member_id == descendant_id:
                    return True

                queue.append(child.member_id)

        return False

    # =========================
    # CEK INCEST
    # Mengecek apakah dua orang memiliki hubungan darah
    # yang tidak boleh menikah (orang tua, anak, saudara, paman/bibi, sepupu)
    # =========================
    def is_incest(self, member_id, spouse_id):

        member_id = str(member_id)
        spouse_id = str(spouse_id)

        if member_id == spouse_id:
            return True

        if (
            member_id not in self.members
            or spouse_id not in self.members
        ):
            return False

        member = self.members[member_id]
        spouse = self.members[spouse_id]

        # orang tua / anak
        if spouse_id in [member.father_id, member.mother_id]:
            return True

        if member_id in [spouse.father_id, spouse.mother_id]:
            return True

        # keturunan
        if self.is_descendant(member_id, spouse_id):
            return True

        if self.is_descendant(spouse_id, member_id):
            return True

        # saudara
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

        # paman / bibi
        for person in self.get_uncles_aunts(member_id):

            if person.member_id == spouse_id:
                return True

        for person in self.get_uncles_aunts(spouse_id):

            if person.member_id == member_id:
                return True

        # sepupu
        for person in self.get_cousins(member_id):

            if person.member_id == spouse_id:
                return True

        for person in self.get_cousins(spouse_id):

            if person.member_id == member_id:
                return True

        return False

    # =========================
    # TAMBAH MEMBER
    # Menambahkan anggota baru ke pohon keluarga
    # dengan validasi lengkap sebelum penyimpanan
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

        # validasi ID
        if member_id in self.members:

            print("Gagal: ID sudah digunakan.")
            return False

        # validasi gender
        gender = gender.upper()

        if gender not in ["L", "P"]:

            print("Gagal: Gender harus L atau P.")
            return False

        # validasi ayah
        if father_id:

            if father_id not in self.members:

                print("Gagal: Ayah tidak ditemukan.")
                return False

            if self.members[father_id].gender != "L":

                print("Gagal: Ayah harus gender L.")
                return False

        # validasi ibu
        if mother_id:

            if mother_id not in self.members:

                print("Gagal: Ibu tidak ditemukan.")
                return False

            if self.members[mother_id].gender != "P":

                print("Gagal: Ibu harus gender P.")
                return False

        # auto isi pasangan ortu
        if father_id and not mother_id:

            father = self.members[father_id]

            if father.spouse_id:
                mother_id = father.spouse_id

        if mother_id and not father_id:

            mother = self.members[mother_id]

            if mother.spouse_id:
                father_id = mother.spouse_id

        # validasi pasangan
        if spouse_id:

            if spouse_id not in self.members:

                print("Gagal: Pasangan tidak ditemukan.")
                return False

            spouse = self.members[spouse_id]

            if spouse.gender == gender:

                print("Gagal: Pasangan tidak boleh sesama gender.")
                return False

            if spouse.spouse_id:

                print("Gagal: Pasangan sudah menikah.")
                return False

            if self.is_incest(member_id, spouse_id):

                print("Gagal: Tidak boleh incest.")
                return False

        # buat member
        new_member = FamilyMember(
            member_id,
            name,
            gender,
            father_id,
            mother_id,
            spouse_id
        )

        self.members[member_id] = new_member

        # hubungkan pasangan
        if spouse_id:

            self.members[spouse_id].spouse_id = member_id

        # root
        if not father_id and not mother_id:

            if member_id not in self.root_ids:
                self.root_ids.append(member_id)

        # hubungan anak
        if father_id:

            self.members[father_id].children.append(
                new_member
            )

        if mother_id:

            self.members[mother_id].children.append(
                new_member
            )

        print("Anggota berhasil ditambahkan.")

        log_change(
            "TAMBAH",
            f"ID={member_id} | Nama={name}"
        )

        return True

    # =========================
    # GENERASI
    # Menghitung level generasi anggota dengan menelusuri ke atas via ayah
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
    # TAMPILKAN SEMUA
    # Menampilkan daftar seluruh anggota keluarga
    # =========================
    def show_all_members(self):

        if not self.members:

            print("Data kosong.")
            return

        print("\n=== DAFTAR ANGGOTA ===")

        for member in self.members.values():
            print(member)

    # =========================
    # DETAIL
    # Menampilkan informasi lengkap satu anggota
    # beserta generasi, pasangan, dan daftar anak
    # =========================
    def show_member_detail(self, member_id):

        member_id = str(member_id)

        if member_id not in self.members:

            print("Anggota tidak ditemukan.")
            return

        member = self.members[member_id]

        print("\n=== DETAIL ANGGOTA ===")
        print(member)

        print(
            f"Generasi ke-{self.get_generation(member_id)}"
        )

        if member.spouse_id:

            spouse = self.members[member.spouse_id]

            print(f"Pasangan : {spouse.name}")

        else:

            print("Pasangan : -")

        if member.children:

            print("Anak:")

            printed = set()

            for child in member.children:

                if child.member_id not in printed:

                    print(f"- {child.name}")

                    printed.add(child.member_id)

        else:

            print("Anak : -")

    # =========================
    # TAMPILKAN TREE
    # Menampilkan pohon keluarga secara visual dari root ke bawah
    # =========================
    def show_family_tree(self):

        if not self.members:

            print("Data keluarga kosong.")
            return

        print("================================")
        print("||                            ||")
        print("||     SILSILAH KELUARGA      ||")
        print("||                            ||")
        print("================================\n")

        visited = set()

        for i, root_id in enumerate(self.root_ids):

            if root_id in visited:
                continue

            root = self.members[root_id]

            self._print_tree(
                root,
                "",
                i == len(self.root_ids) - 1,
                visited
            )

    # Rekursif cetak satu node pohon beserta cabang-cabangnya
    def _print_tree(
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

            spouse_icon = (
                "♂"
                if spouse.gender == "L"
                else "♀"
            )

            spouse_text = (
                f" ══ ♥ ══ "
                f"{spouse.name} {spouse_icon}"
            )

        print(
            prefix +
            connector +
            f"{member.name} {gender_icon}" +
            spouse_text
        )

        new_prefix = (
            prefix + "    "
            if is_last
            else prefix + "│   "
        )

        unique_children = []
        already = set()

        for child in member.children:

            if child.member_id not in already:

                unique_children.append(child)
                already.add(child.member_id)

        for i, child in enumerate(unique_children):

            self._print_tree(
                child,
                new_prefix,
                i == len(unique_children) - 1,
                visited
            )

    # =========================
    # UPDATE
    # Memperbarui data anggota: nama, gender, dan/atau pasangan
    # =========================
    def update_member(
        self,
        member_id,
        new_name=None,
        new_gender=None,
        new_spouse_id=None
    ):

        member_id = str(member_id)

        if member_id not in self.members:

            print("Anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        # update nama
        if new_name:
            member.name = new_name

        # update gender
        if new_gender:

            new_gender = new_gender.upper()

            if new_gender not in ["L", "P"]:

                print("Gender harus L/P.")
                return False

            if member.spouse_id:

                spouse = self.members[member.spouse_id]

                if spouse.gender == new_gender:

                    print("Gagal: pasangan sesama gender.")
                    return False

            member.gender = new_gender

        # update pasangan
        if new_spouse_id is not None:

            # cerai
            if new_spouse_id == "":

                if member.spouse_id:

                    old_spouse = self.members[
                        member.spouse_id
                    ]

                    old_spouse.spouse_id = None
                    member.spouse_id = None

                    print("Berhasil cerai.")

            else:

                new_spouse_id = str(new_spouse_id)

                if new_spouse_id not in self.members:

                    print("Pasangan tidak ditemukan.")
                    return False

                spouse = self.members[new_spouse_id]

                if spouse.gender == member.gender:

                    print("Pasangan sesama gender.")
                    return False

                if spouse.spouse_id:

                    print("Pasangan sudah menikah.")
                    return False

                if self.is_incest(
                    member_id,
                    new_spouse_id
                ):

                    print("Tidak boleh incest.")
                    return False

                # lepas pasangan lama
                if member.spouse_id:

                    old = self.members[member.spouse_id]
                    old.spouse_id = None

                member.spouse_id = new_spouse_id
                spouse.spouse_id = member_id

                print("Pasangan berhasil diupdate.")

        print("Data berhasil diupdate.")

        log_change(
            "UPDATE",
            f"ID={member_id}"
        )

        return True

    # =========================
    # HAPUS
    # Menghapus anggota dari pohon dan memperbaiki semua relasi terkait
    # =========================
    def delete_member(self, member_id):

        member_id = str(member_id)

        if member_id not in self.members:

            print("Anggota tidak ditemukan.")
            return False

        member = self.members[member_id]

        # hapus pasangan
        if member.spouse_id:

            spouse = self.members[member.spouse_id]
            spouse.spouse_id = None

        # hapus hubungan anak
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

        # hapus dari ayah
        if member.father_id:

            father = self.members[member.father_id]

            father.children = [
                child
                for child in father.children
                if child.member_id != member_id
            ]

        # hapus dari ibu
        if member.mother_id:

            mother = self.members[member.mother_id]

            mother.children = [
                child
                for child in mother.children
                if child.member_id != member_id
            ]

        # hapus root
        if member_id in self.root_ids:
            self.root_ids.remove(member_id)

        del self.members[member_id]

        print("Anggota berhasil dihapus.")

        log_change(
            "DELETE",
            f"ID={member_id}"
        )

        return True

    # =========================
    # SAUDARA
    # Mendapatkan daftar saudara kandung/tiri dari seorang anggota
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

            if same_father or same_mother:
                siblings.append(other)

        return siblings

    # =========================
    # PAMAN / BIBI
    # Mendapatkan daftar paman/bibi dari seorang anggota
    # (saudara dari orang tua)
    # =========================
    def get_uncles_aunts(self, member_id):

        member = self.members[member_id]

        results = []

        parents = []

        if member.father_id:
            parents.append(member.father_id)

        if member.mother_id:
            parents.append(member.mother_id)

        for parent_id in parents:

            siblings = self.get_siblings(parent_id)

            for sibling in siblings:

                if sibling not in results:
                    results.append(sibling)

        return results

    # =========================
    # SEPUPU
    # Mendapatkan daftar sepupu dari seorang anggota
    # (anak dari paman/bibi)
    # =========================
    def get_cousins(self, member_id):

        cousins = []

        for person in self.get_uncles_aunts(member_id):

            for child in person.children:

                if child not in cousins:
                    cousins.append(child)

        return cousins

    # =========================
    # RELASI
    # Menentukan jenis relasi antara dua anggota keluarga
    # =========================
    def get_relationship_status(self, id1, id2):

        id1 = str(id1)
        id2 = str(id2)

        if (
            id1 not in self.members
            or id2 not in self.members
        ):

            return "Anggota tidak ditemukan"

        person1 = self.members[id1]
        person2 = self.members[id2]

        # pasangan
        if person1.spouse_id == id2:
            return "SUAMI ISTRI"

        # ayah
        if person2.father_id == id1:
            return "AYAH ANAK"

        if person1.father_id == id2:
            return "ANAK AYAH"

        # ibu
        if person2.mother_id == id1:
            return "IBU ANAK"

        if person1.mother_id == id2:
            return "ANAK IBU"

        # saudara
        for sibling in self.get_siblings(id1):

            if sibling.member_id == id2:
                return "SAUDARA"

        # paman/bibi
        for ua in self.get_uncles_aunts(id2):

            if ua.member_id == id1:

                return (
                    "PAMAN"
                    if person1.gender == "L"
                    else "BIBI"
                )

        # sepupu
        for cousin in self.get_cousins(id1):

            if cousin.member_id == id2:
                return "SEPUPU"

        return "TIDAK ADA RELASI"

    # =========================
    # GET ALL DATA
    # Mengambil seluruh data member dalam bentuk list of dict
    # untuk keperluan penyimpanan CSV
    # =========================
    def get_all_data(self):

        return [
            member.to_dict()
            for member in self.members.values()
        ]

    # =========================
    # BUILD FROM ROWS
    # Membangun ulang struktur pohon dari baris-baris data CSV
    # =========================
    def build_from_rows(self, rows):

        self.members = {}
        self.root_ids = []

        # load member dari baris CSV
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

        # bangun relasi pohon dari data yang sudah di-load
        visited_roots = set()

        for member in self.members.values():

            # tentukan root (anggota tanpa orang tua)
            if (
                not member.father_id
                and not member.mother_id
            ):

                if member.member_id in visited_roots:
                    continue

                # jika punya pasangan, pilih ID terkecil sebagai root
                if member.spouse_id:

                    spouse_id = member.spouse_id

                    root_id = min(
                        member.member_id,
                        spouse_id
                    )

                    if root_id not in self.root_ids:
                        self.root_ids.append(root_id)

                    visited_roots.add(member.member_id)
                    visited_roots.add(spouse_id)

                else:

                    if member.member_id not in self.root_ids:
                        self.root_ids.append(member.member_id)

                    visited_roots.add(member.member_id)

            # hubungkan anak ke orang tua masing-masing
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
# Mencatat setiap perubahan data ke file log dengan timestamp
# =========================
def log_change(action, detail):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    entry = (
        f"[{timestamp}] "
        f"[{action}] "
        f"{detail}\n"
    )

    try:

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(entry)

    except Exception as e:

        print(f"Gagal menulis log: {e}")
