import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re

class DuplicateRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Удаление повторяющихся строк")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Настраиваем стиль
        self.setup_styles()
        
        # Основной контейнер с отступами
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="Удаление дубликатов строк", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Счетчик строк
        self.stats_label = ttk.Label(title_frame, text="Готов к работе", 
                                   font=('Segoe UI', 10))
        self.stats_label.pack(side=tk.RIGHT)
        
        # Фрейм для ввода
        input_frame = ttk.LabelFrame(main_container, text="📝 Исходный текст", padding=15)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Создаем фрейм для кнопок над текстовым полем
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.paste_button = ttk.Button(input_buttons_frame, text="📋 Вставить", 
                                     command=self.paste_text, style="Action.TButton")
        self.paste_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_input_button = ttk.Button(input_buttons_frame, text="🗑️ Очистить", 
                                           command=self.clear_input)
        self.clear_input_button.pack(side=tk.LEFT)
        
        # Поле ввода с улучшенным дизайном
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=8, 
            font=('Consolas', 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.update_input_stats)
        
        # Центральная панель с кнопкой обработки
        process_frame = ttk.Frame(main_container)
        process_frame.pack(fill=tk.X, pady=10)
        
        self.process_button = ttk.Button(
            process_frame, 
            text="⚡ Обработать текст", 
            command=self.remove_duplicates,
            style="Process.TButton"
        )
        self.process_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(process_frame, mode='indeterminate', length=100)
        self.progress.pack(side=tk.RIGHT)
        
        # Фрейм для результата
        output_frame = ttk.LabelFrame(main_container, text="✅ Результат", padding=15)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Кнопки над результатом
        output_buttons_frame = ttk.Frame(output_frame)
        output_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.copy_button = ttk.Button(output_buttons_frame, text="📋 Копировать", 
                                    command=self.copy_result, style="Action.TButton")
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(output_buttons_frame, text="💾 Сохранить", 
                                    command=self.save_result)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_output_button = ttk.Button(output_buttons_frame, text="🗑️ Очистить", 
                                            command=self.clear_output)
        self.clear_output_button.pack(side=tk.LEFT)
        
        # Статистика результата
        self.result_stats_label = ttk.Label(output_buttons_frame, text="", 
                                          font=('Segoe UI', 9, 'italic'))
        self.result_stats_label.pack(side=tk.RIGHT)
        
        # Поле результата
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            height=8, 
            font=('Consolas', 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_bar = ttk.Label(main_container, text="Готов к работе", 
                                  relief=tk.SUNKEN, anchor=tk.W, 
                                  font=('Segoe UI', 9))
        self.status_bar.pack(fill=tk.X, pady=(10, 0), ipady=5)
        
        # Горячие клавиши
        self.setup_hotkeys()
        
        # Начальное состояние кнопок
        self.update_button_states()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Кнопка обработки
        style.configure("Process.TButton", 
                       font=('Segoe UI', 11, 'bold'))
        
        # Кнопки действий
        style.configure("Action.TButton", 
                       font=('Segoe UI', 10))
    
    def setup_hotkeys(self):
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-Return>', lambda e: self.remove_duplicates())
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<F5>', lambda e: self.remove_duplicates())
    
    def paste_text(self):
        try:
            clipboard_content = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", clipboard_content)
            self.update_input_stats()
            self.status_bar.config(text="Текст вставлен из буфера обмена")
        except tk.TclError:
            messagebox.showwarning("Предупреждение", "Буфер обмена пуст")
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.update_input_stats()
        self.status_bar.config(text="Поле ввода очищено")
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.result_stats_label.config(text="")
        self.status_bar.config(text="Поле результата очищено")
        self.update_button_states()
    
    def update_input_stats(self, event=None):
        content = self.input_text.get("1.0", tk.END).strip()
        if content:
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            self.stats_label.config(text=f"Строк: {len(lines)}")
        else:
            self.stats_label.config(text="Готов к работе")
        self.update_button_states()
    
    def update_button_states(self):
        # Проверяем есть ли текст для обработки
        has_input = bool(self.input_text.get("1.0", tk.END).strip())
        has_output = bool(self.output_text.get("1.0", tk.END).strip())
        
        # Управляем состоянием кнопок
        self.process_button.config(state=tk.NORMAL if has_input else tk.DISABLED)
        self.copy_button.config(state=tk.NORMAL if has_output else tk.DISABLED)
        self.save_button.config(state=tk.NORMAL if has_output else tk.DISABLED)
    
    def show_progress(self, show=True):
        if show:
            self.progress.start(10)
            self.process_button.config(state=tk.DISABLED)
        else:
            self.progress.stop()
            self.update_button_states()
    
    def remove_duplicates(self):
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        if not input_content:
            messagebox.showwarning("Предупреждение", "Пожалуйста, вставьте текст для обработки")
            return
        
        # Показываем прогресс
        self.show_progress(True)
        
        # Обрабатываем через небольшую задержку для показа прогресса
        self.root.after(100, self._process_text, input_content)
    
    def _process_text(self, input_content):
        try:
            lines = input_content.split('\n')
            original_count = len([line for line in lines if line.strip()])
            
            # Удаляем повторяющиеся строки
            seen = set()
            unique_lines = []
            duplicates_count = 0
            
            for line in lines:
                line = line.strip()
                if line:
                    if line in seen:
                        duplicates_count += 1
                    else:
                        seen.add(line)
                        unique_lines.append(line)
            
            # Форматируем результат
            formatted_result = []
            processed_count = 0
            
            for line in unique_lines:
                # Ищем паттерн: никнейм + пробелы + числа
                match = re.match(r'^(.+?)\s+(\d+)$', line)
                if match:
                    nickname = match.group(1).strip()
                    user_id = match.group(2)
                    formatted_result.append(f"{nickname} - {user_id}")
                    processed_count += 1
                else:
                    formatted_result.append(line)
            
            # Выводим результат
            result = '\n'.join(formatted_result)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
            # Обновляем статистику
            unique_count = len(unique_lines)
            self.result_stats_label.config(
                text=f"Уникальных: {unique_count} | Удалено дубликатов: {duplicates_count}"
            )
            
            # Статус
            if duplicates_count > 0:
                self.status_bar.config(text=f"✅ Обработано! Удалено {duplicates_count} дубликатов из {original_count} строк")
            else:
                self.status_bar.config(text=f"✅ Обработано! Дубликатов не найдено ({original_count} строк)")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обработке текста: {str(e)}")
            self.status_bar.config(text=f"❌ Ошибка обработки")
        
        finally:
            self.show_progress(False)
    
    def copy_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            
            # Анимация кнопки
            original_text = self.copy_button.cget("text")
            self.copy_button.config(text="✅ Скопировано!")
            self.status_bar.config(text="📋 Результат скопирован в буфер обмена")
            
            # Возвращаем текст кнопки
            self.root.after(2000, lambda: self.copy_button.config(text=original_text))
        else:
            messagebox.showwarning("Предупреждение", "Нет результата для копирования")
    
    def save_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("Предупреждение", "Нет результата для сохранения")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            title="Сохранить результат"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                self.status_bar.config(text=f"💾 Результат сохранен: {filename}")
                messagebox.showinfo("Успех", f"Результат сохранен в файл:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

def main():
    root = tk.Tk()
    
    # Устанавливаем иконку (если есть)
    try:
        root.iconbitmap(default="app.ico")
    except:
        pass
    
    app = DuplicateRemover(root)
    
    # Центрируем окно
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()