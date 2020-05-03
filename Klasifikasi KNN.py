import math as m

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# Penulisan Teks Menjadi Dokumen
def tulis(teks):
    with open('dokumenuji.txt', mode='w') as hasil_file:
        hasil_file.write(teks)
    return parsing("dokumenuji.txt")


# Hitung Dokumen Cyber
def hitungCyber():
    f1 = open("cyberbullying.txt", "r")
    caption = f1.readlines()
    f1.close()
    array_caption = []
    for a in caption:
        array_caption.append(a.splitlines())
    return len(array_caption)


# Parsing
def parsing(file):
    f1 = open(file, "r")
    caption = f1.readlines()
    f1.close()
    array_caption = []
    for a in caption:
        array_caption.append(a.splitlines())
    return cleaning(array_caption)


# Cleaning
def cleaning(caption):
    hasil_cleaning = []
    for a in caption:
        for b in a:
            c = b.split()
            for d in c:
                if d.__contains__("https://") or d.__contains__("http://") or d.__contains__(
                        "<html>") or d.__contains__("<script>"):
                    c.remove(d)
            join_cleaning = " ".join(c)
            hasil_cleaning.append(join_cleaning.splitlines())
    return non_alpha(hasil_cleaning)


# Non-Alpha
def non_alpha(caption):
    temp = []
    for a in caption:
        for b in a:
            c = b + "  "
            for d in c:
                if d.isalpha() or d.__contains__("-") or d.__contains__(" ") or d.__contains__("  "):
                    temp.append(d)
    hasil = "".join(temp)
    hasil2 = hasil.split("  ")
    list2 = [x for x in hasil2 if x]
    hasil_nonalpha = []
    for a in list2:
        hasil_nonalpha.append(a.splitlines())
    return casefolding(hasil_nonalpha)


# Casefold
def casefolding(kata):
    hasil_cf = []
    for a in kata:
        for b in a:
            c = [b.lower()]
            hasil_cf.append(c)
    return tokenisasi(hasil_cf)


# Tokenisasi
def tokenisasi(hasil_folding):
    token = []
    for a in hasil_folding:
        for b in a:
            c = b.split()
            token.append(c)
    return filtering(token)


# Filtering
def filtering(token):
    f2 = open("stopwordbahasa.csv", "r")
    stoplist = f2.read()
    f2.close()
    token_sl = stoplist.split()
    hasil_filter = []
    for a in token:
        for c in token_sl:
            for b in a:
                if b in c:
                    a.remove(b)
        hasil_filter.append(a)
    return stemming(hasil_filter)


# Stemming
def stemming(hasil_filter):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stem = []
    for kata in hasil_filter:
        for x in kata:
            output = stemmer.stem(x)
            if x != output:
                kata.remove(x)
                kata.append(output)
        stem.append(kata)
    return stem


# Mencari Term
def typing(hasil_stem):
    unique_list = []
    for a in hasil_stem:
        for b in a:
            if b not in unique_list:
                unique_list.append(b)
    return unique_list


# Raw Term Frequency
def rawtf(hasil_stem, unique_list):
    count = []
    rtf = []
    counter = 0.0
    for a in hasil_stem:
        for c in unique_list:
            count.append(str(a.count(c)))
        count.append("pembatas")
        counter += 1.0
    hasil = " ".join(count)
    hasil2 = hasil.split("pembatas")
    while '' in hasil2:
        hasil2.remove('')
    for ak in hasil2:
        final = ak.split()
        rtf.append(final)
    return logtf(rtf)


# Log Term Frequency
def logtf(rtf):
    hasil_ltf = []
    ltf = []
    for a in rtf:
        for b in a:
            if b == "0":
                hasil_ltf.append(b)
            else:
                count = round((1 + m.log10(float(b))), 3)
                hasil_ltf.append(str(count))
        hasil_ltf.append("pembatas")
    hasil = " ".join(hasil_ltf)
    hasil2 = hasil.split("pembatas")
    while '' in hasil2:
        hasil2.remove('')
    for ak in hasil2:
        final = ak.split()
        ltf.append(final)
    return ltf


