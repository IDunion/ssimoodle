import json
from threading import Thread
import time
from flask import request
import requests as http_client
import logging
from global_settings import Settings

from database.handler.agent_handler import AgentHandler
from database.handler.credential_issuing_data_handler import CredentialIssuingDataHandler
from database.entities.credential_issuing_data import State

class PollingService():
    def run():
        thread = Thread(target = PollingService.polling)
        thread.start()

    def polling():
        while True:
            dataList = CredentialIssuingDataHandler.getByState(State.Issuing)
            agents = AgentHandler.getAll()
            for data in dataList:
                # ToDo
                agent = list(filter(lambda agent: agent.id == data.agent_id, agents))[0]

                url = agent.url + "/IssuingState"
                headers = {
                    'x-auth-token': agent.api_token
                }
                
                try:
                    response = http_client.request("Get", url, headers=headers, verify=Settings.agentVerifySSL)
                    if response.status_code == 200:
                        res = json.loads(response.text)
                        
                        if res["state"] == State.Issued.value:
                            credentialIssiungData = CredentialIssuingDataHandler.getByCredentialAndAgent(data.id, data.agent_id)
                            credentialIssiungData.state = State.Issued.value
                            credentialIssiungData.data = json.dumps(res["data"])
                            CredentialIssuingDataHandler.update()
                    else:
                        logging.error(f"Error. Agent provider returns {response.status_code}!")
                except http_client.exceptions.ConnectionError as ex:
                    logging.error(f"Can't connect to agent: {ex}")
                except Exception as ex:
                    logging.error(ex)
            
            time.sleep(int(Settings.agentPollingIntervall)) 