import matplotlib.pyplot as plt
import plotly.express as px

class VisualizationService:
    def generate_price_chart(self, data):
        """Genera un gráfico de precios con Matplotlib."""
        plt.plot(data['dates'], data['prices'])
        plt.title('Precio de Activos')
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.show()

    def generate_interactive_dashboard(self, data):
        """Genera un dashboard interactivo con Plotly."""
        fig = px.line(data, x='dates', y='prices', title='Evolución de Precios')
        fig.show()
