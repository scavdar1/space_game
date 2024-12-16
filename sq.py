sayilar = [1,2,3,4,5]
for sayi in sayilar:
    if sayi > 2:
        sayilar.remove(sai)
print(sayilar)


sayilar = [1,2,3,4,5]
for sayi in sayilar[:]:
    if sayi > 2:
        sayilar.remove(sayi)
print(sayilar)

