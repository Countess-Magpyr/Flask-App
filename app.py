#Author: RKW
#Date: 12.04.2024
#Version: v5 03.05.2024 
#v1#button scrape added RKW
#v2 Adding extra feature for checkboxes RKW
#v3 Adding app settings to launch RKW
#v4 Building final structure 
#v5 Revamp to look at study review page (data much easier to sort, copied from the body of the html)
#Environment: Python 3
#Packages: flask, beautifulsoup, pandas, tabulate, io
from flask import Flask, render_template, request, Response
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from io import StringIO
import pyexcel as pe


app = Flask(__name__,
 static_url_path='/static')

@app.route('/')
def index(): return render_template('upload.html')


@app.route('/process', methods=['GET','POST'])
def process():
    uploaded_file = request.files.get('file')
    if uploaded_file:
        contents = uploaded_file.read()
    
    soup = BeautifulSoup(contents, 'html.parser')   ## Scrape data from file
    print(soup.prettify())
    

#with open(r"C:\\Users\krebs-wheaton\Desktop\SDVplan_Scraper\body5.html") as fp:

    variableNames= soup.find_all('div',{'class':'BasicCellContentWrapper-sc-90zwts-0 dfaLxd'})

    varName=[]
    for name in variableNames:print( name.get_text())
    for name in variableNames: varName.append(name.get_text())

    num_columns=3
    words_per_columns=len(varName) // num_columns

    varNameData= [(varName[i], varName[i+1] if i + 1 <len(varName) else '') for i in range(0, len(varName), num_columns)]

##for i in range(0, len(varName), num_columns):
##    print('{:15}{}'.format(varName[i], varName[i+1] if i + 1 <len(varName) else ''))

    namedf=pd.DataFrame(varNameData, columns=['Field Name', 'Variable Name'])

    nameddf1=namedf[['Field Name']]

    print(nameddf1)



###################################################################################################
## Grab Form names (dd and dt)
    formNames= soup.find_all('dt')
    formName=[]
    for form in formNames:print(form.get_text())
    for form in formNames: formName.append(form.get_text())

    num_columns=2
    words_per_columns=len(formName) // num_columns

    formNameData= [(formName[i], formName[i+1] if i + 1 <len(formName) else '') for i in range(0, len(formName), num_columns)]



    formdf=pd.DataFrame(formNameData, columns=['Form', 'Form_Name'])

    formddf1=formdf[['Form']]

    print(formddf1)

###################################################################################################
## Grab Event names (dd and dt)
    eventNames= soup.find_all('dd')
    eventName=[]
    for event in eventNames:print(event.get_text())
    for event in eventNames: eventName.append(event.get_text())


    num_columns=2
    words_per_columns=len(formName) // num_columns

    eventNameData= [(eventName[i], eventName[i+1] if i + 1 <len(eventName) else '') for i in range(0, len(eventName), num_columns)]



    eventdf=pd.DataFrame(eventNameData, columns=['Event', 'Classification'])

    print(eventdf)


#################################################################################################

    merged_df=pd.merge(pd.merge(formddf1, eventdf, left_index=True, right_index=True), nameddf1, left_index=True, right_index=True)

    grouped= merged_df.groupby(['Form'])

   # category_groups = {k: v for k, v in merged_df.groupby('Form')}

    #for category, group_df in category_groups.items():print (f"DataFrame for Category {category}:\n{group_df}\n")

    #data_sums={k: v['Event'].sum()
            #   for k, v in category_groups.items()}
   # print(data_sums)

    html_tables={}
    for(form), data_group in grouped:html_tables[(form)]=data_group.to_html(index=False) 

    tables_list=[]

    for(form), table in html_tables.items():tables_list.append({"Form":form, "table":table})
        


    #for form in category_groups.items():html_tables[category]=group_df.to_html()

   # table_data2=group_df.values.tolist()
   # headers2=group_df.columns.tolist()

# table_str2=tabulate(table_data2, headers=headers2, tablefmt='html')
  #  print(table_str2)
    
#merged_df.to_csv('merged_data.csv', index=False)

    table_data=merged_df.values.tolist()
    headers=merged_df.columns.tolist()

    table_str=tabulate(table_data, headers=headers, tablefmt='html')
    print(table_str)


    return render_template('result.html', table=tables_list)


@app.route('/download', methods=['GET','POST'])
def download():
    uploaded = request.files.get('file2')
    if uploaded:
        content2 = uploaded.read()
    
    soup2 = BeautifulSoup(content2, 'html.parser')   ## Scrape data from file
    print(soup2.prettify())
    

#with open(r"C:\\Users\krebs-wheaton\Desktop\SDVplan_Scraper\body5.html") as fp:

    variableNames= soup2.find_all('div',{'class':'BasicCellContentWrapper-sc-90zwts-0 dfaLxd'})

    varName=[]
    for name in variableNames:print( name.get_text())
    for name in variableNames: varName.append(name.get_text())

    num_columns=3
    words_per_column=len(varName) // num_columns

    varNameData= [(varName[i], varName[i+1] if i + 1 <len(varName) else '') for i in range(0, len(varName), num_columns)]

##for i in range(0, len(varName), num_columns):
##    print('{:15}{}'.format(varName[i], varName[i+1] if i + 1 <len(varName) else ''))

    namedf2=pd.DataFrame(varNameData, columns=['Field Name', 'Variable Name'])

    
    nameddf2=namedf2[['Field Name']]

    print(nameddf2)




###################################################################################################
## Grab Form names (dd and dt)
    formNames= soup2.find_all('dt')
    formName=[]
    for form in formNames:print(form.get_text())
    for form in formNames: formName.append(form.get_text())

    num_columns=2
    words_per_column=len(formName) // num_columns

    formNameData= [(formName[i], formName[i+1] if i + 1 <len(formName) else '') for i in range(0, len(formName), num_columns)]



    formdf2=pd.DataFrame(formNameData, columns=['Form', 'Form_Name'])

    formddf2=formdf2[['Form']]



    print(formddf2)

###################################################################################################
## Grab Event names (dd and dt)
    eventNames= soup2.find_all('dd')
    eventName=[]
    for event in eventNames:print(event.get_text())
    for event in eventNames: eventName.append(event.get_text())


    num_columns=2
    words_per_column=len(eventName) // num_columns

    eventNameData= [(eventName[i], eventName[i+1] if i + 1 <len(eventName) else '') for i in range(0, len(eventName), num_columns)]



    eventdf2=pd.DataFrame(eventNameData, columns=['Event', 'Classification'])

    print(eventdf2)


    df2=pd.merge(pd.merge(formddf2, eventdf2, left_index=True, right_index=True), nameddf2, left_index=True, right_index=True)
 

    output=StringIO()
    df2.to_csv(output, index=False)

    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=data.csv'})
    

if __name__ =='__main__': 
    app.run(host='0.0.0.0')











