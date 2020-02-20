from zipfile import ZipFile
import os, time
import shutil
from Storage.DataContext import Context
from datetime import datetime


def makeDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_imlist(path, extensions):
    return [os.path.join(path, f) for f in os.listdir(path) if any(f.lower().endswith(ext) for ext in extensions)]

def zip_read_files(sourcePath, destinationPath, extensions):

    # nowDate = datetime.date.today()

    nowDate = datetime.today().date()


    # Günlük Data çekilirken kullanılacak - tarihe göre
    # hasar_files = [
    #     os.path.join(sourcePath, f)
    #     for
    #     f
    #     in
    #     os.listdir(sourcePath)
    #     if datetime.datetime.strptime(
    #         time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(os.path.join(sourcePath, f)))), "%Y-%m-%d").date()
    #        == nowDate
    # ]

    # context = Context('Storage/DBImage')
    context = Context('Storage/DBImageV1')

    # Tüm data çekilir..buffer olur mu?
    hasar_files = [
        os.path.join(sourcePath,f)
        for
        f
        in
        os.listdir(sourcePath)
    ]

    # destination_files = [
    #     os.path.join(destinationPath, f)
    #     for
    #     f
    #     in
    #     os.listdir(sourcePath)
    # ]

    destination_files = destinationPath

    count = 0
    for i, hasarPath in enumerate(hasar_files):
        count = count + 1
        fileNumber = os.path.split(hasarPath)[1]

        # Check File Control
        check = context.check_file(fileNumber)
        if check:
            continue

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        context.count_file(str(fileNumber), count, date_time)


        hasarPath = get_imlist(hasarPath, extensions)
        # pathDest = destination_files[i]
        pathDest = destination_files
        l = 0
        a = 0
        # if os.path.exists(pathDest):
        #     continue
        # makeDir(pathDest)
        for j, path in enumerate(hasarPath):
            ext = os.path.splitext(path)

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            context.log(str(os.path.split(path)[1]), 'Harici Dosyalar', date_time)

            hasarFile = os.path.split(path)[1].lower().find("hasarfoto")

            if hasarFile == -1:
                continue

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            context.log(str(os.path.split(path)[1]), 'Hasar Dosyası ilk Format', date_time)

            if path.lower().endswith(".zip"):
                print("path: {} ".format(path))
                # opening the zip file in READ mode

                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                context.log(str(os.path.split(path)[1]), 'Hasar Dosyası-Zip', date_time)

                try:
                    with ZipFile(path, 'r') as zip:
                        # zip.printdir()
                        ext = (".jpg", ".jpeg", ".JPG", ".JPEG")
                        # zip.extractall(pathDest)
                        for file in zip.namelist():
                            if file.endswith(ext):
                                # zip.extractall(pathDest)
                                zip.extract(file, pathDest)
                                p = path.split('\\')[3]
                                a = a + 1

                                now = datetime.now()
                                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                                context.log(str(p), 'Hasar Dosyası-Zip içinde', date_time)

                                # if os.path.exists(os.path.join(pathDest, "{}_{}.{}".format(p, a, file.split('.')[1]))):
                                if os.path.exists(os.path.join(pathDest, "{}_{}{}".format(p, a, ext[0]))) \
                                        or os.path.exists(os.path.join(pathDest, "{}_{}{}".format(p, a, ext[1]))):
                                    continue

                                os.rename(os.path.join(pathDest, file),
                                          os.path.join(pathDest, "{}_{}{}".format(p, a, ext[1])))

                                # for k, name in enumerate(zip.filelist):
                                #     a = a + 1
                                #     os.rename(os.path.join(pathDest, name.filename),
                                #               os.path.join(pathDest, "{}_{}.{}".format(p, a, name.filename.split('.')[1])))
                            else:
                                now = datetime.now()
                                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                                context.log(str("{} dosyası içerisinde, aktarılmayan Dosya: {}".format(os.path.split(path)[1], file)), 'Hasar Dosyası-Zip içinde', date_time)
                                print("Aktarılmayan Dosya: {}".format(file))
                                continue
                        # [zip.extractall(pathDest) for file in zip.namelist() if file.endswith(ext)]
                        # p = pathDest.split('\\')[4]
                        # p = path.split('\\')[4]
                        # for k, name in enumerate(zip.filelist):
                        #     a = a + 1
                        #     os.rename(os.path.join(pathDest, name.filename), os.path.join(pathDest, "{}_{}.{}".format(p, a, name.filename.split('.')[1])))

                        now = datetime.now()
                        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                        context.log(str(os.path.split(path)[1]), 'Hasar Dosyası- Boş Zip File', date_time)
                        print('Done!')
                except:
                     now = datetime.now()
                     date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                     context.log(str(os.path.split(path)[1]), 'Hasar Dosyası- Hatalı Zip File', date_time)
                     continue
            else:
                # p = pathDest.split('\\')[4] #2 olacak server da, normal 4
                l = l + 1
                filename = path.split('\\')[4] # server 3, normal 5
                files = path.split('\\')[3] # server da dosya adını alıyor
                existFile = os.path.join(pathDest, filename)
                print("dosya No: {}".format(l))
                print("dosya Adı: {}".format(filename))
                print("files Adı: {}".format(files))

                # existFileRename = os.path.join(pathDest, "{}_{}.{}".format(files, l, filename.split('.')[1]))
                # filesRename = "{}_{}.{}".format(files, l, filename.split('.')[1])

                existFileRename = os.path.join(pathDest, "{}_{}_{}{}".format(files, "Single", l, ext[1]))
                filesRename = "{}_{}_{}{}".format(files, "Single", l, ext[1])

                if os.path.exists(existFile) or os.path.exists(existFileRename):
                   now = datetime.now()
                   date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                   # context.log("Bu {} Dosya Adı Daha Önce {} olarak Kopyalanmıştır :".format(filename, filesRename), 'Hasar Dosyası-Tek Image', date_time)
                   print("Bu {} Dosya Adı Daha Önce {} olarak Kopyalanmıştır :".format(filename, filesRename))
                   continue

                shutil.copy(path, pathDest)
                print("path: {} -- pathDest: {}".format(path,pathDest))

                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                context.log(str(files), 'Hasar Dosyası-Tek Image', date_time)

                # os.rename(os.path.join(pathDest, name.filename),
                #           os.path.join(pathDest, "{}_{}.{}".format(p, j, name.filename.split('.')[1])))
                # os.rename(os.path.join(pathDest, filename), os.path.join(pathDest, "{}_{}.{}".format(l, j, filename)))
                # os.rename(os.path.join(pathDest, filename), os.path.join(pathDest, "{}".format(filename)))
                # os.rename(os.path.join(pathDest, filename), os.path.join(pathDest, "{}_{}.{}".format(files, l, filename.split('.')[1])))

                os.rename(os.path.join(pathDest, filename), os.path.join(pathDest, "{}_{}_{}{}".format(files, "Single", l, ext[1])))
                print("kopyalanan dosya yolu: {}".format(os.path.join(pathDest, "{}_{}{}".format(filename, l, ext[1]))))

