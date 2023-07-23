import sys
import os


def calc_checksum_3gx(file_name: str) -> int:
    with open(file_name, "rb") as file_read:
        raw_data = list(file_read.read())

    read32 = lambda arr, pos : (arr[pos + 3] << 24) + (arr[pos + 2] << 16) + (arr[pos + 1] << 8) + (arr[pos] << 0)

    code_offset = read32(raw_data, 88)
    data_offset = read32(raw_data, 96)
    data_size = read32(raw_data, 108)

    checksum = 0
    now_pos = code_offset
    end_pos = data_offset + data_size

    while now_pos < end_pos:
        checksum += read32(raw_data, now_pos)
        now_pos += 4
        if 0xFFFFFFFF < checksum:
            checksum -= 0x100000000

    return checksum


def main() -> None:
    if 1 < len(sys.argv):
        if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
            print("0x" + hex(calc_checksum_3gx(sys.argv[1]))[2:].upper().zfill(8))
    else:
        while True:
            file_name = input("File name ('e' to exit) >> ")
            if file_name == "e":
                sys.exit()
            if os.path.exists(file_name) and os.path.isfile(file_name):
                print("\n0x" + hex(calc_checksum_3gx(file_name))[2:].upper().zfill(8) + "\n")


if __name__ == "__main__":
    main()