# Document Frequency
def docf(ltf, hasil_stem, unique_list):
    df = []
    for a in unique_list:
        count = 0
        for b in hasil_stem:
            if a in b:
                count += 1
        df.append(count)
    return inversedf(df, ltf)


# Inverse Document Frequency
def inversedf(list_df, ltf):
    len_doc = len(ltf)
    idf = []
    for a in list_df:
        idf.append((round(m.log10(len_doc / a), 3)))
    return idf


# TF-IDF
def tf_idf(idf, ltf):
    float_ltf = []
    for a in ltf:
        b = [float(i) for i in a]
        float_ltf.append(b)
    result = []
    tfidf = []
    for d in float_ltf:
        for i in range(len(d)):
            result.append(str(round(d[i] * idf[i], 3)))
        result.append("pembatas")
    hasil = " ".join(result)
    hasil2 = hasil.split("pembatas")
    while '' in hasil2:
        hasil2.remove('')
    for ak in hasil2:
        final = ak.split()
        tfidf.append(final)
    return tfidf


# Cosine Similarity
def cossim(tfidf_doklatih, tfidf_dokuji, lenCyber, k):
    float_doklatih = []
    float_dokuji = []
    hasil_kali = []
    for a in tfidf_doklatih:
        float_doklatih.append([float(i) for i in a])
    for b in tfidf_dokuji:
        float_dokuji.append([float(i) for i in b])
    for c in float_doklatih:
        for d in float_dokuji:
            hasil_kali.append([c[i] * d[i] for i in range(len(c))])
    cosinesim = []
    for e in hasil_kali:
        result = 0
        for f in e:
            result = result + f
        cosinesim.append(result)
    return dist(cosinesim, lenCyber, k)


# Distance
def dist(cosinesim, lenCyber, k):
    distance = []
    list_dokumen = []
    for a in cosinesim:
        distance.append((1 - a))
    a = 1
    while a <= len(distance):
        if a <= (len(distance) - lenCyber):
            list_dokumen.append("D" + str(a) + "(Non-Cyberbullying)")
            a += 1
        elif a <= len(distance):
            list_dokumen.append("D" + str(a) + "(Cyberbullying)")
            a += 1
    return klasifikasi(cosinesim, distance, list_dokumen, k)


