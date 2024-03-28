import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def main():
    with st.sidebar: 
        st.title("Instrucciones")
        st.write("¡Bienvenido a la aplicación de análisis de pérdidas!")
        st.markdown("Por favor sigue las instrucciones paso a paso para utilizar la herramienta correctamente.")
        
        # Pasos para el registro de pérdidas
        st.markdown("### Pasos:")
        st.markdown("- **Paso 1:** Ingresa el número de líneas de producción.")
        st.markdown("- **Paso 2:** Para cada línea de producción, ingresa el nombre y las entradas de pérdida asociadas.")
        # Ejemplo de Datos
        st.sidebar.subheader("Ejemplo de Datos:")
        example_data = {
            "Línea de Producción": ["Línea 1", "Línea 1", "Línea 2", "Línea 2", "Línea 2"],
            "Descripción del Tiempo Muerto": ["Falla de equipo", "Cambio de producto", "Espera de material", "Falla de equipo", "Defectos de calidad"],
            "Sub Categoría": ["Paro de equipo", "Preparaciones previas", "Paro de equipo", "Paro de equipo", "Inspecciones"],
            "Tipo de Pérdida": ["Disponibilidad", "Disponibilidad", "Disponibilidad", "Disponibilidad", "Calidad"],
            "Tiempo Perdido (minutos)": [30, 20, 15, 25, 10]
        }
        example_df = pd.DataFrame(example_data)
        st.sidebar.write(example_df)

        st.markdown("- **Paso 3:** Observa el gráfico de Árbol de Pérdidas que muestra la distribución de pérdidas por categorías.")
        st.markdown("- **Paso 4:** ¡Listo! Puedes ver los datos ingresados en la tabla debajo del gráfico.")      
        
        # Información adicional
        st.markdown("### Información Adicional:")
        st.markdown("👉 **Para más información: [LinkedIn](https://www.linkedin.com/in/josemaguilar/)**")

    st.image("arbol.jpg", width=720) 
    st.sidebar.header("Registro de Pérdidas")

    num_lines = st.sidebar.number_input('Número de Líneas de Producción', min_value=1, step=1, value=1, format='%d')

    if num_lines < 1:
        st.sidebar.warning("Debe ingresar al menos una línea de producción.")
        return

    # Crear una lista para almacenar los datos de pérdidas
    data = []

    for i in range(num_lines):
        st.sidebar.markdown(f"**Línea de Producción {i+1}**")
        line_name = st.sidebar.text_input(f'Nombre de la Línea de Producción {i+1}', key=f'line_name_{i}')
        num_entries = st.sidebar.number_input(f'Número de Entradas para la Línea {i+1}', min_value=0, step=1, value=0, format='%d')

        for j in range(num_entries):
            downtime = st.sidebar.text_input(f'Tiempo Muerto - Línea {i+1} - Entrada {j+1}', key=f'downtime_{i}_{j}')
            sub_category = st.sidebar.selectbox(f'Sub Categoría - Línea {i+1} - Entrada {j+1}', ['Paro de equipo', 'Preparaciones previas', 'Velocidad de máquina', 'Defectos/Rechazos', 'Inspecciones'], key=f'sub_category_{i}_{j}')
            loss_type = st.sidebar.selectbox(f'Tipo de Pérdida - Línea {i+1} - Entrada {j+1}', ['Disponibilidad', 'Rendimiento', 'Calidad'], key=f'loss_type_{i}_{j}')
            time_lost = st.sidebar.number_input(f'Tiempo Perdido (minutos) - Línea {i+1} - Entrada {j+1}', min_value=0.0, step=0.1, value=0.0, key=f'time_lost_{i}_{j}')

            data.append({'Línea de Producción': line_name,
                         'Descripción del Tiempo Muerto': downtime,
                         'Sub Categoría': sub_category,
                         'Tipo de Pérdida': loss_type,
                         'Tiempo Perdido (minutos)': time_lost})

    df = pd.DataFrame(data)

    plot_sankey_chart(df)

    # Mostrar los datos ingresados en la aplicación
    st.write(df)

def plot_sankey_chart(df):
    # Crear listas para almacenar los nodos y enlaces del diagrama Sankey
    nodes = []

    # Añadir nodos para las líneas de producción, descripción del tiempo muerto, subcategoría y tipo de pérdida
    for _, row in df.iterrows():
        nodes.append(row['Descripción del Tiempo Muerto'])
        nodes.append(row['Línea de Producción'])
        nodes.append(row['Sub Categoría'])
        nodes.append(row['Tipo de Pérdida'])

    # Eliminar duplicados de la lista de nodos
    unique_nodes = list(set(nodes))

    # Crear diccionario para asignar índices a cada nodo
    node_indices = {node: idx for idx, node in enumerate(unique_nodes)}

    # Crear lista de enlaces para el diagrama Sankey
    links = []
    for _, row in df.iterrows():
        links.append({'source': node_indices[row['Descripción del Tiempo Muerto']], 'target': node_indices[row['Sub Categoría']], 'value': row['Tiempo Perdido (minutos)']})
        links.append({'source': node_indices[row['Sub Categoría']], 'target': node_indices[row['Tipo de Pérdida']], 'value': row['Tiempo Perdido (minutos)']})
        links.append({'source': node_indices[row['Tipo de Pérdida']], 'target': node_indices[row['Línea de Producción']], 'value': row['Tiempo Perdido (minutos)']})

    # Crear el objeto de figura Sankey
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=unique_nodes,
            color="blue"
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links]
        )
    )])

    # Configurar el diseño y el título del gráfico
    fig.update_layout(
        title="Árbol de Pérdidas",
        font=dict(size=10)
    )

    # Mostrar el gráfico en la aplicación
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
