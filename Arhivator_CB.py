from tkinter import filedialog, messagebox
from tkinter import *
from tkcalendar import DateEntry
import libarchive


def BrowseDir():
    try:
        global folderName
        folderName = filedialog.askdirectory(initialdir=r"C:\\", title="Select folder")
        print("Folder selected: ", folderName)
        lblFilename['text'] = "Выбрана папка: " + folderName
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))


def ArchiveExec():
    print(folderName)
    archive_date = cal.get_date().strftime('%d%m%Y')
    try:
        result = libarchive.archive(folderName, archive_date)
        if result == -1:
            messagebox.showinfo("Информация",
                                "Выполнение прервано.\n" + "Встретился архив.\n" + "Распакуйте, либо удалите.\n")
        elif result == -2:
            messagebox.showinfo("Информация",
                                "Выполнение прервано.\n" + "Встретился некорректный файл.\n")
        else:
            messagebox.showinfo("Информация", "Выполнение завершено успешно.")
    except Exception as e:
        messagebox.showerror('Ошибка Python', 'Error:' + str(e) + str(e.args))


if __name__ == "__main__":
    folderName = "<Папка не выбрана>"

    root = Tk()

    root.title("Архиватор для запросов ЦБ")
    root.geometry("700x200")

    frame = LabelFrame(width=100, height=200)
    frame.pack(padx=5, pady=5, side="left", expand=True)

    frame2 = LabelFrame(width=100, height=200)
    frame2.pack(padx=5, pady=5, side="right", expand=True)

    btnBrowseDir = Button(frame, text="1. Выберите папку", command=BrowseDir)
    btnBrowseDir.pack(padx=10, pady=10)

    label = Label(frame, text="2. Выберите дату архива:")
    label.pack(padx=10, pady=10)

    lblFilename = Label(frame2, text="<Папка не выбрана>", width=100, padx=2, pady=2, bd=2, relief=RIDGE)
    lblFilename.pack(padx=10, pady=10)

    cal = DateEntry(frame2, width=16, date_pattern="dd-mm-yyyy")
    cal.pack(padx=10, pady=10, side="left")

    btnBrowseDir = Button(frame2, text="3. Создать архив", command=ArchiveExec)
    btnBrowseDir.pack(padx=10, pady=10, side="left")

    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()
