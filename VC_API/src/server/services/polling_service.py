# import json
# from threading import Thread, Lock
# import time
# import requests as http_client
# import logging
# from global_settings import Settings

# from database.handler.credential_issuing_data_handler import CredentialIssuingDataHandler
# from database.entities.credential_issuing_data import State

# class PollingService():
#     mutex = Lock()

#     def run():
#         thread = Thread(target = PollingService.polling_loop)
#         thread.start()

#     def polling_loop():
#         while True:
#             dataList = CredentialIssuingDataHandler.getByState(State.Issuing)
#             for data in dataList:
#                 # ToDo
#                 cid = data.CredentialIssuingData
#                 agent = data.Agent
#                 PollingService.update_state(cid, agent)
                
#                 time.sleep(int(Settings.agentPollingIntervall)) 

#     def update_state(credentialIssuingData, agent):
#         PollingService.mutex.acquire()
#         url = agent.url + "/IssuingState"
#         headers = {
#             'x-auth-token': agent.api_token
#         }
        
#         try:
#             response = http_client.request("Get", url, headers=headers, verify=Settings.agentVerifySSL)
#             if response.status_code == 200:
#                 res = json.loads(response.text)
                
#                 if res["state"] == State.Issued.value:
#                     credentialIssiungData = CredentialIssuingDataHandler.getByCredentialAndAgent(credentialIssuingData.credential_id, agent.id)
#                     credentialIssiungData.state = State.Issued.value
#                     credentialIssiungData.data = json.dumps(res["data"])
#                     CredentialIssuingDataHandler.update()
#             else:
#                 logging.error(f"Error. Agent provider returns {response.status_code}!")
#         except http_client.exceptions.ConnectionError as ex:
#             logging.error(f"Can't connect to agent: {ex}")
#         except Exception as ex:
#             logging.error(ex)
#         finally:
#             PollingService.mutex.release()
        