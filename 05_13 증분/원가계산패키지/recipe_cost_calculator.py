import tkinter as tk    
from tkinter import messagebox, ttk 
import pandas as pd     
from datetime import datetime   

#예시 데이터
df = pd.DataFrame({
    "Name": ["파스타면", "토마토 소스", "올리브 오일", "파마산 치즈", "토마토","양상추","오이","베이비 당근"],
    "Quantity": [3, 2, 1, 5, 4, 1, 1, 1],
    "Unit Price": [1, 1500, 200, 30, 700, 1150, 2350, 4150],
    "Location": ["냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고", "냉장고"],
    "Expiration Date": ["2024-05-20", "2024-05-15", "2024-05-18", "2024-05-25", "2024-05-22", "2024-05-22", "2024-05-22", "2024-05-22"]
})

recipe_data = {
    "스파게티": [("파스타면", 200), ("토마토 소스", 1), ("올리브 오일", 30), ("파마산 치즈", 20)],
    "셀러드": [("양상추", 100), ("토마토", 2), ("오이", 1), ("베이비 당근", 3), ("올리브 오일", 20), ("레몬 주스", 10)],
}

#실제 데이터는 파일을 통해 가져와 저장할 예정

# GUI 초기화
root = tk.Tk()
root.title("원가 계산 프로그램")


def calculate_recipe_cost(recipe_name):
    recipe_ingredients = recipe_data.get(recipe_name)
    if recipe_ingredients:
        total_cost = 0
        shortage = {}  # 부족한 식재료와 그 부족한 양을 저장할 딕셔너리
        missing_ingredients = []  # 데이터프레임에 없는 식재료를 저장할 리스트
        for ingredient, amount in recipe_ingredients:
            ingredient_info = df[df["Name"] == ingredient]
            if not ingredient_info.empty:
                available_quantity = int(ingredient_info.iloc[0]["Quantity"])
                if available_quantity < amount:
                    shortage[ingredient] = amount - available_quantity
                unit_price = float(ingredient_info.iloc[0]["Unit Price"])
                total_cost += unit_price * amount
            else:
                missing_ingredients.append(ingredient)
        return total_cost, shortage, missing_ingredients
    else:
        return None, None, None  # 레시피 정보가 없는 경우

def show_recipe_cost():
    selected_recipe = recipe_combobox.get()  
    if selected_recipe:
        cost, shortage, missing_ingredients = calculate_recipe_cost(selected_recipe)
        if cost is not None:
            message = f"{selected_recipe}의 총 가격: {cost}원"
            if missing_ingredients:
                message = "등록되지 않은 식재료가 존재합니다"
                message += "\n등록되지 않은 식재료:\n"
                for ingredient in missing_ingredients:
                    message += f"- {ingredient}\n"
            elif shortage:
                message += "\n\n부족한 식재료:\n"
                for ingredient, amount in shortage.items():
                    message += f"- {ingredient}: {amount}개\n"
            messagebox.showinfo("레시피 가격, 부족한 식재료, 데이터프레임 부재료", message)
        else:
            messagebox.showerror("에러", "레시피 정보를 가져올 수 없거나 필요한 식재료가 부족합니다.")
    else:
        messagebox.showerror("에러", "레시피를 선택해주세요.")

# 레시피 목록을 표시하는 드롭다운 목록 생성
recipe_combobox = ttk.Combobox(root, values=list(recipe_data.keys()))
recipe_combobox.pack()

# "가격 및 부족한 식재료 보기" 버튼 생성
show_recipe_cost_button = tk.Button(root, text="가격 및 부족한 식재료 보기", command=show_recipe_cost)
show_recipe_cost_button.pack()

# 이벤트 루프 시작
root.mainloop()