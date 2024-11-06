import streamlit as st
import plotly.graph_objects as go


# Set the configuration for the Plotly chart, including the resolution settings
config = {
    "toImageButtonOptions": {
        "format": "png",  # The format of the exported image (png, svg, etc.)
        "filename": "pcm_data_plot",  # Default filename
        # "height": 1080,  # Image height
        # "width": 1920,   # Image width
        "scale": 3       # Increase the resolution (scales up the image)
    }
}

def set_default_layout(fig):
    fig.update_layout(
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500, 
        margin=dict(l=5, r=5, t=50, b=50),
        template="seaborn",
    )
    return fig



def plot_data(df, rangesliderBool=True):
    fig = go.Figure()

    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'{col}'], name=f'{col}',             
                     hovertemplate=("y: %{y:.2f} °C<br>" + "x: %{x:.0f} sec<br>"),
                     hoverlabel=dict(font_size=14)
                     ))

    fig.update_layout(  
        xaxis=dict(rangeslider=dict(visible=rangesliderBool), title='Time, seconds'),
        yaxis=dict(title="Temperature, °C"),
        xaxis_rangeslider_thickness = 0.1
    )

    fig = set_default_layout(fig)
    
    st.plotly_chart(fig, use_container_width=True, config=config)



if __name__ == '__main__':
    print('plotting file')