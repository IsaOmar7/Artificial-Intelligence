import sys


def on_disks(on_list, disks, n):
    for coord1 in range(n):
        for coord2 in range(n):
            if (coord2 > coord1):
                on_list.append(disks[coord1] + "_on_" + disks[coord2])


def top_bottom_at(top_list, bottom_list, at_disk, disks, pegs):
    for i in range(len(disks)):
        top_list.append(disks[i] + "_top")
        bottom_list.append(disks[i] + "_bottom")
        for j in range(len(pegs)):
            at_disk.append(disks[i] + "at" + pegs[j])


def write_func(at_disk, on_list, top_list, empty_list, bottom_list, file):
    for prop in at_disk:
        file.write(prop + " ")
    for prop in on_list:
        file.write(prop + " ")
    for prop in top_list:
        file.write(prop + " ")
    for prop in empty_list:
        file.write(prop + " ")
    for prop in bottom_list:
        file.write(prop + " ")


def from_1_to_empty_actions(from_1_to_empty, coord1, peg_1, peg_2, disks):
    from_1_to_empty.append("Name: M_" + disks[coord1] + "_fr_" + peg_1 + "_to_" + peg_2 + "_emptypeg")
    from_1_to_empty.append("pre: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_top " + disks[
        coord1] + "_bottom " + peg_2 + "_empty")
    from_1_to_empty.append("add: " + disks[coord1] + "at" + peg_2 + " " + peg_1 + "_empty")
    from_1_to_empty.append("del: " + disks[coord1] + "at" + peg_1 + " " + peg_2 + "_empty")


def to_empty_func(disks, to_empty, coord2, coord1, peg_1, peg_2):
    to_empty.append("Name: M_" + disks[coord1] + "_fr_" + peg_1 + "_toempty" + peg_2)
    to_empty.append(
        "pre: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_top " + disks[coord1] + "_on_" + disks[
            coord2] + " " + peg_2 + "_empty")
    to_empty.append("add: " + disks[coord1] + "at" + peg_2 + " " + disks[coord2] + "_top " + disks[coord1] + "_bottom")
    to_empty.append(
        "del: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_on_" + disks[coord2] + " " + peg_2 + "_empty")


def from_1_to_nonempty_func(disks, from_1_to_nonempty, coord2, coord1, peg_1, peg_2):
    from_1_to_nonempty.append("Name: M_" + disks[coord1] + "frompeg" + peg_1 + "_to_" + peg_2)
    from_1_to_nonempty.append(
        "pre: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_top " + disks[coord1] + "_bottom " + disks[
            coord2] + "at" + peg_2 + " " + disks[coord2] + "_top " + disks[coord2] + "at" + peg_2)
    from_1_to_nonempty.append(
        "add: " + disks[coord1] + "at" + peg_2 + " " + disks[coord1] + "_on_" + disks[coord2] + " " + peg_1 + "_empty")
    from_1_to_nonempty.append(
        "del: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_bottom " + disks[coord2] + "_top")


def to_nonempty_func(disks, to_nonempty, coord2, coord1, peg_1, peg_2, coord3):
    to_nonempty.append("Name: M_" + disks[coord1] + "_fr_" + peg_1 + "_to" + peg_2)
    to_nonempty.append(
        "pre: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_top " + disks[coord1] + "_on_" + disks[
            coord2] + " " + disks[coord3] + "at" + peg_2 + " " + disks[coord3] + "_top")
    to_nonempty.append(
        "add: " + disks[coord1] + "at" + peg_2 + " " + disks[coord1] + "_on_" + disks[coord3] + " " + disks[
            coord2] + "_top")
    to_nonempty.append(
        "del: " + disks[coord1] + "at" + peg_1 + " " + disks[coord1] + "_on_" + disks[coord2] + " " + disks[
            coord3] + "_top")


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    at_disk, top_list, on_list, empty_list, bottom_list = [], [], [], [], []
    domain_file.write("Propositions:\n")
    for peg in pegs:
        empty_list.append(peg + "_empty")
    on_disks(on_list, disks, len(disks))
    top_bottom_at(top_list, bottom_list, at_disk, disks, pegs)
    write_func(at_disk, on_list, top_list, empty_list, bottom_list, domain_file)
    domain_file.write("\nActions:\n")
    to_empty, to_nonempty, from_1_to_empty, from_1_to_nonempty = [], [], [], []
    for coord1 in range(n_):
        for peg_1 in pegs:
            for peg_2 in pegs:
                if peg_1 == peg_2:
                    continue
                from_1_to_empty_actions(from_1_to_empty, coord1, peg_1, peg_2, disks)
                for coord2 in range(n_):
                    if coord1 < coord2:
                        to_empty_func(disks, to_empty, coord2, coord1, peg_1, peg_2)
                        from_1_to_nonempty_func(disks, from_1_to_nonempty, coord2, coord1, peg_1, peg_2)
                    for coord3 in range(coord1 + 1, len(disks)):
                        if coord2 == coord3:
                            continue
                        to_nonempty_func(disks, to_nonempty, coord2, coord1, peg_1, peg_2, coord3)
    actions = to_nonempty + to_empty + from_1_to_nonempty + from_1_to_empty
    i = 0
    while i < len(actions):
        domain_file.write(actions[i] + "\n")
        i += 1
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    top_bottom_list, at_peg_0, all_empty_pegs_without0, on_list, top_bottom_list, n_peg, all_empty_pegs_withoutm = [], [], [], [], [], [], []
    m = n_ - 1
    top_bottom_list.append("d_0_top")
    top_bottom_list.append("d_" + str(n_ - 1) + "_bottom")
    for i in range(n_):
        for j in range(n_):
            if j - 1 == i:
                on_list.append("d_" + str(i) + "_on_" + "d_" + str(j))
    for disk in disks:
        at_peg_0.append(disk + "atp_0")
        n_peg.append(disk + "atp_" + str(m_ - 1))
    for i in range(len(pegs)):
        if i != 0:
            all_empty_pegs_without0.append(pegs[i] + "_empty")
        if i != m_ - 1:
            all_empty_pegs_withoutm.append(pegs[i] + "_empty")
    problem_file.write("Initial state: ")
    for init in at_peg_0:
        problem_file.write(init + " ")
    for init in all_empty_pegs_without0:
        problem_file.write(init + " ")
    for init in on_list:
        problem_file.write(init + " ")
    for init in top_bottom_list:
        problem_file.write(init + " ")
    problem_file.write("\nGoal state: ")
    for init in n_peg:
        problem_file.write(init + " ")
    for init in all_empty_pegs_withoutm:
        problem_file.write(init + " ")
    for init in top_bottom_list:
        problem_file.write(init + " ")
    for init in on_list:
        problem_file.write(init + " ")
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
