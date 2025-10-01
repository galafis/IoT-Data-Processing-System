"""
IoT-Data-Processing-System - Módulo de Utilitários
"""

import yaml
import logging

def load_config(config_path: str = "config.yaml") -> dict:
    """Carrega a configuração de um arquivo YAML."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Arquivo de configuração não encontrado: {config_path}")
        return {}
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return {}

def setup_logging(log_file: str = "app.log", level=logging.INFO):
    """Configura o sistema de logging."""
    logging.basicConfig(filename=log_file, level=level, format='%(asctime)s - %(levelname)s - %(message)s')
    print(f"Logging configurado para {log_file}")

