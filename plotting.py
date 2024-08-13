import streamlit as st
import plotly.graph_objects as go



def set_default_layout(fig):
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=700, 
        margin=dict(autoexpand=True),
        template="seaborn",
    )
    return fig



def plot_data(df):
    fig = go.Figure()

    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'{col}'], name=f'{col}',             
                     hovertemplate=("y: %{y:.2f} °C<br>" + "x: %{x:.0f} sec<br>"),
                     hoverlabel=dict(font_size=14)
                     ))

    fig.update_layout(  
        xaxis=dict(rangeslider=dict(visible=True), title='Time, seconds'),
        yaxis=dict(title="Temperature, °C"),
        xaxis_rangeslider_thickness = 0.1
    )

    fig = set_default_layout(fig)
    st.plotly_chart(fig, use_container_width=True)




if __name__ == '__main__':
    print('plotting file')