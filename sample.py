import csv
import unicodedata
import tkinter as tk
from tkinter import ttk, messagebox

# カードデータを格納するクラス
class CardManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.cards = self.load_cards()

    # CSVからカードデータをロードする
    def load_cards(self):
        cards = {}
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cards[self.normalize_card_name(row['CardName'])] = int(row['Count'])
        except FileNotFoundError:
            print(f"{self.csv_file} が見つかりませんでした。")
        return cards

    # CSVにカードデータを保存する
    def save_cards(self):
        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['CardName', 'Count'])
            writer.writeheader()
            for card, count in self.cards.items():
                writer.writerow({'CardName': card, 'Count': count})

    # カード名の正規化を行う（全角と半角の違いを吸収する）
    def normalize_card_name(self, card_name):
        return unicodedata.normalize('NFKC', card_name)

    # カードの枚数を追加・変更する
    def update_card_count(self, card_name, count):
        normalized_name = self.normalize_card_name(card_name)
        if normalized_name in self.cards:
            self.cards[normalized_name] += count
        else:
            self.cards[normalized_name] = count
        self.save_cards()

    # 部分一致でカードを検索する
    def search_card(self, card_name):
        normalized_name = self.normalize_card_name(card_name)
        results = {card: count for card, count in self.cards.items() if normalized_name in card}
        return results

# GUIクラス
class CardManagerApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("カード管理システム")
        self.geometry("500x500")
        self.configure(bg="#2E2E2E")  # ダークモードの背景色

        # スタイリング設定
        style = ttk.Style(self)
        style.theme_use("clam")  # モダンなテーマを使用
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4A90E2", foreground="white")
        style.configure("TLabel", font=("Helvetica", 12), background="#2E2E2E", foreground="white")
        style.configure("TEntry", font=("Helvetica", 12))

        # メインフレーム
        main_frame = ttk.Frame(self, padding=(20, 10), style="TFrame")
        main_frame.pack(expand=True)

        # タイトルラベル
        title_label = ttk.Label(main_frame, text="カード管理システム", font=("Helvetica", 18, "bold"), style="TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # カード名エントリー
        card_name_label = ttk.Label(main_frame, text="カード名:", style="TLabel")
        card_name_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.card_name_entry = ttk.Entry(main_frame, width=30)
        self.card_name_entry.grid(row=1, column=1, pady=5)

        # カード数エントリー
        card_count_label = ttk.Label(main_frame, text="枚数:", style="TLabel")
        card_count_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.card_count_entry = ttk.Entry(main_frame, width=10)
        self.card_count_entry.grid(row=2, column=1, pady=5, sticky="w")

        # ボタン群
        button_frame = ttk.Frame(main_frame, padding=(10, 5))
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        display_button = ttk.Button(button_frame, text="カードリストを表示", command=self.display_cards)
        display_button.grid(row=0, column=0, padx=5, pady=5)

        update_button = ttk.Button(button_frame, text="枚数を更新", command=self.update_card)
        update_button.grid(row=0, column=1, padx=5, pady=5)

        search_button = ttk.Button(button_frame, text="カードを検索", command=self.search_card)
        search_button.grid(row=0, column=2, padx=5, pady=5)

    # カードリストを表示
    def display_cards(self):
        cards = self.manager.get_cards()
        if cards:
            card_list = "\n".join([f"{card}: {count}枚" for card, count in cards.items()])
            messagebox.showinfo("カードリスト", card_list)
        else:
            messagebox.showinfo("カードリスト", "カードがありません。")

    # カードの枚数を更新
    def update_card(self):
        card_name = self.card_name_entry.get()
        try:
            count = int(self.card_count_entry.get())
            self.manager.update_card_count(card_name, count)
            messagebox.showinfo("更新", f"{card_name}の枚数を更新しました。")
        except ValueError:
            messagebox.showerror("エラー", "有効な枚数を入力してください。")

    # カードを検索
    def search_card(self):
        card_name = self.card_name_entry.get()
        results = self.manager.search_card(card_name)
        if results:
            result_list = "\n".join([f"{card}: {count}枚" for card, count in results.items()])
            messagebox.showinfo("検索結果", result_list)
        else:
            messagebox.showinfo("検索結果", f"{card_name}を含むカードは見つかりませんでした。")

# メインのアプリケーション
def main():
    manager = CardManager('CardList.csv')
    app = CardManagerApp(manager)
    app.mainloop()

if __name__ == "__main__":
    main()
