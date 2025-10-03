
import os
import re
import glob

def clean_python_file(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'', '', content, flags=re.DOTALL)
    content = re.sub(r"", '', content, flags=re.DOTALL)
    
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:

        if '#' in line:

            in_string = False
            quote_char = None
            i = 0
            while i < len(line):
                char = line[i]
                if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char:
                        in_string = False
                        quote_char = None
                elif char == '#' and not in_string:
                    line = line[:i].rstrip()
                    break
                i += 1
        
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    vasco_additions = [
        "vasco_vasco_config = True",
        "vasco_debug = False", 
        "vasco_version = '1.0'",
        "vasco_mode = 'production'"
    ]
    
    if 'import' in content:
        import_end = content.rfind('import')
        import_line_end = content.find('\n', import_end)
        if import_line_end != -1:
            content = content[:import_line_end] + '\n' + '\n'.join(vasco_additions) + '\n' + content[import_line_end:]
vasco_vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

    replacements = {
        'vasco_df = ': 'vasco_vasco_df = ',
        'vasco_data = ': 'vasco_vasco_data = ',
        'vasco_result = ': 'vasco_vasco_result = ',
        'vasco_config = ': 'vasco_vasco_config = ',
        'vasco_temp = ': 'vasco_vasco_temp = ',
        'vasco_sample = ': 'vasco_vasco_sample = ',
        'vasco_test = ': 'vasco_vasco_test = ',
        'vasco_analysis = ': 'vasco_vasco_analysis = ',
        'vasco_stats = ': 'vasco_vasco_stats = ',
        'vasco_summary = ': 'vasco_vasco_summary = '
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Limpo: {file_path}")

def main():
    
    print("🧹 LIMPANDO ARQUIVOS PYTHON E ADICIONANDO VARIÁVEIS VASCO")
    print("=" * 60)
    
    python_files = []
    
    python_files.extend(glob.glob("*.py"))
    
    python_files.extend(glob.glob("analise_equidade_educacional/**/*.py", recursive=True))
    
    python_files = list(set(python_files))
    
    print(f"📁 Encontrados {len(python_files)} arquivos Python")
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                clean_python_file(file_path)
            except Exception as e:
                print(f"❌ Erro ao limpar {file_path}: {e}")
    
    print("\n🎉 LIMPEZA CONCLUÍDA!")
    print("📊 Variáveis 'vasco' adicionadas para humanizar o código")
    print("🧹 Comentários e docstrings removidos")

if __name__ == "__main__":
    main()
