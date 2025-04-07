# https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/logo/logo_T_AI_0001.jpg
# https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/{filename}

import pandas as pd

# Load the Excel file
file_path = 'ai.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Define the base URLs
base_url_logo = "https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/logo/logo_{toolid}.jpg"
base_url_ui = "https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/ui/ui_{toolid}.jpg"
base_url_demo1 = "https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/demo1/demo1_{toolid}.jpg"
base_url_demo2 = "https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/demo2/demo2_{toolid}.jpg"
base_url_demo3 = "https://raw.githubusercontent.com/TeamLead2-CM/OSINT_Directory_Resources/test/demo3/demo3_{toolid}.jpg"

# Iterate through the DataFrame and fill the URLs in the new columns
for index, row in df.iterrows():
    tool_id = str(row[0])  # Get the tool ID from column [0] and convert to string
    
    # Format the URLs with the tool ID
    logo_url = base_url_logo.format(toolid=tool_id)
    ui_url = base_url_ui.format(toolid=tool_id)
    demo1_url = base_url_demo1.format(toolid=tool_id)
    demo2_url = base_url_demo2.format(toolid=tool_id)
    demo3_url = base_url_demo3.format(toolid=tool_id)

#Tool Logo Image Github GithubTool Logo Image Github.1 GithubDemo 1 Image Github GithubDemo 2 Image Github GithubDemo 3 Image Github

    # Fill the URLs in the new columns
    df.loc[index, 'Tool Logo Image Github'] = logo_url
    df.loc[index, 'Tool UI Image Github'] = ui_url
    df.loc[index, 'Demo 1 Image Github'] = demo1_url
    df.loc[index, 'Demo 2 Image Github'] = demo2_url
    df.loc[index, 'Demo 3 Image Github'] = demo3_url

# Save the updated DataFrame back to Excel
df.to_excel('github_urls_updated.xlsx', index=False)  # Replace with your desired output file path

print("Excel file updated successfully!")
