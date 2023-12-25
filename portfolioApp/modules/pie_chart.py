import matplotlib
matplotlib.use('Agg')  # Set the Agg backend

import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
def pie_chart(assets, total_spent):
    data = assets.groupby("asset_class").sum("total_amount")
    labels = list(data.index)
    # print("labels ",labels)
    data = data.reset_index(drop=True)
    print("data ",data)
    values = list(data["total_amount"]*100/total_spent)

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    ax.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    plt.clf()  # Clear the figure
    
    image_uri = base64.b64encode(image_png).decode('utf-8')
    return image_uri