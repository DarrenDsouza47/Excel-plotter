import re
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import os,glob

pwd=os.getcwd()

# Sample data for demonstration
def excel_storage(code,sdf):
    plot_type_patterns = {
    'plot': r"plt\.plot\(",
    'bar': r"plt\.bar\(",
    'scatter': r"plt\.scatter\(",
    'pie': r"plt\.pie\(",
    'column': r"plt\.column\("
}
    plot_type = None
    for key, pattern in plot_type_patterns.items():
        if re.search(pattern, code):
            plot_type = key
            break
        else:
            plot_type='image'
    
    if plot_type is None:
        plot_type='image'

    # Identify the x and y series data using regex
    x_series=re.search(r"df\['(\w+)'\]", code)
    y_series = re.findall(r"df\['(\w+)'\]", code)

    if x_series and len(y_series) > 1:
        x_series = x_series.group(1)
        y_series = y_series[1]
    else:
        plot_type='image'
    

    # Creating an Excel file with a dynamic graph using xlsxwriter
    output_file = 'dynamic_graph.xlsx'
    
    if plot_type=='image':
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            sdf.to_excel(writer,sheet_name='Data', index=False)
            workbook  = writer.book
            worksheet=writer.sheets['Data']
            file = glob.glob(os.path.join(pwd, "*.png"))
            worksheet.insert_image('J10',file[0])
            workbook.close()

    else:

        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet()
        # Write the data to the worksheet
        worksheet.write(0, 0, x_series)
        worksheet.write(0, 1, y_series)

        for i, (x_val, y_val) in enumerate(zip(sdf[x_series], sdf[y_series])):
            worksheet.write(i + 1, 0, x_val)
            worksheet.write(i + 1, 1, y_val)

        # Create a chart object
        chart = workbook.add_chart({'type': plot_type})
        if not chart:
            raise ValueError(f"Unsupported plot type: {plot_type}")

        chart.add_series({
        'categories': f'=Sheet1!$A$2:$A${len(sdf) + 1}',
        'values': f'=Sheet1!$B$2:$B${len(sdf) + 1}',
        'line': {'color': 'red'},  # Using the color red as in the original plot code
        'marker': {'type': 'circle', 'size': 5},})

        # Add titles and labels
        chart.set_title({'name': 'Net Profit Over Years'})
        chart.set_x_axis({'name': x_series})
        chart.set_y_axis({'name': y_series})

        # Insert the chart into the worksheet
        worksheet.insert_chart('D2', chart)

        # Close the workbook
        workbook.close()

        result = {"type": "plot", "value": output_file}
