import tkinter as tk
import mariadb
from tkinter import messagebox

DB_HOST = "localhost"
DB_USER = "*"
DB_PASSWORD = "*"
DB_DATABASE = "*"

class SudokuApp:
    def __init__(self, root):
        try:
            self.conn = mariadb.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE
            )
            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
            root.destroy()

        self.root = root
        self.root.title("Судоку с римскими цифрами")
        self.grid_size = 9
        self.cells = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.h_constraints = [[None for _ in range(self.grid_size - 1)] for _ in range(self.grid_size)]
        self.v_constraints = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size - 1)]
        self.create_grid()
        self.root.geometry("700x750")

        self.btn_solve = tk.Button(root, text="Решить", command=self.solve_puzzle, bg="lightgreen")
        self.btn_solve.pack(pady=10)

        self.btn_load = tk.Button(root, text="Загрузить из БД", command=self.load_from_db, bg="lightblue")
        self.btn_load.pack(pady=10)

        self.btn_save = tk.Button(root, text="Сохранить в БД", command=self.save_to_db, bg="lightcoral")
        self.btn_save.pack(pady=10)

    def create_grid(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                cell.grid(row=row * 2, column=col * 2, padx=2, pady=2)
                self.cells[row][col] = cell

    def get_grid(self):
        try:
            grid = []
            for row in self.cells:
                grid_row = []
                for cell in row:
                    value = cell.get()
                    if not value:
                        grid_row.append(0)
                    elif value.isdigit() and 1 <= int(value) <= 9:
                        grid_row.append(int(value))
                    else:
                        raise ValueError(
                            f"Недопустимое значение: '{value}'. Используйте только числа от 1 до 9."
                        )
                grid.append(grid_row)
            return grid
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return None

    def set_grid(self, grid):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.cells[row][col].delete(0, tk.END)
                if grid[row][col] != 0:
                    self.cells[row][col].insert(0, str(grid[row][col]))

    def load_from_db(self):
        try:
            self.cursor.execute("SELECT row, col, value FROM start_data")
            data = self.cursor.fetchall()

            grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            for row, col, value in data:
                grid[row][col] = value

            self.set_grid(grid)
            messagebox.showinfo("Загрузка завершена", "Данные успешно загружены из базы данных.")
        except mariadb.Error as e:
            messagebox.showerror("Ошибка загрузки", f"Ошибка при загрузке данных из базы данных: {e}")

    def save_to_db(self):
        grid = self.get_grid()
        if grid is None:
            return

        try:
            self.cursor.execute("DELETE FROM start_data")
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if grid[row][col] != 0:
                        self.cursor.execute(
                            "INSERT INTO start_data (row, col, value) VALUES (?, ?, ?)",
                            (row, col, grid[row][col]),
                        )
            self.conn.commit()
            messagebox.showinfo("Сохранение завершено", "Данные успешно сохранены в базу данных.")
        except mariadb.Error as e:
            messagebox.showerror("Ошибка сохранения", f"Ошибка при сохранении данных в базу данных: {e}")

    def solve_puzzle(self):
        grid = self.get_grid()
        if grid is None:
            return

        # Решение судоку (функция solve должна быть реализована)
        solved = True  # Для демонстрации, заменить реальным алгоритмом

        if solved:
            self.set_grid(grid)
        else:
            messagebox.showerror("Ошибка решения", "Судоку не имеет решений.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
