
"""
IoT-Data-Processing-System - Módulo de Análise de Dados
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class DataAnalyzer:
    def __init__(self):
        self.data = None
        self.model = None
        self.results = {}
    
    def load_data(self, data=None):
        """Carrega ou gera dados de exemplo."""
        if data is None:
            np.random.seed(42)
            self.data = pd.DataFrame({
                'feature1': np.random.randn(1000),
                'feature2': np.random.randn(1000),
                'feature3': np.random.randn(1000),
                'target': np.random.choice([0, 1], 1000)
            })
        else:
            self.data = data
        print(f"Dados carregados: {self.data.shape}")
    
    def analyze(self):
        """Realiza análise abrangente."""
        if self.data is None:
            self.load_data()
        
        self.results['statistics'] = self.data.describe()
        
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        self.results['classification_report'] = classification_report(y_test, y_pred)
        
        return self.results
    
    def visualize(self, repo_name="IoT-Data-Processing-System"):
        """Cria visualizações."""
        if self.data is None:
            self.load_data()
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlações de Features')
        
        plt.subplot(2, 2, 2)
        self.data['feature1'].hist(bins=30, alpha=0.7)
        plt.title('Distribuição da Feature 1')
        
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=self.data, x='feature1', y='feature2', hue='target')
        plt.title('Gráfico de Dispersão de Features')
        
        plt.subplot(2, 2, 4)
        if self.model:
            feature_importance = pd.DataFrame({
                'feature': self.data.drop('target', axis=1).columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            sns.barplot(data=feature_importance, x='importance', y='feature')
            plt.title('Importância das Features')
        
        plt.tight_layout()
        plt.savefig(f'{repo_name.lower()}_analysis.png', dpi=300, bbox_inches='tight')
        # plt.show() # Comentado para evitar interrupção em ambiente headless

def main():
    """Função principal de execução."""
    print(f"Executando Análise do Sistema de Processamento de Dados IoT...")
    analyzer = DataAnalyzer()
    results = analyzer.analyze()
    analyzer.visualize()
    print("Análise concluída com sucesso!")
    return analyzer

if __name__ == "__main__":
    main()

