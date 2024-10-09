import tkinter as tk
from tkinter import simpledialog, messagebox
import spacy
import json
import os

# Carregar o modelo de spaCy (pode ser um modelo pré-treinado ou um modelo vazio)
nlp = spacy.blank("pt")  # Para português

# Contador global para arquivos incrementais
global_counter = 0

# Caminho para o arquivo de entidades
ENTITIES_FILE = "entities.json"

class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Anotação de NER")

        # Frame principal para o layout
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame para o texto e anotações
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Texto de entrada
        self.text = tk.Text(text_frame, wrap='word', width=80, height=20)
        self.text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame para botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=5)
        
        # Botão de anotação
        self.annotate_button = tk.Button(button_frame, text="Anotar Entidade", command=self.annotate_entity)
        self.annotate_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Botão de salvar
        self.save_button = tk.Button(button_frame, text="Salvar Anotações", command=self.save_annotations)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Botão para gerenciar entidades
        self.manage_entities_button = tk.Button(button_frame, text="Gerenciar Entidades", command=self.manage_entities)
        self.manage_entities_button.grid(row=0, column=2, padx=5, pady=5)

        self.annotations = []
        self.entities = {}
        self.load_entities()
        #self.load_existing_annotations()

    def annotate_entity(self):
        start_idx = self.text.index(tk.SEL_FIRST)
        end_idx = self.text.index(tk.SEL_LAST)
        entity_text = self.text.get(start_idx, end_idx)
        
        if self.entities:
            self.show_entity_selection_dialog(start_idx, end_idx, entity_text)
        else:
            entity_type = simpledialog.askstring("Input", f"Qual o tipo da entidade '{entity_text}'?")
            if entity_type:
                self.add_annotation(start_idx, end_idx, entity_type)
                self.text.tag_add(entity_type, start_idx, end_idx)
                self.text.tag_config(entity_type, background="yellow")

    def show_entity_selection_dialog(self, start_idx, end_idx, entity_text):
        def on_select():
            selected_entity = listbox.get(tk.ACTIVE)
            if selected_entity:
                self.add_annotation(start_idx, end_idx, selected_entity)
                self.text.tag_add(selected_entity, start_idx, end_idx)
                self.text.tag_config(selected_entity, background="yellow")
                selection_window.destroy()

        selection_window = tk.Toplevel(self.root)
        selection_window.title("Selecionar Entidade")

        tk.Label(selection_window, text=f"Selecione a entidade para '{entity_text}':").pack(padx=10, pady=5)
        
        listbox = tk.Listbox(selection_window)
        for entity in self.entities.keys():
            listbox.insert(tk.END, entity)
        listbox.pack(padx=10, pady=5)

        select_button = tk.Button(selection_window, text="Selecionar", command=on_select)
        select_button.pack(pady=5)
        
        cancel_button = tk.Button(selection_window, text="Cancelar", command=selection_window.destroy)
        cancel_button.pack(pady=5)

    def add_annotation(self, start_idx, end_idx, entity_type):
        start = int(start_idx.split('.')[1])
        end = int(end_idx.split('.')[1])
        self.annotations.append((start, end, entity_type))
        if entity_type not in self.entities:
            self.entities[entity_type] = []
        # Atualiza a interface com a nova anotação
        self.text.tag_add(entity_type, start_idx, end_idx)
        self.text.tag_config(entity_type, background="yellow")

    def get_next_filename(self):
        global global_counter
        while True:
            filename = f"annotations_{global_counter}.json"
            if not os.path.exists(filename):
                break
            global_counter += 1
        return filename

    def save_annotations(self):
        global global_counter
        raw_text = self.text.get("1.0", tk.END)
        annotated_data = {
            "text": raw_text,
            "entities": self.annotations
        }
        filename = self.get_next_filename()
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(annotated_data, f, ensure_ascii=False, indent=2)
        print(f"Anotações salvas em {filename}")
        
        # Limpar texto e anotações
        self.text.delete("1.0", tk.END)
        self.annotations = []

    def load_entities(self):
        if os.path.exists(ENTITIES_FILE):
            with open(ENTITIES_FILE, "r", encoding='utf-8') as f:
                self.entities = json.load(f)
        else:
            self.entities = {}

    def save_entities(self):
        with open(ENTITIES_FILE, "w", encoding='utf-8') as f:
            json.dump(self.entities, f, ensure_ascii=False, indent=2)

    def load_existing_annotations(self):
        # Carregar e aplicar anotações existentes
        for file in sorted(os.listdir(), reverse=True):
            if file.startswith("annotations_") and file.endswith(".json"):
                with open(file, "r", encoding='utf-8') as f:
                    existing_data = json.load(f)
                    self.text.delete("1.0", tk.END)
                    self.text.insert(tk.END, existing_data["text"])
                    self.annotations = existing_data["entities"]
                    self.apply_annotations()
                break

    def apply_annotations(self):
        for start, end, entity_type in self.annotations:
            start_idx = f"1.{start}"
            end_idx = f"1.{end}"
            self.text.tag_add(entity_type, start_idx, end_idx)
            self.text.tag_config(entity_type, background="yellow")
            if entity_type not in self.entities:
                self.entities[entity_type] = []

    def manage_entities(self):
        entity_names = list(self.entities.keys())
        new_entity = simpledialog.askstring("Gerenciar Entidades", 
            f"Entidades existentes: {', '.join(entity_names)}\nAdicione uma nova entidade ou deixe em branco para cancelar:")
        
        if new_entity:
            if new_entity not in self.entities:
                self.entities[new_entity] = []
                self.save_entities()  # Salvar entidades ao adicionar nova
                messagebox.showinfo("Sucesso", f"Entidade '{new_entity}' adicionada.")
            else:
                messagebox.showinfo("Informação", f"A entidade '{new_entity}' já existe.")

if __name__ == "__main__":
    root = tk.Tk()
    tool = AnnotationTool(root)
    root.mainloop()
