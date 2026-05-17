#!/usr/bin/env python3
"""
短链接生成工具 - 使用免费API缩短URL
"""
import sys, json, tkinter as tk
from tkinter import messagebox, scrolledtext
import urllib.request
import urllib.parse

class App:
    def __init__(self, root):
        self.root = root
        root.title("短链接生成工具 v1.0")
        root.geometry("650x500")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#e65100", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔗 短链接生成工具", font=("Arial",14,"bold"),
                 fg="white", bg="#e65100").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        tk.Label(main, text="输入长链接：", font=("Arial",11)).pack(anchor="w", pady=5)
        self.url_entry = tk.Entry(main, font=("Arial",11), width=60)
        self.url_entry.pack(fill="x", pady=5)
        self.url_entry.insert(0, "https://github.com/102839544")
        
        tk.Button(main, text="生成短链接", command=self.shorten,
                  bg="#e65100", fg="white", font=("Arial",11,"bold"),
                  padx=25, pady=8).pack(pady=15)
        
        tk.Label(main, text="短链接列表：", font=("Arial",10,"bold")).pack(anchor="w")
        self.lb = tk.Listbox(main, font=("Consolas",10), bg="#fff3e0", height=12)
        self.lb.pack(fill="both", expand=True, pady=5)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="复制选中", command=self.copy_selected,
                  padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="清空列表", command=lambda: self.lb.delete(0, "end"),
                  bg="#d9534f", fg="white", padx=15).pack(side="left", padx=5)
        
        self.status = tk.Label(main, text="使用免费短链接服务",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def shorten(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入链接")
            return
        
        try:
            self.status.config(text="生成中...")
            self.root.update()
            
            # 使用 is.gd 免费API
            api_url = f"https://is.gd/create.php?format=json&url={urllib.parse.quote(url)}"
            
            with urllib.request.urlopen(api_url, timeout=10) as resp:
                result = json.loads(resp.read().decode())
            
            if "shorturl" in result:
                short_url = result["shorturl"]
                self.lb.insert(0, f"{short_url}")
                self.status.config(text=f"✅ 生成成功")
                messagebox.showinfo("成功", f"短链接：{short_url}")
            else:
                raise Exception(result.get("errormessage", "未知错误"))
                
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 生成失败")
    
    def copy_selected(self):
        sel = self.lb.curselection()
        if sel:
            text = self.lb.get(sel[0])
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("复制成功", f"已复制：{text}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
