# =============================
# search_sort.py
# Berisi fungsi pencarian dan pengurutan anggota keluarga.
# =============================


# =========================
# SEARCH MEMBER
# Mencari anggota berdasarkan kata kunci nama atau ID
# dan menampilkan semua hasil yang cocok
# =========================
def search_member(tree, keyword):

    keyword = keyword.lower()

    results = []

    for member in tree.members.values():

        if (
            keyword in member.name.lower()
            or keyword == member.member_id
        ):

            results.append(member)

    if not results:

        print("Tidak ditemukan.")
        return

    print("\n=== HASIL PENCARIAN ===")

    for member in results:
        print(member)


# =========================
# SORT MEMBERS
# Mengurutkan dan menampilkan anggota berdasarkan kriteria:
# name, id, generation, gender, father_id, atau mother_id
# =========================
def sort_members(tree, by="name", reverse=False):

    if not tree.members:

        print("Data keluarga kosong.")
        return

    if by == "name":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: m.name.lower(),
            reverse=reverse
        )

    elif by == "id":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: int(m.member_id),
            reverse=reverse
        )

    elif by == "generation":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: tree.get_generation(m.member_id),
            reverse=reverse
        )

    elif by == "gender":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: m.gender,
            reverse=reverse
        )

    elif by == "father_id":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: m.father_id if m.father_id else "",
            reverse=reverse
        )

    elif by == "mother_id":
        sorted_members = sorted(
            tree.members.values(),
            key=lambda m: m.mother_id if m.mother_id else "",
            reverse=reverse
        )

    else:

        print("Kriteria sorting tidak valid.")
        return

    order_text = "Menurun" if reverse else "Naik"

    print(
        f"\n=== ANGGOTA KELUARGA TERURUT BERDASARKAN "
        f"{by.upper()} ({order_text}) ==="
    )

    for member in sorted_members:

        if by == "generation":
            gen = tree.get_generation(member.member_id)
            print(f"{member} | Generasi: {gen}")


        else:
            print(member)
