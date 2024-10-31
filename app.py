import json
import os
import urllib.parse
import re
import subprocess
import sys
from colorama import Fore, Style
from datetime import datetime

def log(pesan):
    print(
        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X')} ]{Style.RESET_ALL}"
        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{pesan}",
        flush=True
    )

def pisah_queries(fileInput='query.txt', folderOutput='result_query', opsi='id'):

    if not os.path.exists(fileInput):
        log(f"{Fore.RED + Style.BRIGHT}Error: '{fileInput}' Tidak Ditemukan.{Style.RESET_ALL}")
        return

    with open(fileInput, 'r') as file:
        queries = [baris.strip() for baris in file if baris.strip()]

    os.makedirs(folderOutput, exist_ok=True)

    for idx, query in enumerate(queries):

        queryDecoded = urllib.parse.unquote(query)

        namaFolder = f"query-{idx+1}"
        try:
            queryJson = json.loads(queryDecoded.split('user=')[1].split('&')[0])
            if opsi == 'id':
                namaFolder = 'query-' + str(queryJson.get('id', namaFolder))
            elif opsi == 'username':
                namaFolder = 'query-' + str(queryJson.get('username', namaFolder))

            namaFolder = re.sub(r'[^A-Za-z0-9_\-]', '', namaFolder)
        except (IndexError, json.JSONDecodeError):
            log(f"{Fore.YELLOW + Style.BRIGHT}Peringatan: Gagal Memproses Query Pada Indeks {idx+1}.{Style.RESET_ALL}")

        pathFolder = os.path.join(folderOutput, namaFolder)
        os.makedirs(pathFolder, exist_ok=True)
        with open(os.path.join(pathFolder, 'query.txt'), 'w') as queryFile:
            queryFile.write(query)

    log(f"{Fore.GREEN + Style.BRIGHT}Berhasil Memisah {len(queries)} Query Menjadi Folder Terpisah Di '{folderOutput}' Dengan Opsi '{opsi}'.{Style.RESET_ALL}")

def main():
    opsiMap = {'1': 'id', '2': 'username', '3': 'inkremental'}
    print(f"{Fore.YELLOW + Style.BRIGHT}Pilih Opsi Untuk Penamaan Folder:{Style.RESET_ALL}")
    for key, value in opsiMap.items():
        print(f"{Fore.CYAN + Style.BRIGHT}{key}. Menggunakan {value.capitalize()}{Style.RESET_ALL}")

    pilihan = input(f"{Fore.YELLOW + Style.BRIGHT}Masukkan Nomor Opsi (1/2/3): {Style.RESET_ALL}")
    opsi = opsiMap.get(pilihan)

    if opsi:
        pisah_queries(opsi=opsi)
    else:
        print(f"{Fore.RED + Style.BRIGHT}Pilihan Tidak Valid. Harap Masukkan 1, 2, Atau 3.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()