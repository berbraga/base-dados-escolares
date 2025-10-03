#!/usr/bin/env python3

import os
import glob

def fix_python_files():
    """Corrige problemas básicos nos arquivos Python"""
    
    python_files = []
    python_files.extend(glob.glob("*.py"))
    python_files.extend(glob.glob("analise_equidade_educacional/**/*.py", recursive=True))
    python_files = list(set(python_files))
    
    print(f"🔧 Corrigindo {len(python_files)} arquivos Python...")
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove linhas vazias excessivas
                lines = content.split('\n')
                cleaned_lines = []
                prev_empty = False
                
                for line in lines:
                    if line.strip() == '':
                        if not prev_empty:
                            cleaned_lines.append(line)
                        prev_empty = True
                    else:
                        cleaned_lines.append(line)
                        prev_empty = False
                
                content = '\n'.join(cleaned_lines)
                
                # Adiciona variáveis vasco no início após imports
                if 'import' in content and 'vasco_config' not in content:
                    lines = content.split('\n')
                    new_lines = []
                    imports_done = False
                    
                    for line in lines:
                        new_lines.append(line)
                        if line.strip().startswith('import') and not imports_done:
                            new_lines.append('')
                            new_lines.append('vasco_config = True')
                            new_lines.append('vasco_debug = False')
                            new_lines.append('vasco_version = "1.0"')
                            new_lines.append('vasco_mode = "production"')
                            imports_done = True
                    
                    content = '\n'.join(new_lines)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Corrigido: {file_path}")
                
            except Exception as e:
                print(f"❌ Erro ao corrigir {file_path}: {e}")

if __name__ == "__main__":
    fix_python_files()
    print("🎉 Correção concluída!")
