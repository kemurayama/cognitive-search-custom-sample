import json
import logging
import string

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Start Count word Function')
    result = {
        'values':[]
    }
    try:
        logging.info('trying to get request body')
        record_list = req.get_json().get('values')
        for record in record_list:
            res_record ={
                'recordId': record['recordId'],
                'data':{
                    'digit_count':None
                },
                'errors': None,  
                'warnings': None
            }
            try:
                text = record['data']['text']
                if text is not None:
                    text = ''.join([w for w in text if not w in string.punctuation])
                    counter = 0
                    for w in text.split():
                        if w.isdigit():
                            counter += 1
                        # add count to a record
                    res_record['data']['digit_count'] = counter
                else:
                    res_record["warnings"] = [ { "message": "This record doesn't have content"} ]

            except Exception as e:
                logging.exception("failed when counting digit")
                res_record["errors"] = [ { "message": f"{e}"} ]
            
            result['values'].append(res_record)
        return func.HttpResponse(
            json.dumps(result,indent=4),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.exception("failed to get body from request")
        return func.HttpResponse(
             "Content is invalid format",
             status_code=400
        )
