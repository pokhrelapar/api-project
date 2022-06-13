
import requests
from requests import Session
import base64
import pandas as pd



API_KEY = 'EAF5107A-B955-484C-9723-3F16D3188E32'

'''
  Class with methods to retrieve the end points

'''



class NPG:

    #https://docs.ngpvan.com/reference/broadcastemails

    def __init__(self, token):
        self.apiurl = 'https://api.myngp.com'
        self.username = 'apiuser'
        self.authString = self.username+':'+ token
        self.encodedString = base64.b64encode(self.authString.encode()).decode()
        self.headers = headers = {"Accept": "application/json","Authorization": "Basic %s" % self.encodedString}
        self.session = Session()
        self.session.headers.update(self.headers)


    '''
        Returns all the emails in the endpoint. By default 9 emails were retrieved
        even when using top paramter with value > 
    '''
    def getAllEmails(self):
        url = self.apiurl + '/v2/broadcastEmails'
        r = self.session.get(url)
        data = r.json()
        return data


    '''
       Returns the statistics  for  a given message id. 
    '''

    def getEmailMessageStats(self,emailMessageId):
        url = self.apiurl + f"/v2/broadcastEmails/{emailMessageId}" 
        parameters = {"$expand":"statistics"}
        r = self.session.get(url,params=parameters)
        data = r.json()['statistics']
        return data


    '''
       Returns the  details on all the email message variant associated with given a message id.
    '''

    def getEmailMessageVariants(self,emailMessageId):
        url = self.apiurl + f"/v2/broadcastEmails/{emailMessageId}" 
        r = self.session.get(url)
        data = r.json()
        return data


    '''
      Returns  details on an email message variant given a message id and a variant
      associated with that email id. 

      The optional $expand=statistics parameter provides additional statistics about this email message variant.
    '''
    
    def getMessageVariantStats(self,emailMessageId,emailMessageVariantId):
     
      url = self.apiurl + f"/v2/broadcastEmails/{emailMessageId}/variants/{emailMessageVariantId}"
      parameters = {"$expand":"statistics"}
      r = self.session.get(url,params=parameters)
      data = r.json()
      return data

#intiazling a class object with the API KEY
npg = NPG(API_KEY)


allEmails = npg.getAllEmails()
emailsData = allEmails['items']

#retrive lsit of all the message ids from getAllEmails()
msgIds = [allEmails['items'][idx]['emailMessageId'] for idx in range(len(allEmails['items']))]
msgIds.sort()

#Create a dataframe with emailIds and name of email
df = pd.DataFrame(emailsData, columns =["emailMessageId", "name"])
df1 = df.sort_values(by=['emailMessageId'], ascending=False, ignore_index=True)

#list to append all the stats of a given email id
messageStatsList = []

for id in msgIds:
  messageStats = npg.getEmailMessageStats(id)
  #print(id,messageStats)
  messageStats.update( {'emailMessageId' : id} ) 
  messageStatsList.append(messageStats)





#create a ta frame with the statistics of a given emailMessageID
df2 = pd.DataFrame(messageStatsList, columns=["emailMessageId","recipients", "opens", "clicks","unsubscribes", "bounces"])

#merging two dataframes on the emailMessageId
mergeDF12 = pd.merge(df1, df2, on ="emailMessageId")

messageVariantsList = []
for id in msgIds:
  messageVariants = npg.getEmailMessageVariants(id)
  messageVariantsList.append(messageVariants)





'''
  It will be helpful to map a given message id to a list of vairants associated
  with that email id. Making a list of dictionaries as such.
'''



message2Varaints ={}
for idx in range(len(messageVariantsList)):
  #msg2variants = {lp[idx]['emailMessageId']:[[lp[idx]['variants'][i]['emailMessageVariantId']] for i in range(len(lp[idx]['variants']))]}
  message2Varaints[messageVariantsList[idx]['emailMessageId']] = [messageVariantsList[idx]['variants'][i]['emailMessageVariantId'] for i in range(len(messageVariantsList[idx]['variants']))]

'''
  Need to retrieve the top vairant having a high performance on open 
  associated with an email id.
'''




#map email Id: topVariant
topVariants ={}


#lsit of dictionaries
listOfTopVariants = []

for key, values in message2Varaints.items():
  maxCount = 0
  topVariant =''
  for value in values:
    varStats = npg.getMessageVariantStats(key,value)
    opens2receipients = int(100*(varStats['statistics']['opens']/varStats['statistics']['recipients']))
    if opens2receipients > maxCount:
      openCount = opens2receipients
      topVariant = varStats['name']
  topVariants[key] = topVariant
  listOfTopVariants.append({'emailMessageId':key, 'name':topVariant})

#Create a dataframe with email id and the top variant associated with it.
df3 = pd.DataFrame(listOfTopVariants, columns=["emailMessageId","name"])

# Create the final dataframe

finalDataFrame = pd.merge(mergeDF12 ,df3, on="emailMessageId",how='right')
finalDataFrame = finalDataFrame.sort_values(by=['emailMessageId'], ascending=False, ignore_index=True)
finalDataFrame.columns = ["Email Message ID", "Email Name", "Recipients", "Opens", "Clicks", "Unsubscribes", "Bounces", "Top Variant"]

print("Exporting data to a csv file....")
print("Email report complete, file is EmailReport.csv")
print('Total emails: ', finalDataFrame['Email Message ID'].count())

finalDataFrame.to_csv('EmailReport.csv', index=False)