# *********
if __name__== '__main__':

    # Kod Console dan Parametre girmek
    # import argparse
    # parser = argparse.ArgumentParser()
    # extensions = [".zip", ".jpg", ".jpeg"]
    # parser.add_argument("--sourcePath", "-s", help="source Path")
    # parser.add_argument("--destinationPath", "-d", help="destination Path")
    # args = parser.parse_args()
    # same = zip_read_files(args.sourcePath, args.destinationPath, extensions)
    # Ornek Console yazı şekli : python src/zipFile.py -s "C:\\ZGE\\Image Proje Info" -d "C:\\Destination\\Image"
    # **********************************************************************

    # sourcePath = "C:\\ZGE\\Image Proje Info\\Ornek Resim"
    # destinationPath = "C:\\ZGE\\Image Proje Info\\Directory"

    extensions = [".zip",".jpg", ".jpeg"]
    # sourcePath = "D:\\Proje Hasar Resimleri"
    # destinationPath = "D:\\DamageImages"

    sourcePath = "D:\\SharePointDoc\\HasarDosyaEvrak"
    destinationPath = "D:\\TrainDamageImages"

    # sourcePath = "D:\\deneme1"
    # destinationPath= "D:\\deneme2"

    same =  zip_read_files(sourcePath, destinationPath, extensions)

    print("Bittti..")