# Klasifikasi
def klasifikasi(cosinesim, distance, dokumen, k):
    print("\nJarak Seluruh Dokumen Latih Dengan Uji Menggunakan Distance (1 - Hasil Cossim):")
    print(dokumen)
    print(distance)
    print("\nJarak Seluruh Dokumen Latih Dengan Uji Menggunakan Cosine Similarity:")
    print(dokumen)
    print(cosinesim)
    if all(elem == 1 for elem in distance) and all(elem == 1 for elem in cosinesim):
        print("\nKesimpulan: ")
        print("Dokumen Uji Tidak Dapat Ditentukan\n")
    else:
        distance1 = distance.copy()
        cosinesim1 = cosinesim.copy()
        indeks_distance = []
        indeks_cosinesim = []
        jenis_dokumen_distance = []
        jenis_dokumen_cosinesim = []
        count = 1
        while count <= int(k):
            kecil = distance1.index(min(distance1))
            indeks_distance.append(kecil)
            distance1[kecil] = max(distance1) * (max(distance1) + 1)
            cilik = cosinesim1.index(min(cosinesim1))
            indeks_cosinesim.append(cilik)
            cosinesim[cilik] = max(cosinesim1) * (max(cosinesim1) + 1)
            count += 1
        for c in indeks_distance:
            jenis_dokumen_distance.append(dokumen[c])
        for e in indeks_distance:
            jenis_dokumen_cosinesim.append(dokumen[e])
        print("\nDokumen Dengan Jarak Terkecil Menggunakan Distance (1 - Hasil Cossim):")
        print(jenis_dokumen_distance)
        print("\nDokumen Dengan Jarak Terkecil Menggunakan Cosine Similarity:")
        print(jenis_dokumen_cosinesim)
        katA_dist_non, katB_dist_cyber, katA_cosim_non, katB_cosim_cyber = 0, 0, 0, 0
        for d in jenis_dokumen_distance:
            if d.__contains__("(Non-Cyberbullying)"):
                katA_dist_non += 1
            elif d.__contains__("(Cyberbullying)"):
                katB_dist_cyber += 1
        for f in jenis_dokumen_cosinesim:
            if f.__contains__("(Non-Cyberbullying)"):
                katA_dist_non += 1
            elif f.__contains__("(Cyberbullying)"):
                katB_dist_cyber += 1
        print("\nKesimpulan Hasil Uji Dengan Distance (1 - Hasil Cossim):")
        if katA_dist_non > katB_dist_cyber:
            print("Dokumen Uji Berkelas Non-Cyberbully")
            open('allcaption.txt', 'w').close()
        else:
            print("Dokumen Uji Berkelas Cyberbully")
            open('allcaption.txt', 'w').close()
        print("\nKesimpulan Hasil Uji Dengan Cosine Similarity:")
        if katA_cosim_non > katB_cosim_cyber:
            print("Dokumen Uji Berkelas Non-Cyberbully\n")
            open('allcaption.txt', 'w').close()
        else:
            print("Dokumen Uji Berkelas Cyberbully\n")
            open('allcaption.txt', 'w').close()


# Main Menu
def main():
    count = 0
    while count < 1:
        print("1. Menambah Dokumen Latih Non-Cyberbullying Baru")
        print("2. Menambah Dokumen Latih Cyberbullying Baru")
        print("3. Uji Dokumen")
        print("4. Selesai\n")
        menu = input("Masukan pilihan: ")
        if menu == "1":
            input_noncyber = input("Masukan Teks: ")
            noncyber = open("non-cyberbullying.txt", "a")
            noncyber.write("\n")
            noncyber.write(input_noncyber)
            noncyber.close()
            print()
        elif menu == "2":
            input_cyber = input("Masukan Teks: ")
            cyber = open("cyberbullying.txt", "a")
            cyber.write("\n")
            cyber.write(input_cyber)
            cyber.close()
            print()
        elif menu == "3":
            noncyber = open("non-cyberbullying.txt", "r")
            cyber = open("cyberbullying.txt", "r")
            allcapt = open("allcaption.txt", "a")
            for a in noncyber:
                allcapt.write(a)
            noncyber.close()
            allcapt.write("\n")
            for b in cyber:
                allcapt.write(b)
            cyber.close()
            allcapt.close()
            allcapt1 = open("allcaption.txt", "r")
            allcapt1.close()
            dokuji = input("Masukan Teks: ")
            k = input("Masukan K (Angka Ganjil): ")
            prepro_doklatih = parsing("allcaption.txt")
            unique_doklatih = typing(prepro_doklatih)
            bobot_ltf_doklatih = rawtf(prepro_doklatih, unique_doklatih)
            idf_doklatih = docf(bobot_ltf_doklatih, prepro_doklatih, unique_doklatih)
            tfidf_doklatih = tf_idf(idf_doklatih, bobot_ltf_doklatih)
            prepro_dokuji = tulis(dokuji)
            bobot_ltf_dokuji = rawtf(prepro_dokuji, unique_doklatih)
            tfidf_dokuji = tf_idf(idf_doklatih, bobot_ltf_dokuji)
            dokCyber = hitungCyber()
            cossim(tfidf_doklatih, tfidf_dokuji, dokCyber, k)
        elif menu == "4":
            open('allcaption.txt', 'w').close()
            count += 1
        else:
            print("Pilihan Tidak ada\n")


main()
